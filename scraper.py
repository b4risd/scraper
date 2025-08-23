import requests
import json
from datetime import datetime

# Bu, sitenin fiyatları getirmek için arka planda kullandığı API adresidir.
API_URL = "https://www.izko.org.tr/kurlar.php"

# Siteye normal bir tarayıcı gibi görünmek için Headers bilgisi
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.izko.org.tr/' # Nereden geldiğimizi belirtmek güvenilirliği artırır
}

veriler = {}
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

try:
    print(f"API adresine istek yapılıyor: {API_URL}")
    r = requests.get(API_URL, headers=headers, timeout=10)
    r.raise_for_status()  # Eğer adrese ulaşamazsak hata ver

    # Gelen cevap doğrudan JSON formatında olduğu için parse ediyoruz
    api_data = r.json()
    print("API'den veri başarıyla alındı.")

    # API'den gelen verileri istediğimiz formata çeviriyoruz
    # Senin bulduğun ID'ler burada anahtar olarak kullanılıyor (örn: yeniceyrekalis)
    veriler = {
        "24 Ayar Altın Gram": {
            "Alış": api_data.get('hasgramalis', 'N/A'),
            "Satış": api_data.get('hasgramsatis', 'N/A')
        },
        "Yeni Çeyrek Altın": {
            "Alış": api_data.get('yeniceyrekalis', 'N/A'),
            "Satış": api_data.get('yeniceyreksatis', 'N/A')
        },
        "Eski Çeyrek Altın": {
            "Alış": api_data.get('eskiceyrekalis', 'N/A'),
            "Satış": api_data.get('eskiceyreksatis', 'N/A')
        },
        "Yeni Yarım Altın": {
            "Alış": api_data.get('yeniyarimalis', 'N/A'),
            "Satış": api_data.get('yeniyarimsatis', 'N/A')
        },
        "Eski Yarım Altın": {
            "Alış": api_data.get('eskiyarimalis', 'N/A'),
            "Satış": api_data.get('eskiyarimsatis', 'N/A')
        },
        "Yeni Tam Altın": {
            "Alış": api_data.get('yenitamalis', 'N/A'),
            "Satış": api_data.get('yenitamsatis', 'N/A')
        },
        "Eski Tam Altın": {
            "Alış": api_data.get('eskitamalis', 'N/A'),
            "Satış": api_data.get('eskitamsatis', 'N/A')
        }
    }
    print("Veriler başarıyla formatlandı.")

except requests.exceptions.RequestException as e:
    print(f"HATA: API'ye bağlanılamadı. Hata: {e}")

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
    print("data.json dosyası güncellendi ancak içine yazılacak API verisi bulunamadı.")
