import os
from telegram.ext import Updater, CommandHandler
import socket
import requests
import json

# Token bot Telegram yang didapatkan dari BotFather
TOKEN = '7105555942:AAE3wrYxxgQguINvDn04w7hERKw9MzNG6HY'

# Daftar ID pengguna yang diotorisasi
AUTHORIZED_USER_IDS = ['6238619204', '6238619204', '6238619204']

# Fungsi untuk menjalankan perintah shell dan mengembalikan hasilnya
def run_shell_command(command):
    result = os.popen(command).read()
    return result.strip()

# Menangani pesan dari pengguna untuk perintah /start dan /help
def send_welcome(update, context):
    message = "<b>•═══════•JVO-TEAM•═══════•</b>\n"
    message += "<b>✧ FITUR BOT <a href='https://t.me/fansstoreid'>FANSSTORE.ID</a></b>\n"  # Tautan ditambahkan di sini
    message += "<b>✧ /cek</b> = <b>cek port dan server ON/OFF</b>\n"
    message += "<b>✧ /ip</b> = <b>lookup ip</b>\n"
    message += "<b>✧ CREATED</b> = <b>@fernandairfan</b>\n"
    message += "<b>•═══════•JVO-TEAM•═══════•</b>"
    
    update.message.reply_text(message, parse_mode="HTML")


# Menangani perintah /ip untuk mengecek informasi IP
def check_ip_info(update, context):
    try:
        # Memeriksa apakah pengguna terdaftar
        if str(update.message.from_user.id) not in AUTHORIZED_USER_IDS:
            update.message.reply_text("<b>Anda tidak diotorisasi untuk menggunakan perintah ini.</b>")
            return

        if len(context.args) < 1:
            update.message.reply_text("<b>Format perintah salah. Gunakan /ip <domain_or_IP>.</b>", update.message.reply_text(message, parse_mode="HTML" )
            return

        address = context.args[0]
        ip_address = socket.gethostbyname(address)

        # Mendapatkan informasi ISP
        isp_response = requests.get("https://ipinfo.io/{}/json".format(ip_address))
        isp_data = json.loads(isp_response.text)
        isp = isp_data.get('org', 'Unknown')

        # Mendapatkan informasi lokasi
        location_response = requests.get("https://ipinfo.io/{}/json".format(ip_address))
        location_data = json.loads(location_response.text)
        city = location_data.get('city', 'Unknown')
        region = location_data.get('region', 'Unknown')
        country = location_data.get('country', 'Unknown')
        latitude = location_data.get('loc', 'Unknown').split(',')[0]
        longitude = location_data.get('loc', 'Unknown').split(',')[1]

        message = "<b>═══════•JVO-TEAM•═══════</b>\n"
        message += "<b>✧IP Address:</b> {}\n".format(ip_address)
        message += "<b>✧ISP:</b> {}\n".format(isp)
        message += "<b>✧City:</b> {}\n".format(city)
        message += "<b>✧Region:</b> {}\n".format(region)
        message += "<b>✧Country:</b> {}\n".format(country)
        message += "<b>✧Latitude:</b> {}\n".format(latitude)
        message += "<b>✧Longitude:</b> {}\n".format(longitude)
        message += "<b>═══════•JVO-TEAM•═══════</b>"

        update.message.reply_text(message, parse_mode="HTML")

    except Exception as e:
        update.message.reply_text(f"<b>An error occurred: {e}</b>")

# Menangani perintah /cek untuk mengecek status server dan port
def check_server_status(update, context):
    try:
        # Memeriksa apakah pengguna terdaftar
        if str(update.message.from_user.id) not in AUTHORIZED_USER_IDS:
            update.message.reply_text("<b>Anda tidak diotorisasi untuk menggunakan perintah ini.</b>")
            return

        # Memeriksa format perintah
        if len(context.args) < 1:
            update.message.reply_text("<b>Format perintah salah. Gunakan /cek <domain_or_IP>.</b>")
            return

        target = context.args[0]

        # Memeriksa status server dengan ping
        response = run_shell_command(f"ping -c 4 {target}")

        if "64 bytes from" in response:
            server_status = "<b>ONLINE</b> ✅"
        else:
            server_status = "<b>OFFLINE</b> ❌"

        # Memeriksa status port 80 dan 443
        response_80 = run_shell_command(f"nc -vz {target} 80 2>&1")
        response_443 = run_shell_command(f"nc -vz {target} 443 2>&1")

        port_80_status = "<b>ON</b> ✅" if "succeeded!" in response_80 else "<b>OFF</b> ❌"
        port_443_status = "<b>ON</b> ✅" if "succeeded!" in response_443 else "<b>OFF</b> ❌"

        # Menggabungkan semua pesan notifikasi menjadi satu
        notification_message = f"<b>▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"

        notification_message += "<b>✧DOMAIN:</b> {target}\n"
        notification_message += "<b>✧SERVER:</b> {server_status}\n"
        notification_message += "<b>✧PORT 80:</b> {port_80_status}\n"
        notification_message += "<b>✧PORT 443:</b> {port_443_status}\n"
        notification_message += "<b>▬▬▬▬▬▬▬▬▬▬▬▬▬▬</b>"

        # Mengirim pesan notifikasi ke pengguna dalam format HTML
        update.message.reply_text(notification_message, parse_mode="HTML")

    except Exception as e:
        update.message.reply_text(f"<b>An error occurred: {e}</b>")

# Fungsi untuk memulai bot
def start_bot():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", send_welcome))
    dp.add_handler(CommandHandler("help", send_welcome))
    dp.add_handler(CommandHandler("ip", check_ip_info))
    dp.add_handler(CommandHandler("cek", check_server_status))

    updater
