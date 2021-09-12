import collections
def find_interfaces(handler):

    data_list = []
    arp_stats = handler.send_command("sh ip arp", use_textfsm=True)

    address = []
    mac = []
    for dict in arp_stats:
        address.append(dict['address'])
        mac.append(dict['mac'])

    # print(address)
    # print(mac)

    mac_table = handler.send_command("sh mac address-table", use_textfsm=True)
    # print(mac_table)

    interfaces = []
    flag = []
    new_macs = []
    mapped_ips = []
    new_interfaces = []

    for each_mac_dict in mac_table:
        interfaces.append(each_mac_dict['destination_port'])

    counter = collections.Counter(interfaces)

    i=0
    for each in interfaces:
        if counter[each]==1:
            flag.append(i)
        i+=1

    i=0
    for each_mac_dict in mac_table:
        if i in flag:
            mapped_ips.append(address[mac.index(each_mac_dict['destination_address'])])
            new_macs.append(each_mac_dict['destination_address'])
            new_interfaces.append(each_mac_dict['destination_port'])
        i+=1

    print("\n LISTS of IP's and MAC's running on the different Interfaces")
    print("interfaces:", new_interfaces)
    print("mapped ips :", mapped_ips)
    print("mapped macs:", new_macs)
    # for i in range(len(new_interfaces)):
    #     data_list.append("interface:%s" %new_interfaces[i])
    #     data_list.append("mapped ip:%s" %mapped_ips[i])
    #     data_list.append("mapped mac:%s" %new_macs[i])

    return new_interfaces,mapped_ips,new_macs