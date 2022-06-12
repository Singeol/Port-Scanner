from netaddr import IPRange
import time
import threading
from socket import socket, AF_INET, SOCK_STREAM
ip_list = []
ports_list = []

start_time = time.time()


def port_scanner(host, port):
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(0.3)

    result = s.connect_ex((host, port))

    if result == 0:
        out_with_ports.write(host + ': ' + str(port) + '\n')
        out_without_ports.write(host + '\n')
    s.close()


with open('hosts.txt', 'r') as f:
    ips_range = f.read().splitlines()
with open('ports.txt', 'r') as f:
    ports_range = f.read().splitlines()
out_with_ports = open('out_with_ports.txt', 'w')
out_without_ports = open('out_without_ports.txt', 'w')

for i in range(len(ports_range)):
    if ports_range[i].find('-') != -1:
        start, end = map(int, ports_range[i].split('-'))
        for j in range(start, end):
            ports_list.append(j)
    else:
        ports_list.append(ports_range[i])

for i in range(len(ips_range)):
    if ips_range[i].find('-') != -1:
        start, end = ips_range[i].split('-')
        for ip in IPRange(start, end):
            ip_list.append(str(ip))
    else:
        ip_list.append(str(ips_range[i]))

print("--- %s seconds ---" % (time.time() - start_time))

ips_range.clear()
ports_range.clear()

threads = []
for i in range(0, len(ip_list)):
    for j in range(0, len(ports_list)):
        t = threading.Thread(target=port_scanner, args=(ip_list[i], int(ports_list[j])))
        t.start()
        threads.append(t)

for t in threads:
    t.join()
print("--- %s seconds ---" % (time.time() - start_time))
out_with_ports.close()
out_without_ports.close()
