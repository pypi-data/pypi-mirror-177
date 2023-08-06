class Person(object):
  def __init__(self, name: str, destination_floor: int) -> None:
    self._name = name
    self._destination_floor = destination_floor
    self._tick_started_waiting = 0

  def get_name(self) -> str:
    return self._name

  def get_destination_floor(self) -> int:
    return self._destination_floor

  def get_tick_started_waiting(self) -> int:
    return self._tick_started_waiting
  
  def set_tick_started_waiting(self, tick_started_waiting: int) -> None:
    self._tick_started_waiting = tick_started_waiting
