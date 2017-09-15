#!/usr/bin/env python

"""Get the NETCONF capabilities of a device"""

from ncclient import manager

device_ip = '172.16.1.14'
device_port = '830'
device_type = 'iosxr'
device_user = 'cisco'
device_password = 'cisco'

def sort_capabilities(device_capabilities):
    capabilities = []
    for capability in device_capabilities:
        capabilities.append(capability)
    capabilities.sort()
    return capabilities

def main():
    with manager.connect(
            host = device_ip,
            port = device_port,
            username = device_user,
            password = device_password,
            hostkey_verify = False,
            device_params = {'name': device_type},
            allow_agent = False,
            look_for_keys = False) as device:
        capabilities = sort_capabilities(device.server_capabilities)
        for capability in capabilities:
            print capability

if __name__ == '__main__':
    main()