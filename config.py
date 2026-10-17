from dotenv import load_dotenv
import os

load_dotenv()

class Config:
 # Telegram Bot
 TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
 WEBHOOK_URL = os.getenv("WEBHOOK_URL")
 
 # WormGPT API
 WORMGPT_API_URL = "https://api.wormgpt.live/v1"
 WORMGPT_API_KEY = os.getenv("WORMGPT_API_KEY")
 
 # Database
 DATABASE_URL = "sqlite:///wormgpt_bot.db"
 
 # Bot Settings
 BOT_NAME = "WormGPT"
 BOT_USERNAME = "WormGPT_Bot"
 
config = Config()