import json
from pathlib import Path
from typing import Dict, List, Iterable, Any, NoReturn, Optional

import ndjson
import pandas as pd
from plank.depot.storage import Storage


class DataFrameStorage(Storage):

    @property
    def keys_indexing(self) -> Dict[str, int]:
        return self._keys_indexing

    @classmethod
    def from_records(cls, data: Iterable[dict], columns: List[str], key_column: str = None, name: Optional[str] = None,
                     category: Optional[str] = None):
        key_column = key_column or columns[0]
        records = map(lambda item_dict: {column: item_dict[column] for column in columns}, data)
        pd_dataframe = pd.DataFrame.from_records(records)
        return cls(dataframe=pd_dataframe, columns=columns, key_column=key_column, name=name, category=category)

    @classmethod
    def from_ndjson(cls, filepath: str, columns: List[str] = None, key_column: str = None, name: Optional[str] = None,
                    category: Optional[str] = None):
        filepath = Path(filepath)
        if not filepath.is_file() or not filepath.exists():
            raise FileNotFoundError

        with open(filepath, "r+") as fp:
            reader = ndjson.reader(fp)
            data = [d for d in reader]
            return cls.from_records(data, columns=columns, key_column=key_column, name=name, category=category)

    @classmethod
    def from_json(cls, filepath: str, columns: List[str] = None, key_column: str = None, name: Optional[str] = None,
                  category: Optional[str] = None):
        filepath = Path(filepath)
        if not filepath.is_file() or not filepath.exists():
            raise FileNotFoundError

        with open(filepath, "r+") as fp:
            dicts = json.load(fp=fp)
            return cls.from_records(dicts, columns=columns, key_column=key_column, name=name, category=category)

    @classmethod
    def from_hdf5(cls, filepath: str, columns: List[str] = None, key_column: str = None, name: Optional[str] = None,
                  category: Optional[str] = None):
        dataframe = pd.read_hdf(filepath)
        return cls(dataframe=dataframe, columns=columns, key_column=key_column, name=name, category=category)

    @property
    def dataframe(self):
        return self._dataframe

    @property
    def columns(self):
        return self._columns

    def __init__(self, dataframe: pd.DataFrame, columns: List[str], key_column: str, name: Optional[str] = None,
                 category: Optional[str] = None):
        self.__name = name
        self.__category = category
        self._dataframe = dataframe
        self._key_column = key_column
        self._columns = columns
        self._keys_indexing = dict([(item[1], item[0]) for item in self._dataframe.identifier.to_dict().items()])
        self._records = self._dataframe.to_records(index=False)

    async def get_item(self, identifier: str, default=None) -> Optional[dict]:
        if identifier in self.keys_indexing:
            return dict(zip(self._columns, self._records[self.keys_indexing[identifier]]))
        else:
            return default

    def set_item(self, identifier: str, value: Dict[str, Any]) -> NoReturn:
        value[self._key_column] = identifier
        self._dataframe = self.dataframe.append(value, ignore_index=True)

    def exists(self, identifier) -> bool:
        return identifier in self._keys_indexing

    def export(self, export_path: str):
        self._dataframe.to_hdf(export_path, key=self._key_column)

    def drop_duplicates(self, subset: str = None):
        subset = subset or self._key_column
        self._dataframe = self._dataframe.drop_duplicates(subset=subset)

    def sample(self, n: int):
        sampled_records = self._dataframe.sample(n) \
            .reset_index(drop=True) \
            .to_records(index=False)
        return map(lambda values: dict(zip(self._columns, values)), sampled_records)

    def name(self) -> Optional[str]:
        return self.__name

    def category(self) -> Optional[str]:
        return self.__category
