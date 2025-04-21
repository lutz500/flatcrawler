import hashlib

from bs4 import BeautifulSoup

from .base import BaseCrawler


class StadtbauCrawler(BaseCrawler):
    def __init__(self, url: str) -> None:
        self.url = url
        self.data = {}

    def _hash_id(self, *argv) -> str:
        """Calculate a consistent hash as id based on
        different arguments

        Returns:
            str: Created hash as id
        """
        obj_key = "_".join(str(arg) for arg in argv)
        hashed_id = hashlib.sha256(obj_key.encode()).hexdigest()
        return hashed_id

    def crawl(self):
        # Use Selenium to be able to gather dynamic data
        data = self.get_dynamic_web_page(self.url)

        # Convert data
        soup = BeautifulSoup(data, "html.parser")

        # Scrape data specific for this website
        results = soup.find_all(
            "div",
            class_="col-12 col-md-6 col-lg-4 col-xl-3 property-card-list__card ng-star-inserted",
        )

        for element in results:
            title = element.find(
                "h3",
                class_="title-m d-inline-block mb-0 property-card__title ng-star-inserted",
            ).text
            adress = element.find(
                "span", class_="d-block mt-1 title-s ng-star-inserted"
            ).text
            area = element.find(
                "div", class_="d-flex align-items-center me-3 property-card__stats-item"
            )
            area = area.text if area else "N/A"

            rooms = element.find(
                "div",
                class_="d-flex align-items-center me-3 property-card__stats-item ng-star-inserted",
            )
            rooms = int(rooms.text) if rooms else "N/A"

            rent = element.find(
                "div", class_="my-0 ms-auto property-card__stats-item"
            ).text
            obj_id = element.find(
                "div", class_="mb-1 property-card__external-id ng-star-inserted"
            ).text
            starting_date = (
                element.find(
                    "div",
                    class_="mt-3 property-card__available-from-date ng-star-inserted",
                )
                .find("span", class_="ms-1")
                .text
            )
            badges_normal = element.find_all(
                "div",
                class_="badge badge--border-radius-small badge--border-style- badge--color-neutral badge--size-normal mdc-elevation--z0",
            )
            badges_highlighted = element.find_all(
                "div",
                class_="badge badge--border-radius-small badge--border-style- badge--color-primary-accent badge--size-normal mdc-elevation--z0",
            )
            badges = badges_normal + badges_highlighted
            badges = [
                badge.find("span", class_="badge__inner uppercase").text
                for badge in badges
            ]
            img_link = element.find(
                "img",
                class_="image image--object-fit-default image--border-radius-none image--border-style-none",
            )["src"]

            # Claculate unique id as hash
            id = self._hash_id(title, adress, area, rooms, badges)

            self.data[id] = {
                "title": title,
                "adress": adress,
                "area": area,
                "rooms": rooms,
                "rent": rent,
                "obj_id": obj_id,
                "starting_date": starting_date,
                "badges": badges,
                "WBS": True if "WBS" in badges else False,
                "img_link": img_link,
                "id": id,
            }

        return self.data

    def create_messages(self, filter_ids: list[str]) -> dict:
        """Create telegram message for this website/data

        Args:
            filter_ids (list[str]): List of ids messages should
            be created for.

        Returns:
            dict: Dict of messages
        """
        messages = []

        for key, obj in self.data.items():
            if key not in filter_ids:
                continue

            msg = f"<b>{obj.get('title', 'Apartment')}</b>\n"
            msg += f"<i>{obj.get('adress', 'Adress of Object')}</i>\n"
            msg += f" Miete: {obj.get('rent', 'xxx € .mtl')}\n"
            msg += f" Zimmer: {obj.get('rooms', 'x')}\n"
            msg += f" Fläche: {obj.get('area', 'xx qm^2')}\n"
            msg += f" Verfügbar ab: {obj.get('starting_date', 'xxxx.xx.xx')}\n"
            msg += f"https://www.google.de/maps/place/{obj.get('adress', 'Adress of Object').replace(" ","+")}\n"
            msg += "\n"

            messages.append({"msg": msg, "img_link": obj.get("img_link", None)})

        return messages
