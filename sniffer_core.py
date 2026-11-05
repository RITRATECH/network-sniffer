# sniffer_core.py
import os, csv, time
from scapy.all import sniff, wrpcap, IP
from collections import Counter
from datetime import datetime
from notifier import send_email_alert, send_popup, send_telegram_alert

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

CSV_FILE = os.path.join(LOG_DIR, "packets.csv")
PCAP_FILE = os.path.join(LOG_DIR, "capture.pcap")

packet_list = []
packet_count = 0
protocol_counter = Counter()
ip_counter = Counter()
THRESHOLD = 100

def init_csv():
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Source", "Destination", "Protocol", "Length"])

def log_packet(pkt, notify_type=None):
    global packet_count
    if IP in pkt:
        src = pkt[IP].src
        dst = pkt[IP].dst
        proto = pkt[IP].proto
        length = len(pkt)
        ts = time.strftime("%H:%M:%S")
        proto_name = {1: "ICMP", 6: "TCP", 17: "UDP"}.get(proto, str(proto))

        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([ts, src, dst, proto_name, length])

        ip_counter[src] += 1
        ip_counter[dst] += 1
        protocol_counter[proto_name] += 1
        packet_count += 1
        packet_list.append(pkt)

        for ip in [src, dst]:
            if ip_counter[ip] == THRESHOLD:
                warning = f"⚠️ IP mencurigakan: {ip} (> {THRESHOLD})"
                if notify_type == "gui":
                    send_popup(warning)
                elif notify_type == "email":
                    send_email_alert("Peringatan IP Mencurigakan", warning)
                elif notify_type == "telegram":
                    send_telegram_alert(warning)

def run_sniffer(filter_str, notify_type):
    init_csv()
    sniff(prn=lambda pkt: log_packet(pkt, notify_type), filter=filter_str, store=False)
    if packet_list:
        wrpcap(PCAP_FILE, packet_list)
