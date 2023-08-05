import inspect
from typing import Any, Callable, Dict, List, Optional, Union, get_type_hints

from pydantic import BaseModel

from chalk import MachineType
from chalk.features import Features
from chalk.features.resolver import ResolverAnnotationParser
from chalk.streams._types import StreamResolver, StreamSource


def _parse_stream_resolver(
    *,
    caller_globals: Optional[Dict[str, Any]],
    caller_locals: Optional[Dict[str, Any]],
    fn: Callable,
    source: StreamSource,
    caller_filename: str,
    environment: Optional[Union[List[str], str]] = None,
    machine_type: Optional[MachineType] = None,
) -> StreamResolver:
    fqn = f"{fn.__module__}.{fn.__name__}"
    function_definition = inspect.getsource(fn)
    signature = inspect.signature(fn)
    annotation_parser = ResolverAnnotationParser(fn, caller_globals, caller_locals)
    inputs = [annotation_parser.parse_annotation(p) for p in signature.parameters.keys()]
    if len(inputs) == 0:
        raise TypeError(f"Stream resolver '{fqn}' must take as input the str or Pydantic model representing a message.")

    if not issubclass(inputs[0], (BaseModel, str)):
        raise TypeError(
            f"Stream resolver '{fqn}' must take as the first input the str or Pydantic model representing a message."
        )

    input_type = inputs[0]
    return_annotation = get_type_hints(fn)["return"]

    if not isinstance(return_annotation, type):
        raise TypeError(f"return_annotation {return_annotation} of type {type(return_annotation)} is not a type")
    if not issubclass(return_annotation, Features):
        raise ValueError(f"Stream resolver '{fqn}' did not have a valid return type: must be Features[]")

    # function annotated like def get_account_id(user_id: User.id) -> Features[User.account_id]
    # or def get_account_id(user_id: User.id) -> User:
    output_features = return_annotation
    resolver = StreamResolver(
        filename=caller_filename,
        source=source,
        function_definition=function_definition,
        fqn=fqn,
        doc=fn.__doc__,
        fn=fn,
        model=input_type if isinstance(input_type, BaseModel) else None,
        output_features=output_features,
        environment=environment,
        machine_type=machine_type,
    )

    StreamResolver.registry.append(resolver)
    return resolver


def stream(
    *,
    source: StreamSource,
    environment: Optional[Union[List[str], str]] = None,
    machine_type: Optional[MachineType] = None,
):
    caller_frame = inspect.stack()[1]
    caller_filename = caller_frame.filename
    caller_globals = caller_frame.frame.f_globals
    caller_locals = caller_frame.frame.f_locals

    def decorator(fn: Callable):
        return _parse_stream_resolver(
            caller_globals=caller_globals,
            caller_locals=caller_locals,
            fn=fn,
            source=source,
            caller_filename=caller_filename,
            environment=environment,
            machine_type=machine_type,
        )

    return decorator
