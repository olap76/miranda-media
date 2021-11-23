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
#hosts_file = 'hosts_eltex3348'
#------------------------------------------------------------

password = getpass.getpass()

# activate inactive firmware and show version
def activate_sh_ver(host_list):

  for host in host_list:

    t_link = 'telnet ' + host

    child = pexpect.spawn(t_link)

    child.expect('(User Name:)|(login:)|(Username:)')
    #child.expect('(User Name:)|(login:)')
    child.sendline(username)

    child.expect('Password:')
    child.sendline(password)

    child.expect('#')
    child.sendline('boot system inactive-image\n')

    child.expect('#')
    child.sendline('show version\n')
    child.expect('#')
    print(child.before.decode('utf-8'))
    child.close()

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

def sh_uptime(host_list):

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
    child.sendline('show system | include sec\n')
    child.expect('#')
    print(child.before.decode('utf-8'))
    child.close()

# copy firmware on switches
def copy_firmware(host_list):

  for host in host_list:

    t_link = 'telnet ' + host

    child = pexpect.spawn(t_link)

    child.expect('(User Name:)|(login:)|(Username:)')
    #child.expect('(User Name:)|(login:)')
    child.sendline(username)

    child.expect('Password:')
    child.sendline(password)

    child.expect('#')
    print(child.before.decode('utf-8'))
    child.sendline('boot system tftp://172.31.2.27/mes3300-4016-R2.ros\n')
    child.expect('#', timeout=1200)
    child.sendline('boot system inactive-image\n')
    child.expect('#')

    child.close()

#************************main**************************


# create host list from text file
#with open(hosts_file) as f:
#  host_list = f.read().splitlines()

host_list = ['172.31.51.2',]


# show versin on all switches
sh_ver(host_list)

# show uptime on all switches
#sh_uptime(host_list)

# copy firmware on switches
#copy_firmware(host_list)

# activate inactive firmware and show version
#activate_sh_ver(host_list)
