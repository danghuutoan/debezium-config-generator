from sink import Sink
from source import Source


class DebeziumConfig:
    def __init__(self, url: str, sink: Sink, source: Source) -> None:
        self.url = url
        self.sink = Sink
        self.source = Source
