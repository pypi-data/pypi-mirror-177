from typing import Any, Generic, Type, TypeVar, cast

from typing_extensions import TypeAlias

T = TypeVar("T")
TState = TypeVar("TState", bound="StateImpl")


class StateWrapper(Generic[T]):
    typ: Type[T]

    def __init__(self, typ: Type[T]):
        self.typ = typ


class StateMeta(type):
    def __getitem__(cls, item: Type[T]) -> Type[T]:
        return cast(Type[T], StateWrapper(item))  # noqa


class StateImpl(metaclass=StateMeta):
    def __new__(cls: Type[TState], *args: Any, **kwargs: Any) -> TState:
        raise RuntimeError("State should never be instantiated")


# Hack to get intellij to not complain about the type of State[...]
# This hack is compatible with vscode
State: TypeAlias = (lambda: StateImpl)()
