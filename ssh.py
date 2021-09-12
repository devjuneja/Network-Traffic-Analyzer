from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException


def check_ssh(ip):
    ios = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': 'dev',
        'password': 'datla',
        'global_delay_factor': 2
    }

    try:
        print("\nEstablishing SSH connection with: " + str(ip))
        net_connect = ConnectHandler(**ios)
        print("\nSuccessfully established connection\n")
        return net_connect
    except AuthenticationException:
        print("\nAuthentication failed, please verify your credentials or define an SSH on the IP:%s\n" % ip)
    except SSHException:
        print("\nUnable to establish SSH connection: %s" % SSHException)
    except paramiko.BadHostKeyException as badHostKeyException:
        print("\nUnable to verify server's host key: %s" % badHostKeyException)
    except NetMikoTimeoutException:
        print("\nUnable to reach the ip:%s .. A timeout Exception" % NetMikoTimeoutException)

    return None