#!/usr/bin/env python

"""Get the current traffic rates on active interfaces from a Cisco Nexus switch through the NETCONF protocol"""

__author__ = 'Tom Lijnse'
__version__ = '0.2'

from ncclient import manager
from getpass import getpass
from terminaltables import SingleTable

switch_names = ['n9kv-1.lab.layerzero.nl',
                'n9kv-2.lab.layerzero.nl',
                ]
switch_user = raw_input("Switch user name: ")
switch_pwd = getpass("Switch password: ")

def get_intf_rates(device):
    interface_filter = '''
        <show xmlns="http://www.cisco.com/nxos:1.0">
            <interface>
            </interface>
        </show>
        '''
    interface_tree = device.get(('subtree', interface_filter))
    ns_map = {'if_manager':'http://www.cisco.com/nxos:1.0:if_manager'}
    interface_rows = interface_tree.data_ele.findall('.//if_manager:ROW_interface', ns_map)
    interfaces = [['Interface', 'Description', 'Bitrate in (Mbps)', 'Bitrate out (Mbps)']]
    for interface_row in interface_rows:
    	interface_state = interface_row.find('if_manager:state', ns_map)
    	if interface_state.text == 'up':
    		interface_id = interface_row.find('if_manager:interface', ns_map)
    		interface_description = interface_row.find('if_manager:desc', ns_map)
    		interface_bitrate_in = interface_row.find('if_manager:eth_inrate1_bits', ns_map)
    		interface_bitrate_out = interface_row.find('if_manager:eth_outrate1_bits', ns_map)
    		if interface_description is None:
    			interface_description = '""'
    		else:
    			interface_description = interface_description.text
    		if interface_bitrate_in is None:
    			interface_bitrate_in = '?'
    		else:
    			interface_bitrate_in = round(float(interface_bitrate_in.text)/1000000, 3)
    		if interface_bitrate_out is None:
    			interface_bitrate_out = '?'
    		else:
    			interface_bitrate_out = round(float(interface_bitrate_out.text)/1000000, 3)
        	interfaces.append([interface_id.text, interface_description, interface_bitrate_in, interface_bitrate_out])
    return(interfaces)

def main():
    for switch_name in switch_names:
	    with manager.connect(
                host = switch_name,
                port = 22,
                username = switch_user,
                password = switch_pwd,
                hostkey_verify = False,
                device_params = {'name': 'nexus'},
                allow_agent = False,
                look_for_keys = False) as device:
	        interfaces = get_intf_rates(device)
	        interface_table = SingleTable(interfaces, title=switch_name)
	        print '\n' + interface_table.table

if __name__ == '__main__':
    main()
