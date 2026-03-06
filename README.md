# xp

Successor to [netbruter](https://github.com/nsm-barii/netbruter).

A mass IP scanning framework designed to quickly identify vulnerable devices exposed to the internet. Built for security researchers and penetration testers to efficiently locate misconfigured IoT devices, IP cameras, routers, NAS systems, and other network-exposed hardware.

## Overview

This tool performs rapid port scanning across IP ranges to detect devices with open services, then fingerprints them using HTTP response analysis, favicon hashing, and server headers. With targeted preset scan modes, it can identify specific device types like IP cameras with minimal configuration.

## Use Cases

- Filter IP blocks by country to scan specific geographic regions
- Target vulnerabilities in specific countries using geo-filtered scanning
- Locate unsecured IP cameras and surveillance systems
- Identify exposed IoT devices (MQTT, CoAP, mDNS)
- Find misconfigured routers and network infrastructure
- Detect open databases and remote access services
- Map NAS devices exposed to the internet

With additional fingerprinting data, this framework could become a highly efficient tool for rapidly identifying vulnerable IP cameras at scale.

## Installation

```bash
git clone https://github.com/nsm-barii/vader.git
cd vader/src
python3 -m venv venv
source venv/bin/activate
pip install -r requiremenets.txt
```

## Usage

Run with sudo for raw socket access:

```bash
sudo venv/bin/python main.py [options]
```

### Preset Scan Modes

```bash
# IP cameras (RTSP, ONVIF, web interfaces)
sudo venv/bin/python main.py --camera

# IoT devices (MQTT, CoAP, mDNS)
sudo venv/bin/python main.py --iot

# Routers and infrastructure (admin panels, SSH, Telnet)
sudo venv/bin/python main.py --router

# NAS devices (SMB, Synology, web panels)
sudo venv/bin/python main.py --nas

# Remote access services (RDP, VNC, SSH, FTP)
sudo venv/bin/python main.py --remote

# Open databases (MySQL, PostgreSQL, MongoDB, Redis, Elasticsearch)
sudo venv/bin/python main.py --database
```

### Options

```
-p PORT              Port to scan
-t THREADS           Maximum number of threads (default: 250)
-f                   Save all active IPs to database/ips.txt
--all                Show all active IPs
--paths {nas,router,camera}  Manually set path for directory bruteforcing

# Geo Lookup Options
--country {country}  Filter IPs to specific country (see database/ip_blocks/README.MD)
--geo local          Enable offline geo lookup using local database
--geo ipinfo         Enable geo lookup using ipinfo.io API
--save               Save generated IPs (format: {Country}_timestamp.txt or timestamp.txt)
```

## Features

- Multi-threaded scanning for high performance
- HTTP fingerprinting with favicon hash matching
- Preset port lists for common device types
- Path bruteforcing for web interfaces
- Country-based IP filtering (200+ countries)
- Offline and online geolocation lookup
- Database connectivity testing (MongoDB)
- Server header and HTML title analysis

## Known Issues / Work in Progress

**Do not use directory search (preset ports: --camera, --iot, --router, --nas, --remote, --database with --paths) and geo lookup (--country, --geo) at the same time.** The program is not yet efficient when using both features simultaneously.

## Contributing

Contributions are welcome. This tool has potential to become a powerful asset for security research with expanded fingerprinting databases and additional device signatures. Submit pull requests or open issues for improvements.

## Disclaimer

This tool is intended for authorized security testing and research only. Users are responsible for ensuring they have permission to scan target networks. Unauthorized scanning may be illegal in your jurisdiction.
