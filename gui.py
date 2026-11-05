# gui.py
import streamlit as st
import pandas as pd
import os, subprocess
from threading import Thread
import time
from sniffer_core import LOG_DIR, CSV_FILE, PCAP_FILE
import base64

st.set_page_config(layout="wide")
st.title("🌐 Network Packet Sniffer - GUI")

if "sniffing" not in st.session_state:
    st.session_state.sniffing = False
if "process" not in st.session_state:
    st.session_state.process = None

col1, col2 = st.columns(2)
with col1:
    notify_type = st.selectbox("Notifikasi", [None, "gui", "email", "telegram"], index=0)
with col2:
    bpf_filter = st.text_input("BPF Filter (opsional)", "")

def start_sniffing():
    st.session_state.sniffing = True
    command = ["python3", "sniffer_core.py"]
    def target():
        subprocess.run(["python3", "-c", 
            f"from sniffer_core import run_sniffer; run_sniffer('{bpf_filter}', '{notify_type}')"
        ])
    t = Thread(target=target)
    t.start()

def stop_sniffing():
    st.session_state.sniffing = False
    os.system("pkill -f sniffer_core")

col1, col2 = st.columns(2)
if col1.button("▶️ Start Sniffing", disabled=st.session_state.sniffing):
    start_sniffing()
if col2.button("⏹️ Stop Sniffing", disabled=not st.session_state.sniffing):
    stop_sniffing()

st.markdown("---")
st.header("📥 Upload PCAP File")
uploaded_file = st.file_uploader("Upload PCAP", type=["pcap", "pcapng"])
if uploaded_file:
    st.write("File uploaded:", uploaded_file.name)
    with open(os.path.join(LOG_DIR, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.read())

st.markdown("---")
st.header("📄 Packet Log (CSV)")
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
    protocol_filter = st.multiselect("Filter Protocol", options=df["Protocol"].unique(), default=list(df["Protocol"].unique()))
    filtered_df = df[df["Protocol"].isin(protocol_filter)]
    st.dataframe(filtered_df, use_container_width=True)

    # Download CSV
    csv_download = filtered_df.to_csv(index=False).encode()
    st.download_button("⬇ Download CSV", csv_download, "filtered_packets.csv", "text/csv")

st.markdown("---")
st.header("📊 Statistik")
col1, col2 = st.columns(2)
with col1:
    if os.path.exists(os.path.join(LOG_DIR, "protocol_statistics.png")):
        st.image(os.path.join(LOG_DIR, "protocol_statistics.png"), caption="Protocol Stats")
with col2:
    if os.path.exists(os.path.join(LOG_DIR, "ip_statistics.png")):
        st.image(os.path.join(LOG_DIR, "ip_statistics.png"), caption="IP Stats")

# Download PCAP/HTML/PNG
st.markdown("---")
st.header("📦 Download Lainnya")
download_cols = st.columns(3)
files = {
    "PCAP": PCAP_FILE,
    "HTML": os.path.join(LOG_DIR, "packets.html"),
    "Protocol PNG": os.path.join(LOG_DIR, "protocol_statistics.png"),
}
for i, (label, path) in enumerate(files.items()):
    if os.path.exists(path):
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            download_cols[i].markdown(f"[⬇ Download {label}](data:application/octet-stream;base64,{b64})", unsafe_allow_html=True)

st.markdown("---")
st.caption("Made with ❤️ using Scapy, Streamlit & Python.")

