# DNS-Like Server System

## 🧠 Overview

This project simulates a DNS-like system implemented in Python. It includes three components:  
- **Server** – handles direct domain resolution using a local zone file.  
- **Resolver** – acts as an intermediate DNS resolver with recursive capabilities and caching.  
- **Client** – sends domain name queries and receives responses.

The system supports basic `A` records and recursive `NS` resolution via UDP, and includes a caching mechanism in the resolver to improve performance.

---

## 🧩 Components

### 🖥️ Server

Handles incoming DNS queries using a `zone.txt` file.  
It supports direct resolution of `A` records and delegates `NS`-type queries to higher-level servers.

#### Functionality:
- Listens on a given UDP port.
- Parses and responds to queries from the zone file.
- Supports both `A` and `NS` record types.
- Returns "non-existent domain" if no match is found.

#### Usage:
```bash
python3 server.py [PORT] [ZONE_FILE_PATH]
```

#### Example:
```bash
python3 server.py 12345 zone.txt
```

---

### 🔄 Resolver

Acts as a recursive DNS resolver with a caching layer.  
If the domain is cached, it returns the cached result. If not, it contacts the parent server.

#### Functionality:
- Caches responses for a specified TTL (time-to-live).
- Handles recursive lookup logic for NS-type responses.
- Contacts parent server for resolution if needed.

#### Usage:
```bash
python3 resolver.py [PORT] [PARENT_SERVER_IP] [PARENT_SERVER_PORT] [TTL]
```

#### Example:
```bash
python3 resolver.py 11111 127.0.0.1 12345 60
```

---

### 💻 Client

Sends queries to the resolver and displays the responses.

#### Functionality:
- Sends a domain query to a specified server and port.
- Displays the IP address or error message in response.

#### Usage:
```bash
python3 client.py [SERVER_IP] [SERVER_PORT]
```

#### Example:
```bash
python3 client.py 127.0.0.1 11111
```

---

## 📄 Zone File Format

The zone file is a CSV-like file where each line contains a DNS record:

```text
domain,ip_address_or_target,record_type
```

#### Examples:
```
biu.ac.il,1.2.3.4,A
co.il,1.2.3.5:777,NS
example.com,1.2.3.7,A
```

- `A` – direct mapping of domain to IP address.
- `NS` – referral to another server and port for further resolution.

---

## 🧪 Example Flow

1. The client sends a query for `mail.google.co.il`.
2. The resolver checks its cache:
   - If not found, it contacts the main server.
   - If the server returns an `NS` record, the resolver follows it recursively.
3. The resolver caches the response (e.g., `1.2.3.9`) for future queries.
4. The client displays the result.

---

## 🐍 Requirements

- Python 3.6+
- No external libraries required – only standard Python libraries are used.

---

## 🧰 File Structure

```
.
├── server.py
├── resolver.py
├── client.py
├── zone.txt
├── zone2.txt (optional)

```
