#!/usr/bin/python3

import sys
import pexpect
import re
import getpass

# -------------------------------- vars ---------------------
username = 'o.laposhin'

# for eltex 3324 switches
#hosts_file = 'hosts_eltex3324'

# for eltex 3348 switches
hosts_file = 'hosts_eltex3348'
#------------------------------------------------------------

password = getpass.getpass()

# show version
def sh_ver(host_list):

  for host in host_list:

    print('----------------------------')

    t_link = 'telnet ' + host

    child = pexpect.spawn(t_link)

    child.expect('(User Name:)|(login:)|(Username:)')
    #child.expect('(User Name:)|(login:)')
    child.sendline(username)

    child.expect('Password:')
    child.sendline(password)

    child.expect('#')
    child.sendline('show version\n')
    child.expect('#')
    print(child.before.decode('utf-8'))
    child.close()

# show version
def sh_lldp_nei(host_list):

  for host in host_list:

    print('----------------------------')

    t_link = 'telnet ' + host

    child = pexpect.spawn(t_link)

    child.expect('(User Name:)|(login:)|(Username:)')
    #child.expect('(User Name:)|(login:)')
    child.sendline(username)

    child.expect('Password:')
    child.sendline(password)

    child.expect('#')
    child.sendline('show lldp neighbors > flash://lldp1.txt\n')
    child.sendline('copy flash://lldp1.txt scp://admin-mkt:rhsv2014@172.16.2.4/' + host + '.txt\n')
    child.expect('#')
#    print(child.before.decode('utf-8'))
    child.close()


#************************main**************************


# create host list from text file
with open(hosts_file) as f:
  host_list = f.read().splitlines()

# show versin on all switches
sh_lldp_nei(host_list)
#sh_ver(host_list)

