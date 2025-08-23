import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# Siteye normal bir tarayıcı gibi görünmek için Headers bilgisi ekliyoruz
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

url = "https://canlipiyasalar.haremaltin.com/"

veriler = {}
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

try:
    # Headers bilgisiyle birlikte istek yapıyoruz
    r = requests.get(url, headers=headers, timeout=10)
    
    # Eğer siteye ulaşamazsak hata ver (404, 500 vs.)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    # Sitedeki her bir fiyat satırını (<tr>) bulmaya çalışalım
    # Güncel yapıya göre her bir satır 'tr' etiketi içinde
    rows = soup.select("tbody tr")
    
    # Hata ayıklama için kaç satır bulduğunu yazdır
    print(f"Toplam {len(rows)} adet fiyat satırı bulundu.")

    if not rows:
        print("HATA: Siteden fiyat satırları alınamadı. HTML yapısı değişmiş olabilir.")

    for row in rows:
        # Satır içindeki ürün ismini ve fiyatı bulalım
        # Ürün ismi: <a class="item title"> içinde
        # Fiyat: <span class="item end price"> içinde
        title_element = row.select_one("a.item.title")
        price_element = row.select_one("span.item.end.price")

        if title_element and price_element:
            # get_text(" ", strip=True) ile "YENİ<br>ÇEYREK" gibi ifadeleri "YENİ ÇEYREK" yapar
            isim = title_element.get_text(" ", strip=True)
            fiyat = price_element.get_text(strip=True)
            veriler[isim] = fiyat
            print(f"Bulundu: {isim} - {fiyat}")

except requests.exceptions.RequestException as e:
    print(f"HATA: Siteye bağlanılamadı. Hata kodu: {e}")

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
    print("data.json dosyası güncellendi ancak içine yazılacak fiyat bulunamadı.")
