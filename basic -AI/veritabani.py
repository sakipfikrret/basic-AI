import sqlite3
import datetime

def baglanti_olustur():
    return sqlite3.connect('bilginay.db', check_same_thread=False)

def tablo_olustur():
    conn = baglanti_olustur()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS sohbetler 
                      (kullanici_id TEXT, mesaj TEXT, yanit TEXT, tarih DATETIME)''')
    conn.commit()

def sohbet_kaydet(kullanici_id, mesaj, yanit):
    conn = baglanti_olustur()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sohbetler VALUES (?, ?, ?, ?)",
                   (kullanici_id, mesaj, yanit, datetime.datetime.now()))
    conn.commit()

def baglami_getir(kullanici_id, limit=3):
    conn = baglanti_olustur()
    cursor = conn.cursor()
    cursor.execute("SELECT mesaj, yanit FROM sohbetler WHERE kullanici_id=? ORDER BY tarih DESC LIMIT ?",
                   (kullanici_id, limit))
    return cursor.fetchall()

tablo_olustur()