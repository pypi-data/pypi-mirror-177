from typing import Any, Optional, Protocol, Sequence, TYPE_CHECKING, Tuple, Union

if TYPE_CHECKING:
    from dropland.engines.base import AsyncEngine, SyncEngine


class ModelProtocol(Protocol):
    def get_id_value(self) -> Any:
        ...

    @classmethod
    def get_engine(cls) -> Union['SyncEngine', 'AsyncEngine']:
        ...

    #
    # Retrieve operations
    #

    @classmethod
    async def get(cls, id_value: Any, **kwargs) -> Optional['ModelProtocol']:
        ...

    @classmethod
    async def get_any(cls, indices: Sequence[Any], **kwargs) -> Sequence[Optional['ModelProtocol']]:
        ...

    @classmethod
    async def exists(cls, id_value: Any, **kwargs) -> bool:
        ...

    #
    # Modification operations
    #

    @classmethod
    async def create(cls, data: Any, **kwargs) -> Optional['ModelProtocol']:
        ...

    @classmethod
    async def get_or_create(cls, id_value: Any, data: Any, **kwargs) -> Tuple[Optional['ModelProtocol'], bool]:
        ...

    async def update(self, data: Any) -> bool:
        ...

    @classmethod
    async def update_by_id(cls, id_value: Any, data: Any) -> bool:
        ...

    async def save(self, *args, **kwargs) -> bool:
        ...

    async def load(self, field_names: Sequence[str] = None) -> bool:
        ...

    @classmethod
    async def save_all(cls, objects: Sequence['ModelProtocol'], *args, **kwargs) -> bool:
        ...

    async def delete(self) -> bool:
        ...

    @classmethod
    async def delete_all(cls, indices: Sequence[Any] = None) -> bool:
        ...

    @classmethod
    async def delete_by_id(cls, id_value: Any) -> bool:
        ...
