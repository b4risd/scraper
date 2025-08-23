import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

url = "https://canlipiyasalar.haremaltin.com/"

r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

# Ürün isimleri
titles = soup.select("a.item.title")

# Fiyatlar (aynı sırada geliyor)
prices = soup.select("span.item.end.price")

veriler = {}
for t, p in zip(titles, prices):
    isim = t.get_text(" ", strip=True)   # "YENİ ÇEYREK", "GRAM ALTIN" vs.
    fiyat = p.get_text(strip=True)       # "7.337"
    veriler[isim] = fiyat

data = {
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "fiyatlar": veriler
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Data kaydedildi:", data)
