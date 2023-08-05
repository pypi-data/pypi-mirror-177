import dataclasses

from pydantic import BaseModel

from chalk import State
from chalk.features import Features, features
from chalk.streams import KafkaSource, stream


@features
class StreamFeatures:
    scalar_feature: str


class KafkaMessage(BaseModel):
    val_a: str


s = KafkaSource(broker=[], topic=[], message_model=KafkaMessage)


@dataclasses.dataclass
class MyState:
    a: int = 4


@stream(source=s)
def fn(message: KafkaMessage, s: State[MyState]) -> Features[StreamFeatures.scalar_feature]:
    return StreamFeatures(
        scalar_feature=message.val_a,
    )


def test_callable():
    assert fn(KafkaMessage(val_a="hello"), MyState()) == StreamFeatures(scalar_feature="hello")


def test_parsed_source():
    assert fn.source == s
