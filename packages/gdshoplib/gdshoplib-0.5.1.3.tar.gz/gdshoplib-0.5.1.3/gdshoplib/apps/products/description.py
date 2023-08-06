# Работа с описаниями товаров
from jinja2 import Environment, FileSystemLoader, select_autoescape

from gdshoplib.core import BaseManager, settings
from gdshoplib.services import NotionManager


class Description:
    def __init__(self):
        self.jinja2_env = self.jinja2_env()
        self.notion_manager = NotionManager(cache=True)

    def generate(self, product, platform):
        manager = BaseManager.get_manager(platform)(cache=True)
        return self.render(manager, product)

    def get(self, sku, platform):
        """Получить описание из Notion"""
        product = self.notion_manager.get_product(sku)
        descriptions = product.get("descriptions", {})
        if not descriptions:
            return ""

        if platform in descriptions:
            return descriptions[platform]["description"]
        return descriptions[None]["description"]

    def update(self, sku, platform=None):
        # Обновить описание продукта
        product = self.notion_manager.get_product(sku)

        if platform and product["descriptions"].get(platform):
            self.notion_manager.update_block(
                product["descriptions"].get(platform)["id"],
                self.generate(product, platform),
            )

        for k, v in product["descriptions"].items():
            new_description = self.generate(product, k)
            self.notion_manager.update_block(v["id"], new_description)

    def get_template(self, manager):
        return self.jinja2_env.get_template(manager.DESCRIPTION_TEMPLATE)

    def render(self, manager, params):
        return self.get_template(manager).render(product=params)

    @classmethod
    def jinja2_env(cls):
        return Environment(
            loader=FileSystemLoader(settings.TEMPLATES_PATH),
            autoescape=select_autoescape(),
        )
