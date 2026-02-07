from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Tadawi API is running"})

@app.route("/doctors")
def get_doctors():
    try:
        url = "https://tadawi.ae/"
        
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        doctors = []

        # Example extraction (you may adjust based on actual HTML structure)
        for tag in soup.find_all("h3"):
            name = tag.get_text(strip=True)
            if name and len(name) < 50:
                doctors.append(name)

        return jsonify({
            "status": "success",
            "count": len(doctors),
            "doctors": doctors
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)              + CategoryInfo          : ObjectNotFound: (ngrok  
 :String) [], CommandNotFoundException
  + FullyQualifiedErrorId : CommandNotFoundExcepti  
 on\
        })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)