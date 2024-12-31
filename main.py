from flask import Flask, request, jsonify, render_template
import random
import requests

app = Flask(__name__)

# Fetch card data from Scryfall API
def fetch_cards(set_code):
    url = f"https://api.scryfall.com/cards/search?q=set:{set_code}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["data"]
    return []

# Simulate a pack
def simulate_pack(cards, set_code):
    commons = [card for card in cards if card.get("rarity") == "common" and card.get("set") == set_code]
    uncommons = [card for card in cards if card.get("rarity") == "uncommon" and card.get("set") == set_code]
    rares = [card for card in cards if card.get("rarity") in ["rare", "mythic"] and card.get("set") == set_code]

    pack = {
        "commons": random.sample(commons, 10) if len(commons) >= 10 else commons[:10],
        "uncommons": random.sample(uncommons, 3,) if len(uncommons) >= 3 else uncommons[:3],
        "rare": random.choice(rares),
    }

    return pack

# Serve the main page
@app.route("/")
def index():
    return render_template("index.html")

# API endpoint to open a pack
@app.route("/open_pack", methods=["POST"])
def open_pack():
    set_code = request.json.get("set_code", "khm")
    cards = fetch_cards(set_code)
    if not cards:
        return jsonify({"error": "Failed to fetch cards"}), 500
        # Simulate the pack and collect debug information
    commons = [card for card in cards if card.get("rarity") == "common"]
    uncommons = [card for card in cards if card.get("rarity") == "uncommon"]
    rares = [card for card in cards if card.get("rarity") in ["rare", "mythic"]]
    pack = simulate_pack(cards, set_code)

    # Debugging information
    debug_info = {
        "set_code": set_code,
        "card_counts": {
            "commons": len(commons),
            "uncommons": len(uncommons),
            "rares": len(rares),
        },
        "pack_details": {
            "commons": [card["name"] for card in pack["commons"]],
            "uncommons": [card["name"] for card in pack["uncommons"]],
            "rare": pack["rare"]["name"] if pack["rare"] else "None",
        },
    }

    # Include debugging information in the response
    return jsonify({"pack": pack, "debug": debug_info})

if __name__ == "__main__":
    app.run(debug=True)