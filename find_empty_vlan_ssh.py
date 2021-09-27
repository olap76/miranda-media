#!/usr/bin/python3

import sys
import re
import getpass

from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

def parse_host(host):
    match_ip = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', host)
    # if arg is IP address
    if match_ip:
        host = match_ip.group()
    else:
      # if arg is hostname
        match_domain = re.search('.net$', host)
        if not match_domain:
            host = host + ".miranda-media.net"

    return host

# exec cli command on device and print output
def display_info(net_connect, cli_commmand):
    output = net_connect.send_command(cli_commmand)
    print(output)

def dev_connect(start_vlan, end_vlan):
  try:
    device = {
        "device_type": "juniper",
        "host": parse_host(in_host),
        "username": user_name,
        "password": password
        }

    net_connect = ConnectHandler(**device)

    curr_vlan = int(start_vlan)

# loop checks if interface unit is not used
    while True:
        cli_line = 'show interface terse | match ' + str(curr_vlan)

        # print every 10-th check as debug
#        if (curr_vlan % 10 == 0):
#            print('--- checking ' + str(curr_vlan)[:-1] + '_')

        output = net_connect.send_command(cli_line)

#        print("vlan: ", output)
#        print("len:", len(output))

        #
        # find empty units using length of cli output
        # if juniper cli has {master} : len=9 means 'empty' unit
        # if juniper cli without {master} : len=XXX means 'empty' unit
        #

        if len(output) == 9:
            print(curr_vlan)

        curr_vlan += 1
        if curr_vlan > int(end_vlan):
            break

    # close connection
    net_connect.disconnect()

  except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
    print('<<<ERROR:>>>', router, error)

if __name__ == '__main__':

    # get pe
    in_host = input("PE hostname or IP: ")

    user_name = input("Login: ")
    # get password
    password = getpass.getpass()
    #get start vlan
    start_vlan = int(input("Start vlan: ")) 
    #get finish vlan
    while True:
        end_vlan = int(input("End vlan: "))
        if (end_vlan > start_vlan):
            break

    dev_connect(start_vlan, end_vlan)
