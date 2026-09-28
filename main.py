from classes.CSV_to_TXT_router import CSV_to_TXT_router


csv_to_txt_router = CSV_to_TXT_router()

input_file = input("What is the input file? (leave blank for default = ./data/input/input.csv)")
if not input_file:
    input_file = ".\\data\\input\\input.csv"
output_file = input("What is the output file? (leave blank for default = ./data/output/cisco_commands-router.txt)")
if not output_file:
    output_file = ".\\data\\output\\cisco_commands-router.txt"
hostname = input("What is the hostsname (leave blank for default = 'BRouter')")
if not hostname:
    hostname = "BRouter"

csv_to_txt_router.make_router_file(input_file=input_file, output_file=output_file, hostname=hostname)