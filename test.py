# from source import path
#
# src = '192.168.1.1'
# dst = '192.168.1.226'
#
# print("")
# print("")
# print("Route from source: %s to destination: %s" %(src,dst))
# print("Retrieving the Path...")
# print(path(src,dst))
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

from ssh import check_ssh

handler = check_ssh("172.16.1.20")
clock_info = handler.send_command(commands[9])
if(len(clock_info) == 0):
    print("hello")
