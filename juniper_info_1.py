
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


# read loopback ip's from file
file = open('device_list.txt', 'r')

# exec cli command on device and print output
def display_info(cli_commmand):
    output = net_connect.send_command(cli_commmand)
    print(output)

for router in file.readlines():

  try:
    device = {
        "device_type": "juniper",
        "host": router,
        "username": "o.laposhin",
        "password": "Ureacoh9"
        }

    net_connect = ConnectHandler(**device)

#    print('\n')
    print('--- ' + router)

    #net_connect.find_prompt()

#    display_info('show chassis hardware | match PEM')
#    display_info('show conf snmp')
    display_info('show configuration snmp | match 185.64.46.60/32')

    # close connection
    net_connect.disconnect()


  except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
    print('   --- ip:', router, error)

