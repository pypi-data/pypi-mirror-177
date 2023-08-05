from pydantic import BaseModel

from chalk import realtime
from chalk.features import Features, features
from chalk.streams import KafkaSource, Windowed, windowed


@features
class StreamFeaturesWindow:
    scalar_feature: Windowed[str] = windowed("10m")
    uid: str


class KafkaMessage(BaseModel):
    val_a: str


s = KafkaSource(broker=[], topic=[], message_model=KafkaMessage)


@realtime
def fn(x: StreamFeaturesWindow.scalar_feature) -> Features[StreamFeaturesWindow.uid]:
    pass


def test_window_definition():
    pass
