import csv

class CSV_to_TXT_router():
    def __init__(self):
        pass

    def wildcard_mask(self, netmask):
        return ".".join(str(255 - int(octet)) for octet in netmask.split("."))

    def network_address(self, ip, netmask):
        ip_parts = ip.split(".")
        mask_parts = netmask.split(".")

        network = []

        for i in range(4):
            network.append(str(int(ip_parts[i]) & int(mask_parts[i])))

        return ".".join(network)

    def make_router_file(self, input_file: str, output_file: str=None, hostname: str=None):
        if not output_file:
            output_file = "cisco_commands-router.txt"

        with open(input_file, "r", encoding="utf-8") as csv_file, \
            open(output_file, "w", encoding="utf-8") as output_file:

            output_file.write(f"ena\n")
            output_file.write(f"conf t\n")
            if hostname:
                output_file.write(f"hostname {hostname}\n")
            else:
                output_file.write(f"hostname BRouter\n")
            output_file.write(f"ip routing\n")

            lan_interfaces = []


            csv_reader = csv.reader(csv_file, delimiter=";")
            next(csv_reader, None)
            for line in csv_reader:
                if not line:
                    continue

                network = line[0]
                interface = line[1]
                description = line[2]
                vlan = line[3]
                ipadress = line[4]
                subnetmask = line[5]
                defaultgateway = line[6]

                if network.lower() == "wan":
                    # output_file.write(f"\n")
                    output_file.write(f"int {interface}\n")
                    output_file.write(f"description {description}\n")
                    if not ipadress or ipadress.lower() == "dhcp":
                        output_file.write(f"ip address dhcp\n")
                    else:
                        if not subnetmask:
                            print("No subnet mask for WAN!")
                            break
                        output_file.write(f"ip address {ipadress} {subnetmask}\n")
                    output_file.write(f"ip nat outside\n")
                    output_file.write(f"no shut\n")
                    output_file.write(f"ip nat inside source list 1 interface {interface} overload\n")

                    if not ipadress or ipadress.lower() == "dhcp":
                        output_file.write(f"ip route 0.0.0.0 0.0.0.0 dhcp\n")
                    else:
                        output_file.write(f"ip route 0.0.0.0 0.0.0.0 {ipadress}\n")

                elif network.lower() == "lan":
                    if vlan and vlan != 0:
                        # met vlan
                        if interface not in lan_interfaces:
                            # interface zelf zit niet in csv, dus aanmaken:
                            lan_interfaces.append(interface)
                            output_file.write(f"int {interface}\n")
                            output_file.write(f"description LAN\n")
                            output_file.write(f"no ip address\n")
                            output_file.write(f"ip nat inside\n")
                            output_file.write(f"no shut\n")

                        output_file.write(f"int {interface}.{vlan}\n")
                        output_file.write(f"encapsulation dot1Q {vlan}\n")
                        output_file.write(f"ip address {ipadress} {subnetmask}\n")
                        output_file.write(f"ip nat inside\n")
                        output_file.write(f"no shut\n")
                        output_file.write(f"access-list 1 permit {self.network_address(ipadress, subnetmask)} {self.wildcard_mask(subnetmask)}\n")

                        

                    
                    else:
                        # zonder vlan
                        output_file.write(f"int {interface}\n")
                        output_file.write(f"description {description}\n")
                        if ipadress:
                            output_file.write(f"ip address {ipadress} {subnetmask}\n")
                        else:
                            output_file.write(f"no ip address\n")
                        
                        output_file.write(f"no shut\n")

                else:
                    print(f"line {line} cannot be parsed")

            output_file.write(f"copy r s\n")
                    
                    

