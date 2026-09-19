import telebot
import requests
from bs4 import BeautifulSoup
from datetime import datetime

TOKEN = '8687584261:AAH18U8BiC2abt5qyXW5oAoxcwjMfYsnwkE'
bot = telebot.TeleBot(TOKEN)

# --- MESIN SCRAPER (CONTOH) ---
def scrape_harga_saham(ticker):
    url = f"https://www.google.com/finance/quote/{ticker}:IDX"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        harga_element = soup.find('div', class_='YMlKvd dsq28e')
        return harga_element.text if harga_element else "N/A"
    except Exception as e:
        return "Error"

# --- FUNGSI BOT ---
@bot.message_handler(commands=['start', 'tpia'])
def send_stock_data(message):
    now = datetime.now().strftime("%d-%m-%Y || %H:%M:%S Wib.")
    
    # Bot akan melakukan scraping saat perintah diketik
    bot.reply_to(message, "⏳ Sedang mengambil data dari market...", parse_mode='HTML')
    harga_terkini = scrape_harga_saham("TPIA")
    
    header = f"📅 {now}\n"
    header += f"Halo Kak {message.from_user.first_name}🤩,\n"
    header += "Berikut adalah Data Saham TPIA :\n"
    header += "--------------------------------------------------\n"
    
    # Format tabel monospaced sesuai referensi awal
    tabel_data = f"""<pre>
🗓 Date   |Price|
-----------------
Hari Ini  {harga_terkini}
</pre>"""

    bot.send_message(message.chat.id, header + tabel_data, parse_mode='HTML')

print("Bot berhasil menyala di Koyeb!")
# Polling agar bot standby 24 jam menerima pesan
bot.polling(non_stop=True)
