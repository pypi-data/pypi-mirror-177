from typing import Protocol


class Config(Protocol):
  access_token: str
  backend_url: str