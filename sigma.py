#!/usr/bin/env python3

import platform
import pyfiglet
import argparse
import socket
import sys
import itertools
import threading
import time
import nmap
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored


if len(sys.argv) == 1:
    print(r'''
 ____  _                       ____                  _ _ 
/ ___|(_) __ _ _ __ ___   __ _/ ___|  ___ __ _ _ __ | | |
\___ \| |/ _` | '_ ` _ \ / _` \___ \ / __/ _` | '_ \| | |
 ___) | | (_| | | | | | | (_| |___) | (_| (_| | | | |_|_|
|____/|_|\__, |_| |_| |_|\__,_|____/ \___\__,_|_| |_(_|_)
         |___/                                           

Created By : Fazalu,Vishnu (VN),Augustin,Vyshakh, Nobel, Sudharshan, Afthab, HariThejas,Akshara, Akshay,Nihal,Nithin

Help : python sigma.py -h
        ''')
    sys.exit()


ascii_banner = pyfiglet.figlet_format("SigmaScan!!")
print(ascii_banner)

result = pyfiglet.figlet_format("Created By ", font="digital")
print(result)
print("Fazalu,Vishnu (VN),Augustin,Vyshakh, Nobel, Sudharshan, Afthab, HariThejas,Akshara, Akshay,Nihal,Nithin")

done = False
# here is the animation
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     ')

t = threading.Thread(target=animate)
t.start()

# long process here
time.sleep(3)
done = True

# Create the command-line argument parser
parser = argparse.ArgumentParser(description='Scan a remote host for open ports.')
parser.add_argument('host', metavar='HOST', type=str, help='the remote host to scan')
parser.add_argument('-s', '--scan-option', type=str, choices=['basic', 'medium', 'high'], default='medium',
                    help='the scan option to use (default: medium)')
args = parser.parse_args()

# Map scan options to port ranges
scan_options = {
    'medium': range(1, 1025),
    'high': range(1, 65536),
    'basic': [20, 21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 587, 993, 995],
}
ports = scan_options[args.scan_option]

remoteServer = args.host
remoteServerIP = socket.gethostbyname(remoteServer)

print("-" * 60)
print(f"Please wait, scanning remote host {remoteServerIP}")
print(f"Scan option: {args.scan_option}")
print("-" * 60)

t1 = datetime.now()

def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((remoteServerIP, port))
        if result == 0:
            print(f"Port {port}: Open")
    except Exception as e:
        print(f"Error scanning port {port}: {e}")
    finally:
        sock.close()

# Scan ports using multiple threads
with ThreadPoolExecutor(max_workers=50) as executor:
    for port in ports:
        executor.submit(scan_port, port)

# Perform an additional scan using nmap
nm = nmap.PortScanner()
nm.scan(remoteServerIP, arguments='-sV -p ' + ','.join(map(str, ports)))

print(" " * 60)
print(f"Scan completed in {datetime.now() - t1}")
print("-" * 60)

# Print the results from the nmap scan
for host in nm.all_hosts():
    print(f"Open ports for {host}:")
    for port in nm[host]['tcp']:
        if nm[host]['tcp'][port]['state'] == 'open':
            print(f"\t{port}: {nm[host]['tcp'][port]['name']} - {nm[host]['tcp'][port]['product']} {nm[host]['tcp'][port]['version']}")
            
# Print a final message
print("-" * 60)
# Get the operating system name
os_name = platform.system()

# Get the operating system version
os_version = platform.release()

# Get the machine architecture
arch = platform.machine()

# Print the information
print("Operating System: ", os_name)
print("Version: ", os_version)
print("Architecture: ", arch)
print("Scan complete!")

