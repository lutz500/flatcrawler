from geopy.geocoders import Nominatim
import folium
import io
from PIL import Image


def create_map(objs: dict):
    geolocator = Nominatim(user_agent="flatcrawler")

    base_lat = 49.783333
    base_lon = 9.933333

    m = folium.Map(location=[base_lat, base_lon], zoom_start=13)

    for obj in objs.values():
        wbs = obj.get("WBS", None)

        icon = folium.Icon(color="blue")
        if wbs:
            icon = folium.Icon(color="red")

        location = geolocator.geocode(obj.get("adress"))
        folium.Marker(
            [location.latitude, location.longitude], popup=create_popup(obj), icon=icon
        ).add_to(m)

    m.save("map.html")

    img_data = m._to_png(5)
    img = Image.open(io.BytesIO(img_data))
    img.save("map.png")


def create_popup(data: dict):
    html = """
    <h1>{adress}</h1><br>   
    WBS: {WBS}<br>
    Rooms: {rooms}<br>
    Area: {area}<br>
    Rent: {rent}<br>
    """
    return html.format(**data)


def save_map_as_img():
    img_data = open("map.html", "rb").read()
    img = Image.open(io.BytesIO(img_data))
    img.save("map.png")
