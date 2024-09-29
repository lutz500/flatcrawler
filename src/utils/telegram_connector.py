import requests
import os
from dotenv import load_dotenv


class TelegramConnector:
    def __init__(self) -> None:
        load_dotenv()

        self.bot = os.getenv("TELEGERAM_BOT")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.url_message = (
            f"https://api.telegram.org/{self.bot}:{self.token}/sendMessage"
        )
        self.url_photo = f"https://api.telegram.org/{self.bot}:{self.token}/sendPhoto"

    def send_message(self, text: str):
        url = f"https://api.telegram.org/{self.bot}:{self.token}/sendMessage"
        data = {"chat_id": self.chat_id, "text": text, "parse_mode": "html"}

        requests.post(url, data=data)

    def send_messages(self, messages: list, filter_ids: list = None):
        for obj in messages:
            msg = obj.get("msg", None)
            img_link = obj.get("img_link", None)

            if img_link:
                data_message = {"chat_id": self.chat_id, "photo": img_link}
                requests.post(self.url_photo, data=data_message)

            if msg:
                data_message = {
                    "chat_id": self.chat_id,
                    "text": msg,
                    "parse_mode": "html",
                }
                requests.post(self.url_message, data=data_message)
