from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import pytest
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


def test_all_provided(capfd):

    with pytest.raises(SystemExit):
        set_module_args({
            "login": "SOMELOGIN",
            "name": "SOMENAME",
            "user_password": "SOMEPASS",
            "url_password": "SOMEOTHERPASS",
            "client": 1
        })
        auth.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    assert results['failed'] is True
    assert "required" not in results['msg'], "msg returned: " + results['msg']
