import asyncio
import websockets
import json
import socket
import random

# --- CONFIGURATION ---
UDP_LISTEN_IP = "0.0.0.0"
UDP_LISTEN_PORT = 9999
CLIENTS = set()

# --- ADVANCED AI MEMORY ---
ip_profiles = {}       # Stores temporary hit counts and locations
active_analysis = set() # Tracks which IPs are in the 1-second "waiting room"

# --- SIMULATION DATA ---
THREAT_ACTORS = [
    {"country": "China", "city": "Shanghai", "lat": 31.2304, "lng": 121.4737},
    {"country": "North Korea", "city": "Pyongyang", "lat": 39.0392, "lng": 125.7625},
    {"country": "Russia", "city": "Moscow", "lat": 55.7558, "lng": 37.6173},
    {"country": "USA", "city": "New York", "lat": 40.7128, "lng": -74.0060},
    {"country": "Brazil", "city": "Sao Paulo", "lat": -23.5505, "lng": -46.6333},
    {"country": "Nigeria", "city": "Lagos", "lat": 6.5244, "lng": 3.3792},
    {"country": "Iran", "city": "Tehran", "lat": 35.6892, "lng": 51.3890},
    {"country": "UK", "city": "London", "lat": 51.5074, "lng": -0.1278},
    {"country": "Japan", "city": "Tokyo", "lat": 35.6762, "lng": 139.6503},
    {"country": "Australia", "city": "Sydney", "lat": -33.8688, "lng": 151.2093}
]

class HoneypotProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        try:
            message = data.decode()
            parts = message.split("|")
            if len(parts) >= 3:
                src_ip = parts[1]
                target_port = parts[2]

                # 1. Initialize this IP if it's completely new (or was recently wiped)
                if src_ip not in ip_profiles:
                    ip_profiles[src_ip] = {
                        'hits': 0, 
                        'location': random.choice(THREAT_ACTORS).copy() # Pick random country
                    }

                # 2. Add a hit to their counter
                ip_profiles[src_ip]['hits'] += 1

                # 3. Start the Analysis Window (Only if not already analyzing!)
                if src_ip not in active_analysis:
                    active_analysis.add(src_ip)
                    asyncio.create_task(self.analyze_burst(src_ip, target_port))
                    
        except Exception as e:
            print(f"[!] Error: {e}")

    async def analyze_burst(self, ip, initial_port):
        """ The AI waits 1 second to gather all packets before reacting """
        
        # WAIT 1 SECOND (Gathers all Nmap packets)
        await asyncio.sleep(1.0)

        # Look at how many hits arrived during that 1 second
        hits = ip_profiles[ip]['hits']
        geo_data = ip_profiles[ip]['location'].copy()
        
        # THE AI DECISION
        if hits > 2:
            ai_verdict = "Botnet"
            final_port = "Multiple Scan" # Nmap hits many ports
        else:
            ai_verdict = "Human Actor"
            final_port = initial_port

        # Prepare the payload
        geo_data["ip"] = ip
        geo_data["port"] = final_port
        geo_data["status"] = "Threat Detected"
        geo_data["ai_label"] = ai_verdict
        
        print(f"[>>] AI VERDICT: {ai_verdict} | Packets in burst: {hits} | Location: {geo_data['city']}")
        
        # --- THE FULL WIPE (AMNESIA) ---
        # We completely delete the IP from memory. 
        # Next time they attack, they get a new country and a fresh AI evaluation!
        if ip in ip_profiles:
            del ip_profiles[ip]
        if ip in active_analysis:
            active_analysis.remove(ip)

        # Send EXACTLY ONE alert to the dashboard
        await broadcast_attack(geo_data)

async def broadcast_attack(data):
    if CLIENTS:
        message = json.dumps(data)
        for client in list(CLIENTS):
            try:
                await client.send(message)
            except:
                CLIENTS.remove(client)

async def handler(websocket):
    CLIENTS.add(websocket)
    await websocket.wait_closed()
    CLIENTS.remove(websocket)

async def main():
    print("=========================================")
    print("          NETLURE SERVER: ACTIVE         ")
    print("          ANALYZING THREATS.....         ")
    print("=========================================")
    loop = asyncio.get_running_loop()
    await websockets.serve(handler, "0.0.0.0", 8765)
    await loop.create_datagram_endpoint(
        lambda: HoneypotProtocol(), 
        local_addr=(UDP_LISTEN_IP, UDP_LISTEN_PORT)
    )
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())