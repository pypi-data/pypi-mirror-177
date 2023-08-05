from typing import Any, Callable, List, Optional, Type, Union

from pydantic import BaseModel

from chalk import MachineType
from chalk.features import Features


class StreamSource:
    message_model: Union[Type[Any], None] = None

    def config_to_json(self) -> Any:
        ...


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
        model: Union[BaseModel, None],
        output_features: Type[Features],
        environment: Optional[Union[List[str], str]],
        machine_type: Optional[MachineType],
    ):
        super(StreamResolver, self).__init__()
        self.function_definition = function_definition
        self.fqn = fqn
        self.filename = filename
        self.source = source
        self.fn = fn
        self.model = model
        self.environment = environment
        self.doc = doc
        self.machine_type = machine_type
        self.output_features = output_features

    def __eq__(self, other):
        return isinstance(other, StreamResolver) and self.fqn == other.fqn

    def __hash__(self):
        return hash(self.fqn)

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)

    def __repr__(self):
        return f"StreamResolver(name={self.fqn})"
