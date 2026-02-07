from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # IMPORTANT for Vapi

@app.route("/", methods=["GET", "POST"])
def home():
    return jsonify({"status": "Tadawi API running"})

@app.route("/doctors", methods=["GET", "POST"])
def get_doctors():
    try:
        url = "https://tadawi.ae/"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=8)
        soup = BeautifulSoup(response.text, "html.parser")

        doctors = []

        for tag in soup.find_all("h3"):
            name = tag.get_text(strip=True)
            if name:
                doctors.append(name)

        # ⚠️ Return simple JSON (Vapi prefers this)
        return jsonify(doctors)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
