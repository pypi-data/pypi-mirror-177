from gdshoplib.core.manager.basemanager import BaseManager
from gdshoplib.services.vk.settings import Settings


class InstagramManager(BaseManager):
    DESCRIPTION_TEMPLATE = "instagram.txt"
    KEY = "INSTAGRAM"
    SETTINGS = Settings
