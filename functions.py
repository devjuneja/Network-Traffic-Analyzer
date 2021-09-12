from router_functions import *
import re

commands = {1: "sh ip protocol summary",
            2: "sh ip eigrp nei",
            3: "sh version",
            4: "sh clock",
            5: "sh proc mem | ex 0.00",
            6: "show proc cpu",
            7: "sh ip bgp sum",
            8: "sh clock",
            9: "sh ntp associations",
            10: "sh access-lists"}

def acl_check(handler):

    data_list = []
    data = handler.send_command(commands[10])
    return data

def device_stats(handler):

    data_list=[]
    up_time,r,version_info = uptime(handler)
    # up_time  = [int(i) for i in up_time.split() if i.isdigit()] #up_time list of hours and minutes

    x,reload_reason = r.split("Last reload reason:")
    reload_reason,x = reload_reason.split('reason')

    clock = handler.send_command(commands[8])

    print("\n---NTP stats---")
    print("ClOCK TIME: %s" % clock)
    data_list.append("\n---NTP stats---")
    data_list.append("ClOCK TIME: %s" % clock)

    clock_info = handler.send_command(commands[9])

    if(len(clock_info) == 0):
        data_list.append("NTP not configured")

    else:
        clock_info = clock_info.splitlines()
        clock_stats = re.split(' +', clock_info[1])
        clock_stats[0]=clock_stats[0][2:]
        time_delay = clock_stats[-3]


        if clock_stats[0] == '127.127.1.1':
            print("Synchronised with the master server: 127.127.1.1")
            data_list.append("Synchronised with the master server: 127.127.1.1")

        else:
            print("Time Synchronised with the Server: %s" %clock_stats[0])
            data_list.append("Time Synchronised with the Server: %s" %clock_stats[0])


        print("Time delay: %s" %time_delay)
        data_list.append("Time delay: %s" %time_delay)


    print("\nDevice Stats")
    data_list.append("\n---Device Stats---")
    print("VERSION INFO: %s" %version_info)
    data_list.append("VERSION INFO: %s" %version_info)
    print("UP_TIME: %s" %up_time)
    data_list.append("UP_TIME: %s" %up_time.rstrip())
    print("RELOAD REASON: %s" %reload_reason)
    data_list.append("RELOAD REASON: %s" %reload_reason)

    return data_list



def proc_info(handler,ip):

    data_list = []
    error_flag = 0

    proc_mem = handler.send_command(commands[5],use_textfsm=True)
    proc_mem = proc_mem.splitlines()
    proc_pool = proc_mem[0]
    proc_pool = [int(i) for i in proc_pool.split() if i.isdigit()]
    proc_used = round((proc_pool[1] * 100 / proc_pool[0]), 3)
    proc_free = round((proc_pool[2] * 100 / proc_pool[0]), 3)

    io_pool = proc_mem[1]
    io_pool = [int(i) for i in io_pool.split() if i.isdigit()]
    io_used = round(io_pool[1]*100 / io_pool[0], 3)
    io_free = round(io_pool[2]*100 / io_pool[0], 3)

    print("\nMemory Utilisation")
    data_list.append("\n---Memory Utilisation---")
    print("proc_used: %s%%" %proc_used)
    data_list.append("proc_used: %s%%" %proc_used)
    print("proc_free: %s%%" %proc_free)
    data_list.append("proc_free: %s%%" %proc_free)
    print("io_used: %s%%" %io_used)
    data_list.append("io_used: %s%%" %io_used)
    print("io_free: %s%%" %io_free)
    data_list.append("io_free: %s%%" %io_free)

    cpu_info = handler.send_command(commands[6],use_textfsm=True)
    cpu_info = cpu_info[0]
    cpu_5_sec = cpu_info['cpu_5_sec']
    cpu_1_min = cpu_info['cpu_1_min']
    cpu_5_min = cpu_info['cpu_5_min']
    print("\n CPU Utilisation")
    data_list.append("\n---CPU Utilisation---")
    print("5sec:%s%% 1min:%s%% 5min:%s%%" %(cpu_5_sec,cpu_1_min,cpu_5_min))
    data_list.append("5sec:%s%%" %cpu_5_sec)
    data_list.append("1min:%s%%" % cpu_1_min)
    data_list.append("5min:%s%%" % cpu_5_min)

    lst = [proc_used,io_used,cpu_5_min,cpu_1_min,cpu_5_sec]
    if any(float(y) > 80 for y in lst):
        error_flag = 1
    return data_list,error_flag

def protocol_summary(handler,ip,uptime):

    data_list = []
    pflag=9999
    error_flag = []
    protocol_summary = handler.send_command(commands[1])

    print("\n Protocols running on this device are: ")
    if 'eigrp' in protocol_summary:
        print("EIGRP enabled")
    if 'bgp' in protocol_summary:
        print("BGP enabled")


    if 'eigrp' in protocol_summary:

        data_list.append("\n---Eigrp Enabled and its Stats---")
        print("\n EIGRP Stats")
        flap_text,fcf = flap_check(handler)

        error_flag.append(fcf)

        for i in flap_text:
            data_list.append(i)

        eigrp_nei = handler.send_command(commands[2],use_textfsm=True)
        eigrp_neighbours = []
        eigrp_interfaces = []

        for dict in eigrp_nei:
            eigrp_neighbours.append(dict['address'])
            eigrp_interfaces.append(dict['interface'])

        print("Eigrp Neighbours %s on Interfaces %s" %(eigrp_neighbours,eigrp_interfaces))
        data_list.append("Eigrp Neighbours %s on Interfaces %s" %(eigrp_neighbours,eigrp_interfaces))
        for i in range(len(eigrp_neighbours)):
            ping_text = ping_stats(handler,eigrp_neighbours[i])
            int_text,ecif = check_interface(handler,eigrp_interfaces[i])

            error_flag.append(ecif)

            for j in ping_text:
                data_list.append(j)

            for k in int_text:
                data_list.append(k)


    if 'bgp' in protocol_summary:
        print("\n BGP stats")
        data_list.append("\n---Bgp Enabled and its Stats---")
        bgp_nei = handler.send_command(commands[7],use_textfsm=True)
        bgp_neigbours = []
        uptimes =[]
        prefixes = []

        for dict in bgp_nei:
            bgp_neigbours.append(dict['bgp_neigh'])
            uptimes.append(dict['up_down'])
            prefixes.append(dict['state_pfxrcd'])

        print("BGP neighbours:",bgp_neigbours)
        print("BGP uptimes:",uptimes)
        print("BGP prefixes:",prefixes)

        for i in range(len(bgp_neigbours)):
            data_list.append("\nBGP neighbour:%s" %bgp_neigbours[i])
            data_list.append("BGP uptime:%s" %uptimes[i])
            data_list.append("BGP prefix:%s" % prefixes[i])

            each_interface = fetch_bgp_interface(handler,bgp_neigbours[i])
            if each_interface is not None:
                int_text2,bcif = check_interface(handler,each_interface)
                error_flag.append(bcif)
                for i in int_text2:
                    data_list.append(i)


            else:
                print("This neighbour is enrolled under Stale BGP")
                data_list.append("This neighbour is enrolled under Stale BGP")

    e_flag = 0
    if 1 in error_flag:
        e_flag = 1


    return data_list,pflag,e_flag


def check_interface(handler,interface):

    error_flag = 0
    data_list = []
    print("\nRunning on this interface: %s" %interface)
    data_list.append("Running on this interface: %s" %interface)
    int_stats = handler.send_command('sh int '+ interface,use_textfsm=True)
    int_stats = int_stats[0]
    crc = int_stats['crc']
    input_errors = int_stats['input_errors']
    bandwidth = int_stats['bandwidth']

    print("crc: %s,input_errors: %s, bandwidth: %s"%(crc,input_errors,bandwidth))
    data_list.append("crc: %s" %crc)
    data_list.append("input errors: %s" %input_errors)
    data_list.append("bandwidth: %s" %bandwidth)

    if int(crc) > 5 or int(input_errors) > 100:
        error_flag=1

    load_stats = handler.send_command('sh int ' + interface)
    load_stats = re.findall('(\d+[/]\d+)', load_stats)
    num,den = load_stats[2].split('/')
    reliability = round(float(num)*100/float(den),2)
    num,den = load_stats[3].split('/')
    tx_load = round(float(num)*100/float(den),2)
    num,den = load_stats[4].split('/')
    rx_load = round(float(num)*100/float(den),2)

    print("reliability:%s,tx_load:%s,rx_load:%s" %(reliability,tx_load,rx_load))
    data_list.append("reliability:%s,tx_load:%s,rx_load:%s" %(reliability,tx_load,rx_load))

    return data_list,error_flag






