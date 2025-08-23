import requests
import json
from datetime import datetime

API_URL = "https://www.izko.org.tr/kurlar.php"

# Sitenin bot olmadığınıza ikna olması için gönderilebilecek en kapsamlı başlık bilgisi
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9,tr;q=0.8',
    'Referer': 'https://www.izko.org.tr/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

veriler = {}
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

try:
    print(f"API adresine istek yapılıyor: {API_URL}")
    # Timeout süresini biraz artıralım
    r = requests.get(API_URL, headers=headers, timeout=20)
    
    # === HATA AYIKLAMA İÇİN EKLENEN KISIM ===
    print(f"Sunucudan gelen durum kodu: {r.status_code}")
    # Sunucudan gelen cevabın ilk 500 karakterini yazdırarak ne döndüğünü görelim
    print(f"Sunucu cevabının başlangıcı: {r.text[:500]}")
    # ==========================================

    r.raise_for_status()

    # Sunucudan gelen cevabın JSON olup olmadığını kontrol edelim
    if 'application/json' in r.headers.get('Content-Type', ''):
        api_data = r.json()
        print("API'den JSON verisi başarıyla alındı ve çözüldü.")

        veriler = {
            "24 Ayar Altın Gram": {"Alış": api_data.get('hasgramalis'), "Satış": api_data.get('hasgramsatis')},
            "Yeni Çeyrek Altın": {"Alış": api_data.get('yeniceyrekalis'), "Satış": api_data.get('yeniceyreksatis')},
            "Eski Çeyrek Altın": {"Alış": api_data.get('eskiceyrekalis'), "Satış": api_data.get('eskiceyreksatis')},
            "Yeni Yarım Altın": {"Alış": api_data.get('yeniyarimalis'), "Satış": api_data.get('yeniyarimsatis')},
            "Eski Yarım Altın": {"Alış": api_data.get('eskiyarimalis'), "Satış": api_data.get('eskiyarimsatis')},
            "Yeni Tam Altın": {"Alış": api_data.get('yenitamalis'), "Satış": api_data.get('yenitamsatis')},
            "Eski Tam Altın": {"Alış": api_data.get('eskitamalis'), "Satış": api_data.get('eskitamsatis')}
        }
        print("Veriler başarıyla formatlandı.")
    else:
        print("HATA: Sunucudan gelen cevap JSON formatında değil. Site muhtemelen isteği engelledi.")

except requests.exceptions.RequestException as e:
    print(f"HATA: API'ye bağlanırken bir sorun oluştu. Hata: {e}")
except json.JSONDecodeError:
    print("HATA: Sunucudan gelen cevap JSON olarak çözülemedi. Muhtemelen bir engelleme sayfası geldi.")


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
    print("SONUÇ: data.json dosyası güncellendi ancak içine yazılacak fiyat bulunamadı.")
