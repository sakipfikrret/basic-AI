import pyttsx3

# Global ses motoru
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Konuşma hızı

def seslendir(metin):
    global engine
    try:
        engine.say(metin)
        engine.runAndWait()
    except RuntimeError:
        # Motoru yeniden başlat
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        seslendir(metin)