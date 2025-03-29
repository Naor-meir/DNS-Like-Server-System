import socket
import sys

# Function to load the zone file and parse records into a dictionary
def load_zone_file(zone_file):
    zone_records = {}
    with open(zone_file, 'r') as f:
        for line in f:
            domain, ip, record_type = line.strip().split(',')
            zone_records[domain] = (ip, record_type)
    return zone_records

# Function to handle incoming requests
def handle_request(data, zone_records):
    domain = data.decode().strip()
    for d in zone_records:
        ip, record_type = zone_records[d]
        # Check for exact match for "A" records or a suffix match for "NS" records
        if (record_type == "A" and domain == d) or (record_type == "NS" and domain.endswith(d)):
            return f"{d},{ip},{record_type}".encode()
    return "non-existent domain".encode() # Default response for no match

# Function to start the server
def start_server(port, zone_file):
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', port))
    # Load records from the zone file
    zone_records = load_zone_file(zone_file)
    # Server loop to handle incoming requests
    while True:
        data, client_address = server_socket.recvfrom(1024)
        response = handle_request(data, zone_records)
        server_socket.sendto(response, client_address)

if __name__ == "__main__":
    # Retrieve port and zone file from cli args
    port = int(sys.argv[1])
    zone_file = sys.argv[2]
    start_server(port, zone_file)