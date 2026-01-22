import csv
import os
import google.generativeai as genai
from datetime import datetime

# إعداد Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

def get_ai_analysis(device_name, specs, price):
    try:
        # نطلب تحليل مختصر جداً يناسب شكل التطبيق
        prompt = (
            f"قيم جهاز '{device_name}' ({specs}) بسعر ({price} ريال). "
            "هل يصلح للأمن السيبراني؟ "
            "اجب بكلمة 'نعم' أو 'لا' ثم جملة تعليلية قصيرة جداً."
        )
        response = model.generate_content(prompt)
        return response.text.replace("\n", " ").replace('"', '').replace("'", "")
    except:
        return "جاري التحليل..."

def scan_market():
    # بيانات أولية لملء التطبيق
    market_data = [
        {"Name": "Lenovo Legion 5", "Price": "4500", "Type": "Laptop", "Specs": "RTX 3060, i7, 16GB", "Image": "https://m.media-amazon.com/images/I/71f5Eu5lJSL._AC_SL1500_.jpg", "Link": "https://amzn.sa"},
        {"Name": "MacBook Air M1", "Price": "3200", "Type": "Laptop", "Specs": "M1 Chip, 8GB, 256GB", "Image": "https://m.media-amazon.com/images/I/71TPda7cwUL._AC_SL1500_.jpg", "Link": "https://amzn.sa"},
        {"Name": "HP Victus 15", "Price": "2800", "Type": "Laptop", "Specs": "GTX 1650, i5, 8GB", "Image": "https://m.media-amazon.com/images/I/71M2I8i8R-L._AC_SL1500_.jpg", "Link": "https://amzn.sa"},
        {"Name": "Beelink SER5", "Price": "1260", "Type": "Mini PC", "Specs": "Ryzen 7, 16GB, 500GB", "Image": "https://m.media-amazon.com/images/I/71a6+q6yivL._AC_SL1500_.jpg", "Link": "https://amzn.sa"}
    ]
    
    # اسم الملف الذي سيسحبه جوجل شيت
    csv_file = "market_data.csv"
    csv_columns = ["Name", "Price", "Type", "Specs", "Image", "AI_Review", "Link", "Last_Update"]
    
    # إنشاء ملف CSV
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        
        print("Starting AI Analysis...")
        for device in market_data:
            print(f"Analyzing {device['Name']}...")
            device['AI_Review'] = get_ai_analysis(device['Name'], device['Specs'], device['Price'])
            device['Last_Update'] = datetime.now().strftime("%Y-%m-%d %H:%M")
            writer.writerow(device)

if __name__ == "__main__":
    scan_market()
    print("CSV Database Generated!")
