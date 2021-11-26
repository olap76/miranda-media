#!/usr/bin/python3

import csv
import sys
import pexpect
import re
import getpass

username = 'o.laposhin'
password = getpass.getpass()

read_file = 'asw_26.txt'
write_file = 'unavailable_asw.txt'

def asw_del_zond_vlan(read_file):

    with open(read_file, "r", encoding="utf-8") as f:
        raw_data = csv.reader(f, delimiter=";")
        for ip, vid in raw_data:

            print('--- Connecting to ...', ip)

            try:
                t_link = 'telnet ' + ip

                child = pexpect.spawn(t_link)

                child.expect('(User Name:)|(login:)|(Username:)', timeout=3)

                child.sendline(username)

                child.expect('Password:')
                child.sendline(password)

                child.expect('#')
                #print(child.before.decode('utf-8'))

                child.sendline('show vlan tag ' + vid)
                child.expect('#')
                print(child.before.decode('utf-8'))

                child.sendline('conf')
                child.expect('#')

                child.sendline('interface vlan ' + vid)
                child.expect('#')

                child.sendline('no ip address')
                child.expect('#')

                child.sendline('exit')
                child.expect('#')

                child.sendline('vlan database')
                child.expect('#')
                child.sendline('no vlan ' + vid)
                child.expect('#')

                child.sendline('end')
                child.expect('#')

                child.sendline('show vlan tag ' + vid)
                child.expect('#')
                print(child.before.decode('utf-8'))
#---
                child.sendline('wr')
                child.sendline('y')
                child.expect('#')
                print(child.before.decode('utf-8'))
#---
                child.close()


            except (pexpect.exceptions.TIMEOUT) as error:
#                print('   !!! ip:', ip, error)
                print('!!! UNAVAILABLE:', ip)
                with open(write_file, "a", encoding="utf-8", newline='') as wr_f:
                    writer = csv.writer(wr_f, delimiter=';')
                    line = [ip, vid]
                    writer.writerow(line)


#--------------main---------------------

if __name__ == '__main__':

    asw_del_zond_vlan(read_file)
