#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: download

short_description: Ansible module to download AppDynamics agent installer.

version_added: "21.10.0"

description: |
    Gets download command in order to download required agent installer.

options:
    controller_url:
        description: Appdynamics Controller API URL (i.e. https://<your controller>)
        required: true
        type: str
    client_id:
        description: Client ID (i.e. <username>@<account>)
        required: false
        type: str
    client_secret:
        description: Client secret
        required: false
        type: str
    api_prefix:
        description: Zero Agent API prefix (i.e. /zero)
        required: false
        type: str
        default: /zero
    api_token:
        description: Token for controller auth.
        required: false
        type: str
    java_version:
        description: Java agent version to use. Defaults to using the latest.
        required: false
        type: str
        default: latest
    machine_version:
        description: Machine agent version to use. Defaults to using the latest.
        required: false
        type: str
        default: latest
    infra_version:
        description: Infra agent version to use. Defaults to using the latest.
        required: false
        type: str
        default: latest
    zero_version:
        description: Zero agent version to use. Defaults to using the latest.
        required: false
        type: str
        default: latest
    install_java:
        description: Set to true to download Java agent
        required: false
        type: bool
        default: true
    install_machine:
        description: Set to true to download machine agent
        required: false
        type: bool
        default: true
    install_infra:
        description: Set to true to download infra agent
        required: false
        type: bool
        default: false
    dest:
        description: Provide path where to store downloaded artifacts
        required: true
        type: path
    force:
        description: Forces agent redownload
        required: false
        type: bool
        default: false


author:
    - Vitaly Zhuravlev
'''

EXAMPLES = r'''

- name: Download agent installer
  appdynamics.agent_installer.download:
    controller_url: https://company1.saas.appdynamics.com
    client_id: user@company1
    client_secret: somesecret
    dest: /opt/appdynamics/agent_installer_store

- name: Download agent installer (java agent only)
  appdynamics.agent_installer.download:
    controller_url: https://company1.saas.appdynamics.com
    client_id: user@company1
    client_secret: somesecret
    install_machine: False
    dest: /opt/appdynamics/agent_installer_stagestore

- name: Get download command without downloading
  appdynamics.agent_installer.download:
    controller_url: https://company1.saas.appdynamics.com
    client_id: user@company1
    client_secret: somesecret
    dest: /opt/appdynamics/agent_installer_stagestore
  check_mode: yes
'''

RETURN = r'''

download:
    description: Shell download command
    returned: success
    type: str
checksum:
    description: Checksum of download command. Can be used to make decisions if agent upgrade is required.
    returned: success
    type: str
    sample: a4e12de7078bc61e77c1b0d567a61064
checksum_changed:
    description: Indicates if command checksum is changed
    returned: success
    type: bool
    sample: true
dest_subdir:
    description: Sub directory with installation files.
    returned: success
    type: str
    sample: /tmp/appdynamics-agent-installer/a4e12de7078bc61e77c1b0d567a61064

'''

import hashlib
import json
import os
import errno
from ansible_collections.appdynamics.agent_installer.plugins.module_utils.auth import get_token
from ansible.module_utils.basic import env_fallback
from ansible.module_utils.urls import fetch_url
from ansible.module_utils.basic import AnsibleModule

try:
    # python 3.x
    from urllib.parse import urlencode
except ImportError:
    # python 2.x
    from urllib import urlencode

# if sys.version_info < (3, 0):
#     from urllib import urlencode
# else:
#     from urllib.parse import urlencode

API_VERSION = "v1beta"


def get_download_cmd(module):

    url = module.params["controller_url"] + module.params["api_prefix"] + \
        "/" + API_VERSION + "/install/downloadCommand"

    # javaVersion=latest&machineVersion=latest&infraVersion=latest&zeroVersion=latest&multiline=true"
    url_params = {"multiline": "true",
                  "zeroVersion": module.params["zero_version"],
                  }
    if module.params["install_java"]:
        url_params["javaVersion"] = module.params["java_version"]
    if module.params["install_machine"]:
        url_params["machineVersion"] = module.params["machine_version"]
    if module.params["install_infra"]:
        url_params["infraVersion"] = module.params["infra_version"]

    headers = {
        'Authorization': "Bearer " + module.params["api_token"]
    }
    resp_bytes, info = fetch_url(module,
                                 url + "?" + urlencode(url_params),
                                 headers=headers,
                                 method="GET")
    status_code = info["status"]

    if status_code == -1:
        module.fail_json(msg="Failed to connect", error=info["msg"])
    if status_code >= 400:
        module.fail_json(msg=info["msg"], error=json.loads(info["body"]))

    # Dropping first line with "mktemp -d -t appd-zero-XXXXXXX"
    return " ".join(json.loads(resp_bytes.read().decode("utf-8"))[1:]).replace("&& ", "", 1)


def get_checksum_subdir(download_cmd, dest):
    """Returns tuple of (checksum, changed)"""

    # If the download is not forced and there is a checksum, allow
    # checksum match to skip the download.
    download_cmd_digest = ""
    try:
        download_cmd_digest = hashlib.md5(download_cmd).hexdigest()
    except TypeError:
        download_cmd_digest = hashlib.md5(
            download_cmd.encode('utf-8')).hexdigest()

    try:
        dir_ls = os.listdir("%s" % (dest))
    except (IOError, OSError) as e:
        # no subdir with downloaded agents found
        return (download_cmd_digest, True)

    if download_cmd_digest in dir_ls:
        return (download_cmd_digest, False)
    else:
        return (download_cmd_digest, True)


def run_module():

    module_args = dict(
        controller_url=dict(type="str", required=True),
        client_id=dict(type="str", required=False, fallback=(
            env_fallback, ['APPDYNAMICS_API_CLIENT_ID'])),
        client_secret=dict(type="str", required=False, no_log=True, fallback=(
            env_fallback, ['APPDYNAMICS_API_CLIENT_SECRET'])),
        api_token=dict(type="str", required=False, no_log=True,
                       fallback=(env_fallback, ['APPDYNAMICS_API_TOKEN'])),
        api_prefix=dict(type="str", required=False, default="/zero"),
        java_version=dict(type="str", required=False, default="latest"),
        machine_version=dict(type="str", required=False, default="latest"),
        infra_version=dict(type="str", required=False, default="latest"),
        zero_version=dict(type="str", required=False, default="latest"),
        install_java=dict(type="bool", required=False, default=True),
        install_machine=dict(type="bool", required=False, default=True),
        install_infra=dict(type="bool", required=False, default=False),
        dest=dict(type="path", required=True),
        force=dict(type="bool", required=False, default=False)
    )

    result = dict(
        changed=False,
        download_cmd=""
    )

    module = AnsibleModule(
        argument_spec=module_args,
        mutually_exclusive=[
            ("client_secret", "api_token"),
        ],
        required_one_of=[
            ("install_java", "install_machine", "install_infra"),
            ("api_token", "client_secret")
        ],
        supports_check_mode=True
    )

    if not module.params["api_token"]:
        module.params["api_token"] = get_token(module)

    dest = module.params["dest"]

    force = module.params["force"]
    download_cmd = get_download_cmd(module)

    (checksum, checksum_changed) = get_checksum_subdir(download_cmd, dest)
    dest_subdir = dest + "/" + checksum

    if not module.check_mode:
        if force or checksum_changed:
            # Create dir first
            try:
                os.makedirs(dest_subdir)
            except OSError as e:
                if e.errno != errno.EEXIST:  # if not already exists
                    module.fail_json(
                        msg='Failed to create destination directory %s: %s' % (dest_subdir, e.strerror))

            (rc, out, err) = module.run_command("%s" % (download_cmd),
                                                check_rc=True, cwd=dest_subdir, use_unsafe_shell=True)
            if rc != 0:
                module.fail_json(
                    msg='Failed to retrieve submodule status: %s' % out + err)
                result["message"] = out + err
            result["changed"] = True

    result["download_cmd"] = download_cmd
    result["checksum"] = checksum
    result["checksum_changed"] = checksum_changed
    result["dest_subdir"] = dest_subdir

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
