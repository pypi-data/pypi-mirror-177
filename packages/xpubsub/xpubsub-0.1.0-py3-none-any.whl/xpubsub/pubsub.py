from typing import Hashable, Union, Iterable, Callable, Any
from enum import Enum, auto

# from icecream import ic

HashOrList = Union[Hashable, list[Hashable]]


class Alerts(Enum):
    ADD = auto()
    ALL = auto()
    NEW = auto()
    REMOVE = auto()
    SEND = auto()


def fix(topic_list: HashOrList) -> list[Hashable]:
    if isinstance(topic_list, list):
        return topic_list
    return [topic_list]


class PubSub:
    def __init__(self) -> None:
        self.__topics: dict[Hashable, set[Callable]] = dict()

    def new_topic(self, topic: Hashable) -> set[Callable]:
        cbs: set[Callable] = set()
        self.__topics[topic] = cbs
        return cbs

    def remove_topic(self, topic: Hashable) -> None:
        del self.__topics[topic]

    def get_topics(self) -> Iterable[Hashable]:
        return set(self.__topics.keys())

    def subscribers(self, topic: Hashable) -> set[Callable]:
        topics = self.__topics
        if topic not in topics:
            self.new_topic(topic)
        return topics[topic]

    def add(self, topic_list: HashOrList, callback: Callable):
        for topic in fix(topic_list):
            subs = self.subscribers(topic)
            subs.add(callback)

    def remove(self, topic_list: HashOrList, callback: Callable):
        for topic in fix(topic_list):
            subs = self.subscribers(topic)
            subs.remove(callback)
            if not len(subs):
                self.remove_topic(topic)

    # TODO: alert if no subscribers?
    def send(self, topic_list: HashOrList, message):
        subs = self.subscribers
        for topic in fix(topic_list):
            self._send(topic, subs(topic), message)

    def _send(self, topic: Hashable, subs, message: Any):
        for cb in self.subscribers(topic):
            cb(topic, message)
            self.send_alert(Alerts.ALL, topic, message)

    def send_alert(self, alert: Alerts, topic: Hashable, message: Any):
        assert isinstance(alert, Alerts)
        for cb in self.subscribers(alert):
            cb(alert, topic, message)
