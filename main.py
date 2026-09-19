import telebot
from flask import Flask, request
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

TOKEN = '8687584261:AAH18U8BiC2abt5qyXW5oAoxcwjMfYsnwkE'
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# --- MESIN SCRAPER ---
def scrape_harga_saham(ticker):
    url = f"https://www.google.com/finance/quote/{ticker}:IDX"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        harga_element = soup.find('div', class_='YMlKvd dsq28e')
        return harga_element.text if harga_element else "N/A"
    except Exception:
        return "Error"

# --- FUNGSI BOT ---
@bot.message_handler(commands=['start', 'tpia'])
def send_stock_data(message):
    bot.reply_to(message, "⏳ Mengambil data...", parse_mode='HTML')
    harga = scrape_harga_saham("TPIA")

    tabel = f"<pre>\n🗓 Date   |Price|\n-----------------\nHari Ini  {harga}\n</pre>"
    bot.send_message(message.chat.id, tabel, parse_mode='HTML')

# --- WEBHOOK ROUTE ---
@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Server Render Aktif!'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
