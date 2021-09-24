from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import pytest
import io
from ansible.module_utils import urls
# from _pytest.monkeypatch import monkeypatch

from ansible_collections.appdynamics.zeroagent.tests.unit.compat import unittest
from ansible_collections.appdynamics.zeroagent.tests.unit.compat.mock import patch
from ansible_collections.appdynamics.zeroagent.tests.unit.plugins.module_utils.utils import (
    exit_json,
    set_module_args,
    fail_json,
    AnsibleFailJson,
    AnsibleExitJson,
)

# from ansible.module_utils import basic
# from ansible.module_utils.common.text.converters import to_bytes
from ansible_collections.appdynamics.zeroagent.plugins.modules import auth


def test_name_is_a_required_parameter(capfd):

    with pytest.raises(SystemExit):
        set_module_args({})
        auth.main()

    out, err = capfd.readouterr()
    results = json.loads(out)

    # assert all(txt in results['msg'] for txt in ('state', 'required'))
    assert results['failed'] is True
    assert "missing required arguments" in results['msg']


def test_all_provided(default_args, capfd):

    with pytest.raises(SystemExit):
        set_module_args(default_args)
        auth.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert results['failed'] is True
    assert "required" not in results['msg'], "msg returned: " + results['msg']
    # assert all(txt in results['msg'] for txt in (
    #     'missing',
    #     'required',
    #     'access_token',
    # ))

# monkeypatched requests.get moved to a fixture
# @pytest.fixture
# def mock_response(monkeypatch):
#     """Requests.get() mocked to return {'mock_key':'mock_response'}."""

#     def mock_get(*args, **kwargs):
#         data = "{\"access_token\": \"mytoken.mytoken.mytoken\"}"
#         #data = bytes(str(data).encode("utf-8"))
#         data = io.BytesIO(b'"{\"access_token\": \"mytoken.mytoken.mytoken\"}"')
#         info = dict(
#             status = 200,
#             msg    = "ALL COOL"
#         )
#         return (data, info)
#         #return MockResponse()

#     monkeypatch.setattr(auth, "fetch_url", mock_get)

# notice our test uses the custom fixture instead of monkeypatch directly


def test_get_token(default_args, jwt_token, capfd):

    with pytest.raises(SystemExit):
        set_module_args(default_args)
        auth.main()

    out, err = capfd.readouterr()
    results = json.loads(out)

    # result = auth.get_token(module)
    assert results["changed"] is True
    # assert results["msg"] == "mock_response"
