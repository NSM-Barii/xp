<div align="center">
  <img src="assets/banner.svg" alt="VADER - Brother Program of Maul" width="100%"/>
</div>

---

### *By a Star Wars Nerd*

> **"I find your lack of security disturbing."** - Darth Vader

A memory-efficient mass IP scanner designed to map entire countries, ASNs, and IP blocks for network reconnaissance and security research.

## Overview

Vader scans massive IP ranges by breaking them into blocks and processing one block at a time. Each block gets its own dynamically-sized BloomFilter to prevent duplicate scans while keeping memory usage minimal. This allows you to scan entire countries without running out of RAM.

## Key Features

- **Country-based scanning** - Map all IPs within a specific country
- **ASN filtering** - Target specific autonomous systems within countries
- **Memory-efficient** - Processes one IP block at a time with dynamic BloomFilters (2x block size)
- **Multi-threaded** - High-performance concurrent scanning (default: 250 threads)
- **Deduplication** - BloomFilter prevents scanning the same IP twice per block

## How It Works

1. Loads all IP blocks for the target country/ASN
2. Processes blocks sequentially (pops from queue)
3. Creates a BloomFilter sized to 2x the current block's IP count
4. Generates random IPs from the block, checking BloomFilter for duplicates
5. When block is exhausted, discards BloomFilter and moves to next block
6. Tracks progress: scanned IPs, active IPs, blocks completed

This approach lets you scan billions of IPs without storing them all in memory.

## Installation

```bash
git clone https://github.com/nsm-barii/vader.git
cd vader/src
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Scan entire country
```bash
sudo venv/bin/python main.py --country Iran -p 80 -t 500
```

### Scan specific ASN within country
```bash
sudo venv/bin/python main.py --country Iran --asn AS44244 -p 22,80,443
```

### Save results
```bash
sudo venv/bin/python main.py --country Iran -p 8080 --save
```

## Options

```
-p PORT              Port(s) to scan (comma-separated)
-t THREADS           Max threads (default: 250)
--save               Save active IPs to database/ips.txt
--country NAME       Target country (e.g., Iran, China, Russia)
--asn NUMBER         Filter by ASN within country
--show-all           Display all active IPs found
```

## Preset Port Modes

```bash
--camera     # IP cameras (RTSP, ONVIF, web interfaces)
--iot        # IoT devices (MQTT, CoAP, mDNS)
--router     # Routers (admin panels, SSH, Telnet)
--nas        # NAS devices (SMB, Synology, web panels)
--remote     # Remote access (RDP, VNC, SSH, FTP)
--database   # Databases (MySQL, PostgreSQL, MongoDB, Redis)
```

## About

Created by **NSM-Barii** - Star Wars nerd | Cybersecurity enthusiast

**NSM Toolset:**
- **Vader** - Recon & discovery (this tool)
- **Maul** - Infrastructure mapping ([github.com/nsm-barii/maul](https://github.com/nsm-barii/maul))

---

## Disclaimer

For authorized security testing and research only. Unauthorized network scanning may be illegal in your jurisdiction. Users are responsible for obtaining proper permissions.

MIT License
