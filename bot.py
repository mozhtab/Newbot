import requests
from bs4 import BeautifulSoup
import json
import os

TOKEN = "8992012354:AAEpB0n1l6fkbWogSRvbWq8m-gi6CcQmiHs"
CHAT_ID = "278118706"
MEMORY_FILE = "memory.json"

sites = {
    "اخبار اصلی دانشگاه": "https://aut.ac.ir/page_arch.php?slc_pg_id=257&slc_lang=fa&sid=1",
    "امور آموزشی": "https://ugrad.aut.ac.ir/page/3040/%D8%A7%D8%B7%D9%84%D8%A7%D8%B9%DB%8C%D9%87-%D9%87%D8%A7",
    "تحصیلات تکمیلی": "https://grad.aut.ac.ir/page/2937/%D8%A7%D8%B7%D9%84%D8%A7%D8%B9%DB%8C%D9%87%E2%80%8C%D9%87%D8%A7",
    "استعداد درخشان": "https://gto.aut.ac.ir/page/3505/%D8%A7%D8%B7%D9%84%D8%A7%D8%B9%DB%8C%D9%87-%D8%B5%D9%81%D8%AD%D9%87-%D8%AF%D8%A7%D9%86%D8%B4%DA%AF%D8%A7%D9%87",
    "کتابخانه": "https://library.aut.ac.ir/"
}

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("   ✅ پیام با موفقیت به تلگرام شما ارسال شد.")
        else:
            print(f"   ❌ خطا در ارسال پیام به تلگرام: {response.text}")
    except Exception as e:
        print(f"   ❌ مشکل در ارتباط با تلگرام: {e}")

def extract_latest_title(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for a in soup.find_all('a'):
            text = a.get_text(strip=True)
            ignore_words = ['صفحه اصلی', 'درباره ما', 'تماس با ما', 'نقشه سایت', 'امیرکبیر', 'دانشگاه', 'English']
            if len(text) > 30 and not any(w in text for w in ignore_words):
                 return text
        print("   ⚠️ تیتری در این صفحه پیدا نشد (شاید قالب سایت متفاوت است).")
        return None
    except Exception as e:
        print(f"   ❌ خطا در باز کردن سایت: {e}")
        return None

def main():
    print("🚀 ربات شروع به کار کرد...\n" + "-"*30)
    
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            memory = json.load(f)
    else:
        memory = {}

    for name, url in sites.items():
        print(f"🔍 در حال بررسی: {name}")
        latest_title = extract_latest_title(url)
        
        if latest_title:
            print(f"   📌 تیتر پیدا شد: {latest_title}")
            last_title = memory.get(name, "")
            
            if latest_title != last_title:
                print("   📬 این یک خبر جدید است! در حال ارسال به تلگرام...")
                msg = f"🆕 <b>خبر جدید در {name}</b>\n\n📌 {latest_title}\n\n🔗 <a href='{url}'>مشاهده صفحه</a>"
                send_telegram(msg)
                memory[name] = latest_title
            else:
                print("   💤 این خبر تکراری است (قبلاً بررسی شده).")
        print("-" * 30)
    
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(memory, f, ensure_ascii=False, indent=4)
        
    print("🏁 کار ربات تمام شد!")

if __name__ == "__main__":
    main()
