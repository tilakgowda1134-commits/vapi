from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# -------------------------------
# SCRAPER FUNCTION (REUSABLE)
# -------------------------------
def fetch_doctors():
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

    return sorted(doctors)


# -------------------------------
# ROOT / HEALTH
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    return jsonify({
        "status": "ok",
        "message": "Tadawi API running"
    }), 200


# -------------------------------
# DOCTORS API (BROWSER / TESTING)
# -------------------------------
@app.route("/doctors", methods=["GET"])
def get_doctors():
    try:
        doctors = fetch_doctors()
        return jsonify({
            "status": "success",
            "count": len(doctors),
            "doctors": doctors
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# -------------------------------
# WEBHOOK (VAPI CALLS THIS)
# -------------------------------
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True) or {}
    action = data.get("action", "").lower()

    # 🔑 CONNECT WEBHOOK → SCRAPER
    if "doctor" in action:
        try:
            doctors = fetch_doctors()

            if not doctors:
                return jsonify({
                    "message": "I could not fetch doctor information right now."
                }), 200

            top = doctors[:5]

            return jsonify({
                "message": (
                    "Some doctors at Al Tadawi Hospital include "
                    + ", ".join(top)
                    + ". Would you like doctors by department?"
                )
            }), 200

        except Exception:
            return jsonify({
                "message": "There was an issue fetching doctor data. Please try again later."
            }), 200

    # DEFAULT RESPONSE
    return jsonify({
        "message": "I can help you with doctors, departments, services, and timings at Al Tadawi Hospital."
    }), 200


# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
