from __future__ import annotations
from plank.depot.storage import Storage
from typing import List, Optional

_Depot__singleton_key = "__sigleton"

class Depot:

    @classmethod
    def standard(cls) -> Depot:
        if not hasattr(cls, _Depot__singleton_key):
            instance = cls()
            setattr(cls, _Depot__singleton_key, instance)
        return getattr(cls, _Depot__singleton_key)

    @property
    def categories(self)->List[str]:
        return list(self.__categories.keys())

    def __init__(self):
        self.__storages = {}
        self.__categories = {}

    def __storage_key(self, name: str, category: str)->str:
        return f"{category}:{name}"

    def storage(self, name: str, category: str)->Optional[Storage]:
        key = self.__storage_key(name=name, category=category)
        return self.__storages.get(key)

    def storages(self, category: str)->List[Storage]:
        assert category in self.__categories.keys(), f"The category `{category}` not found. please check registered names."
        storage_names = self.__categories[category]
        return [
            self.storage(name=storage_name, category=category)
            for storage_name in storage_names
        ]

    def register_storage(self, name: str, category: str, storage:Storage):
        key = self.__storage_key(name=name, category=category)
        self.__storages[key] = storage
        storage_names = self.__categories.setdefault(category, [])
        storage_names.append(name)


