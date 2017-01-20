#!/usr/bin/env python

"""Get a list of VLANs from a Cisco Nexus switch through the NETCONF protocol"""

__author__ = 'Tom Lijnse'
__version__ = '0.2'

from ncclient import manager

n9kv = '192.168.221.3'
n9kv_user = 'admin'
n9kv_pwd = '1234QWer'

def get_vlans(device):
    vlan_filter = '''
        <show xmlns="http://www.cisco.com/nxos:1.0">
            <vlan>
            </vlan>
        </show>
        '''
    vlan_tree = device.get(('subtree', vlan_filter))
    ns_map = {'vlan_mgr_cli':'http://www.cisco.com/nxos:1.0:vlan_mgr_cli'}
    vlan_rows = vlan_tree.data_ele.findall('.//vlan_mgr_cli:ROW_vlanbrief', ns_map)
    vlans = []
    for vlan_row in vlan_rows:
        vlan_id = vlan_row.find('vlan_mgr_cli:vlanshowbr-vlanid',ns_map)
        vlan_name = vlan_row.find('vlan_mgr_cli:vlanshowbr-vlanname',ns_map)
        vlans.append({'vlan_id' : int(vlan_id.text), 'vlan_name': vlan_name.text})
    return(vlans)

def main():
    with manager.connect(
            host = n9kv,
            port = 22,
            username = n9kv_user,
            password = n9kv_pwd,
            hostkey_verify = False,
            device_params = {'name': 'nexus'},
            allow_agent = False,
            look_for_keys = False) as device:
        vlans = get_vlans(device)
        for vlan in vlans:
            print 'VLAN id {} with name "{}"'.format(vlan['vlan_id'],vlan['vlan_name'])

if __name__ == '__main__':
    main()
