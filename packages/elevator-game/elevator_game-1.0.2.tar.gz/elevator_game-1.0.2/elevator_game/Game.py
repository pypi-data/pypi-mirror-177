import string
import random
from time import time
from typing import Any

from . import Building, Person, Elevator, get_difficulty

_SCORE_FEEL_GOOD_MULTIPLIER = 100

def _subarray_count(array: list[list[Any]]):
  count = 0
  for arr in array:
    count += len(arr)
  return count

class Game(object):
  def __init__(self, difficulty: int) -> None:
    self.score = 0.0
    self.is_game_over = False
    self.ticks_passed = -1
    self.__difficulty = get_difficulty(difficulty)
    self.people_to_arrive = self.__difficulty.number_of_people
    self.number_of_floors = self.__difficulty.number_of_floors
    self.__time_of_last_tick = 0
    self.__building = Building(self.number_of_floors, self.__difficulty.number_of_elevators)

  def tick_time_check(self) -> bool:
    now = time()
    if now - self.__time_of_last_tick > self.__difficulty.seconds_between_ticks:
      self.ticks_passed += 1
      self.__time_of_last_tick = now
      self._tick()
      return True
    return False

  def _tick(self) -> None:
    self.__building.tick()
    arrived_people = self.__building.unload_passengers_who_have_arrived()
    for person in arrived_people:
      self.score += _SCORE_FEEL_GOOD_MULTIPLIER * self.number_of_floors * self.__difficulty.difficulty / (self.ticks_passed - person.get_tick_started_waiting())
    if self.ticks_passed % self.__difficulty.ticks_between_people == 0 and self.people_to_arrive > 0:
      destination_floor = random.randint(1, self.number_of_floors)
      possible_names = set(string.ascii_lowercase)
      all_people_in_building: list[Person] = []
      for floor in self.__building.get_people_on_floors():
        all_people_in_building.extend(floor)
      for elevator in self.get_elevators():
        all_people_in_building.extend(elevator.get_passengers())
      names_in_use = set([person.get_name() for person in all_people_in_building])
      available_names = list(possible_names - names_in_use)
      available_names.sort()
      if len(available_names) > 0:
        name = list(available_names)[0]
        person = Person(name, destination_floor)
        source_floor = person.get_destination_floor()
        while source_floor == person.get_destination_floor():
          source_floor = random.randint(1, self.number_of_floors)
        person.set_tick_started_waiting(self.ticks_passed)
        self.__building.add_person_to_floor(person, source_floor)
        self.people_to_arrive -= 1

    # Game-state change
    count_people_on_floors = _subarray_count(self.__building.get_people_on_floors())
    count_people_on_elevators = _subarray_count([elevator.get_passengers() for elevator in self.__building.get_elevators()])
    if self.people_to_arrive < 1 and count_people_on_floors < 1 and count_people_on_elevators < 1:
      self.is_game_over = True

  def get_elevators(self) -> list[Elevator]:
    return self.__building.get_elevators()

  def get_people_on_floors(self) -> list[list[Person]]:
    return self.__building.get_people_on_floors()

  def send_elevator_to_floor(self, elevator_name: str, floor_number: int) -> None:
    self.__building.send_elevator_to_floor(elevator_name, floor_number)
  
  def open_door(self, elevator_name: str) -> None:
    self.__building.open_door(elevator_name)

  def load_or_unload_passenger(self, person_name: str) -> None:
    for floor in self.__building.get_people_on_floors():
      for person in floor:
        if person.get_name() == person_name:
          self.__building.load_passenger(person_name)
          return
    self.__building.unload_passenger(person_name)
