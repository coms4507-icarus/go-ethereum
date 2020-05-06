import json
import sys


BOOT_NODES = set(["18.138.108.67", "3.209.45.79", "34.255.23.113", "35.158.244.151", "52.187.207.27", "191.234.162.198", "52.231.165.108", "104.42.217.25"])

def write_json_to_file(filename, data):
    with open(filename,"w") as f:
            json.dump(data, f)

def create_node(id, group):
    return {"id": id, "group": group}

def create_link(source_id, target_id):
    return {"source": source_id, "target": target_id}

def create_boot_nodes():
    result = []
    for ip in BOOT_NODES:
        result.append(create_node(ip, 1))
    return result

def get_all_ips(data):
    result = set()
    for node in data["nodes"]:
        result.add(node["ip"])
        for neighbour_ip in node["neighbours"]:
            result.add(neighbour_ip)
    return result

def data_to_graph_data(filename):
    with open(filename,"r") as f:
        data = json.load(f)
        nodes = data["nodes"]

        result = {}
        result["nodes"] = create_boot_nodes()
        result["links"] = []

        seen_before = set(list(BOOT_NODES))

        for node in nodes:
            ip = node["ip"]
            if ip not in seen_before:
                seen_before.add(ip)
                result["nodes"].append(create_node(ip, 2))
            for neighbour in node["neighbours"]:
                result["links"].append(create_link(ip, neighbour))
                if neighbour not in seen_before:
                    seen_before.add(neighbour)
                    result["nodes"].append(create_node(neighbour, 2))
    write_json_to_file("graph-data-d3-ready.json", result)


def data_to_graph_data_from_boot_nodes(filename, levels):
    with open(filename,"r") as f:
        data = json.load(f)
        nodes = data["nodes"]

        result = {}
        result["nodes"] = create_boot_nodes()
        result["links"] = []

        seen_before = set(list(BOOT_NODES))
        to_visit = set()
        for node in nodes:
            if node["ip"] in BOOT_NODES:
                for neighbour in node["neighbours"]:
                    if neighbour not in seen_before:
                        result["nodes"].append(create_node(neighbour, 2))
                        seen_before.add(neighbour)
                    result["links"].append(create_link(node["ip"], neighbour))
        write_json_to_file("graph-data-d3-ready-boot-nodes.json", result)
   

if __name__ == "__main__":
    data_to_graph_data_from_boot_nodes("graph-data-raw.json",1)