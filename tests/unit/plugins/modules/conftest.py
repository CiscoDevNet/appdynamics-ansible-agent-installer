# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
from ansible_collections.appdynamics.agent_installer.plugins.modules import auth


@pytest.fixture
def default_args():
    return {"client_id": "user@account", "client_secret": "supersecret", "url": "http://localhost"}


@pytest.fixture
def jwt_token(monkeypatch):
    """Requests.get() mocked to return {'mock_key':'mock_response'}."""

    def get_mock_token(*args, **kwargs):
        return """eyJraWQiOiI1YTNkZmEyOC00MDc0LTQ3MTMtYmU3Zi1jNDc0MmZhOGI3NmQiLCJhbGciOiJIUzI1NiJ9
                  eyJpc3MiOiJBcHBEeW5hbWljcyIsImF1ZCI6IkFwcERfQVBJcyIsImp0aSI6InVPMl9kQWkwMUdjTTlE
                  ckE5aUhUUmciLCJzdWIiOiJ2emh1cmF2bGV2LWFwaSIsImlkVHlwZSI6IkFQSV9DTElFTlQiLCJpZCI6
                  IjdlMDQxMTFjLTVmNjEtNGQ2MC04ZTQ0LTViZjIzZDFiMjFiNCIsImFjY3RJZCI6IjVhM2RmYTI4LTQw
                  NzQtNDcxMy1iZTdmLWM0NzQyZmE4Yjc2ZCIsInRudElkIjoiNWEzZGZhMjgtNDA3NC00NzEzLWJlN2Yt
                  YzQ3NDJmYThiNzZkIiwiYWNjdE5hbWUiOiJwcm9qZWN0LXplcm8tMiIsInRlbmFudE5hbWUiOiIiLCJm
                  bW1UbnRJZCI6bnVsbCwiYWNjdFBlcm0iOltdLCJyb2xlSWRzIjpbXSwiaWF0IjoxNjI2MDk0MjYyLCJu
                  YmYiOjE2MjYwOTQxNDIsImV4cCI6MTYyNjE4MDY2MiwidG9rZW5UeXBlIjoiQUNDRVNTIn0y89q1tFhv
                  jPm6-nyprSqVLDyQdkELiM-GMJUxeaNLZ0"""

    monkeypatch.setattr(auth, "get_token", get_mock_token)
