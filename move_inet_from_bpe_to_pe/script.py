#!/usr/bin/python3

from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

import json
import getpass
import csv
from jinja2 import Environment, FileSystemLoader

def main(pe_name, bpe_ip, user, passwd, out_pe_file):

    variables = []
    with open("file_28_11.txt", "r", encoding="utf-8") as f:
        for line in f:

            sw = {}

            # input file format:
            # ge-1/2/0.1058   up    up   -- VPLS | - | RNKB | 2M | s.Mezhvodnoe,ul.Pervomaiskaya,3A to BPE | 13.10.20 | nabokov | 110-1058 --
            line_list = line.split("|")

            # extract iface and unit to list
            iface_unit_list = line_list[0].split()[0].split(".")
            # for debug
            print('---')
            print('iface: ', iface_unit_list[0] + "." + iface_unit_list[1])

            sw["interface"] = iface_unit_list[0]
            sw["unit"] = iface_unit_list[1]
            sw["suz"] = "_SUZ-XXXXX_"
            sw["client"] = line_list[2].strip()
            sw["policerdesc"] = line_list[3].strip()

            # extract lacation to list
            loc_list = line_list[4].split()
            sw["location"] = loc_list[0].strip()

            sw["date"] = line_list[5].strip()
            sw["who"] = line_list[6].strip()
            sw["policer"] = "lim" + line_list[3][1:-2] + line_list[3][-2].lower()

            # get ip from bpe using iface description
            pe_ip = get_ip(line_list[7], bpe_ip, user, passwd)

            print('ip: ', pe_ip)

            sw["ip"] = pe_ip
            sw["instance"] = "INET-B2B"

            # ask PE from user
            sw["pe_site"] = pe_name

            variables.append(sw)

    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("L3VPN.j2")
    # save PE config
    with open(out_pe_file, "w", encoding="utf-8") as f:
        for line in variables:
            f.write(template.render(line))
            f.write("\n")

def check_desc(desc_string):

#    print(desc_string)
    desc_list = desc_string.split()
    # string for search on bpe
    search_str = desc_list[0]

    # if start with 2 digits - string valid, else - get next field
    if not search_str[0].isdigit() or not search_str[1].isdigit():

        temp_list = desc_list[0].split(",")
        search_str = temp_list[1]

    return search_str

def get_ip(desc_string, bpe_ip, user, passwd):

    search_str = check_desc(desc_string)

#    print(search_str)

    try:
        device = {
            "device_type": "juniper",
            "host": bpe_ip,
            "username": user,
            "password": passwd
        }

        net_connect = ConnectHandler(**device)

        cli_line = 'show interfaces descriptions | match ' + search_str

        output = net_connect.send_command(cli_line).split()

        iface = output[0]

#        print(iface)

        cli_line = 'show configuration interfaces ' + iface + ' | display json'

        output = net_connect.send_command(cli_line)

#        print(output)

        temp = json.loads(output)

        ip_addr = temp['configuration']['interfaces']['interface'][0]['unit'][0]['family']['inet']['address'][0]['name']

       # close connection
        net_connect.disconnect()

    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print('<<<ERROR:>>>', router, error)


#    print(ip_addr)
    return ip_addr

#--------------main---------------------

if __name__ == "__main__":

    # ask pe
    pe_name = str(input("Enter PE (ex: KRCH-00-AR2):" ))

    out_pe_file = pe_name + '.txt'

    out_bpe_file = 'SMFL-04-BPE1' + '_' + 'pe_name.txt'

    bpe_ip = "185.64.44.44"

    user= "o.laposhin"

    # get password
    passwd = getpass.getpass()

    main(pe_name, bpe_ip, user, passwd, out_pe_file)

