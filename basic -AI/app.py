from flask import Flask, request, jsonify, render_template
from chatbot import yanit_olustur

app = Flask(__name__)

@app.route("/")
def ana_sayfa():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    kullanici_id = data.get("kullanici_id", "anonim")
    mesaj = data.get("mesaj", "")
    return jsonify({"yanit": yanit_olustur(kullanici_id, mesaj)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)