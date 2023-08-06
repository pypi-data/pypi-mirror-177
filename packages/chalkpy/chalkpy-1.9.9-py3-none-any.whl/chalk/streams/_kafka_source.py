from typing import Any, List, Literal, Optional, Union

from pydantic import BaseModel

from chalk.streams._types import StreamSource


class KafkaSource(StreamSource, BaseModel):
    bootstrap_server: Union[str, List[str]]
    topic: Union[str, List[str]]
    ssl_keystore_location: Optional[str] = None
    client_id_prefix: str = "chalk/"
    group_id_prefix: str = "chalk/"

    security_protocol: Literal["PLAINTEXT", "SSL", "SASL_PLAINTEXT", "SASL_SSL"] = "PLAINTEXT"
    """
    Protocol used to communicate with brokers.
            Valid values are: PLAINTEXT, SSL, SASL_PLAINTEXT, SASL_SSL.
            Default: PLAINTEXT.
    """

    sasl_mechanism: Literal["PLAIN", "GSAPI", "SCRAM-SHA-256", "SCRAM-SHA-512"] = "PLAIN"
    """
    Authentication mechanism when security_protocol
            is configured for SASL_PLAINTEXT or SASL_SSL. Valid values are:
            PLAIN, GSSAPI, SCRAM-SHA-256, SCRAM-SHA-512, OAUTHBEARER.
            Default: PLAIN
    """

    sasl_username: Optional[str] = None
    """
    username for sasl PLAIN, SCRAM-SHA-256, or SCRAM-SHA-512 authentication.
            Default: None
    """

    sasl_password: Optional[str] = None
    """
    password for sasl PLAIN, SCRAM-SHA-256, or SCRAM-SHA-512 authentication.
            Default: None
    """

    def config_to_json(self) -> Any:
        return self.json()
