# 📡 Network Packet Sniffer - CyberSecurity Tools

Network Packet Sniffer adalah salah satu tools keamanan jaringan yang dibangun menggunakan Python dan GUI Streamlit. Tools ini memungkinkan pengguna untuk memantau paket jaringan secara real-time, mendeteksi aktivitas mencurigakan seperti DoS atau pemindaian port, serta menyediakan berbagai fitur ekspor dan visualisasi data.

---

## 🔧 Fitur Utama

- 🎯 **Sniffing Paket Jaringan** dengan filter protokol (BPF: TCP, UDP, ICMP, dst.)
- 📦 **Log CSV, PCAP, HTML** dari hasil sniffing
- 📊 **Statistik Interaktif**: Distribusi protokol & IP
- 🛑 **Deteksi IP Mencurigakan** berdasarkan jumlah paket mencurigakan
- 🔔 **Notifikasi Otomatis** (GUI popup, Email, Telegram)
- 🌐 **GUI Berbasis Streamlit** untuk penggunaan yang mudah
- ⬆️ **Upload PCAP**, tampilkan isinya
- 🔍 **Filter Protokol** secara dinamis dari GUI
- 📥 **Download hasil sniffing**: CSV, PCAP, PNG, HTML

---

## 📁 Struktur Folder

```
network-sniffer/
├── gui.py                # Antarmuka Streamlit utama
├── sniffer_core.py       # Core fungsi sniffing
├── notifier.py           # Modul notifikasi (popup, email, telegram)
├── logs/                 # Folder hasil log (.csv, .pcap, .html, .png)
└── README.md             # Dokumentasi
```

---

## 🚀 Cara Menjalankan

### 1. 🔹 Persiapan Virtual Environment (opsional tapi disarankan)
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. 🔹 Install Dependensi
```bash
pip install -r requirements.txt
```

Isi `requirements.txt` (bisa kamu buat manual):
```txt
scapy
streamlit
matplotlib
pandas
colorama
```

### 3. 🔹 Jalankan GUI
```bash
streamlit run gui.py
```

---

## ⚙️ Opsi yang Tersedia di GUI

- 🟢 Start Sniffing
- 🔴 Stop Sniffing
- 🔍 Filter protokol
- ⏳ Auto-refresh log
- ⬆ Upload file PCAP
- 📈 Statistik protokol & IP (dengan grafik)
- ⬇ Download semua file log

---

## 📬 Notifikasi

Tersedia 3 jenis:

1. **GUI Popup** (menggunakan tkinter)
2. **Email**
   - Aktifkan 2FA di akun Gmail
   - Buat [App Password](https://myaccount.google.com/apppasswords)
   - Masukkan app password ke dalam file `notifier.py`
3. **Telegram**
   - Buat bot via [@BotFather](https://t.me/BotFather)
   - Dapatkan `bot_token` dan `chat_id`

---

## 📌 Contoh Penggunaan (tanpa GUI)
Jika ingin jalankan dari CLI:
```bash
python3 -c "from sniffer_core import run_sniffer; run_sniffer('tcp', 'email')"
```

---

## 🛡️ Tools Ini Cocok Untuk:

- Edukasi CyberSecurity
- Simulasi pentest jaringan
- Analisis forensik jaringan
- Monitoring jaringan pribadi

---

## 📈 Rencana Pengembangan Selanjutnya

- [ ] Integrasi database SQLite untuk log
- [ ] Deteksi serangan DoS/Port Scan otomatis
- [ ] Auto-rotate log berdasarkan ukuran
- [ ] Ekspor ke Excel (.xlsx)
- [ ] Statistik interaktif dengan Chart.js
- [ ] Deploy sebagai aplikasi web (Flask/Streamlit Sharing)

---

## 🙏 Terima Kasih

Proyek ini dikembangkan untuk edukasi dan latihan keamanan jaringan. Gunakan dengan bijak dan hanya di jaringan yang kamu izinkan.

Happy Sniffing! 🕵️‍♂️
