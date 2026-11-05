import smtplib
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import messagebox
import requests

# === EMAIL ===
def send_email_alert(subject, message):
    sender = "jc1460879@gmail.com"  # Ganti dengan email pengirim
    password = "lgvtfyvinrobuzkk"  # Gunakan password aplikasi, bukan password biasa
    recipient = "jc1460879@gmail.com"

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender, password)
        server.sendmail(sender, [recipient], msg.as_string())
        server.quit()
        print("📧 Email notifikasi berhasil dikirim.")
    except Exception as e:
        print("❌ Gagal mengirim email:", e)

# === GUI POPUP ===
def send_popup(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning("Notifikasi Sniffer", message)

# === TELEGRAM BOT ===
def send_telegram_alert(message):
    token = "TOKEN_BOT_Telegram"      # <-- Ganti dengan token bot kamu
    chat_id = "CHAT_ID_KAMU"          # <-- Ganti dengan chat_id kamu
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    payload = {"chat_id": chat_id, "text": message}

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("📲 Telegram notifikasi berhasil dikirim.")
        else:
            print(f"❌ Gagal mengirim Telegram. Status: {response.status_code}")
    except Exception as e:
        print("❌ Exception Telegram:", e)
