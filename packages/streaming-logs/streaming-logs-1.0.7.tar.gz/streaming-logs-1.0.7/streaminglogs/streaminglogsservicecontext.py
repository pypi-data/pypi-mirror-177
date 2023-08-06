from dataclasses import dataclass


@dataclass
class StreamingLogsServiceContext:

    endpoint: str
    origin: str

    def __init__(self, settings: dict):
        self.endpoint = settings.get('endpoint')
        self.origin = settings.get('origin', 'some-origin')
