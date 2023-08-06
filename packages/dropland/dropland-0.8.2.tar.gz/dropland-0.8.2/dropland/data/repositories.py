from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, Dict, Generic, Optional, Sequence, Tuple, Type, TypeVar, Union

from .entities import Entity
from .models.base import ModelProtocol
from .models.model import UpdateSchemaType
from .models.sql import SqlModel

EntityType = TypeVar('EntityType', bound=Entity, covariant=True)
ModelType = TypeVar('ModelType', bound=ModelProtocol, covariant=True)
SqlModelType = TypeVar('SqlModelType', bound=SqlModel, covariant=True)
ModelTypeFactory = Callable[[...], ModelType]
SqlModelTypeFactory = Callable[[...], SqlModelType]


class Repository(Generic[EntityType], ABC):
    @abstractmethod
    def __call__(self, *args, **kwargs) -> Union[EntityType, Awaitable[EntityType]]:
        ...

    @abstractmethod
    async def get(self, id_value: Any, **kwargs) -> Optional[EntityType]:
        ...

    @abstractmethod
    async def get_any(self, indices: Sequence[Any], **kwargs) -> Sequence[Optional[EntityType]]:
        ...

    @abstractmethod
    async def exists(self, id_value: Any, **kwargs) -> bool:
        ...

    @abstractmethod
    async def create(self, data: Any, **kwargs) -> Optional[EntityType]:
        ...

    @abstractmethod
    async def get_or_create(self, id_value: Any, data: Any, **kwargs) -> Tuple[Optional[EntityType], bool]:
        ...

    @abstractmethod
    async def update_by_id(self, id_value: Any, data: Any) -> bool:
        ...

    @abstractmethod
    async def save_all(self, objects: Sequence[EntityType], *args, **kwargs) -> bool:
        ...

    @abstractmethod
    async def delete_all(self, indices: Sequence[Any] = None) -> bool:
        ...


class ModelRepository(Repository[ModelType]):
    def __init__(self, model_class: Type[ModelType], model_factory: Optional[ModelTypeFactory] = None):
        self._model_class = model_class
        self._model_factory = model_factory or model_class

    def __call__(self, *args, **kwargs) -> Union[ModelType, Awaitable[ModelType]]:
        return self._model_factory(*args, **kwargs)

    @property
    def model_class(self):
        return self._model_class

    #
    # Retrieve operations
    #

    async def get(self, id_value: Any, **kwargs) -> Optional[ModelType]:
        return await self._model_class.get(id_value, **kwargs)

    async def get_any(self, indices: Sequence[Any], **kwargs) -> Sequence[Optional[ModelType]]:
        return await self._model_class.get_any(indices, **kwargs)

    async def exists(self, id_value: Any, **kwargs) -> bool:
        return await self._model_class.exists(id_value, **kwargs)

    #
    # Modification operations
    #

    async def create(self, data: Any, **kwargs) -> Optional[ModelType]:
        return await self._model_class.create(data, **kwargs)

    async def get_or_create(self, id_value: Any, data: Any, **kwargs) -> Tuple[Optional[ModelType], bool]:
        return await self._model_class.get_or_create(id_value, data, **kwargs)

    async def update_by_id(self, id_value: Any, data: Any) -> bool:
        return await self._model_class.update_by_id(id_value, data)

    async def save_all(self, objects: Sequence[ModelType], *args, **kwargs) -> bool:
        return await self._model_class.save_all(objects, *args, **kwargs)

    async def delete_all(self, indices: Sequence[Any] = None) -> bool:
        return await self._model_class.delete_all(indices)


class SqlModelRepository(ModelRepository[SqlModelType]):
    def __init__(self, model_class: Type[SqlModelType], model_factory: Optional[SqlModelTypeFactory] = None):
        super(SqlModelRepository, self).__init__(model_class, model_factory)

    async def list(
        self, filters: Optional[Sequence[Any]] = None, sorting: Optional[Sequence[Any]] = None,
            skip: int = 0, limit: int = 0, params: Dict[str, Any] = None, **kwargs) -> Sequence[SqlModelType]:
        return await self._model_class.list(filters, sorting, skip, limit, params, **kwargs)

    async def count(self, filters: Optional[Sequence[Any]] = None, params: Dict[str, Any] = None, **kwargs) -> int:
        return await self._model_class.count(filters, params, **kwargs)

    async def exists_by(self, filters: Sequence[Any], params: Dict[str, Any] = None, **kwargs) -> bool:
        return await self._model_class.exists_by(filters, params, **kwargs)

    async def update_by(self, filters: Sequence[Any],
                        data: Union[UpdateSchemaType, Dict[str, Any]],
                        /, params: Dict[str, Any] = None, **kwargs) -> int:
        return await self._model_class.update_by(filters, data, params, **kwargs)

    async def delete_by(self, filters: Sequence[Any], /, params: Dict[str, Any] = None, **kwargs) -> int:
        return await self._model_class.delete_by(filters, params, **kwargs)
