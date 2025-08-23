import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# Siteye normal bir tarayıcı gibi görünmek için Headers bilgisi
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

url = "https://www.izko.org.tr/"

veriler = {}
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

try:
    # Headers bilgisiyle birlikte istek yapıyoruz
    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()  # Eğer siteye ulaşamazsak hata ver

    soup = BeautifulSoup(r.text, "html.parser")

    # Fiyatların olduğu tablodaki tüm satırları (tr) seçiyoruz
    rows = soup.select(".kurlar-table table tbody tr")
    
    print(f"Toplam {len(rows)} adet fiyat satırı bulundu.")

    if not rows:
        print("HATA: Siteden fiyat satırları alınamadı. HTML yapısı değişmiş olabilir.")

    for row in rows:
        # Satırdaki tüm hücreleri (td) al
        cells = row.find_all("td")
        
        # Eğer bir satırda en az 3 hücre varsa (İsim, Alış, Satış) veriyi al
        if len(cells) >= 3:
            isim = cells[0].get_text(strip=True)
            alis = cells[1].get_text(strip=True)
            satis = cells[2].get_text(strip=True)
            
            # Veriyi sözlüğe ekle
            veriler[isim] = {
                "Alış": alis,
                "Satış": satis
            }
            print(f"Bulundu: {isim} - Alış: {alis}, Satış: {satis}")

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
