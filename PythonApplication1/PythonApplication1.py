# -*- coding: utf-8 -*-
import os
import sys
from dotenv import load_dotenv
from google import genai

# 1. Ortam değişkenlerini yüklüyoruz (.env dosyasından)
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Hata: GEMINI_API_KEY bulunamadı! .env dosyasını kontrol et.")
    sys.exit(1)

# 2. İstemciyi başlatıyoruz
client = genai.Client()

# 3. Hafızalı bir sohbet oturumu (Chat Session) başlatıyoruz
chat = client.chats.create(model="gemini-3.8-flash")

print("=" * 60)
print(" Gemini Konsol Sohbetine Hoş Geldin!")
print(" Çıkmak için 'q' veya 'exit' yazıp Enter'a basabilirsin.")
print("=" * 60 + "\n")

# 4. Sonsuz bir döngü ile kullanıcıdan sürekli girdi alıyoruz
while True:
    kullanici_girdisi = input("Sen: ").strip()

    # Çıkış kontrolü
    if kullanici_girdisi.lower() in ["q", "exit", "cikis"]:
        print("\nSohbet sonlandırıldı. Görüşmek üzere!")
        break

    # Boş mesaj kontrolü
    if not kullanici_girdisi:
        continue

    # 5. Mesajı sohbet oturumuna gönderiyoruz (Retry mantığı eklenmiş)
    max_deneme = 3
    for deneme in range(max_deneme):
        try:
            response = chat.send_message(kullanici_girdisi)
            print(f"\nGemini: {response.text}\n")
            print("-" * 60)
            break
        except Exception as e:
            if "503" in str(e) and deneme < max_deneme - 1:
                print(f"\nSunucu yoğun, 2 saniye içinde tekrar deneniyor ({deneme + 1}/{max_deneme})...")
                import time
                time.sleep(2)
            else:
                print(f"\nBir hata oluştu: {e}\n")
                break