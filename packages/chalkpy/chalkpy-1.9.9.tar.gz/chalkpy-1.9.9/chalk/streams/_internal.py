from typing import Any, Callable, List, Optional, Sequence, Set, Type, Union

from pydantic import BaseModel

from chalk import MachineType
from chalk.streams._types import StreamSource


class StreamResolverParam(BaseModel):
    name: str


class StreamResolverParamMessage(StreamResolverParam):
    typ: Union[Type[str], Type[bytes], Type[BaseModel]]


AnyDataclass = Any


class StreamResolverParamKeyedState(StreamResolverParam):
    typ: Union[Type[BaseModel], Type[AnyDataclass]]
    default_value: Any


class StreamResolverSignature(BaseModel):
    params: Sequence[StreamResolverParam]
    output_feature_fqns: Set[str]


class StreamResolver:
    registry: "List[StreamResolver]" = []

    def __init__(
        self,
        function_definition: str,
        fqn: str,
        filename: str,
        doc: Optional[str],
        source: StreamSource,
        fn: Callable,
        signature: StreamResolverSignature,
        environment: Optional[Union[List[str], str]],
        machine_type: Optional[MachineType],
    ):
        super(StreamResolver, self).__init__()
        self.function_definition = function_definition
        self.fqn = fqn
        self.filename = filename
        self.source = source
        self.fn = fn
        self.environment = environment
        self.doc = doc
        self.machine_type = machine_type
        self.signature = signature

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)

    def __repr__(self):
        return f"StreamResolver(name={self.fqn})"
