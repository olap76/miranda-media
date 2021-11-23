#!/usr/bin/python3

import sys
import re
import getpass
import json


from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


# exec cli command on device and print output
def display_info(net_connect, cli_commmand):
    output = net_connect.send_command(cli_commmand)
    print(output)

def dev_connect(bpe_ip):
  try:
    device = {
        "device_type": "juniper",
        "host": bpe_ip,
        "username": "o.laposhin",
        "password": password
        }

    net_connect = ConnectHandler(**device)


    with open('file_08_11_21.txt') as f:
        route_list = f.read().splitlines()


    for route in route_list:

        cli_line = 'show route ' + route + '| display json'

        output = net_connect.send_command(cli_line)

        temp = json.loads(output)

        # if 'show route ...' not empty 
        if len(temp['route-information'][0]) > 1:

#            print(temp['route-information'][0])
            # get BPE interface
            ae20_iface = temp['route-information'][0]['route-table'][0]['rt'][1]['rt-entry'][0]['nh'][0]['nh-local-interface'][0]['data']

            cli_line = 'show interfaces descriptions ' + ae20_iface
            output = net_connect.send_command(cli_line)
            print(output)


    # close connection
    net_connect.disconnect()

  except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
    print('<<<ERROR:>>>', router, error)

if __name__ == '__main__':

    # get pe
    bpe_ip = ""
    # get password
    password = getpass.getpass()

    dev_connect(bpe_ip)
