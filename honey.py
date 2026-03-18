
import socket
import threading
import time
import sys

# --- CONFIGURATION ---
BIND_IP = "0.0.0.0"
PORTS = [21, 22, 80]
DASHBOARD_IP = "192.168.52.1"  # IP of your Windows PC running server.py
DASHBOARD_PORT = 9999

def send_alert(src_ip, port):
    """Sends a UDP packet to the Windows Dashboard"""
    try:
        msg = f"ATTACK|{src_ip}|{port}".encode()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(msg, (DASHBOARD_IP, DASHBOARD_PORT))
        print(f"    [->] Alert sent to Dashboard.")
    except Exception as e:
        print(f"    [!] Failed to send alert: {e}")

def handle_client(conn, addr, port):
    src_ip = addr[0]
    print(f"[>>] HIT! Attack detected from {src_ip} on Port {port}")

    # 1. Alert the Dashboard
    send_alert(src_ip, port)

    # 2. Fake the Service (The Deception)
    try:
        if port == 21:
            conn.send(b"220 vsFTPd 3.0.3\r\n")
            time.sleep(1)
        elif port == 22:
            conn.send(b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.3\r\n")
            time.sleep(1)
        elif port == 80:
            http_response = (
                b"HTTP/1.1 200 OK\r\n"
                b"Server: Apache/2.4.41 (Ubuntu)\r\n"
                b"Content-Type: text/html\r\n\r\n"
                b"<html><body><h1>System Error: Access Denied</h1></body></html>"
            )
            conn.send(http_response)

        conn.close()
    except:
        pass

def start_listener(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((BIND_IP, port))
        s.listen(5)
        print(f"[*] Listening on Port {port}...")

        while True:
            conn, addr = s.accept()
            # Handle each attack in a separate thread
            t = threading.Thread(target=handle_client, args=(conn, addr, port))
            t.start()
    except Exception as e:
        print(f"[!] Error on Port {port}: {e}")

def main():
    print(f"[*] NetLure Honeypot Online. Target Dashboard: {DASHBOARD_IP}:{DASHBOARD_PORT}")
    threads = []
    for p in PORTS:
        t = threading.Thread(target=start_listener, args=(p,))
        t.daemon = True
        t.start()
        threads.append(t)

    # Keep main thread alive
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Shutting down...")

if __name__ == "__main__":
    main()
