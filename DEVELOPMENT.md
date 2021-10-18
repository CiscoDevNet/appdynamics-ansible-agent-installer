# Development and testing

## Molecule local tests

To run molecule tests locally you can use molecule with molecule-docker driver.
You would need SaaS controller available as well.

```shell
cat << EOF > .env.yml
APPDYNAMICS_API_CLIENT_ID: api_user@account1
APPDYNAMICS_API_CLIENT_SECRET: <somesecret>
APPDYNAMICS_AGENT_ACCOUNT_ACCESS_KEY: <controllerkey>
APPDYNAMICS_CONTROLLER_URL: https://account1.saas.appdynamics.com
APPDYNAMICS_AGENT_ACCOUNT_NAME: account1
EOF
./install_collection.sh
pip3 install molecule molecule[docker] ansible-lint[community,yamllint]
molecule --base-config molecule/base-docker.yml test --all
```

If you need to explore your molecule container interactively you can run tests like so:

```
molecule --base-config molecule/base-docker.yml create -s zeroagent-local
```

or

```
molecule --base-config molecule/base-docker.yml test -s zeroagent-local --destroy never
```

and then do:

```
molecule --base-config molecule/base-docker.yml login -s zeroagent-local
```
