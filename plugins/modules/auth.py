#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: auth

short_description: Module to obtain JWT token for AppDynamics Zero API.

version_added: "1.0.0"

description: |
    Token is stored in environment variable.

options:
    url:
        description: Zero Agent API URL (i.e. https://<your controller>/auth/v1/oauth/token)
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

author:
    - Vitaly Zhuravlev (@v-zhuravlev)
'''

EXAMPLES = r'''
#Get token
- name: Get token
  appdynamics.zeroagent.auth:
    url: https://company1.saas.appdynamics.com/auth/v1/oauth/token
    client_id: user@company1
    client_secret: somesecret
'''

RETURN = r'''

'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url


import json

try:
    # python 3.x
    from urllib.parse import urlencode
except ImportError:
    # python 2.x
    from urllib import urlencode


def get_token(module):

    url = module.params["url"]
    payload = {"grant_type": "client_credentials",
               "client_id": module.params["client_id"],
               "client_secret": module.params["client_secret"]}
    headers = {
        "content-type": "application/x-www-form-urlencoded"
    }

    resp_bytes, info = fetch_url(module,
                                 url,
                                 data=urlencode(payload),
                                 headers=headers,
                                 method="POST")
    status_code = info["status"]

    if status_code == -1:
        module.fail_json(msg="Failed to connect", error=info["msg"])
    if status_code >= 400:
        module.fail_json(msg=info["msg"], error=json.loads(info["body"])["error"])

    return json.loads(resp_bytes.read().decode("utf-8"))["access_token"]


def run_module():

    module_args = dict(
        url=dict(type="str", required=True),
        client_id=dict(type="str", required=True),
        client_secret=dict(type="str", required=True, no_log=True)
    )

    result = dict(
        changed=False,
        token=""
        # will be saved in ENV
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )
    token = get_token(module)

    # store_token_in_env()

    if len(token) > 0:
        result["changed"] = True

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
