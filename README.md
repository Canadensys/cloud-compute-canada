# Cloud-ComputeCanada
All informations related to deployement on the Compute Canada Cloud

## vm_deployment_scripts
Scripts to launch VMs on Openstack ComputeCanada

### Connexion to CC Openstack
[Get and set openstack access](https://docs.computecanada.ca/wiki/OpenStack_Command_Line_Clients#Connecting_CLI_to_OpenStack) \
Test the connexion: \
`$ source /path/to/project/name/openrc/<project name>-openrc.sh` \
`$ openstack security group list`

**Use information in `<project name>-openrc.sh` to set variables in `vms_info.yml`**

### ip-local
ip-local is the the subdomain with from /0 to /31, the end of the ip address could be set per vm in 'ip'. \
See vms_info.yml template

### Packages on Ubuntu 16.04, local machine
install packages \
`$ sudo apt-get update` \
`$ sudo apt-get install python-dev python-pip` \
`$ sudo apt-get install python-openstackclient` \
`$ sudo apt-get install python-yaml` \
`$ sudo apt-get install python-shade`

### STEPS:
0- Prepare access information in vms_info.yml \
1- Prepare VMs information with vms_info.yml \
2- Create user default with user_vm-default.txt \
3- `$ python create_user_config.py` \
4- `$ python deploy_volume.py` \
5- `$ python deploy_instance.py`

### Few command lines
create ssh keys for connection \
`$ ssh-keygen -t rsa`

create an hashed password \
`$ mkpasswd -m SHA-512 --rounds=4096`
