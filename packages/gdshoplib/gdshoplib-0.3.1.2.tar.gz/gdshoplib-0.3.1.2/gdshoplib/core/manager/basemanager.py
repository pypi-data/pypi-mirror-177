import datetime
import functools
import logging
import requests as r


logger = logging.getLogger(__name__)


class BaseManager:
    CACHE = {}
    DESCRIPTION_TEMPLATE = "basic.txt"
    KEY = None

    def __init__(self, cache=False, cache_period=20) -> None:
        self.cache = cache
        self.cache_period = cache_period
        self.settings = self.SETTINGS()

    @classmethod
    def get_platform_keys(cls):
        return [
            manager.KEY.upper() if manager.KEY else None
            for manager in cls.get_managers()
        ]

    @classmethod
    def get_managers(cls):
        return [manager for manager in cls.__subclasses__()]

    @classmethod
    def get_manager(cls, key):
        for manager in cls.get_managers():
            if (key is None and manager.KEY is key) or (
                key and manager.KEY == key.upper()
            ):
                return manager
        assert False, f"Менеджер по ключу {key} не найден"

    def get_cache_key(self, path, **kwargs):
        return f"{path}"

    def check_cacheble(self, *args, **kwargs):
        return kwargs.get("method").upper() == "GET"

    def auth(self):
        raise NotImplementedError

    def pagination(self, url, *, params=None, **kwargs):
        raise NotImplementedError

    def pagination_next(self, response):
        raise NotImplementedError

    def cache_response(func):
        @functools.wraps(func)
        def wrap(self, *args, **kwargs):
            if self.cache and self.check_cacheble(*args, **kwargs):
                cache_key = self.get_cache_key(*args, **kwargs)
                cached = self.CACHE.get(cache_key)

                if cached and cached["time"] > datetime.datetime.now():
                    cached["time"] += datetime.timedelta(seconds=self.cache_period)
                    return cached["data"]

                self.CACHE[cache_key] = {
                    "data": func(self, *args, **kwargs),
                    "time": datetime.datetime.now()
                    + datetime.timedelta(seconds=self.cache_period),
                }

                return self.CACHE[cache_key]["data"]
            return func(self, *args, **kwargs)

        return wrap

    @cache_response
    def make_request(self, path, *, method, params=None):
        _path = f"{self.BASE_URL}{path}"
        _params = (
            dict(params=params) or {}
            if method.upper() == "GET"
            else dict(json=params) or {}
        )

        _r = r.request(
            method,
            _path,
            headers=self.get_headers(),
            **_params,
        )
        if not _r.ok:
            logger.warning(_r.json())
            assert (
                False
            ), f"Запрос {method.upper()} {_path} прошел с ошибкой {_r.status_code}/n"
        return _r
