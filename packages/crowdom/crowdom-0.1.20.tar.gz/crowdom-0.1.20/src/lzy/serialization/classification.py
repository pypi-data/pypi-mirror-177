from dataclasses import dataclass
from typing import List, Type

from pure_protobuf.dataclasses_ import field, message, one_of, part

from ... import classification
from .base import Label, StrEnum
from .common import ProtobufSerializer


@message
@dataclass
class LabelProba(ProtobufSerializer[classification.LabelProba]):
    label: Label = field(1)
    proba: float = field(2)

    @staticmethod
    def serialize(obj: classification.LabelProba) -> 'LabelProba':
        label, proba = obj
        return LabelProba(label=Label.serialize(label), proba=proba)

    def deserialize(self) -> classification.LabelProba:
        return self.label.deserialize(), self.proba


@message
@dataclass
class TaskLabelsProbas(ProtobufSerializer[classification.TaskLabelsProbas]):
    items: List[LabelProba] = field(1, default_factory=list)

    @staticmethod
    def serialize(obj: classification.TaskLabelsProbas) -> 'TaskLabelsProbas':
        return TaskLabelsProbas(items=[LabelProba.serialize((label, proba)) for label, proba in obj.items()])

    def deserialize(self) -> classification.TaskLabelsProbas:
        return {item.label.deserialize(): item.proba for item in self.items}


@message
class AggregationAlgorithm(StrEnum[classification.AggregationAlgorithm]):
    @staticmethod
    def enum_cls() -> Type[classification.AggregationAlgorithm]:
        return classification.AggregationAlgorithm

