from googlesearch import search

def google_ara(sorgu, sonuc_sayisi=3):
    try:
        sonuclar = []
        for url in search(sorgu, num_results=sonuc_sayisi, lang="tr"):
            sonuclar.append(f"🔗 {url}")
        return "\n".join(sonuclar[:sonuc_sayisi])
    except Exception as e:
        return f"Arama başarısız: {str(e)} 🧐"