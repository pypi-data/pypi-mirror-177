from typing import Protocol, List


class Config(Protocol):
  access_token: str
  backend_url: str
  available_brokers: List[str]
  available_modes: List[str]