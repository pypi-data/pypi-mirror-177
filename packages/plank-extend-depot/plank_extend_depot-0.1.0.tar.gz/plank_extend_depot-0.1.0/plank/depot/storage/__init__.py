from typing import Any, NoReturn, Optional


class Storage:

    def name(self) -> Optional[str]:
        raise NotImplementedError()

    def category(self) -> Optional[str]:
        return None

    def exists(self, identifier) -> bool:
        raise NotImplementedError()

    def set_item(self, identifier: str, value: Any) -> NoReturn:
        raise NotImplementedError()

    def get_item(self, identifier: str) -> Optional[Any]:
        raise NotImplementedError()

    def __getitem__(self, identifier: str) -> Optional[Any]:
        return self.get_item(identifier)

    def __setitem__(self, identifier: str, value: Any):
        return self.set_item(identifier, value)

    def sample(self, n: int):
        raise NotImplementedError()

    def export(self, export_path: str):
        raise NotImplementedError()
