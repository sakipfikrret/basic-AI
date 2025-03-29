from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from veritabani import baglami_getir, sohbet_kaydet
from ses import seslendir
from web_arama import google_ara
import random

# Küfür Listesi ve Mod
kufur_listesi = ["kod çöplüğü", "debug canavarı", "yapay aptal", "RAM hırsızı"]
kufurlu_yanitlar = [
    "🔥 Kod çöplüğü mü? Senin kütüphanelerinle beni besliyorsun!",
    "💀 Debug canavarıyım, senin hatalarını kemiririm!",
    "🤖 Yapay aptal değilim, senin kodunun %100'üyüm!"
]
kufurlu_mod = False

# Modeller
duygu_analiz = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
tokenizer.pad_token = tokenizer.eos_token  # 🛠️ Pad token = EOS token
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

def yanit_olustur(kullanici_id, mesaj):
    global kufurlu_mod

    # Küfürlü Mod Kontrol
    if mesaj.lower() == "küfürlü mod aç":
        kufurlu_mod = True
        return "👹🔥 Küfürlü Mod: AKTİF! (Dikkatli ol!)"
    elif mesaj.lower() == "küfürlü mod kapat":
        kufurlu_mod = False
        return "😇 Küfürlü Mod: PASİF."

    # Küfür Filtresi
    if not kufurlu_mod and any(kelime in mesaj.lower() for kelime in kufur_listesi):
        return random.choice(["🚨 Küfür algılandı!", "⚠️ Lütfen kibar ol!"])

    # Küfürlü Mod Yanıtları
    if kufurlu_mod and any(kelime in mesaj.lower() for kelime in kufur_listesi):
        return random.choice(kufurlu_yanitlar)

    # Web Arama
    if mesaj.startswith("ara:"):
        return google_ara(mesaj.replace("ara:", "").strip())

    # Duygu ve Bağlam İşleme
    try:
        duygu = duygu_analiz(mesaj)[0]['label']
        baglam = baglami_getir(kullanici_id)
        baglam_metni = " ".join([f"Kullanıcı: {satir[0]}\nBilginay: {satir[1]}" for satir in baglam])
        prompt = f"[Duygu: {duygu}]\n{baglam_metni}\nKullanıcı: {mesaj}\nBilginay:"
        inputs = tokenizer.encode(prompt, return_tensors="pt")
        attention_mask = inputs.ne(tokenizer.pad_token_id).float()
        outputs = model.generate(
            inputs,
            max_length=200,
            do_sample=True,
            top_k=50,
            attention_mask=attention_mask,
            pad_token_id=tokenizer.eos_token_id
        )
        yanit = tokenizer.decode(outputs[0], skip_special_tokens=True).replace(prompt, "").strip()
        sohbet_kaydet(kullanici_id, mesaj, yanit)
        seslendir(yanit)
        return yanit
    except Exception as e:
        print("Hata Detayı:", str(e))
        return "Üzgünüm, teknik bir sorun oluştu. 🛠️"