


from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

user = 'o.laposhin'
passwd = ''


# read loopback ip's from file
file = open('device_list.txt', 'r')

# exec cli command on device and print output
def display_info(cli_commmand):
    output = net_connect.send_command(cli_commmand)
    print(output)

# count devices to print omn screen, start with '2'
count = 2

for router in file.readlines():

  try:
    device = {
        "device_type": "huawei",
        "host": router,
        "username": user,
        "password": passwd
        }

    net_connect = ConnectHandler(**device)

    print('\n')
    print(count, '-----------------------------------------')

    #net_connect.find_prompt()
    #display_info('display version | include NE')

    display_info('display current-configuration | include sysname')
#    display_info('display isis peer')
    display_info('display current-configuration interface Eth-Trunk0 | include ip address')
    display_info('display current-configuration interface Eth-Trunk1 | include ip address')

    # close connection
    net_connect.disconnect()


  except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
    print(count, '-----------------------------------------')
    print('   --- ip:', router, error)

  #inc counter
  count += 1
