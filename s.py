#!/usr/bin/python3

import sys
import pexpect
import re

username = ''
password = ''

def parse_host():

    match_ip = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', sys.argv[1])

    # if arg is IP address
    if match_ip:
        host = match_ip.group()

    # if arg is hostname
    else:
        match_domain = re.search('.net$', sys.argv[1])
        if match_domain:
            host = str(sys.argv[1])
        else:
            host = str(sys.argv[1]) + ".miranda-media.net"

    return host

s_link = 'ssh ' + username + '@' + parse_host()

#print(s_link)

child = pexpect.spawn(s_link)

#child.expect('Password: ')
child.expect('(Password:)|(Enter password:)|(User password:)')
child.sendline(password)

child.expect('>')
child.sendline('\n')
child.interact()
