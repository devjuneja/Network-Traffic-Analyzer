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

def uptime(handler):

    device_info = handler.send_command(commands[3])
    version_info = device_info.splitlines()
    version_info = version_info[0].split('IOS Software,')
    version_info = version_info[1]
    r, device_info = device_info.split('uptime is')
    up_time, r = device_info.split("System returned to ROM by reload")
    # up_time  = [int(i) for i in up_time.split() if i.isdigit()] #up_time list of hours and minutes

    return up_time,r,version_info

def ping_stats(handler,neighbour):

    data_list = []
    upt,x,y = uptime(handler)
    print("Up-Time of the device %s: %s " %(neighbour,upt))
    data_list.append("Up-Time of the device %s: %s " %(neighbour,upt))
    print("\nPing stats of the EIGRP Neighbour: %s" %neighbour)
    data_list.append("Ping stats of the EIGRP Neighbour: %s" %neighbour)

    ping_info = handler.send_command('ping '+ neighbour + ' re 100')
    rtt_match = re.findall('(\d+[/]\d+[/]\d+)', ping_info)
    rtt_stats = rtt_match[0].split('/')  #min/avg/max in the list rtt stats
    print("\nRound_Trip_Time min:%s,avg:%s,max:%s"%(rtt_stats[0],rtt_stats[1],rtt_stats[2]))
    data_list.append("Round_Trip_Time min:%s,avg:%s,max:%s"%(rtt_stats[0],rtt_stats[1],rtt_stats[2]))

    ping_success_rate = [int(i) for i in ping_info.split() if i.isdigit()]
    ping_success_rate = ping_success_rate[1]
    print("Ping success rate: %s" %ping_success_rate)
    data_list.append("Ping success rate: %s" %ping_success_rate)

    return data_list

def fetch_bgp_interface(handler,neighbour):

    print("\n Neighbour: %s" %neighbour)

    fetch_info = handler.send_command('sh ip cef '+neighbour,use_textfsm=True)

    if 'Ethernet' in fetch_info:
        p, interface = fetch_info.split('Ethernet')
        interface = 'Gi' + interface
        return interface
    return None


def flap_check(handler):

    data_list = []
    flap_flag = 0
    data = handler.send_command('sh log | i DUAL-5', use_textfsm=True)

    data_list.append("Flap Stats")

    if(len(data)<3):
        print("No flapping on this Device")
        data_list.append("flaps: 0")

    else:
        flaps = int(len(data) / 2)
        start_data = data[0]
        start_time = start_data['time']
        end_data = data[len(data) - 1]
        end_time = end_data['time']

        start_time = start_time.split('.')
        start_time = start_time[0]
        end_time = end_time.split('.')
        end_time = end_time[0]
        data_list.append("Device flapping")
        print("flaps: %s" % flaps)

        if int(flaps) > 5:
            flap_flag = 1

        data_list.append("flaps: %s" % flaps)
        print("start time: %s" % start_time)
        data_list.append("start time: %s" % start_time)
        print("end time: %s" % end_time)
        data_list.append("end time: %s" % end_time)

        start_time = [int(i) for i in start_time.split(':') if i.isdigit()]
        end_time = [int(i) for i in end_time.split(':') if i.isdigit()]
        difference = []
        for i in range(len(start_time)):
            difference.append(end_time[i] - start_time[i])
        print("Flap time- hours:%s%%,minutes:%s%%,seconds:%s%%" %(difference[0],difference[1],difference[2]))
        data_list.append("Flap time- hours:%s%%,minutes:%s%%,seconds:%s%%" %(difference[0],difference[1],difference[2]))

    return data_list,flap_flag



