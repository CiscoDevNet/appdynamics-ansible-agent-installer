# Development and testing

## Molecule tests

To run molecule tests locally you can use [Vagrant](https://www.vagrantup.com/)+[Virtualbox](https://www.virtualbox.org/wiki/Downloads) with molecule-vagrant driver. You would need SaaS controller available as well.

```shell
cat << EOF > .env.yml
APPDYNAMICS_API_CLIENT_ID: api_user@account1
APPDYNAMICS_API_CLIENT_SECRET: <somesecret>
APPDYNAMICS_AGENT_ACCOUNT_ACCESS_KEY: <controllerkey>
APPDYNAMICS_CONTROLLER_URL: https://account1.saas.appdynamics.com
APPDYNAMICS_AGENT_ACCOUNT_NAME: account1
EOF
./install_collection.sh
pip3 install molecule molecule-vagrant python-vagrant
molecule --base-config molecule/base-vagrant.yml test --all
```
