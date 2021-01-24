'''
This script scans through all IP addresses of a given network to search
for a device having a specific MAC address.
Useful for IT admins or Developers working remotely

Tested on Ubuntu Linux. For windows usage change the flags and response message strings
for ping and arp commands
'''

# Import modules
import subprocess
import ipaddress

# Prompt the user to input a network address
print("="*80)
# If you dont know your n/w addr, you can calculate this easily
# Assume your PC and device being searched for are in the same network
# Type ifconfig on your PC to get its ip address and subnet mask
# Assume this is 192.168.193.45 and subnet mask is 255.255.240.0
# Bitwising ANDing the two together your network address 192.168.192.0/20
print("Usage: Please enter your Network address")
print("Then a / followed by how many bits are high in the subnet mask of the network (obtained by ipcofnig)")
print("Eg: 192.168.1.0/20 (subnet mask is 255.255.240.0 = 20 bits high)")
print("="*80)

net_addr = input("Enter a network address in (IpAddr/SubnetMaskHighBitCount) format(ex.192.168.1.0/24): ")

mac_addr = input("Enter MAC Address of the board to search for(ex:1d:ad:cc:a2:xd:c0)")

# Create the network
ip_net = ipaddress.ip_network(net_addr)

# Get all hosts on that network
all_hosts = list(ip_net.hosts())

#Number of requests
req_count = '1'

#Found the hardware you are searching for
found_hardware = False

#request timeout in seconds
timeout = '1'
# For each IP address in the subnet, 
# run the ping command with subprocess.popen interface
print("Start Scanning IP addresses in Network. Please wait")

for i in range(len(all_hosts)):
    print("Pinging: " + str(all_hosts[i]))
    output = subprocess.Popen(['ping', '-c', req_count, '-W', timeout, str(all_hosts[i])], stdout=subprocess.PIPE).communicate()[0]
    
    if "Destination Host Unreachable" in output.decode('utf-8'):
        #print(str(all_hosts[i]), "is Offline")
        continue
    elif ("Request timed out" in output.decode('utf-8')) or (output.decode('utf-8') == '') :
        #print(str(all_hosts[i]), "is Offline")
        continue
    else:
        arp_out = subprocess.Popen(['arp', '-a', str(all_hosts[i])], stdout=subprocess.PIPE).communicate()[0]
        if ((mac_addr.lower() in arp_out.decode('utf-8')) or (mac_addr.upper() in arp_out.decode('utf-8'))):
            found_hardware = True
            print("MAC addr {} found in {}" .format(mac_addr, str(all_hosts[i])))
            user_input = input("Do you want to continue scan further (y/n)")
            if user_input == 'y' or user_input == 'Y' :
                found_hardware = False
                continue
            else:
                print("User terminated program")
                break

if found_hardware == False:
    print("Sorry no hardware found. Try increasing echo count(req_count) and timeout(timeout) to scan intensively")
