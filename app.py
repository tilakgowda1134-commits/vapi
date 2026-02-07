from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "Tadawi API running"})

@app.route("/doctors")
def get_doctors():
    try:
        url = "https://tadawi.ae/"
        headers = {"User-Agent": "Mozilla/5.0"}

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
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run()
