import socket
import sys

def query_resolver(resolver_ip, resolver_port, domain):
    # sent udp query to resolver
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(domain.encode(), (resolver_ip, resolver_port))
        response, _ = sock.recvfrom(1024)
        return response.decode()

def start_client(resolver_ip, resolver_port):
    # Loop of input and print answer from resolver server
    while True:
        domain = input("").strip()
        response = query_resolver(resolver_ip, resolver_port, domain)
        ans = response.split(',')
        if len(ans) == 3:
            print(ans[1])
        else:
            print(response)

if __name__ == "__main__":
    # Parse arguments and call for client loop
    resolver_ip = sys.argv[1]
    resolver_port = int(sys.argv[2])
    start_client(resolver_ip, resolver_port)
