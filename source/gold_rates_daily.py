import requests
import os
import logging

# ------------------------------------------
# Logger setup
# ------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# ------------------------------------------
# Env variables
# ------------------------------------------
def get_env_variable(var_name: str) -> str:
    value = os.getenv(var_name)
    if not value:
        logger.error(f"Environment variable '{var_name}' is not set.")
        raise ValueError(f"Environment variable '{var_name}' is required.")
    return value


BOT_TOKEN: str = get_env_variable("BOT_TOKEN")
CHAT_ID: str = get_env_variable("TELE_CHAT_ID")
GOLD_API_KEY: str = get_env_variable("GOLD_API_KEY")
GOLD_API_URL: str = "https://www.goldapi.io/api/XAU/INR"
TELE_BOT_MSG_URL: str = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# ------------------------------------------
# Core functions
# ------------------------------------------

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
        print("Error fetching gold price: ", str(e))
        logger.error(f"Error fetching gold price: {str(e)}")
        raise

def calculate_prices(price_24k):
    price_per_gram_22k = round(price_24k * 0.916, 2)
    price_per_gram_18k = round(price_24k * 0.75, 2)
    return price_per_gram_22k, price_per_gram_18k

def send_telegram(message):
    logger.info("Sending message to Telegram...")
    logger.info(f"Message: {message}")
    logger.info(f"Chat ID: {CHAT_ID}")

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