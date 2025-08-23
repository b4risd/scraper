import requests
import json
from datetime import datetime

# Senin bulduğun, halka açık ve stabil API adresi
API_URL = "https://finance.truncgil.com/api/gold-rates"

headers = {
    # DOKÜMANTASYONDA BELİRTİLEN VE YENİ EKLENEN SATIR
    'Accept': 'application/json',
    # Göndermeye devam etmemizde sakınca olmayan User-Agent bilgisi
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}

veriler = {}
timestamp = "" # API zaten kendi zaman damgasını veriyor, onu kullanacağız.

try:
    print(f"API adresine bağlanılıyor: {API_URL}")
    r = requests.get(API_URL, headers=headers, timeout=20)
    r.raise_for_status() # Bağlantı hatası olursa durdur
    print("API'den veri başarıyla alındı.")

    # Gelen cevabı JSON formatında çöz
    api_data = r.json()
    
    # API'nin kendi "Son Güncelleme" zamanını alalım
    timestamp = api_data.get("update_date_str", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # API'den gelen listedeki her bir altın için döngü
    for item in api_data.get("data", []):
        isim = item.get("name")
        alis_str = item.get("buying_str")
        satis_str = item.get("selling_str")
        
        if isim and alis_str and satis_str:
            veriler[isim] = {
                "Alış": alis_str,
                "Satış": satis_str
            }
            print(f"Bulundu: {isim} - Alış: {alis_str}, Satış: {satis_str}")

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
