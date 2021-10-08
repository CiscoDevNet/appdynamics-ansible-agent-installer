# Ansible Collection - appdynamics.agent_installer

This Ansible collection downloads and installs [AppDynamics Agent Installer](https://docs.appdynamics.com/latest/en/application-monitoring/install-app-server-agents/agent-installer), which:

- Deploys Java and Machine Agents on Linux
- Automatically instruments applications
- Assigns unique names to tiers and nodes

Ansible collection supports the following deployment patterns:

- Download the agent installer directly to target hosts (remote)
- Download the agent installer to Ansible controller and distribute it across target hosts (local)

see example playbooks.

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

```shell
git clone <this repo>
./install_collection.sh
```

OR 

TODO: via galaxy

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
agent_installer_access_key: <you controleler access key>
agent_installer_account_name: mycompany
agent_installer_application_name: zfi-ansible-sample-app
```

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

## Development and testing

To run molecule tests locally you can use [Vagrant](https://www.vagrantup.com/)+[Virtualbox](https://www.virtualbox.org/wiki/Downloads) with molecule-vagrant driver. You would need SaaS controller available as well.

```shell
cat << EOF > .env.yml
APPDYNAMICS_API_CLIENT_ID: api_user@account1
APPDYNAMICS_API_CLIENT_SECRET: <somesecret>
APPDYNAMICS_AGENT_ACCOUNT_ACCESS_KEY: <controllerkey>
APPDYNAMICS_CONTROLLER_URL: https://account1.saas.appdynamics.com
APPDYNAMICS_AGENT_ACCOUNT_NAME: account1
EOF
./install-collection.sh
pip3 install molecule molecule-vagrant python-vagrant
molecule --base-config molecule/base-vagrant.yml test --all
```
