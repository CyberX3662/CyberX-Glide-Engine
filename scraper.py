import csv
import os
import time
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from datetime import datetime

# إعداد Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

def get_ai_analysis(device_name, price):
    try:
        prompt = f"جهاز '{device_name}' سعره الحالي {price}. هل يعتبر صفقة جيدة للأمن السيبراني؟ اجب بكلمة واحدة (ممتاز/جيد/غالي) ثم جملة قصيرة جداً."
        response = model.generate_content(prompt)
        return response.text.replace("\n", " ").replace('"', '').replace("'", "")
    except:
        return "تحليل غير متاح"

def fetch_price(url, site_type):
    # تمويه البوت ليظهر كأنه متصفح طبيعي
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = "غير معروف"
        price = "0"
        image = ""

        if site_type == "amazon":
            try:
                title = soup.find(id="productTitle").get_text().strip()[:50] + "..."
                price_whole = soup.find(class_="a-price-whole")
                if price_whole:
                    price = price_whole.get_text().replace(".", "").strip()
                image = soup.find(id="landingImage")['src']
            except:
                pass

        elif site_type == "jarir":
            try:
                # محاولة سحب البيانات من جرير (قد تتغير حسب تصميم موقعهم)
                title = soup.find("h1", class_="product-title").get_text().strip()[:50]
                price = soup.find("span", class_="price").get_text().replace("SR", "").strip()
                image = soup.find("img", class_="product-image")['src']
            except:
                title = "منتج جرير (تحديث يدوي)"
        
        return title, price, image
        
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None, None, None

def scan_market():
    # هنا نضع الروابط التي نريد مراقبتها (يمكنك إضافة 100 رابط)
    products_to_track = [
        {"url": "https://www.amazon.sa/dp/B0CT3S3X4D", "type": "amazon"}, # مثال: لابتوب آسوس
        {"url": "https://www.amazon.sa/dp/B0CCSKQ78K", "type": "amazon"}, # مثال: ماك بوك
        # يمكنك إضافة روابط جرير هنا ولكنها تتطلب صيانة مستمرة
    ]
    
    csv_file = "market_data.csv"
    csv_columns = ["Name", "Price", "Type", "Image", "AI_Review", "Link", "Last_Update"]
    
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        
        print("Starting Real Market Scan...")
        for product in products_to_track:
            print(f"Tracking: {product['url']}")
            
            # سحب البيانات الحقيقية من الموقع
            real_name, real_price, real_image = fetch_price(product['url'], product['type'])
            
            if real_name:
                ai_opinion = get_ai_analysis(real_name, real_price)
                
                device_data = {
                    "Name": real_name,
                    "Price": real_price,
                    "Type": "Laptop", # يمكن جعلها ديناميكية لاحقاً
                    "Image": real_image,
                    "AI_Review": ai_opinion,
                    "Link": product['url'],
                    "Last_Update": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                writer.writerow(device_data)
                time.sleep(2) # انتظار بسيط لعدم الحظر

if __name__ == "__main__":
    scan_market()
    print("Database Updated with REAL prices!")
