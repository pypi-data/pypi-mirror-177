from . import Person

class Elevator(object):
  def __init__(self, name: str) -> None:
    self._name = name
    self._current_floor = 1
    self._destination_floor = 1
    self._is_door_open = False
    self._passengers: list[Person] = []

  def get_name(self) -> str:
    return self._name

  def get_current_floor(self) -> int:
    return self._current_floor

  def get_destination_floor(self) -> int:
    return self._destination_floor

  def get_is_door_open(self) -> bool:
    return self._is_door_open

  def get_passengers(self) -> list[Person]:
    return self._passengers

  def go_to_floor(self, destination_floor: int) -> None:
    self._is_door_open = False
    self._destination_floor = destination_floor

  def open_door(self) -> None:
    self._destination_floor = self._current_floor
    self._is_door_open = True

  def load_passenger(self, passenger: Person) -> None:
    self._passengers.append(passenger)

  def unload_passenger(self, passenger_name: str) -> Person:
    if not self._is_door_open:
      raise Exception('Elevator door is not open')
    for passenger in self._passengers:
      if passenger.get_name() == passenger_name:
        self._passengers.remove(passenger)
        return passenger
    raise IndexError('There is no passenger by that name on this elevator')

  def unload_passengers_who_have_arrived(self) -> list[Person]:
    arrived = []
    for passenger in self._passengers:
      if self._is_door_open and self._current_floor == passenger.get_destination_floor():
        arrived.append(passenger)
    for passenger in arrived:
      self._passengers.remove(passenger)
    return arrived

  def tick(self) -> None:
    if self._destination_floor > self._current_floor:
      self._current_floor += 1
    elif self._destination_floor < self._current_floor:
      self._current_floor -= 1
