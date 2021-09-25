# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


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

    if "@" not in module.params["client_id"]:
        module.fail_json(msg="Please provide client_id in form user@company1", error="Invalid client_id")

    url = module.params["controller_url"] + "/auth/v1/oauth/token"
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
        module.fail_json(msg=info["msg"], error=json.loads(info["body"])["message"])

    return json.loads(resp_bytes.read().decode("utf-8"))["access_token"]


# def store_token(token):
#     """This stores token in env for further usage"""
#     os.environ["APPDYNAMICS_ZFI_TOKEN"] = token
