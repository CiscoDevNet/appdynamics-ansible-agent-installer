# Ansible Collection - appdynamics.agent_installer

This Ansible collection downloads and installs [AppDynamics Agent Installer](https://docs.appdynamics.com/latest/en/application-monitoring/install-app-server-agents/agent-installer), which:

- Deploys Java and Machine Agents on Linux
- Automatically instruments applications
- Assigns unique names to tiers and nodes

Ansible collection supports the following deployment patterns:

- Download the agent installer directly to target hosts (remote)
- Download the agent installer to Ansible controller and distribute it across target hosts (local)

## Requirements

- AppDynamics SaaS controller only. For more details please refer to [agent installer docs](https://docs.appdynamics.com/latest/en/application-monitoring/install-app-server-agents/agent-installer#AgentInstaller-AgentInstallerRequirements)
- Ansible 2.9 and above
- `unzip` and `curl` must be installed on target hosts

## Using this collection

1. In order to download agent installer using Agent installer API, it is required to use [API client](https://docs.appdynamics.com/latest/en/extend-appdynamics/appdynamics-apis/api-clients#APIClients-Create_API_ClientCreatingAPIClients) on SaaS controller.

When creating API client:

- Keep `Roles` tab empty, as it is not required to assign any Roles for Agent installer API access
- Keep token expiration short, default (5m) is good enough.

2. Install collection

from ansible-galaxy:

```shell
ansible-galaxy collection install appdynaics.agent_installer
```

or from source:

```shell
git clone https://github.com/CiscoDevNet/appdynamics-ansible-agent-installer.git
./install_collection.sh
```

3. Create sample playbook

```yaml

- name: Appdynamics agent installer
  hosts: all
  vars_files: 
    - agent_installer_vars.yaml
  roles:
    - name: appdynamics.agent_installer.agent_installer
```

and sample vars file agent_installer_vars.yaml (it's to user to choose how to load variables of course)

```yaml
agent_installer_download_mode: local
agent_installer_client_id: api_user@mycompany
agent_installer_client_secret: <secret>
agent_installer_controller_url: https://mycompany.saas.appdynamics.com
agent_installer_access_key: <your controller access key>
agent_installer_account_name: mycompany
agent_installer_application_name: zfi-ansible-sample-app
```

Now you are ready to deploy AppDynamics agent intaller!

## Agent installer role variables

Here is the list of variables you can define to adjust agent installer deployment:

Variables related to agents download:

|Variable<img width="200"/>     | Description | Default |
|--|--|--|
|`agent_installer_client_id`|(required) Client ID ||
|`agent_installer_client_secret`|(required) Client secret||
|`agent_installer_controller_url`|(required) Controller URL, i.e. https://mycompany.saas.appdynamics.com||
|`agent_installer_download_mode`| Set to 'local' to download archives via Ansible controller host and 'remote' for direct download by target hosts|local|
|`agent_installer_temp_local_dir`|Temporary directory to store agents archives on Ansible controller (only for agent_installer_download_mode=local) |/tmp/appdynamics-agent-installer|
|`agent_installer_stage_dir_prefix`|Temporary directory to store agents archives on target hosts|/tmp/appdynamics-agent-installer-stage|
|`agent_installer_api_prefix`|API prefix|/zero|
|`agent_installer_java_version`|Java agent version to download|latest|
|`agent_installer_machine_version`|Machine agent version to download|latest|
|`agent_installer_infra_version`|Infra agent version to download|latest|
|`agent_installer_zero_version`|Agent installer version to download|latest|
|`agent_installer_install_java`| Set to 'false' to skip java agent installation|true|
|`agent_installer_install_machine`| Set to 'false' to skip machine agent installation|true|
|`agent_installer_install_infra`| Set to 'false' to skip infra agent installation. Defaults to false|false|
|`agent_installer_force`| Set to true to force download even if archives with the same download command are present| false|

Variables related to agents installation:

|Variable<img width="200"/>     | Description | Default |
|--|--|--|
|`agent_installer_access_key`|(required) Controller access key||
|`agent_installer_account_name`|(required) Controller account name||
|`agent_installer_application_name`|(required) Application name to be used in AppDynamics||
|`agent_installer_state`| Set to 'absent` to uninstall agent installer instead of installing it|installed|
|`agent_installer_enable_proxy`   | Set to 'true' to enable http proxy configuration  | false |
|`agent_installer_proxy_host`  | HTTP proxy host to use |  |
|`agent_installer_proxy_port`  | HTTP proxy port to use |  |
|`agent_installer_install_path` | Installation directory of agent installer | /opt/appdynamics/zeroagent for system wide installation, and $HOME/appdynamics/zeroagent for single user installations |
|`agent_installer_enable_systemd` | Set to 'false' to disable systemd service installation. Forced to 'false' if agent_installer_user is not `root` | true |
|`agent_installer_user`|System user to install and run Agent installer |root|
|`agent_installer_log_level`|Logging level to use, choose from `panic fatal error warning info debug trace` |info|
|`agent_installer_validate_install`|Set to 'false' to skip post install validations|true|

## Tips

For human readable outputs, running this role with stdout callback = yaml is recommended in favor of default json:

```shell
export ANSIBLE_STDOUT_CALLBACK=yaml
```

or permanently by setting stdout_callback=yaml in the [default] section of ansible.cfg

```ini
[default]
stdout_callback = yaml
```
