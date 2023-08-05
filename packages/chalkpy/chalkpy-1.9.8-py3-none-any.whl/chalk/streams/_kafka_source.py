from typing import List, Optional, Union

from pydantic import BaseModel

from chalk.streams._types import StreamSource


class KafkaSource(BaseModel, StreamSource):
    broker: Union[str, List[str]]
    topic: Union[str, List[str]]
    ssl_keystore_location: Optional[str] = None
    client_id_prefix: Optional[str] = None
    group_id_prefix: Optional[str] = None
    topic_metadata_refresh_interval_ms: Optional[int] = None
    security_protocol: Optional[str] = None

    def config_to_json(self):
        return self.json(exclude={"message_model"})
