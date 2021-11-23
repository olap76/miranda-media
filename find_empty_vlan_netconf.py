#!/usr/bin/python3

import re
import getpass
from jnpr.junos import Device
from myTables.ConfigTables import IfaceTable

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

def get_used_vids_set(host, uname, pw):
    # initialize empty unit list
    unit_set = {None}

    # get data from router and store to dev_units
    with Device(host=parse_host(host), user=uname, password=pw) as dev:
        dev_units = IfaceTable(dev)
        dev_units.get()

    # this is shit, but works
    # parse device output, extract vlans(units) and add to unit_set
    for outer_unit in dev_units:
        for inner_unit in outer_unit.values():
            if (type(inner_unit) is list):
                for vlan in inner_unit:
                    unit_set.add(vlan)
            elif (type(inner_unit) is str):
                unit_set.add(inner_unit)

    return unit_set

def print_unit_set():
    """ print unit set for debug """
    unit_list = list(unit_set)
    unit_list.remove(None)
    sorted_unit_list = unit_list.sort()
    for i in range(0, len(unit_list)):
        print(unit_list[i])

def get_busy_units_in_range(unit_set, start_unit, end_unit):

    #set to store busy units from device
    busy_set = {None}

    # check every unit from start to end
    for user_unit in range(int(start_unit),  int(end_unit) + 1):
        user_unit_str = str(user_unit)
        #check every unit(vlan) from device
        for dev_unit in unit_set:
            # if match add unit(vlan) to busy_set and go to next unit
                if (user_unit_str == dev_unit):
                    busy_set.add(user_unit_str)
                    break

    return busy_set

def print_empty_units(busy_set, start_unit, end_unit):
    """ prints every user unit NOT in busy_set"""
    vid_list = get_empty_units_list(busy_set, start_unit, end_unit)
    for vid in vid_list:
        print(vid)

def get_empty_units_list(busy_set, start_unit, end_unit):
    """ return list of every user unit NOT in busy_set"""

    vid_list = []

    for user_unit in range(int(start_unit),  int(end_unit) + 1):
        user_unit_str = str(user_unit)
        if user_unit_str not in busy_set:
            vid_list.append(user_unit_str)

    return vid_list

if __name__ == '__main__':
    #connection vars
    host = input("Hostname or IP: ")
#    uname = input("Username: ")
    uname = 'o.laposhin'    
    pw = getpass.getpass()

    # get start vlan
    start_unit = input("Start unit: ")
    # get finish vlan
    end_unit = input("End unit: ")

    print("Available units:")

    # get set of used vids from device
    used_vids_set = get_used_vids_set(host, uname, pw)
    # checks units in range (start_unit, end_unit) and add available on device to set  
    busy_set = get_busy_units_in_range(used_vids_set, start_unit, end_unit)
    # print available units
    print_empty_units(busy_set, start_unit, end_unit)
