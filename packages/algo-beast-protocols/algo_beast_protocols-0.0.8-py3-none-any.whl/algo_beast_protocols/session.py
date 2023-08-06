from typing import Protocol


class Session(Protocol):
  id: int
  mode: str
  project_name: str
  broker_name: str
  broker_config: dict