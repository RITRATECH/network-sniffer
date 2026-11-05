import argparse
import os
import csv
import time
from scapy.all import sniff, wrpcap, IP
from collections import Counter
import matplotlib.pyplot as plt
from colorama import init, Fore, Style
from notifier import send_email_alert, send_popup, send_telegram_alert  # Pastikan semua ini tersedia

init()

# Argument parsing
parser = argparse.ArgumentParser(description="Network Packet Sniffer")
parser.add_argument("--filter", help="Filter for BPF (e.g., tcp, udp, icmp)", default="")
parser.add_argument("--notify", help="Tipe notifikasi: gui, email, telegram", choices=["gui", "email", "telegram"], default=None)
args = parser.parse_args()

# Paths
LOG_DIR = "logs"
CSV_FILE = os.path.join(LOG_DIR, "packets.csv")
PCAP_FILE = os.path.join(LOG_DIR, "capture.pcap")
HTML_FILE = os.path.join(LOG_DIR, "packets.html")
PROTOCOL_PNG = os.path.join(LOG_DIR, "protocol_statistics.png")
IP_PNG = os.path.join(LOG_DIR, "ip_statistics.png")

os.makedirs(LOG_DIR, exist_ok=True)

# Stats & Counters
packet_count = 0
protocol_counter = Counter()
ip_counter = Counter()
packet_list = []  # for pcap

THRESHOLD = 100  # for suspicious IPs

# Write CSV header
with open(CSV_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Timestamp", "Source", "Destination", "Protocol", "Length"])

def log_packet(pkt):
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

        print(f"{Fore.CYAN}[{ts}]{Style.RESET_ALL} {Fore.YELLOW}{src}{Style.RESET_ALL} → {Fore.GREEN}{dst}{Style.RESET_ALL} | {proto_name} | {length}B")

        ip_counter[src] += 1
        ip_counter[dst] += 1
        protocol_counter[proto_name] += 1
        packet_count += 1
        packet_list.append(pkt)

        for ip in [src, dst]:
            if ip_counter[ip] == THRESHOLD:
                warning = f"⚠️ Warning: IP {ip} terlalu sering muncul! (>{THRESHOLD})"
                print(f"{Fore.YELLOW}{warning}{Style.RESET_ALL}")

                if args.notify == "gui":
                    send_popup(warning)
                elif args.notify == "email":
                    send_email_alert("Peringatan IP Mencurigakan", warning)
                elif args.notify == "telegram":
                    send_telegram_alert(warning)

def generate_html():
    with open(CSV_FILE, "r") as f:
        rows = f.readlines()
    html = """<html><head><style>
    table {border-collapse: collapse; width: 100%; font-family: monospace;}
    th, td {border: 1px solid #ddd; padding: 8px;}
    tr:nth-child(even){background-color: #f2f2f2;}
    th {background-color: #04AA6D; color: white;}
    </style></head><body>
    <h2>Packet Log</h2><table>
    <tr><th>Timestamp</th><th>Source</th><th>Destination</th><th>Protocol</th><th>Length</th></tr>
    """
    for row in rows[1:]:
        html += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row.strip().split(",")) + "</tr>\n"
    html += "</table></body></html>"
    with open(HTML_FILE, "w") as f:
        f.write(html)

def plot_statistics():
    if protocol_counter:
        plt.figure(figsize=(5,5))
        plt.title("Protocol Distribution")
        plt.pie(protocol_counter.values(), labels=protocol_counter.keys(), autopct='%1.1f%%')
        plt.savefig(PROTOCOL_PNG)
        plt.close()

    common_ips = ip_counter.most_common(10)
    if common_ips:
        labels, counts = zip(*common_ips)
        plt.figure(figsize=(10,4))
        plt.bar(labels, counts, color='skyblue')
        plt.xticks(rotation=45)
        plt.title("Top IPs")
        plt.tight_layout()
        plt.savefig(IP_PNG)
        plt.close()
def main():
    print(f"{Fore.GREEN}📱 Memulai sniffing... Tekan Ctrl+C untuk berhenti.{Style.RESET_ALL}")

    try:
        sniff(prn=log_packet, filter=args.filter, store=False)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⏹️ Sniffing dihentikan. Menyimpan hasil...{Style.RESET_ALL}")
    except PermissionError:
        print(f"{Fore.RED}❌ Jalankan script dengan sudo: sudo python3 sniffer.py{Style.RESET_ALL}")
    finally:
        if packet_list:
            wrpcap(PCAP_FILE, packet_list)
        generate_html()
        plot_statistics()
        print(f"{Fore.GREEN}✅ Semua file disimpan di folder 'logs/'{Style.RESET_ALL}")
        print(f"{Fore.BLUE}📁 File: {CSV_FILE}, {PCAP_FILE}, {HTML_FILE}, {PROTOCOL_PNG}, {IP_PNG}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📊 Statistik: {len(packet_list)} paket ditangkap.{Style.RESET_ALL}")

        # === Kirim notifikasi akhir ===
        final_msg = f"Sniffing selesai. {len(packet_list)} paket ditangkap. Lihat folder logs."
        if args.notify == "gui":
            send_popup(final_msg)
        elif args.notify == "email":
            send_email_alert("Sniffer Selesai", final_msg)
        elif args.notify == "telegram":
            send_telegram_alert(final_msg)
# Ini penting agar script bisa dipanggil dari GUI
if __name__ == "__main__":
    main()