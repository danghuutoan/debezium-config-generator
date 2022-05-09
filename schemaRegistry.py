from typing import List


class SchemaRegistryConfig:
    def __init__(self, urls: List[str]) -> None:
        self.urls = urls