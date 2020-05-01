import json
import sys

def print_pretty(deserialized_json_data):
    print(json.dumps(deserialized_json_data, indent=4, sort_keys=True))

def write_json_to_file(filename, data):
    with open(filename,"w") as f:
            print_pretty(data)
            json.dump(data, f)

if __name__ == "__main__":
    print("This python script is for pretty printing json files - and for extracting IP data from struct")
    if len(sys.argv) != 2:
        print("Expects path to a json file")
        exit()
    with open(sys.argv[1], "r") as f:
        data = json.load(f)
        ips = []
        for node in data['Nodes']:
            ip = node['IP']
            ips.append(ip)

        # print_pretty(data)
        print(f"There were {len(data['Nodes'])} nodes.")
    
    write_json_to_file("icarus-files/ips.json", ips)