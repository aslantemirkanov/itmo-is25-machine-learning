from pathlib import Path

BASE_DIR = Path(__file__).parent
PAGES = BASE_DIR.parent / 'pages'
PAGES.mkdir(exist_ok=True)
FLATS = BASE_DIR.parent / 'flats'
FLATS.mkdir(exist_ok=True)
root_url = "https://m2.ru/sankt-peterburg/nedvizhimost/kupit-kvartiru/second/?pageNumber="
flat_links = "flat_links.csv"
unique_flat_links = "unique_flat_links.csv"
flat_dataset = "flat_dataset.csv"
headers = {
    'Cookie': 'site_local_address=false; user_region_id_detected=444; '
              'anonymous_token=eyJraWQiOiJtMiIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0'
              '.eyJzdWIiOiJhbm9ueW1vdXMiLCJ1c2VyX2lkIjoiYW5vbnltIzMxMTYxNDIwLTJiMzQtNGUwZC04MTRlLTBlMGNlYTk4ZmNiMiIsImlzcyI6Imh0dHBzOlwvXC9tMi5ydSIsInRva2VuX2Zsb3dfdHlwZSI6IkFOT05ZTU9VUyIsInJlYWxtIjoiTTIiLCJpc19hdXRoZW50aWNhdGVkIjpmYWxzZSwiaWF0IjoxNjk1NTA5NzE5LCJqdGkiOiIwOWFiODBlYy1jMTI3LTRmNDMtOTJmMC03MjBiNGRkYjYwNWEifQ.odJLX-X2CpCHMojmBkDmjqgwcRSFWVBGgIeJBRjTfJr2fwMK30SrvAYTsVlb3HR5sOIm9AtLn6uzBlw4_EXEvDP7njQqBY5jzI4Zari9Wkagala2lV-pXCIO65yfIRONSIHYIyliaqsbQkyyINuA10cOjwXKDYIXQtes_1eesIlAQP-xj6AWq0AtYFLWB9a9KVaPHwvrRwsciNNOslaaievEXlVfJGld_0gx_DyQ0uiMk7ObjKbIgRF8bRhYYA4d0E7jtPDeo99n3uqHB1K1mJ9Zqv_9OmBjiRGVTU86upnXs7xyhrQ5TsGXOto11Uy15hlk8_E5O2RqxuFT5B_F8w; anonymous_user_id=anonym#31161420-2b34-4e0d-814e-0e0cea98fcb2; site_local_address=false; ab-testing=%7B%22main-page-rotation%22%3A%22A%22%2C%22redirect%20a%2Fb%20test%22%3A%22A%22%2C%22cookie%20a%2Fb%20test%22%3A%22A%22%7D; _pk_id.1.343d=bbb11e5c672657d5.1695509720.; _pk_ses.1.343d=1; _ga=GA1.2.1281163354.1695509720; _gid=GA1.2.106449675.1695509720; _gat_m2=1; _ym_uid=1695509720473278833; _ym_d=1695509720; _ym_isad=2; _ym_visorc=w; tmr_lvid=f460a85336a01e79c5ed8ee35e0a213d; tmr_lvidTS=1695509721038; uxs_uid=463bd5e0-5a64-11ee-aca4-ad8f9b64498a; tmr_detect=0%7C1695509725415; _ga_W3WJZ5VT3B=GS1.1.1695509720.1.1.1695509727.53.0.0; _ga_BF94W927JF=GS1.2.1695509720.1.1.1695509727.53.0.0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/114.0.0.0 YaBrowser/23.7.5.734 Yowser/2.5 Safari/537.36 '
}


class Apartment:
    def __init__(self):
        self.title = None
        self.address = None
        self.description = None
        self.repair_type = None
        self.metro = None
        self.year = None
        self.materials = None
        self.heating = None
        self.area = None
        self.living_area = None
        self.height = None
        self.floor = None
        self.room_count = None
        self.price = None
        self.elevator = 0

    def __str__(self):
        return f"Title:{self.title}\nAddress:{self.address}\nDescription:{self.description}\nRepair Type:{self.repair_type}\n" \
               f"Metro: {self.metro}\nBuilding year: {self.year}\nMaterials: {self.materials}\nHeating: {self.heating}\n" \
               f"Area: {self.area} sq. meters\nLiving Area: {self.living_area} sq. meters\nHeight: {self.height} meters\n" \
               f"Floor: {self.floor}\nRoom Count: {self.room_count}\nPrice: {self.price} RUB\nElevator: {self.elevator}"
