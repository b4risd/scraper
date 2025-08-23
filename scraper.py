import requests
import json
from datetime import datetime

# Kullandığımız halka açık ve stabil API adresi
API_URL = "https://finance.truncgil.com/api/gold-rates"

headers = {
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}

veriler = {}
timestamp = ""

try:
    print(f"API adresine bağlanılıyor: {API_URL}")
    r = requests.get(API_URL, headers=headers, timeout=20)
    r.raise_for_status()
    print("API'den veri başarıyla alındı.")

    api_data = r.json()
    
    # API'nin kendi güncelleme zamanını alıyoruz
    timestamp = api_data.get("Meta_Data", {}).get("Update_Date", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # === DOĞRU YAPIYA GÖRE DEĞİŞTİRİLEN KISIM ===
    # "Rates" anahtarının içindeki objeyi alıyoruz
    rates_object = api_data.get("Rates", {})
    
    # Bu objenin içindeki her bir altın kuru için döngü (GRA, CEY, YAR...)
    for key, item in rates_object.items():
        isim = item.get("Name")
        alis = item.get("Buying")
        satis = item.get("Selling")
        
        # Sadece isim ve fiyatları olanları alalım
        if isim and alis is not None and satis is not None:
            veriler[isim.title()] = { # .title() ile baş harfleri büyütelim (örn: GRAMALTIN -> Gramaltin)
                "Alış": str(alis),
                "Satış": str(satis)
            }
            print(f"Bulundu: {isim.title()} - Alış: {alis}, Satış: {satis}")
    # ============================================

except Exception as e:
    print(f"Bir hata oluştu: {e}")

# Sonuçları JSON dosyasına yaz
data = {
    "timestamp": timestamp,
    "fiyatlar": veriler
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

if veriler:
    print("data.json dosyası API verileriyle başarıyla güncellendi.")
else:
    print("SONUÇ: data.json dosyası güncellendi ancak API'den veri alınamadı.")
