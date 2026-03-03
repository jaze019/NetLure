# NetLure: AI-Driven Network Deception & Threat Visualization

NetLure is an interactive, real-time Network Intrusion Detection System (NIDS) and honeypot visualizer. It is designed to intercept live network attacks, intelligently classify the threat level using a deterministic AI threshold model, and visualize the telemetry on a cinematic global map. 

Built to solve the problem of "Alert Fatigue" in cybersecurity, NetLure aggregates burst traffic (like Nmap scans) into actionable, single-event visual intelligence and simulates automated edge-firewall mitigation.

# Disclaimer!!!
NetLure is an educational project developed for demonstrating network security, intrusion detection, and telemetry visualization. Do not deploy honeypots on production networks without proper isolation and authorization.

# Key Features

* **Real-Time Threat Mapping:** Streams live attack data from a network sensor to a Leaflet.js global map via asynchronous WebSockets.
* **AI-Driven Threat Classification:** Utilizes a heuristic expert system to differentiate between manual human probes (Low severity) and automated Botnet attacks (High severity) based on packet frequency.
* **Event Aggregation:** Buffers high-volume burst traffic (e.g., volumetric scans or DDoS attempts) within a 1-second analysis window to prevent dashboard flooding and alert fatigue.
* **Cinematic UI/UX:** Features a Hollywood-style boot-up sequence, audio alerts, red-screen flash for critical threats, and dynamic map rendering.
* **Automated Mitigation Simulation:** Demonstrates incident response by automatically generating firewall ACL blocking logs 1.5 seconds after a botnet is detected.

# System Architecture

NetLure operates on a lightweight, decoupled Client-Server architecture:
1. **The Sensor (Network Layer):** A honeypot listener (simulated via UDP) deployed in a GNS3 network environment to catch unauthorized lateral movement and reconnaissance.
2. **The Analytics Engine (Python Backend):** An `asyncio` server that ingests raw packets, runs the AI thresholding logic, aggregates burst events, assigns geolocation tracking, and acts as a WebSocket broadcaster.
3. **The Presentation Layer (Frontend):** A browser-based dashboard that decodes the JSON telemetry and renders the live global cyber-warfare map.

# Installation & Setup

# Prerequisites
* Python 3.8+
* A modern web browser (Chrome, Edge, Firefox)
* A virtual network environment (like GNS3) or an attack machine (like Kali Linux)

### Setup Instructions
1. Clone this repository:
   ```bash
   git clone [https://github.com/jaze019/NetLure.git](https://github.com/jaze019/NetLure.git)
   cd NetLure

# Future Scope: Enterprise Deployment
While this repository serves as a proof-of-concept, the architecture is designed to scale into a Distributed Threat Intelligence Network. Future iterations will include deploying lightweight sensors across cloud VPCs, forwarding telemetry to an AWS SQS message queue, and upgrading the deterministic AI model to an Unsupervised Machine Learning model trained on baseline enterprise traffic.


