# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
from ansible_collections.appdynamics.agent_installer.plugins.module_utils import auth
from ansible_collections.appdynamics.agent_installer.plugins.modules import download

# Test in checkmode to avoid actual download attempt
@pytest.fixture
def default_args():
    return {"_ansible_check_mode": True, "client_id": "user@account", "client_secret": "supersecret", "controller_url": "http://localhost", "dest": "/tmp/appdynamics-agent-installer"}

# Test in checkmode to avoid actual download attempt
@pytest.fixture
def default_args_token():
    return {"_ansible_check_mode": True, "api_token": "footoken", "controller_url": "http://localhost", "dest": "/tmp/appdynamics-agent-installer"}


@pytest.fixture
def jwt_token(monkeypatch):
    def get_mock_token(*args, **kwargs):
        return "eyJraWQiOiI1YTNkZmEyOC00MDc0LTQ3MTMtYmU3Zi1jNDc0MmZhOGI3NmQiLCJhbGciOiJIUzI1NiJ9" + \
            "eyJpc3MiOiJBcHBEeW5hbWljcyIsImF1ZCI6IkFwcERfQVBJcyIsImp0aSI6InVPMl9kQWkwMUdjTTlE" + \
            "ckE5aUhUUmciLCJzdWIiOiJ2emh1cmF2bGV2LWFwaSIsImlkVHlwZSI6IkFQSV9DTElFTlQiLCJpZCI6" + \
            "IjdlMDQxMTFjLTVmNjEtNGQ2MC04ZTQ0LTViZjIzZDFiMjFiNCIsImFjY3RJZCI6IjVhM2RmYTI4LTQw" + \
            "NzQtNDcxMy1iZTdmLWM0NzQyZmE4Yjc2ZCIsInRudElkIjoiNWEzZGZhMjgtNDA3NC00NzEzLWJlN2Yt" + \
            "YzQ3NDJmYThiNzZkIiwiYWNjdE5hbWUiOiJwcm9qZWN0LXplcm8tMiIsInRlbmFudE5hbWUiOiIiLCJm" + \
            "bW1UbnRJZCI6bnVsbCwiYWNjdFBlcm0iOltdLCJyb2xlSWRzIjpbXSwiaWF0IjoxNjI2MDk0MjYyLCJu" + \
            "YmYiOjE2MjYwOTQxNDIsImV4cCI6MTYyNjE4MDY2MiwidG9rZW5UeXBlIjoiQUNDRVNTIn0y89q1tFhv" + \
            "jPm6-nyprSqVLDyQdkELiM-GMJUxeaNLZ0"

    monkeypatch.setattr(download, "get_token", get_mock_token)


@pytest.fixture
def download_cmd(monkeypatch):
    def get_mock_download_cmd(*args, **kwargs):
        return "curl https://download-files.saas.appd-test.com/download-file/zero-agent-bootstrap/21.10.0.875/appdynamics-zero-agent-bootstrap-21.10.0.875.sh" + \
            " -o zero-agent.sh" + \
            " && chmod +x zero-agent.sh" + \
            " && ./zero-agent.sh download sun-java -u https://download-files.saas.appd-test.com -v 21.5.0.32605 -c 00cc2ce77f93dc262347c60bf4434e0b" + \
            " && ./zero-agent.sh download ibm-java -u https://download-files.saas.appd-test.com -v 21.5.0.32605 -c af9cf557d9eb2fb7c058a431ff8d13e7" + \
            " && ./zero-agent.sh download machine -u https://download-files.saas.appd-test.com -v 21.9.0.3184 -c 3bebea27d413261ff02752bf86c4bfbf" + \
            " && ./zero-agent.sh download zero -u https://download-files.saas.appd-test.com -v 21.10.0.875 -c 2a5168f50323f9b1215944b42f352f4f"
    monkeypatch.setattr(download, "get_download_cmd", get_mock_download_cmd)


@pytest.fixture
def api_token_in_env(monkeypatch):
    monkeypatch.setenv('APPDYNAMICS_API_TOKEN', 'footoken')
