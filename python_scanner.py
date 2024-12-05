import nmap
import os

def scan_target(ip):
    scanner = nmap.PortScanner()
    open_ports = []

    try:
        print(f"Scanning IP: {ip}...")
        scanner.scan(ip, '1-1000', arguments='-O -sV')     # put your preferred num of ports and also the arguments

        if scanner[ip].state() == 'up':
            print(f"\nState: up")
            
            # detect open ports
            if 'tcp' in scanner[ip]:
                print("Open Ports:")
                for port in scanner[ip]['tcp']:
                    port_info = scanner[ip]['tcp'][port]
                    service_name = port_info.get('name', 'unknown')
                    print(f"  Port {port}/TCP: {port_info['state']} ({service_name})")
                    open_ports.append(f"{service_name}({port})")
            
            # display OS information
            if 'osmatch' in scanner[ip]:
                print("\nDetected Operating System(s):")
                for os in scanner[ip]['osmatch']:
                    print(f"  {os['name']} ({os['accuracy']}% accuracy)")
            else:
                print("\nNo OS information detected.")

            if open_ports:
                print("\nSummary of open ports:")
                print(f"You have {len(open_ports)} open port(s) and they are {', '.join(open_ports)}.")
        else:
            print(f"Host {ip} is down or unresponsive.")
    
    except Exception as e:
        print(f"An error occurred while scanning {ip}: {e}")

def main():
    target = input("Enter a single IP or the path to a file containing a list of IPs: ")

    if os.path.isfile(target):
        with open(target, 'r') as file:
            ips = file.readlines()
        ips = [ip.strip() for ip in ips if ip.strip()]
    else:
        ips = [target.strip()]

    for ip in ips:
        scan_target(ip)
        print("-" * 50)

if __name__ == "__main__":
    main()