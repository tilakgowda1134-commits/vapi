from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# ROOT / HEALTH + WEBHOOK (GET + POST)
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        payload = request.get_json(silent=True)
        return jsonify({
            "status": "ok",
            "message": "POST received successfully",
            "payload": payload
        }), 200

    return jsonify({
        "status": "ok",
        "message": "Tadawi API running"
    }), 200


# DOCTORS API (GET only – scraping)
@app.route("/doctors", methods=["GET"])
def get_doctors():
    try:
        url = "https://tadawi.ae/"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        doctors = set()
        for tag in soup.find_all("h3"):
            name = tag.get_text(strip=True)
            if name and len(name) < 60:
                doctors.add(name)

        return jsonify({
            "status": "success",
            "count": len(doctors),
            "doctors": sorted(doctors)
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# OPTIONAL: Dedicated webhook (best practice for Vapi)
@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.get_json(silent=True)
    return jsonify({
        "status": "received",
        "payload": payload
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
