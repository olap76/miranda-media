#!/usr/bin/python3

import sys
import pexpect
import re
import getpass

password = getpass.getpass()

def parse_host():

    match = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', sys.argv[1])

    # if arg is IP address
    if match:
        host = match.group()
    else:
    # if arg is hostname
        if len(sys.argv[1]) < 25:
            host = str(sys.argv[1]) + ".miranda-media.net"
        else:
            host = str(sys.argv[1])
    return host


def cli_login():

    child.expect('Password: ')
    child.sendline(password)
    child.expect('>')

# check if interface unit is not used
def check_jun_unit():

    curr_vlan = int(s_vlan)
#    print('######################################################')

    while True:

        cli_line = 'show interface terse | match ' + str(curr_vlan)

        # print every 10-th check as debug
        if (curr_vlan % 10 == 0):
            print('--- checking ' + str(curr_vlan)[:-1] + '_')
###        print(cli_line)

        child.sendline(cli_line)
        child.expect(cli_line)
        child.expect('>')

        #
        # find empty units using length of cli output
        # if juniper cli has {master} : len=37 means 'empty' unit
        # if juniper cli without {master} : len=27 means 'empty' unit
        #

#        print('len=' + str(len(child.before)))

        if (len(child.before) == 37):
#            print('unit ' + str(curr_vlan))
            print(str(curr_vlan))

        curr_vlan += 1
        if curr_vlan > int(f_vlan):
            break

# exit juniper cli
def logout():
    child.sendline('quit')


#********************** main script *****************************

if __name__ == '__main__':

    #start vlan
    s_vlan = int(input("Start vlan: ")) 

    #finish vlan
    while True:
        f_vlan = int(input("Finish vlan: "))
        if (f_vlan > s_vlan):
            break

    s_link = 'ssh o.laposhin@' + parse_host()

    # ssh to juniper
    child = pexpect.spawn(s_link)

    # login to juniper
    cli_login()

    # check unit
    check_jun_unit()

    # exit juniper cli
    logout()
