#!/usr/bin/python
# create the config files for all vm
# copy/paste default with new name, sed to change lines in the new file

from shutil import copyfile
import fileinput
import yaml

vms_info = {}
# extract information from yaml file
with open("vms_info.yml", 'r') as stream:
    try:
        vms_info = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        
# sort vm names
vm_names = sorted(vms_info['vms'])

# copy file with mofidification for hostname
sFile = './user_vm-default.txt'
ddFile = './user_config/'
h = 'hostname'
for vm_name in vm_names:
    if 'ip' in vms_info['vms'][vm_name]:
        dFile = ddFile+'user_'+vm_name+'.txt'
        copyfile(sFile,dFile)
        for line in fileinput.input(dFile, inplace=True):
            if h in line:
                print "%s\n" % (h+': '+vm_name),
            else:
                print "%s" % (line),
