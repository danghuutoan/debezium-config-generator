from kafka import KafkaConfig
from schemaRegistry import SchemaRegistryConfig
from sink import Sink
from source import Source


class DebeziumConfig:
    def __init__(
        self,
        url: str,
        sink: Sink,
        source: Source,
        kafka: KafkaConfig,
        schema_registry: SchemaRegistryConfig,
    ) -> None:
        self.url = url
        self.sink = sink
        self.source = source
        self.kafka = kafka
        self.schema_registry = schema_registry
