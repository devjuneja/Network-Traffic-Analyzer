import os
from netmiko import ConnectHandler
from ssh import check_ssh
from functions import *
from switch_functions import *

src = '192.168.1.50'
dst = '22.23.1.1'

commands = {1: "sh ip protocol summary",
            2: "sh ip eigrp nei",
            3: "sh version",
            4: "sh clock",
            5: "sh proc mem | ex 0.00",
            6: "show proc cpu"}

error_device_flag=[]

def log_tree(ip):

    net_connect = check_ssh(ip)

    if net_connect == None:
        print("Sorry you have an issue at this ip: %s\n"%ip)

    else:

        host_name = net_connect.find_prompt()
        host_name = host_name[:-1]
        f = open("C:\\Users\\devju\\PycharmProjects\\my_app\\static\\logs\\%s.txt" %host_name, 'w')
        f.write(" ---Hostname---\n")
        f.write("%s\n" %host_name)
        print("\n HOSTNAME: %s" %host_name)

        if 'Router' in host_name:

            error_temp_flag = []
            print("\nI'm in router")
            f.write("\n---Device type---\n")
            f.write("Router\n")

            text1 = device_stats(net_connect)
            for i in text1:
                f.write("%s\n" %i)
            text2,epi = proc_info(net_connect,ip)
            error_temp_flag.append(epi)
            for i in text2:
                f.write("%s\n" % i)

            text4=acl_check(net_connect)

            f.write("\n---Access Lists---\n")
            for i in text4:
                f.write("%s" % i)

            text3,flag,eps = protocol_summary(net_connect,ip,uptime)
            error_temp_flag.append(eps)

            if flag==1:
                f.write(text3[0])
            else:
                for i in text3:
                    f.write("%s\n" %i)

            if 1 in error_temp_flag:
                error_device_flag.append(1)
            else:
                error_device_flag.append(0)

        if 'Switch' in host_name:

            print("\nI'm in switch")
            f.write("\n---Device type---\n")
            f.write("Switch\n")

            text4 = device_stats(net_connect)
            for i in text4:
                f.write("%s\n" %i)
            interfaces,ips,macs = find_interfaces(net_connect)

            text5 = []
            error_flag = []
            for i in range(len(interfaces)):
                print("\n INTERFACE ",interfaces[i])
                text5.append("\nINTERFACE %s" %interfaces[i])
                text5.append("Ip %s" % ips[i])
                text5.append("Mac %s" % macs[i])
                text6,ef = check_interface(net_connect,interfaces[i])
                error_flag.append(ef)
                text5.extend(text6)

            if 1 in error_flag:
                error_device_flag.append(1)
            else:
                error_device_flag.append(0)

            for i in text5:
                f.write("%s\n" %i)

        f.close()
        net_connect.disconnect()


def path(src,dst):

    addr = [src]
    hop = ['0']

    ios = {
            'device_type': 'cisco_ios',
            'ip': src,
            'username': 'dev',
            'password': 'datla',
            'global_delay_factor': 2
    }

    net_connect = ConnectHandler(**ios)
    command = 'trace '
    command += dst
    route_dict = net_connect.send_command(command, use_textfsm=True)

    # print("Route dict:",route_dict)
    for hop_dict in route_dict:
        address = hop_dict['address']
        if address == '123.168.2.10':
            addr.append('172.16.1.225')
        else:
            addr.append(address)
        hop.append(hop_dict['hop_num'])

    route_info = dict(zip(hop, addr))
    return route_info

def host_name_ip(src,dst):

    dict = path(src,dst)
    # print("-----Dictionary in hostname----- :" ,dict)
    host_names=[]
    ips=[]
    device_type=[]

    loc = 0

    # print(error_device_flag)

    for ip in dict.values():
        handler = check_ssh(ip)
        if handler!= None:
            hostname = handler.find_prompt()
            hostname = hostname[:-1]

            if 'Router' in hostname and error_device_flag[loc]==0:
                device_type.append(1)

            elif 'Switch' in hostname and error_device_flag[loc]==0:
                device_type.append(2)

            elif 'Router' in hostname and error_device_flag[loc]==1:
                device_type.append(3)

            elif 'Switch' in hostname and error_device_flag[loc]==1:
                device_type.append(4)

            loc += 1

            host_names.append(hostname)
            ips.append(ip)
            handler.disconnect()


    return host_names,ips,device_type


def begin():

    print("Enter the Source IP:")
    src = input()
    print("Enter the Destination IP:")
    dst = input()

    print(" source: %s and dest: %s" %(src,dst))

    print("In the main function")
    print(" Calculating the Route")
    route_table = path(src,dst)
    print(route_table)

    # print(host_name_ip(src,dst))
    dir_name = "C:\\Users\\devju\\PycharmProjects\\my_app\\static\\logs\\"
    test = os.listdir(dir_name)

    for item in test:
        if item.endswith(".txt"):
            os.remove(os.path.join(dir_name, item))

    for ip in route_table.values():
        log_tree(ip)

    return src,dst


if __name__ == '__main__':
    begin(src,dst)