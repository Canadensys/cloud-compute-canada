#!/usr/bin/python

# deploy volumes
# test if volume name exists openstack volume show vm-002
# if no: No volume with a name or ID of 'vm-002' exists.
# openstack volume create --image IMAGENAME --description "VM DESCRIPTION" --size VMSIZE --availability-zone ZONE VMNAME

'''
https://docs.openstack.org/openstacksdk/latest/user/connection.html

create_volume(size, wait=True, timeout=None, image=None, bootable=None, **kwargs)

    Create a volume.
    Parameters:	
        size - Size, in GB of the volume to create.
        name - (optional) Name for the volume.
        description - (optional) Name for the volume.
        wait - If true, waits for volume to be created.
        timeout - Seconds to wait for volume creation. None is forever.
        image - (optional) Image name, ID or object from which to create the volume
        bootable - (optional) Make this volume bootable. If set, wait will also be set to true.
        kwargs - Keyword arguments as expected for cinder client.

    Returns:    The created volume object.
    Raises:     OpenStackCloudTimeout if wait time exceeded.
    Raises:     OpenStackCloudException on operation error.

'''

import openstack.cloud
import shade
from shade import exc

def get_vms_info():
    # extract information from yaml file
    import yaml
    vms_info = {}
    with open("vms_info.yml", 'r') as stream:
        try:
            vms_info = yaml.safe_load(stream)
            return vms_info
        except yaml.YAMLError as exc:
            print(exc)
    
def connexion(vms_info):
    from openstack import connection
    from os import environ as env
    import getpass
    
    userName = ''
    passwd = ''
    if 'OS_USERNAME' in env:
        userName=env['OS_USERNAME']
    if 'OS_PASSWORD' in env:
        passwd=env['OS_PASSWORD']
    
    if userName == '':
        userName = raw_input("user name:\n")
        env['OS_USERNAME']=passwd
    if passwd == '':
        passwd = getpass.getpass('Password:\n')
        env['OS_PASSWORD']=passwd

    try:
        conn = connection.Connection(
            region_name=vms_info['region_name'],
            auth=dict(
                auth_url=vms_info['auth_url'],
                username=userName,
                password=passwd,
                project_name=vms_info['project_name'],
                tenant_name=vms_info['tenant_name'],
                tenant_id=vms_info['tenant_id']),
            compute_api_version='2',
            identity_interface='internal')
        return conn
    except (IOError,ValueError) as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)

def get_volumes(conn):
    return conn.list_volumes()

def is_volume_here(volumes,vName):
    for volume in volumes:
        if 'name' in volume:
            if vName == volume['name']:
                return True
    return False

def main():
    #openstack.enable_logging(debug=True)
    vms_info = get_vms_info();
    conn = connexion(vms_info)
    vms = vms_info['vms']
    vms_name = sorted(vms)
    volumes  = get_volumes(conn)
    for vm_name in vms_name:
        if not is_volume_here(volumes,vm_name):
            try:
                vo = conn.create_volume(vms[vm_name]['size'], wait=True, image=vms_info['image'], description=vms[vm_name]['desc'], name=vm_name, bootable=True)
                print 'The volume '+vo['name']+' has been created'
            except (exc.OpenStackCloudException,exc.OpenStackCloudTimeout) as e:
                print 'Error from openstack'
                print e
        else:
            print 'The Volume '+vm_name+' is already available'

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
