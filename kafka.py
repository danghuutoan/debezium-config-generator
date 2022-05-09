from typing import List


class KafkaConfig:
    def __init__(self, bootstrap_servers: List[str]) -> None:
        self.bootstrap_servers = bootstrap_servers