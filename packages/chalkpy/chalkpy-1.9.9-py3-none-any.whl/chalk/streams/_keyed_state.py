from typing import Any, Generic, Type, TypeVar, cast

from typing_extensions import TypeAlias

T = TypeVar("T")
TState = TypeVar("TState", bound="StateImpl")


class KeyedStateWrapper(Generic[T]):
    typ: Type[T]

    def __init__(self, typ: Type[T]):
        self.typ = typ


class KeyedStateMeta(type):
    def __getitem__(cls, item: Type[T]) -> Type[T]:
        return cast(Type[T], KeyedStateWrapper(item))  # noqa


class KeyedStateImpl(metaclass=KeyedStateMeta):
    def __new__(cls: Type[TState], *args: Any, **kwargs: Any) -> TState:
        raise RuntimeError("KeyedState should never be instantiated")


# Hack to get intellij to not complain about the type of KeyedState[...]
# This hack is compatible with vscode
KeyedState: TypeAlias = (lambda: KeyedStateImpl)()
