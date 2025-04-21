import os

from dotenv import load_dotenv

from src.crawler.stadtbau_crawler import StadtbauCrawler
from src.utils.storeage import Storage
from src.utils.telegram_connector import TelegramConnector

if __name__ == "__main__":
    # Load env variables
    load_dotenv()
    url_stadtbau = os.getenv("URL_STADTBAU")

    # Initalize Crawler of type StadtbauCrawler
    crawler = StadtbauCrawler(url=url_stadtbau)

    # Crawl data
    crawler.crawl()

    # Initalize Storage Instance and save new results
    storage = Storage("storage.json")
    update_objs = storage.save_objs(crawler.data)

    # Create new Telegram Messages
    messages = crawler.create_messages(filter_ids=update_objs)

    # Initialize TelegramConnector to send messages
    telegram = TelegramConnector()
    telegram.send_messages(messages, filter_ids=update_objs)

    # Create map if new objects are found
    # if len(update_objs) > 0:
    #     create_map(storage.get_all())
    #     telegram.send_map("map.png")
