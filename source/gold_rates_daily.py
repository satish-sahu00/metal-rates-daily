import requests
import os

BOT_TOKEN: str = os.getenv("BOT_TOKEN")
CHAT_ID: str = os.getenv("TELE_CHAT_ID")
GOLD_API_KEY: str = os.getenv("GOLD_API_KEY")
GOLD_API_URL: str = "https://www.goldapi.io/api/XAU/INR"
TELE_BOT_MSG_URL: str = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def get_gold_prices():
    headers = {
            "x-access-token": GOLD_API_KEY,
            "Content-Type": "application/json"
        }
    try:

        response = requests.get(GOLD_API_URL, headers=headers)
        data = response.json()

        price_per_gram_24k = data["price"] / 31.1035 # ounce -> gram
        return round(price_per_gram_24k, 2)
    except requests.exceptions.RequestException as e:
        print("Error: ", str(e))

def calculate_prices(price_24k):
    price_per_gram_22k = round(price_24k * 0.916, 2)
    price_per_gram_18k = round(price_24k * 0.75, 2)
    return price_per_gram_22k, price_per_gram_18k

def send_telegram(message):
    requests.post(TELE_BOT_MSG_URL, data={
        "chat_id": CHAT_ID,
        "text": message
    })

if __name__ == "__main__":
    price_24k = get_gold_prices()
    price_22k, price_18k = calculate_prices(price_24k)

    msg = f"""
        📊 *Gold Price Today*
        🟡 24K: ₹ {price_24k}/g
        🟠 22K: ₹ {price_22k}/g
        ♦️ 18K: ₹ {price_18k}/g
        """
    send_telegram(msg.strip())