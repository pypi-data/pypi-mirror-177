from typing import Protocol


class Broker(Protocol):
  name: str

  def __init__(self) -> None: ...

  def fetch_data(self): ...
  def subscribe(self, on_data): ...
