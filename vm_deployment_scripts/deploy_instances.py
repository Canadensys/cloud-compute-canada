#!/usr/bin/python

# deploy instances
# if not it's only a volume
# test if server name exists openstack server show VM
# if no No server with a name or ID of 'VM' exists.
# test if volume to used is here
# openstack server create --flavor flavorType --volume VOLUMENAME --nic port-id='NUMPORTID' --security-group default --user-data ./userdataFILE VMNAME
# test if ip is there
# openstack server add floating ip to specific vm
# openstack server add volume on scpecific vm

'''
https://docs.openstack.org/openstacksdk/latest/user/connection.html


create_port(network_id, **kwargs)

    Create a port
    Parameters:	

        network_id - The ID of the network. (Required)
        name - A symbolic name for the port. (Optional)
        admin_state_up - The administrative status of the port, which is up (true, default) or down (false). (Optional)
        mac_address - The MAC address. (Optional)
        fixed_ips - List of ip_addresses and subnet_ids. See subnet_id and ip_address. (Optional) For example:
            [
              {
                "ip_address": "10.29.29.13",
                "subnet_id": "a78484c4-c380-4b47-85aa-21c51a2d8cbd"
              }, ...
            ]

        subnet_id - If you specify only a subnet ID, OpenStack Networking allocates an available IP from that subnet to the port. (Optional) If you specify both a subnet ID and an IP address, OpenStack Networking tries to allocate the specified address to the port.
        ip_address - If you specify both a subnet ID and an IP address, OpenStack Networking tries to allocate the specified address to the port.
        security_groups - List of security group UUIDs. (Optional)
        allowed_address_pairs - Allowed address pairs list (Optional) For example:
            [
              {
                "ip_address": "23.23.23.1",
                "mac_address": "fa:16:3e:c4:cd:3f"
              }, ...
            ]

        extra_dhcp_opts - Extra DHCP options. (Optional). For example:
            [
              {
                "opt_name": "opt name1",
                "opt_value": "value1"
              }, ...
            ]
        device_owner - The ID of the entity that uses this port. For example, a DHCP agent. (Optional)
        device_id - The ID of the device that uses this port. For example, a virtual server. (Optional)

    Returns:    a munch.Munch describing the created port.
    Raises:     OpenStackCloudException on operation error.




create_server(name, image=None, flavor=None, auto_ip=True, ips=None, ip_pool=None, root_volume=None, terminate_volume=False, wait=False, timeout=180, reuse_ips=True, network=None, boot_from_volume=False, volume_size='50', boot_volume=None, volumes=None, nat_destination=None, group=None, **kwargs)

    Create a virtual server instance.
    Parameters:	

        flavor - Flavor dict, name or ID to boot onto.
        boot_volume - Name or ID of a volume to boot from (defaults to None)
        nics - (optional extension) an ordered list of nics to be added to this server, with information about connected networks, fixed IPs, port etc.
        security_groups - A list of security group names
        userdata - user data to pass to be exposed by the metadata server this can be a file type object as well or a string.
        name - Something to name the server.
        wait - (optional) Wait for the address to appear as assigned to the server. Defaults to False.

        volumes - (optional) A list of volumes to attach to the server
        ip_pool - Name of the network or floating IP pool to get an address from. (defaults to None)
        root_volume - Name or ID of a volume to boot from (defaults to None - deprecated, use boot_volume)
        terminate_volume - If booting from a volume, whether it should be deleted when the server is destroyed. (defaults to False)
        meta - (optional) A dict of arbitrary key/value metadata to store for this server. Both keys and values must be <=255 characters.
        files - (optional, deprecated) A dict of files to overwrite on the server upon boot. Keys are file names (i.e. /etc/passwd) and values are the file contents (either as a string or as a file-like object). A maximum of five entries is allowed, and each file must be 10k or less.
        reservation_id - a UUID for the set of servers being requested.
        min_count - (optional extension) The minimum number of servers to launch.
        max_count - (optional extension) The maximum number of servers to launch.
        key_name - (optional extension) name of previously created keypair to inject into the instance.
        availability_zone - Name of the availability zone for instance placement.
        block_device_mapping - (optional) A dict of block device mappings for this server.
        block_device_mapping_v2 - (optional) A dict of block device mappings for this server.
        scheduler_hints - (optional extension) arbitrary key-value pairs specified by the client to help boot an instance
        config_drive - (optional extension) value for config drive either boolean, or volume-id
        disk_config - (optional extension) control how the disk is partitioned when the server is created. possible values are AUTO or MANUAL.
        admin_pass - (optional extension) add a user supplied admin password.
        timeout - (optional) Seconds to wait, defaults to 60. See the wait parameter.
        reuse_ips - (optional) Whether to attempt to reuse pre-existing floating ips should a floating IP be needed (defaults to True)
        network - (optional) Network dict or name or ID to attach the server to. Mutually exclusive with the nics parameter. Can also be be a list of network names or IDs or network dicts.
        boot_from_volume - Whether to boot from volume. boot_volume implies True, but boot_from_volume=True with no boot_volume is valid and will create a volume from the image and use that.
        nat_destination - Which network should a created floating IP be attached to, if it's not possible to infer from the cloud's configuration. (Optional, defaults to None)
        auto_ip - Whether to take actions to find a routable IP for the server. (defaults to True)
        ips - List of IPs to attach to the server (defaults to None)
        image - Image dict, name or ID to boot with. image is required unless boot_volume is given.
        group - ServerGroup dict, name or id to boot the server in. If a group is provided in both scheduler_hints and in the group param, the group param will win. (Optional, defaults to None)
        volume_size - When booting an image from volume, how big should the created volume be? Defaults to 50.

    Returns:    A munch.Munch representing the created server.
    Raises:     OpenStackCloudException on operation error.
    
    




    
attach_volume(server, volume, device=None, wait=True, timeout=None)

    Attach a volume to a server.

    This will attach a volume, described by the passed in volume dict (as returned by get_volume()), to the server described by the passed in server dict (as returned by get_server()) on the named device on the server.

    If the volume is already attached to the server, or generally not available, then an exception is raised. To re-attach to a server, but under a different device, the user must detach it first.
    Parameters:	

        server - The server dict to attach to.
        volume - The volume dict to attach.
        device - The device name where the volume will attach.
        wait - If true, waits for volume to be attached.
        timeout - Seconds to wait for volume attachment. None is forever.

    Returns:    a volume attachment object.
    Raises:     OpenStackCloudTimeout if wait time exceeded.
    Raises:     OpenStackCloudException on operation error.    

'''

#import openstack.cloud
import shade
from shade import exc
import novaclient
import shlex, subprocess
import openstack

def get_vms_info():
    # extract information from yaml file
    import yaml
    vms_info = {}
    with open("vms_info.yml", 'r') as stream:
        try:
            vms_info = yaml.safe_load(stream)
            return vms_info
        except yaml.YAMLError as exc:
            print 'Yaml error'
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

def get_volume_by_name(conn,vName):
    volumes = get_volumes(conn)
    for volume in volumes:
        if 'name' in volume:
            if vName == volume['name']:
                return volume
    return ''

def get_servers(conn):
    return conn.list_servers()

def is_server_here(servers,vName):
    for server in servers:
        if 'name' in server:
            if vName in server['name']:
                return True
    return False

def get_server_from_name(conn,vName):
    servers = get_servers(conn)
    for server in servers:
        if 'name' in server:
            if vName in server['name']:
                return server
    return ''

def list_networks(conn):
    print("List Networks:")

    for network in conn.network.networks():
        print(network)

def list_ports(conn):
    print("List Networks:")
    
    for port in conn.network.ports():
        if (port.name != ''):
            print '>'+port.name+'<'
        #if 'name' in port:
        #    print(port['name'])

def get_ports(conn):
    ports = conn.network.ports()
    portsF = {}
    for port in ports:
        if (port.name != ''):
            portsF[str(port.name)] = port
    
    return portsF
    
def is_port_here(ports, vm_name):
    for port in ports:
        return vm_name in ports
    return False

def is_lgName_in_lgs(lgName,lgs):
    for lg in lgs:
        if(lg.name == lgName):
            return True
    return False

def main():
    #openstack.enable_logging(debug=True)
    vms_info = get_vms_info();
    conn = connexion(vms_info)
    vms = vms_info['vms']
    vms_name = sorted(vms)
    volumes  = get_volumes(conn)
    servers  = get_servers(conn)
    ports = get_ports(conn)
    
    #
    # Create ports
    # 
    for vm_name in vms_name:
        if (vms[vm_name]['ip']):
            # if port is not here need to create it
            if (not is_port_here(ports, vm_name)):
                try:
                    securityGroupsVal = vms[vm_name]['security-group']
                    ipAdress = vms_info['ip-local']+str(vms[vm_name]['ip'])
                    fixedIps = [{'ip_address':ipAdress,'subnet_id':vms_info['subnet-id']}]
                    newPort = conn.network.create_port(network_id=vms_info['network-id'],name=vm_name,fixed_ips=fixedIps,security_group=securityGroupsVal)
                    print 'The Port '+vm_name+' is now available with port_id '+newPort.id
                    ports[vm_name] = newPort
                except (exc.OpenStackCloudException,exc.OpenStackCloudTimeout) as e:
                    print 'Error from openstack'
                    print e
            else:
                print 'The Port '+vm_name+' is already available.'
    
    #
    # Create servers
    # 
    server = ''
    for vm_name in vms_name:
        if vms[vm_name]['ip'] and (vm_name in ports):
            if (is_volume_here(volumes,vm_name)):
                securityGroupsVal = vms[vm_name]['security-group']
                
                # Launch server
                if (not is_server_here(servers,vm_name)):
                    try:
                        # Variables
                        portID = ports[vm_name].id
                        
                        flavorVal = ''
                        if 'flavor' in vms[vm_name]:
                            flavorVal = vms[vm_name]['flavor']
                        else :
                            print 'no flavorVal'
                            system.exit
                        # Need a file object
                        userdataVal = './user_config/user_'+vm_name+'.txt'
                        userdataValObject  = open(userdataVal, 'r')
                        
                        # command to launch
                        server = conn.create_server(vm_name, flavor=flavorVal, reuse_ips=False, boot_volume=vm_name, volumes=None, nics=[{'port-id':portID}], userdata=userdataValObject)
                        # remove auto ip or ConflictException: 409
                        server = conn.wait_for_server(server,timeout=180,auto_ip=False) 
                        print 'The Instance '+vm_name+' is now available'
                    except (exc.OpenStackCloudException,exc.OpenStackCloudTimeout) as e:
                        print 'Error from openstack'
                        print e
                else:
                    server = get_server_from_name(conn,vm_name)
                    print 'The Instance '+vm_name+' is already available'
                
                # Check security group
                # if security group is ok do nothing else remove the current add the other
                # In our case we just have two security groups
                if (server != ''):
                    lgs = conn.list_server_security_groups(server)
                    b = is_lgName_in_lgs(securityGroupsVal,lgs)
                    if (not b):
                        for lg in lgs:
                            print 'Remove the '+lg.name+' security group from '+vm_name
                            print conn.remove_server_security_groups(server,lg)
                        print 'Add the '+securityGroupsVal+' security group for '+vm_name
                        print conn.add_server_security_groups(server, securityGroupsVal)
                
                # Assign floating ip
                # In our case we just have one floating ip
                if ('floating-ip' in vms[vm_name]) and server!='':
                    try:
                        fip= [vms[vm_name]['floating-ip']]
                        ip = conn.add_ip_list(server,fip,wait=False)
                        print 'The floating ip address '+vms[vm_name]['floating-ip']+' has been assign to '+ip['name']
                    except (exc.OpenStackCloudException,exc.OpenStackCloudTimeout) as e:
                        print 'Error from openstack'
                        print e
                
                # Assign mounted volumes
                # In our case we just have one nfs
                if ('mounted-volume' in vms[vm_name]) and (server!='') :
                    try:
                        vb = get_volume_by_name(conn,vms[vm_name]['mounted-volume'])
                        if (vb!=''):
                            v = conn.get_volume_attach_device(vb, server.id)
                            if (v==None):
                                va = conn.attach_volume(server, vb, device=None, wait=True, timeout=None)
                                v = conn.get_volume_attach_device(vb, server.id)
                                print 'The volume '+vms[vm_name]['mounted-volume']+' is mounted on '+v+' for the Instance '+vm_name
                            else:
                                print 'The volume '+vms[vm_name]['mounted-volume']+' is already mounted on '+v+' for the Instance '+vm_name
                    except (exc.OpenStackCloudException,exc.OpenStackCloudTimeout) as e:
                        print 'Error from openstack'
                        print e
            else:
                print 'The Volume '+vm_name+' is not available'
    
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print 'main error'
        print(e)
