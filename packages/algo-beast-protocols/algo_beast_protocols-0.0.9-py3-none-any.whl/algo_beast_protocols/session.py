from typing import Protocol


class Session(Protocol):
  id: int
  mode: str
  project: dict
  algo_broker: dict
  user: dict