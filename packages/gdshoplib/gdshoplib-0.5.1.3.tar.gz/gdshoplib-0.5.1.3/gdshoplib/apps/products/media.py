from gdshoplib.packages import BaseConverter, Disk, Marker
from gdshoplib.services import NotionManager


class Media:
    def __init__(self):
        self.disk = Disk()
        self.notion_manager = NotionManager(cache=True)

    def product_update(self, sku):
        product = self.notion_manager.get_product(sku, format="model")
        self.save(product)

    def save(self, product):
        """Сохранить фотки продукта"""
        for media in product.media:
            content = media.get_content()
            self.disk.save(content, **self.disk.get_media_path(product, media))
            # self.notion_manager.set_comment(
            #     parent={"type": "page_id", "page_id": media.block_id},
            #     discussion_id=media.discussion_id,
            #     rich_text={"text": {"content": media.url, "link": {"type": "url", "url": media.url}}}
            # )
            # converter = BaseConverter.get_converter(media.type)(original)

            # converter.convert() if converter.need_convert else original
            # converter.mark() if converter.need_mark else original
