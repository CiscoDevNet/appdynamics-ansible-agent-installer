#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: download_cmd

short_description: Module to get download command.

version_added: "1.0.0"

description: |
    Gets download command in order to download required agent installer.

options:
    url:
        description: Appdynamics Controller API URL (i.e. https://<your controller>)
        required: true
        type: str
    client_id:
        description: Client ID (i.e. <username>@<account>)
        required: true
        type: str
    client_secret:
        description: Client secret
        required: true
        type: str
    api_prefix:
        description: Zero Agent API prefix (i.e. /zero)
        required: false
        type: str
        default: /zero
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
        descripton: Zero agent version to use. Defaults to using the latest.
        required: false
        type: str
        default: latest
    install_java:
        description: Set to true to download Java agent
        required: false
        type: bool
        default: True
    install_machine:
        description: Set to true to download machine agent
        required: false
        type: bool
        default: True
    install_infra:
        description: Set to true to download infra agent
        required: false
        type: bool
        default: False
    drop_mktemp:
        description: Drop part of the download command that creates temporary folder (i.e. mktemp -d -t appd-zero-XXXXXXX)
        required: false
        type: bool
        default: True


author:
    - Vitaly Zhuravlev (@v-zhuravlev)
'''

EXAMPLES = r'''
#Get token
- name: Get download url
  appdynamics.zeroagent.download_cmd:
    url: https://company1.saas.appdynamics.com
    client_id: user@company1
    client_secret: somesecret

- name: Get download url and download java agent only
  appdynamics.zeroagent.download_cmd:
    url: https://company1.saas.appdynamics.com
    client_id: user@company1
    client_secret: somesecret
    install_machine: False
'''

RETURN = r'''

'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url
from ansible.module_utils.basic import env_fallback

from ansible_collections.appdynamics.zeroagent.plugins.module_utils.auth import get_token

import os
import json

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

    url = module.params["url"] + module.params["api_prefix"] + "/" + API_VERSION + "/install/downloadCommand"

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
    if module.params['drop_mktemp']:
        return " ".join(["true"] + json.loads(resp_bytes.read().decode("utf-8"))[1:])
    else:
        return " ".join(json.loads(resp_bytes.read().decode("utf-8")))


def run_module():

    module_args = dict(
        url=dict(type="str", required=True),
        client_id=dict(type="str", required=True, fallback=(env_fallback, ['APPDYNAMICS_API_CLIENT_ID'])),
        client_secret=dict(type="str", required=True, no_log=True, fallback=(env_fallback, ['APPDYNAMICS_API_CLIENT_SECRET'])),
        api_token=dict(type="str", required=False, no_log=True, fallback=(env_fallback, ['APPDYNAMICS_API_TOKEN'])),
        api_prefix=dict(type="str", required=False, default="/zero"),
        java_version=dict(type="str", required=False, default="latest"),
        machine_version=dict(type="str", required=False, default="latest"),
        infra_version=dict(type="str", required=False, default="latest"),
        zero_version=dict(type="str", required=False, default="latest"),
        install_java=dict(type="bool", required=False, default=True),
        install_machine=dict(type="bool", required=False, default=True),
        install_infra=dict(type="bool", required=False, default=True),
        drop_mktemp=dict(type="bool", required=False, default=True),
    )

    result = dict(
        changed=False,
        download_cmd=""
    )

    module = AnsibleModule(
        argument_spec=module_args,
        mutually_exclusive=[
            ("client_id", "api_token"),
        ],
        required_one_of=[
            ("install_java", "install_machine", "install_infra"),
        ],
        supports_check_mode=False
    )

    if not module.params["api_token"]:
        module.params["api_token"] = get_token(module)

    download_cmd = get_download_cmd(module)
    if len(download_cmd) > 0:
        result["changed"] = True
        result["download_cmd"] = download_cmd

    module.exit_json(**result)


def main():
    run_module()

if __name__ == "__main__":
    main()
