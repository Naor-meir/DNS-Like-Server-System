import socket
import sys
import time

def query_server(server_ip, server_port, domain):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # Send the domain query to the server
        sock.sendto(domain.encode(), (server_ip, int(server_port)))
        # Receive the response from the server
        response, _ = sock.recvfrom(1024)
        return response.decode()

def loop_query(res, domain, cache):
    while True:
        # Extract the next server's IP and port from the response
        ip, port = res.split(',')[1].split(':')
        res = query_server(ip, port, domain)
        cache[res.split(',')[0]] = {'response': res, 'timestamp': time.time()}
        # Check if the response is a messege answer 
        if len(res.split(',')) == 1:
            return res
        record_type = res.split(',')[2]
        d = res.split(',')[0]
        # Check if the response is the final answer (A record)
        if record_type == "A" and domain == d:
            return res

def resolver(port, parent_ip, parent_port, cache_time):
    # Create a UDP socket for the resolver
    resolver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    resolver_socket.bind(('', port))
    cache = {} # Initialize the cache
    while True:
        # Flag to indicate if the domain was found in the cache
        found = False
        data, client_address = resolver_socket.recvfrom(1024)
        data = data.decode()
        domain = data.strip()
        # Check if the domain is in the cache and the record is 'A'
        for d in cache:
            res = cache[d]['response']
            times = cache[d]['timestamp']
            if time.time() - float(times) < cache_time and domain == d:
                # If the response is a message answer, send it directly
                if len(res.split(',')) == 1:
                    resolver_socket.sendto(res.encode(), client_address)
                    found = True
                    break
                record_type = res.split(',')[2]
                # If the record type is 'A', send the cached response
                if record_type == "A":
                    resolver_socket.sendto(res.encode(), client_address)
                    found = True
                    break
        
        # Check if the domain is in the cache and the record is 'NS'
        if not found:
            for d in cache:
                res = cache[d]['response']
                times = cache[d]['timestamp']
                # Check for cached NS records that match the domain
                if time.time() - float(times) < cache_time and domain.endswith(d) and len(res.split(',')) == 3:
                    record_type = res.split(',')[2]
                    if record_type == "NS":
                        # Recursively query the next server
                        res = loop_query(res, domain, cache)
                        resolver_socket.sendto(res.encode(), client_address)
                        found = True
                        break

        # If the domain is not found in the cache, query the parent server
        if not found:
            response = query_server(parent_ip, parent_port, domain)
            # Cache the response
            cache[response.split(',')[0]] = {'response': response, 'timestamp': time.time()}
            if len(response.split(',')) == 3:
                record_type = response.split(',')[2]
                # Handle 'A' or 'NS' records from the parent server
                if record_type == "A":
                    resolver_socket.sendto(response.encode(), client_address)
                elif record_type == "NS":
                    response = loop_query(response, domain, cache)
                    resolver_socket.sendto(response.encode(), client_address)
            else:
                # Send the msg response to the client
                resolver_socket.sendto(response.encode(), client_address)

if __name__ == "__main__":
    # Parse command-line arguments
    port = int(sys.argv[1])
    parent_ip = sys.argv[2]
    parent_port = int(sys.argv[3])
    cache_time = int(sys.argv[4])
    # Start the resolver
    resolver(port, parent_ip, parent_port, cache_time)