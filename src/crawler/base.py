from typing import Optional
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BaseCrawler:
    def get_dynamic_web_page(self, url: str) -> Optional[str]:
        """Get data from webpage using selenium.
        This way we are able to gather dynamicall created
        data from webpages.

        Args:
            url (str): Url of web page that should be loaded

        Returns:
            (str|None): String representation of the html code of
            the request webpage. If not found None is returned.
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")

        web = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        web.get(url)
        data = WebDriverWait(web, poll_frequency=1, timeout=30).until(
            EC.presence_of_element_located((By.TAG_NAME, "app-properties"))
        )
        html_content = data.get_attribute("innerHTML")
        web.quit()

        return html_content

    def print_data(self):
        print(self.data)
