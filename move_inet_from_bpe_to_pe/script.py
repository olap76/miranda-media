#!/usr/bin/python3

import csv
from jinja2 import Environment, FileSystemLoader

def main(user_pe):

    variables = []
    with open("file_28_11.txt", "r", encoding="utf-8") as f:
        for line in f:

            sw = {}

            # input file format:
            # ge-1/2/0.1058   up    up   -- VPLS | - | RNKB | 2M | s.Mezhvodnoe,ul.Pervomaiskaya,3A to BPE | 13.10.20 | nabokov | 110-1058 -- 
            line_list = line.split("|")

            # extract iface and unit to list
            iface_unit_list = line_list[0].split()[0].split(".")

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
            sw["ip"] = "_IP_"
            sw["instance"] = "INET-B2B"

            # ask PE from user
            sw["pe_site"] = user_pe

            variables.append(sw)

    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("L3VPN.j2")

    with open("L3VPN_config.txt", "w", encoding="utf-8") as f:
        for line in variables:
            f.write(template.render(line))
            f.write("\n")

#--------------main---------------------

if __name__ == "__main__":

    user_pe = str(input("Enter PE (ex: KRCH-00-AR2):" ))

    main(user_pe)
