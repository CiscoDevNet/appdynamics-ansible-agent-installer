from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
import pytest
import io
from ansible.module_utils import urls
# from _pytest.monkeypatch import monkeypatch

from ansible_collections.appdynamics.agent_installer.tests.unit.compat import unittest
from ansible_collections.appdynamics.agent_installer.tests.unit.compat.mock import patch
from ansible_collections.appdynamics.agent_installer.tests.unit.plugins.module_utils.utils import (
    exit_json,
    set_module_args,
    fail_json,
    AnsibleFailJson,
    AnsibleExitJson,
)

# from ansible.module_utils import basic
# from ansible.module_utils.common.text.converters import to_bytes
from ansible_collections.appdynamics.agent_installer.plugins.modules import download


def test_missing_required_parameter(capfd):

    with pytest.raises(SystemExit):
        set_module_args({})
        download.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    print(results)

    assert results['failed'] is True
    assert "missing required arguments" in results['msg']


def test_auth_with_client_secret(default_args, jwt_token, download_cmd, capfd):

    with pytest.raises(SystemExit):
        set_module_args(default_args)
        download.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    print(results)

    # assert that checksum corresponds to the mocked download_cmd
    assert 'failed' not in results
    assert results['checksum'] == "1d80b8f7b02e7e5705bc51b9ed8013f4"


def test_auth_with_api_token(default_args_token, jwt_token, download_cmd, capfd):

    with pytest.raises(SystemExit):
        set_module_args(default_args_token)
        download.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    print(results)

    # assert that checksum corresponds to the mocked download_cmd
    assert 'failed' not in results
    assert results['checksum'] == "1d80b8f7b02e7e5705bc51b9ed8013f4"


def test_auth_with_api_token_from_env(default_args_token, api_token_in_env, download_cmd, capfd):
    """Read token from env"""

    with pytest.raises(SystemExit):

        args = default_args_token
        del args["api_token"]
        set_module_args(args)
        download.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    print(results)

    # assert that checksum corresponds to the mocked download_cmd
    assert results['checksum'] == "1d80b8f7b02e7e5705bc51b9ed8013f4"


def test_auth_mutually_exclusive(default_args, jwt_token, download_cmd, capfd):

    with pytest.raises(SystemExit):

        args = default_args
        args["api_token"] = "footoken"
        set_module_args(args)
        download.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    print(results)

    assert results['failed'] is True
    assert "parameters are mutually exclusive: client_secret|api_token" in results['msg']


def test_expected_output_is_present(default_args, jwt_token, download_cmd, capfd):
    """Check that all output params are present"""

    with pytest.raises(SystemExit):
        set_module_args(default_args)
        download.main()

    out, err = capfd.readouterr()
    results = json.loads(out)
    print(results)
    assert 'failed' not in results
    assert all(txt in results for txt in ('download_cmd',
               'checksum', 'dest_subdir', 'checksum_changed'))
