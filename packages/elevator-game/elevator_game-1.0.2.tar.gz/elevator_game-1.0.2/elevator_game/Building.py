import string

from . import Person, Elevator, NoFloorError, NoElevatorError, CannotLoadError

class Building(object):
  def __init__(self, number_of_floors: int, number_of_elevators: int) -> None:
    self._number_of_floors = number_of_floors
    # This includes an unused floor 0 for ease of development. It's worth 64 bits of memory.
    self._people_on_floors: list[list[Person]] = [[] for i in range(self._number_of_floors + 1)]
    self._number_of_elevators = number_of_elevators
    self._elevators: list[Elevator] = [Elevator(string.ascii_uppercase[i]) for i in range(self._number_of_elevators)]

  def send_elevator_to_floor(self, elevator_name: str, floor_number: int) -> None:
    if floor_number < 1 or floor_number > self._number_of_floors + 1:
      raise NoFloorError('Floor does not exist')
    for elevator in self._elevators:
      if elevator.get_name() == elevator_name:
        elevator.go_to_floor(floor_number)
        return
    raise NoElevatorError('There is no elevator by that name')

  def get_elevators(self) -> list[Elevator]:
    return self._elevators

  def get_people_on_floors(self) -> list[list[Person]]:
    return self._people_on_floors

  def open_door(self, elevator_name: str) -> None:
    for elevator in self._elevators:
      if elevator.get_name() == elevator_name:
        elevator.open_door()
        return
    raise NoElevatorError('There is no elevator by that name')

  def add_person_to_floor(self, person: Person, floor: int) -> None:
    if floor < 1 or floor > self._number_of_floors:
      raise NoFloorError("That floor does not exist")
    self._people_on_floors[floor].append(person)

  def load_passenger(self, person: str) -> None:
    for floor in range(1, self._number_of_floors + 1):
      for person_on_floor in self._people_on_floors[floor]:
        if person_on_floor.get_name() == person:
          for elevator in self._elevators:
            if elevator.get_current_floor() == floor and elevator.get_is_door_open():
              elevator.load_passenger(person_on_floor)
              self._people_on_floors[floor].remove(person_on_floor)
              return
    raise CannotLoadError('There is no person by that name, or no elevator on that floor with the door open')

  def unload_passenger(self, person: str) -> None:
    for elevator in self._elevators:
      for passenger in elevator.get_passengers():
        if passenger.get_name() == person:
          ex_passenger = elevator.unload_passenger(person)
          self._people_on_floors[elevator.get_current_floor()].append(ex_passenger)
          return
    raise CannotLoadError('There is no passenger by that name')

  def tick(self) -> None:
    """
    This doesn't include unloading passengers.
    That's left to the game to do later so it can get a list of persons unloaded successfully
    """
    for elevator in self._elevators:
      elevator.tick()

  def unload_passengers_who_have_arrived(self) -> list[Person]:
    total_arrived: list[Person] = []
    for elevator in self._elevators:
      arrived = elevator.unload_passengers_who_have_arrived()
      total_arrived.extend(arrived)
    return total_arrived
