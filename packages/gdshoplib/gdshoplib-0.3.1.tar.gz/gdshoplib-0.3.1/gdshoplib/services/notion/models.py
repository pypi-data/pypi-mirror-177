import re
import requests

from enum import Enum
from typing import Callable, Dict, List, Optional, Union
from pydantic import BaseModel
from gdshoplib.packages import Disk


def list_addon(data):
    if not data:
        return []

    elements = [i.strip().lower() for i in data.split("/")]
    return [element for element in elements if element]


properties_keys_map = {
    "title": dict(name="Name", key="title"),
    "BeEA": dict(name="Публикация", key="status_public"),
    "MUl%7C": dict(name="Статус описания", key="status_description"),
    "BKOs": dict(name="Наш SKU", key="sku"),
    "pXTy": dict(name="Количество", key="quantity"),
    #
    "iwg%3C": dict(name="🎟️ Поставщик", key="supplier"),
    "BHve": dict(name="SKU поставщика", key="sku_supplier"),
    #
    "NEgM": dict(name="Категория товара", key="category_product"),
    "ePC%5C": dict(name="Вид спорта", key="product_sport"),
    #
    "%3D%3FrC": dict(name="🐴 Каналы", key="chanels"),
    "AyqD": dict(name="Цена (eur)", key="price_source"),
    #
    "TbyK": dict(name="Created by", key="created_by"),
    "v%5Dsj": dict(name="Created time", key="created_at"),
    "~%7BrF": dict(name="Last edited by", key="updated_by"),
    "mVEw": dict(name="Last edited time", key="updated_at"),
    #
    "pyiW": dict(name="Закупочная", key="price_supplier"),
    "opcQ": dict(name="Себестоимость", key="price_buy"),
    "VmWm": dict(name="Базовая", key="price_base"),
    "x%3A%5Ci": dict(name="Ходовая", key="price_general"),
    "%7Bh%7D%7B": dict(name="Скидка, 10%", key="price_sale_10"),
    "cPu~": dict(name="Скидка, 20%", key="price_sale_20"),
    "%7D%7CBr": dict(name="Скидка, 30%", key="price_sale_30"),
    #
    "COmf": dict(
        name="Материалы / Состав", key="description_materials", addon=list_addon
    ),
    "HI%5DA": dict(name="Основное фото", key="photo_general"),
    "Jvku": dict(name="Цвет", key="description_color"),
    "PJXf": dict(name="ШиринаxГлубинаxВысота (мм)", key="description_measurement"),
    "Tss%5D": dict(name="Название на русском", key="description_title"),
    "W%5BhI": dict(name="Коллекция", key="description_collection"),
    "%5DZ%3Az": dict(name="Бренд", key="description_brand"),
    "%5Dk%5CH": dict(name="Фото коллекции", key="photo_collection"),
    "%60jru": dict(name="Фото с сантиметром", key="photo_size"),
    "jiSN": dict(name="Подробное видео с голосом", key="video_description"),
    "sXND": dict(name="Примечания", key="description_notes", addon=list_addon),
    "taW%3B": dict(name="Размер", key="description_size"),
    "u_tU": dict(name="Короткое описание", key="description_short"),
    "ytWy": dict(name="Вес (кг)", key="description_weight"),
    "zejc": dict(name="Видео рилс", key="video_reals"),
    "MqdC": dict(name="Теги", key="tags", addon=list_addon),
}

properties_type_parse_map = {
    "rich_text": lambda data: " ".join(
        [t.get("plain_text", "") for t in data["rich_text"]]
    )
    or "",
    "number": lambda data: data["number"] or 0,
    "select": lambda data: data.get("select").get("name")
    if data.get("select")
    else None,
    "multi_select": lambda data: data,
    "status": lambda data: data["status"]["name"],
    "date": lambda data: data,
    "formula": lambda data: data["formula"]["number"],
    "relation": lambda data: str(data["relation"]),
    "rollup": lambda data: data,
    "title": lambda data: str(data["title"]),
    "people": lambda data: data,
    "files": lambda data: data,
    "checkbox": lambda data: data,
    "url": lambda data: data["url"],
    "email": lambda data: data,
    "phone_number": lambda data: data,
    "created_time": lambda data: data["created_time"],
    "created_by": lambda data: str(data["created_by"]),
    "last_edited_time": lambda data: data["last_edited_time"],
    "last_edited_by": lambda data: str(data["last_edited_by"]),
    "image": lambda data: data["image"]["file"]["url"],
    "video": lambda data: data["video"]["file"]["url"],
}


class ProductProperties(BaseModel):
    name: str
    key: str
    value: Optional[Union[float, int, str]]
    addon: Optional[Callable]


class ProductSettingsBlock(BaseModel):
    id: str
    media: Optional[Dict[str, List[Optional[str]]]]
    price: Dict[str, Union[int, str]]


class ProductDescriptionBlock(BaseModel):
    id: str
    platform: Optional[str]
    description: str


class MediaEnum(str, Enum):
    video = "video"
    image = "image"


class ProductMedia(BaseModel):
    block_id: str
    discussion_id: Optional[str]
    key: str
    name: Optional[str]
    type: MediaEnum
    url: str
    format: Optional[str]
    content: Optional[bytes]
    md5: Optional[str]

    @staticmethod
    def parse_format(url):
        pattern = re.compile(r"\/.*\.(\w+)(\?|$)")
        r = re.findall(pattern, url)
        return r[0][0] if r else None

    @staticmethod
    def parse_name(url):
        # Не знаю как сделать красивее
        pattern1 = re.compile(r".*\/(?P<name>.*)")
        r = re.findall(pattern1, url)
        if not r or not r[0]:
            return None
        return r[0].split("?")[0]

    def get_content(self):
        if self.content is None:
            response = requests.get(self.url)
            self.content = response.content
            self.md5 = Disk.get_md5(self.content)
        return self.content


class Product(BaseModel):
    # Нужна полноценная карточка товара со всеми параметрами
    id: str
    properties: List[ProductProperties]
    settings: Optional[ProductDescriptionBlock]
    descriptions: Dict[Union[str, None], ProductDescriptionBlock] = {}
    media: List[Optional[ProductMedia]] = []

    def dict(self, *args, **kwargs):
        _d = super(Product, self).dict(*args, **kwargs)

        props = {}
        for prop in _d.pop("properties"):
            props[prop["key"]] = (
                prop["addon"](prop["value"]) if prop["addon"] else prop["value"]
            )

        medias = {}
        for media in _d.pop("media"):
            medias[media["key"]] = media

        return {**_d, **props, **medias}


class User(BaseModel):
    id: str
    name: str
    email: str
