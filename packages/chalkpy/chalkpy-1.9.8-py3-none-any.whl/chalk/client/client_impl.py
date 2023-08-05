from __future__ import annotations

import enum
import logging
from datetime import datetime
from itertools import chain
from typing import Any, Dict, Iterator, List, Mapping, Optional, Sequence, Tuple, Type, TypeVar, Union
from urllib.parse import urljoin

import polars as pl
import requests
from pydantic import BaseModel, ValidationError
from requests import HTTPError

from chalk.client.client_protocol import (
    ChalkAPIClientProtocol,
    ChalkBaseException,
    ChalkError,
    FeatureResult,
    OfflineQueryContext,
    OnlineQueryContext,
    OnlineQueryResponse,
    ResolverRunResponse,
    WhoAmIResponse,
)
from chalk.config.auth_config import load_token
from chalk.features import DataFrame, Feature, Features, FeatureWrapper, unwrap_feature
from chalk.features.pseudofeatures import CHALK_TS_FEATURE
from chalk.serialization.codec import FEATURE_CODEC

_logger = logging.getLogger(__name__)

import pandas as pd


class _ExchangeCredentialsRequest(BaseModel):
    client_id: str
    client_secret: str
    grant_type: str


class _ExchangeCredentialsResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    engines: Optional[Mapping[str, str]] = None


class _OfflineQueryResponse(BaseModel):
    columns: List[str]
    output: List[List[Any]]
    errors: Optional[List[ChalkError]]


class _OfflineQueryInput(BaseModel):
    columns: List[str]
    values: List[List[Any]]


class _OfflineQueryRequest(BaseModel):
    output: List[str]
    input: Optional[_OfflineQueryInput] = None
    dataset: Optional[str] = None
    max_samples: Optional[int] = None


class _QueryRequest(BaseModel):
    inputs: Mapping[str, Any]
    outputs: List[str]
    staleness: Optional[Mapping[str, str]] = None
    context: Optional[OnlineQueryContext]
    deployment_id: Optional[str] = None
    correlation_id: Optional[str] = None
    query_name: Optional[str] = None
    meta: Optional[Mapping[str, str]] = None


class _TriggerResolverRunRequest(BaseModel):
    resolver_fqn: str


class _GetRunStatusRequest(BaseModel):
    run_id: str


T = TypeVar("T")


class _ChalkClientConfig(BaseModel):
    client_id: str
    client_secret: str
    api_server: str
    active_environment: Optional[str]


class _OnlineQueryResponse(BaseModel):
    data: List[FeatureResult]
    errors: Optional[List[ChalkError]]


class ChalkConfigurationException(ChalkBaseException):
    message: str

    def __init__(self, message: str):
        super().__init__(message)

    @classmethod
    def missing_dependency(cls, name: str):
        return cls(f"Missing pip dependency '{name}'. Please add this to your requirements.txt file and pip install.")


class ChalkOfflineQueryException(ChalkBaseException):
    message: str
    errors: List[ChalkError]

    def __init__(self, message: str, errors: List[ChalkError]):
        self.message = message
        self.errors = errors
        super().__init__(message + "\n" + "\n".join(["\t" + e.message for e in errors[0:3]]))


class ChalkResolverRunException(ChalkBaseException):
    message: str

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class OnlineQueryResponseWrapper(OnlineQueryResponse):
    data: List[FeatureResult]
    errors: Optional[List[ChalkError]]

    def __init__(
        self,
        data: List[FeatureResult],
        errors: Optional[List[ChalkError]],
    ):
        self.data = data
        self.errors = errors
        for d in self.data:
            if d.value is not None:
                d.value = FEATURE_CODEC.decode_fqn(d.field, d.value)
        self._values = {d.field: d for d in self.data}

    def get_feature(self, feature: Any) -> Optional[FeatureResult]:
        # Typing `feature` as Any, as the Features will be typed as the underlying datatypes, not as Feature
        return self._values.get(_get_feature_root_fqn(feature))

    def get_feature_value(self, feature: Any) -> Optional[Any]:
        # Typing `feature` as Any, as the Features will be typed as the underlying datatypes, not as Feature
        v = self.get_feature(feature)
        return v and v.value


def _get_feature_root_fqn(feat: Union[str, Feature, FeatureWrapper, Any]) -> str:
    if isinstance(feat, str):
        return feat
    elif isinstance(feat, FeatureWrapper):
        return unwrap_feature(feat).root_fqn
    elif isinstance(feat, Feature):
        return feat.root_fqn
    raise ValueError(f"Reference must be to a leaf feature. Received '{feat}'")


def _expand_scalar_features_shallow(fs: Sequence[Any]) -> Iterator[str]:
    for o in fs:
        if isinstance(o, str):
            yield o
        if isinstance(o, type) and issubclass(o, Features):
            for f in o.features:
                if f.is_scalar:
                    yield f.root_fqn
        if isinstance(o, FeatureWrapper):
            o = unwrap_feature(o)

        if isinstance(o, Feature) and o.is_scalar:
            yield o.root_fqn
        elif isinstance(o, Feature) and o.is_has_one:
            assert o.joined_class is not None
            for f in o.joined_class.features:
                if isinstance(f, Feature) and f.is_scalar:
                    yield f"{o.root_fqn}.{f.name}"


class ChalkAPIClientImpl(ChalkAPIClientProtocol):
    _headers: Optional[Tuple[Dict[str, str], Optional[Mapping[str, str]]]]
    _config: _ChalkClientConfig

    def __init__(
        self,
        *,
        client_id: Optional[str],
        client_secret: Optional[str],
        environment: Optional[str],
        api_server: Optional[str],
    ):
        if client_id is not None and client_secret is not None:
            self._config = _ChalkClientConfig(
                client_id=client_id,
                client_secret=client_secret,
                api_server=api_server or "https://api.chalk.ai",
                active_environment=environment,
            )
        else:
            token = load_token()
            if token is None:
                raise ValueError(
                    (
                        "Could not find .chalk.yml config file for project, "
                        "and explicit configuration was not provided. "
                        "You may need to run `chalk login` from your command line, "
                        "or check that your working directory is set to the root of "
                        "your project."
                    )
                )
            self._config = _ChalkClientConfig(
                client_id=token.clientId,
                client_secret=token.clientSecret,
                api_server=api_server or token.apiServer or "https://api.chalk.ai",
                active_environment=environment or token.activeEnvironment,
            )

        self._headers = None

    def _exchange_credentials(self) -> _ExchangeCredentialsResponse:
        resp = requests.post(
            url=urljoin(self._config.api_server, f"v1/oauth/token"),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            json=_ExchangeCredentialsRequest(
                client_id=self._config.client_id,
                client_secret=self._config.client_secret,
                grant_type="client_credentials",
            ).dict(),
            timeout=10,
        )
        response_json = resp.json()
        try:
            return _ExchangeCredentialsResponse(**response_json)
        except ValidationError:
            raise HTTPError(response_json)

    def _get_headers(self, environment_override: Optional[str], bust_cache: bool = False):
        if not bust_cache and self._headers is not None:
            _logger.debug("Returning cached authorization headers")
            return self._headers

        _logger.debug("Performing a credentials exchange")
        creds = self._exchange_credentials()
        x_chalk_env_id = environment_override or self._config.active_environment
        headers: Dict[str, str] = {
            "Authorization": f"Bearer {creds.access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if x_chalk_env_id is not None:
            headers["X-Chalk-Env-Id"] = x_chalk_env_id

        self._headers = (
            headers,
            creds.engines or {},
        )

        return self._headers

    def _request(
        self,
        method: str,
        uri: str,
        response: Type[T],
        json: Optional[BaseModel] = None,
        use_engine: bool = False,
        environment_override: Optional[str] = None,
    ) -> T:
        x = self._get_headers(environment_override=environment_override)
        headers, engines = x
        active_env = environment_override or self._config.active_environment
        if use_engine and engines is not None and active_env in engines:
            assert isinstance(active_env, str)
            base = engines[active_env]
        else:
            base = self._config.api_server
        url = urljoin(base, uri)
        json_body = json and json.dict()
        r = requests.request(method=method, headers=headers, url=url, json=json_body)
        if r.status_code == 401:
            headers, _ = self._get_headers(environment_override=environment_override, bust_cache=True)
            r = requests.request(method=method, headers=headers, url=url, json=json_body)

        r.raise_for_status()
        return response(**r.json())

    def whoami(self) -> WhoAmIResponse:
        return self._request(method="GET", uri=f"/v1/who-am-i", response=WhoAmIResponse)

    def upload_features(
        self,
        input: Mapping[Union[str, Feature, Any], Any],
        context: Optional[OnlineQueryContext] = None,
        preview_deployment_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        query_name: Optional[str] = None,
        meta: Optional[Mapping[str, str]] = None,
    ) -> Optional[List[ChalkError]]:
        return self.query(
            input=input,
            output=list(input.keys()),
            staleness=None,
            context=context,
            preview_deployment_id=preview_deployment_id,
            correlation_id=correlation_id,
            query_name=query_name,
            meta=meta,
        ).errors

    def query(
        self,
        input: Mapping[Union[str, Feature, FeatureWrapper, Any], Any],
        output: List[Union[str, Feature, Any]],
        staleness: Optional[Mapping[Union[str, Feature, Any], str]] = None,
        context: Optional[OnlineQueryContext] = None,
        preview_deployment_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        query_name: Optional[str] = None,
        meta: Optional[Mapping[str, str]] = None,
    ) -> OnlineQueryResponse:
        encoded_inputs = {}
        for feature, value in input.items():
            fqn = _get_feature_root_fqn(feature)
            encoded_inputs[fqn] = FEATURE_CODEC.encode_fqn(fqn, value)

        request = _QueryRequest(
            inputs=encoded_inputs,
            outputs=list(_expand_scalar_features_shallow(output)),
            staleness=staleness and {_get_feature_root_fqn(k): v for k, v in staleness.items()},
            context=context,
            deployment_id=preview_deployment_id,
            correlation_id=correlation_id,
            query_name=query_name,
            meta=meta,
        )

        resp = self._request(
            method="POST",
            uri="/v1/query/online",
            json=request,
            response=_OnlineQueryResponse,
            use_engine=preview_deployment_id is None,
            environment_override=context.environment if context else None,
        )
        return OnlineQueryResponseWrapper(
            data=resp.data,
            errors=resp.errors,
        )

    def get_training_dataframe(
        self,
        input: Union[Mapping[Union[str, Feature], Any], pl.DataFrame, pd.DataFrame, DataFrame],
        input_times: List[datetime],
        output: List[Union[str, Feature, Any]],
        context: Optional[OfflineQueryContext] = None,
        dataset: Optional[str] = None,
        branch: Optional[str] = None,
    ) -> pd.DataFrame:
        if not isinstance(input, DataFrame):
            input = DataFrame(input)

        self._get_headers(environment_override=None)

        return self._get_training_dataframe(
            input=input.to_pandas(),
            input_times=input_times,
            output=output,
            context=context,
            dataset=dataset,
        )

    def _decode_offline_response(self, offline_query_response: _OfflineQueryResponse) -> pd.DataFrame:
        data = {}
        for col_index, column in enumerate(offline_query_response.output):
            series_values = []
            for value in column:
                value = FEATURE_CODEC.decode_fqn(
                    fqn=offline_query_response.columns[col_index],
                    value=value,
                )
                if isinstance(value, enum.Enum):
                    value = value.value
                series_values.append(value)

            data[offline_query_response.columns[col_index]] = pd.Series(
                data=series_values,
                dtype=FEATURE_CODEC.get_pandas_dtype(offline_query_response.columns[col_index]),
            )
        return pd.DataFrame(data)

    def _get_training_dataframe(
        self,
        input: pd.DataFrame,
        input_times: List[datetime],
        output: List[Union[str, Feature, Any]],
        context: Optional[OfflineQueryContext] = None,
        dataset: Optional[str] = None,
    ) -> pd.DataFrame:
        columns = input.columns
        matrix = input.T.values.tolist()

        columns_fqn = [_get_feature_root_fqn(c) for c in chain(columns, (CHALK_TS_FEATURE,))]

        matrix.append([a for a in input_times])

        for col_index, column in enumerate(matrix):
            for row_index, value in enumerate(column):
                matrix[col_index][row_index] = FEATURE_CODEC.encode_fqn(
                    fqn=columns_fqn[col_index],
                    value=value,
                )

        request = _OfflineQueryRequest(
            input=_OfflineQueryInput(
                columns=columns_fqn,
                values=matrix,
            ),
            output=list(_expand_scalar_features_shallow(output)),
            dataset=dataset,
        )

        response = self._request(
            method="POST",
            uri="/v1/query/offline",
            json=request,
            response=_OfflineQueryResponse,
            use_engine=True,
            environment_override=context and context.environment,
        )

        if response.errors is not None and len(response.errors) > 0:
            raise ChalkOfflineQueryException(message="Failed while processing training query", errors=response.errors)

        return self._decode_offline_response(response)

    def sample(
        self,
        output: list[Union[str, Feature, Any]],
        max_samples: Optional[int] = None,
        context: Optional[OfflineQueryContext] = None,
    ) -> pd.DataFrame:
        self.request = _OfflineQueryRequest(
            output=list(_expand_scalar_features_shallow(output)),
            max_samples=max_samples,
        )

        response = self._request(
            method="POST",
            uri="/v1/query/offline",
            json=self.request,
            response=_OfflineQueryResponse,
            use_engine=True,
            environment_override=context and context.environment,
        )

        if response.errors is not None and len(response.errors) > 0:
            raise ChalkOfflineQueryException(message="Failed while processing sample query", errors=response.errors)

        return self._decode_offline_response(response)

    def trigger_resolver_run(
        self,
        resolver_fqn: str,
        deployment_id: Optional[str] = None,
    ) -> ResolverRunResponse:
        _logger.debug(f'Triggering resolver {resolver_fqn} to run with deployment ID "{deployment_id}"')

        request = _TriggerResolverRunRequest(resolver_fqn=resolver_fqn)
        try:
            response = self._request(
                method="POST",
                uri="/v1/runs/trigger",
                json=request,
                response=ResolverRunResponse,
            )
        except HTTPError as e:
            message = str(e)

            detail = e.response.json().get("detail")
            if detail is not None:
                message = detail

            raise ChalkResolverRunException(message=message)

        return response

    def get_run_status(self, run_id: str) -> ResolverRunResponse:
        try:
            response = self._request(
                method="GET",
                uri=f"/v1/runs/{run_id}",
                response=ResolverRunResponse,
            )
        except HTTPError as e:
            message = str(e)

            detail = e.response.json().get("detail")
            if detail is not None:
                message = detail

            raise ChalkResolverRunException(message=message)

        return response
