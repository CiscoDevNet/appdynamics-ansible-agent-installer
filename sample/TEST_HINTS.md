export ANSIBLE_LIBRARY=${PWD}/appdynamics/zeroagent/plugins/modules
ansible localhost -m auth -e='@sample_vars.yaml' -a "client_id={{client_id}} client_secret={{client_secret}} url={{url}}"
