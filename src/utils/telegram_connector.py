import os

import requests
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

    def send_messages(self, messages: list[dict], filter_ids: list = None):
        """Send telegram messages

        Args:
            messages (list[dict]): List of dicts for messages to send
            filter_ids (list, optional): List of filter id for which to send messages.
            Defaults to None.
        """
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

    def send_map(self, map_path: str):
        """Send map to telegram

        Args:
            map_path (str): Path to map file
        """
        with open(map_path, "rb") as file:
            data_message = {"chat_id": self.chat_id}
            files = {"photo": file}
            requests.post(self.url_photo, data=data_message, files=files)
