# Ansible Collection - appdynamics.agent_installer

This Ansible collection downloads and installs [AppDynamics Agent Installer](https://docs.appdynamics.com/21.9/en/application-monitoring/install-app-server-agents/agent-installer), which 

- Dploys Java and Machine Agents, and is compatible with Linux 
- Automatically instruments applications 
- Assigns unique names to tiers and nodes

Ansible collection supports the following deployment patterns:

- Download the agent installer directly to target hosts
- Download the agent installer to Ansible controller and distribute it across target hosts

see example playbooks.

## Requirements

- AppDynamics SaaS controller only
- Ansible 2.9 and above
- `unzip` and `curl` on target hosts

## Getting started

1. In order to download agent installer using Agent installer API, it is required to use [API client](https://docs.appdynamics.com/21.3/en/extend-appdynamics/appdynamics-apis/api-clients#APIClients-Create_API_ClientCreatingAPIClients) on SaaS controller.

When creating API client:

- Keep `Roles` tab empty, as it is not required to assign any Roles for Agent installer API access
- Keep token expiration short, default (5m) is good enough.

2. Install collection

TODO: via galaxy


2. Download agent installer using `appdynamics.agent_installer.download` module locally:

```yaml
- name: Appdynamics agent installer
  hosts: all
  tasks:
    - name: Download
      run_once: yes
      delegate_to: localhost
      register: download
      appdynamics.agent_installer.download:
        client_id: api_user@mycompany
        client_secret: <secret>
        controller_url: https://mycompany.saas.appdynamics.com
        dest: /tmp/agentdir
```

Note: It is also helpful to set APPDYNAMICS_API_CLIENT_ID, APPDYNAMICS_API_CLIENT_SECRET environment variables when running module locally instead of providing client_id, client_secret.

For all availble options see appdynamics.agent_installer.download reference.

3. Copy files Install agent installer to target hosts, using retrieved zero agent archives

```yaml
    - name: Copy files to hosts
      copy:
        src: "{{ appdynamics_agent_installer_temp_local_dir }}/"
        dest: "{{ appdynamics_agent_installer_stage_dir }}"

    - name: Install agent_installer
      import_role:
        name: appdynamics.agent_installer.install
```

## Known issues

appdynamics_agent_installer_user - 