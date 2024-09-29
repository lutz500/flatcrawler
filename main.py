from src.crawler.stadtbau_crawler import StadtbauCrawler
from src.utils.telegram_connector import TelegramConnector
from src.utils.storeage import Storage
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    url_stadtbau = os.getenv("URL_STADTBAU")

    crawler = StadtbauCrawler(url=url_stadtbau)
    crawler.crawl()

    storage = Storage("storage.json")
    update_objs = storage.save_objs(crawler.data)

    messages = crawler.create_messages(filter_ids=update_objs)

    telegram = TelegramConnector()
    telegram.send_messages(messages, filter_ids=update_objs)
