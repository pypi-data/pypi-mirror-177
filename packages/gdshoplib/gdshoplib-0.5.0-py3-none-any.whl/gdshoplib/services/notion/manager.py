# Менеджер управления Notion
import json
from random import randrange

from dateutil.parser import parse as date_parser

from gdshoplib.core import BaseManager
from gdshoplib.packages import transliterate
from gdshoplib.services.notion.models import (Product, ProductDescriptionBlock,
                                              ProductMedia, ProductProperties,
                                              ProductSettingsBlock, User,
                                              properties_keys_map,
                                              properties_type_parse_map)
from gdshoplib.services.notion.settings import Settings


class NotionManager(BaseManager):
    SETTINGS = Settings
    BASE_URL = "https://api.notion.com/v1/"

    def get_headers(self):
        return {
            **self.auth_headers(),
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
            "Accept": "application/json",
        }

    def auth(self):
        return True

    def auth_headers(self):
        return {"Authorization": "Bearer " + self.settings.NOTION_SECRET_TOKEN}

    def get_user(self, user_id):
        data = self.make_request(f"users/{user_id}", method="get").json()
        if data.get("results"):
            data = data.get("results")[0]
        return User.parse_obj(
            {**data, "email": data.get("person", {}).get("email") or data.get("name")}
        )

    def is_settings_block(self, capture):
        return "base_settings" in capture

    def is_description_block(self, capture):
        return "description" in capture

    def is_media_block(self, capture):
        return capture in (
            "photo_general",
            "photo_collection",
            "photo_size",
            "photo_additional",
            "video_reals",
            "video_description",
            "video_general",
        )

    def get_capture(self, block):
        _capture = block[block["type"]].get("caption")
        return _capture[0].get("plain_text") if _capture else None

    def set_media_block(self, product: Product):
        result = []
        for raw_block in self.get_blocks(product.id):
            _type = raw_block["type"]
            if _type not in ("image", "video"):
                continue

            capture = self.get_capture(raw_block) or (
                "photo_additional" if _type == "image" else "video_description"
            )
            if self.is_media_block(capture):
                url = properties_type_parse_map[_type](raw_block)
                media = ProductMedia(
                    key=capture,
                    type=_type,
                    url=url,
                    discussion_id=self.get_discussion_id(raw_block["id"]),
                    block_id=raw_block["id"],
                )

                media.name = ProductMedia.parse_name(media.url)
                media.format = ProductMedia.parse_format(media.url)
                result.append(media)

        product.media = result

    def set_technical_blocks(self, product: Product):
        # Поиск блока с настройками и загрузка
        for raw_block in self.get_blocks(product.id):
            if raw_block["type"] != "code":
                continue

            capture = self.get_capture(raw_block)
            content = properties_type_parse_map["rich_text"](raw_block["code"])

            if self.is_settings_block(capture):
                block = ProductSettingsBlock(id=raw_block["id"], **json.loads(content))
                product.settings = block

            elif self.is_description_block(capture):
                platform = capture.split(":")
                platform = platform[-1].upper() if len(platform) > 1 else None
                block = ProductDescriptionBlock(
                    id=raw_block["id"],
                    platform=platform if platform else None,
                    description=content,
                )
                product.descriptions[platform] = block

    def get_products(self, format="dict", as_generator=False):
        products = []
        for page in self.pagination(
            f"databases/{self.settings.PRODUCT_DB}/query", method="post", params=None
        ):
            for raw_product in page.json()["results"]:
                product = self.parse_product(raw_product)
                if as_generator:
                    yield product.dict() if format == "dict" else product
                    continue
                products.append(product.dict() if format == "dict" else product)

        if not as_generator:
            return products

    def get_blocks(self, parent_id):
        for block_response in self.pagination(
            f"blocks/{parent_id}/children/", method="get"
        ):
            for raw_block in block_response.json()["results"]:
                if raw_block["has_children"]:
                    yield from self.get_blocks(raw_block["id"])
                else:
                    yield raw_block

    def get_discussion_id(self, block_id):
        data = self.make_request(
            "comments", method="get", params={"block_id": block_id}
        ).json()["results"]
        return data[0]["discussion_id"] if data else None

    def set_comment(self, /, parent=None, discussion_id=None, rich_text=None):
        assert rich_text, "Нет текста комментария"
        assert parent or discussion_id, "Нужно передать parrent или discussion_id"
        params = (
            {"discussion_id": discussion_id} if discussion_id else {"parent": parent}
        )
        self.make_request(
            "comments", method="post", params={**params, **dict(rich_text=[rich_text])}
        ).json()

    def get_comments(self, parent_id):
        for comment_response in self.pagination(
            "comments", params={"block_id": parent_id}, method="get"
        ):
            for raw_comment in comment_response.json()["results"]:
                yield raw_comment

    def get_product(self, sku, format="dict"):
        data = self.make_request(
            f"databases/{self.settings.PRODUCT_DB}/query",
            method="post",
            params={"filter": {"property": "Наш SKU", "rich_text": {"contains": sku}}},
        ).json()["results"]

        try:
            return (
                self.parse_product(data[0]).dict()
                if format == "dict"
                else self.parse_product(data[0])
            )
        except IndexError:
            return None

    def generate_sku(self, product):
        # Сгенерировать SKU на основе продукта
        # Категория.Бренд.Цена_покупки.месяц_добавления.год_добавления.случайные_4_числа

        created_at = date_parser(product["created_at"])
        sku = (
            f"{transliterate(product['category_product']).upper()}."
            f"{product['description_brand'].upper()}."
            f"{product['price_source']}."
            f"{created_at.month}."
            f"{created_at.year}."
            f"{randrange(1111, 9999)}"
        )

        return sku.replace(" ", "")

    def set_sku(self):
        # Найти товары без SKU и проставить
        for page in self.pagination(
            f"databases/{self.settings.PRODUCT_DB}/query",
            method="post",
            params={"filter": {"property": "Наш SKU", "rich_text": {"is_empty": True}}},
        ):
            for raw_product in page.json()["results"]:
                product = self.parse_product(raw_product)
                sku = self.generate_sku(product.dict())
                assert self.update_sku(
                    product.id, sku
                ), f"Не удалось обновить SKU для {raw_product['url']}"

    def update_sku(self, product_id, sku):
        _r = self.make_request(
            f"pages/{product_id}",
            method="patch",
            params={"properties": {"Наш SKU": [{"text": {"content": sku}}]}},
        )
        return _r.ok

    def update_block(self, block_id, content):
        _r = self.make_request(
            f"blocks/{block_id}",
            method="patch",
            params={"code": {"rich_text": [{"text": {"content": content}}]}},
        )
        return _r.ok

    def parse_properties(self, properties):
        result = []
        for k, v in properties.items():
            prop = properties_keys_map.get(v["id"], {})
            if not prop.get("key"):
                continue

            value_parser = properties_type_parse_map.get(
                v["type"], lambda data: str(data)
            )

            result.append(
                ProductProperties(
                    name=k,
                    value=value_parser(v),
                    key=prop.get("key"),
                    addon=prop.get("addon"),
                )
            )

        return result

    def parse_product(self, product):
        _product = Product.parse_obj(
            {
                **product,
                **{
                    "created_by": self.get_user(product["created_by"]["id"]).email,
                    "last_edited_by": self.get_user(
                        product["last_edited_by"]["id"]
                    ).email,
                    "properties": self.parse_properties(product["properties"]),
                },
            }
        )
        self.set_technical_blocks(_product)
        self.set_media_block(_product)
        return _product

    def pagination(self, url, *, params=None, **kwargs):
        _params = params or {}
        response = None
        while True:
            response = self.make_request(url, params=_params, **kwargs)
            next_cursor = self.pagination_next(response)

            match next_cursor:
                case None:
                    yield response
                case False:
                    yield response
                    return
                case _:
                    _params = {**_params, **dict(start_cursor=next_cursor)}

    def pagination_next(self, response):
        """Выдаем данные для следующего"""
        if not response:
            return None

        if not response.json().get("has_more"):
            return False

        return response.json()["next_cursor"]
