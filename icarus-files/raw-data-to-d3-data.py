import json
import sys
from collections import deque


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

def get_adj_list(filename):
    with open(filename,"r") as f:
        data = json.load(f)
        nodes = data["nodes"]
        result =  {v: [] for v in get_all_ips(data)}
        for node in nodes:
            ip = node["ip"]
            for neighbour in node["neighbours"]:
                result[ip].append(neighbour)
        return result

def data_to_graph_data_from_boot_nodes(filename, levels):
    with open(filename,"r") as f:
        data = json.load(f)
        nodes = data["nodes"]

        result = {}
        result["nodes"] = create_boot_nodes()
        result["links"] = []

        levels_remaining = levels

        adj_list = get_adj_list(filename)
        write_json_to_file("graph-data-adj-list.json", adj_list)
        
        visited = set(list(BOOT_NODES))
        q = deque(list(BOOT_NODES))
        final_node = q[-1]
        while len(q) > 0:
            ip = q.popleft()
            for neighbour in adj_list[ip]:
                if neighbour not in visited:
                    result["nodes"].append(create_node(neighbour, 2))
                    q.append(neighbour)
                    visited.add(neighbour)
                result["links"].append(create_link(ip, neighbour))
            if ip == final_node:
                levels_remaining -= 1
                if levels_remaining == 0 or len(q) == 0:
                    return result
                else:
                    final_node = q[-1]
        return result

if __name__ == "__main__":
    result = data_to_graph_data_from_boot_nodes("graph-data-raw.json",3)
    write_json_to_file("graph-data-d3.json", result)