import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# YENİ VE GÜVENİLİR KAYNAK
URL = "https://bigpara.hurriyet.com.tr/altin/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}

veriler = {}
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

try:
    print(f"Veri çekilecek adres: {URL}")
    r = requests.get(URL, headers=headers, timeout=20)
    r.raise_for_status()
    print(f"Sunucudan gelen durum kodu: {r.status_code}")

    soup = BeautifulSoup(r.text, "html.parser")

    # Fiyatların bulunduğu ana kutuyu seçiyoruz
    altin_kurlari_div = soup.find("div", class_="gold-page-data")
    
    # Her bir altın kurunun bulunduğu satırları seçiyoruz
    rows = altin_kurlari_div.find_all("div", class_="t-row")
    
    print(f"Toplam {len(rows)} adet altın kuru bulundu.")

    for row in rows:
        # Satır içindeki hücreleri al
        isim = row.find("a", class_="name").get_text(strip=True)
        alis = row.find("div", class_="cell-buying").get_text(strip=True)
        satis = row.find("div", class_="cell-selling").get_text(strip=True)
        
        veriler[isim] = {
            "Alış": alis,
            "Satış": satis
        }
        print(f"Bulundu: {isim} - Alış: {alis}, Satış: {satis}")

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
    print("data.json dosyası başarıyla güncellendi.")
else:
    print("SONUÇ: data.json dosyası güncellendi ancak içine yazılacak fiyat bulunamadı.")
