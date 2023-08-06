import inspect
from inspect import Parameter
from typing import Any, Callable, Dict, List, Optional, Type, Union, cast, get_type_hints

from pydantic import BaseModel

from chalk import MachineType
from chalk.features import Features
from chalk.features.resolver import ResolverAnnotationParser, get_state_default_value
from chalk.streams._internal import (
    StreamResolver,
    StreamResolverParam,
    StreamResolverParamKeyedState,
    StreamResolverParamMessage,
    StreamResolverSignature,
)
from chalk.streams._keyed_state import KeyedStateWrapper
from chalk.streams._types import StreamSource


def _parse_stream_resolver_param(
    param: Parameter, annotation_parser: ResolverAnnotationParser, resolver_fqn_for_errors: str
) -> StreamResolverParam:
    if param.kind not in {Parameter.KEYWORD_ONLY, Parameter.POSITIONAL_OR_KEYWORD}:
        raise ValueError(
            f"Stream resolver {resolver_fqn_for_errors} includes unsupported keyword or variadic arg '{param.name}'"
        )

    annotation = annotation_parser.parse_annotation(param.name)
    if isinstance(annotation, KeyedStateWrapper):
        default_value = get_state_default_value(
            state_typ=annotation.typ,
            declared_default=param.default,
            resolver_fqn_for_errors=resolver_fqn_for_errors,
            parameter_name_for_errors=param.name,
        )
        return StreamResolverParamKeyedState(name=param.name, typ=annotation.typ, default_value=default_value)

    if annotation in {str, bytes} or issubclass(annotation, BaseModel):
        return StreamResolverParamMessage(name=param.name, typ=annotation)

    raise ValueError(
        f"Stream resolver parameter '{param.name}' of resolver '{resolver_fqn_for_errors}' is not recognized. "
        + f"Message payloads must be one of `str`, `bytes`, or pydantic model class. "
        + f"Keyed state parameters must be chalk.streams.KeyedState[T]. "
        + f"Received: {annotation}"
    )


def parse_stream_resolver_signature(
    user_func: Callable, *, resolver_fqn_for_errors: str, annotation_parser: ResolverAnnotationParser
) -> StreamResolverSignature:
    sig = inspect.signature(user_func)
    params = [
        _parse_stream_resolver_param(p, annotation_parser, resolver_fqn_for_errors) for p in sig.parameters.values()
    ]

    uses_message_body = sum(1 for p in params if isinstance(p, StreamResolverParamMessage)) > 0
    if not uses_message_body:
        raise ValueError(
            f"Stream resolver '{resolver_fqn_for_errors}' must take as input "
            + f"a pydantic model, `str`, or `bytes` representing the message body"
        )

    keyed_state_params = [p.name for p in params if isinstance(p, StreamResolverParamKeyedState)]
    if len(keyed_state_params) > 1:
        raise ValueError(
            f"Stream resolver '{resolver_fqn_for_errors}' includes more than one KeyedState parameter: {keyed_state_params}"
        )

    return_annotation = get_type_hints(user_func)["return"]
    if not isinstance(return_annotation, type):
        raise TypeError(f"return_annotation {return_annotation} of type {type(return_annotation)} is not a type")

    if not issubclass(return_annotation, Features):
        raise ValueError(
            f"Stream resolver '{resolver_fqn_for_errors}' did not have a valid return type: "
            + f"must be a features class or chalk.features.Features[]"
        )

    # TODO: validate that these features are in the same namespace and include a pkey
    output_features = cast(Type[Features], return_annotation)

    return StreamResolverSignature(params=params, output_feature_fqns=set(f.fqn for f in output_features.features))


def _parse_and_register_stream_resolver(
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
    annotation_parser = ResolverAnnotationParser(fn, caller_globals, caller_locals)
    signature = parse_stream_resolver_signature(fn, resolver_fqn_for_errors=fqn, annotation_parser=annotation_parser)
    resolver = StreamResolver(
        filename=caller_filename,
        source=source,
        function_definition=function_definition,
        fqn=fqn,
        doc=fn.__doc__,
        fn=fn,
        environment=environment,
        machine_type=machine_type,
        signature=signature,
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
        return _parse_and_register_stream_resolver(
            caller_globals=caller_globals,
            caller_locals=caller_locals,
            fn=fn,
            source=source,
            caller_filename=caller_filename,
            environment=environment,
            machine_type=machine_type,
        )

    return decorator
