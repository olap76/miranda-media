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

# LOGIN
user = ''

# exec cli command on device and print output
def display_info(net_connect, cli_commmand):
    output = net_connect.send_command(cli_commmand)
    print(output)

def dev_connect(pe, user):
  try:
    device = {
        "device_type": "juniper",
        "host": pe,
        "username": user,
        "password": password
        }

    net_connect = ConnectHandler(**device)

    with open('file_09_11_21.txt') as f:
        file = f.read().splitlines()

    for entry in file:

        sub_if = entry.split('.')[1]

#        cli_line = 'show configuration interfaces ae16.' + sub_if
        cli_line = 'show interfaces descriptions ae16.' + sub_if

        output = net_connect.send_command(cli_line)

        print(output)

    # close connection
    net_connect.disconnect()

  except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
    print('<<<ERROR:>>>', router, error)

if __name__ == '__main__':

    # get pe
    pe = "185.64.44.12"
    # get password
    password = getpass.getpass()

    dev_connect(pe, user)

