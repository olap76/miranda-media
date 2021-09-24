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
    else:
    # if arg is hostname
        match_domain = re.search('.net$', sys.argv[1])
        if match_domain:
            host = str(sys.argv[1])
        else:
            host = str(sys.argv[1]) + ".miranda-media.net"

    return host

t_link = 'telnet ' + parse_host()

child = pexpect.spawn(t_link)

child.expect('(User Name:)|(login:)|(Username:)')
#child.expect('(User Name:)|(login:)')
child.sendline(username)

child.expect('Password:')
child.sendline(password)

child.expect('#')
child.sendline('\n')
child.interact()
