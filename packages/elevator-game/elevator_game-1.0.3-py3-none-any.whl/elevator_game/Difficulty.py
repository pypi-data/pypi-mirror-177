from . import NoDifficultyError

MINIMUM_DIFFICULTY = 1
MAXIMUM_DIFFICULTY = 10

class Difficulty(object):
  def __init__(self, difficulty: int, number_of_people: int, ticks_between_people: int, seconds_between_ticks: float, number_of_floors: int, number_of_elevators: int) -> None:
    self.difficulty = difficulty
    self.number_of_people = number_of_people
    self.ticks_between_people = ticks_between_people
    self.number_of_floors = number_of_floors
    self.number_of_elevators = number_of_elevators
    self.seconds_between_ticks = seconds_between_ticks

def get_difficulty(difficulty: int) -> Difficulty:
  if difficulty == 1:
    return Difficulty(difficulty, 20, 6, 3.0, 4, 1)
  if difficulty == 2:
    return Difficulty(difficulty, 20, 7, 2.2, 5, 1)
  if difficulty == 3:
    return Difficulty(difficulty, 20, 7, 2.0, 7, 2)
  if difficulty == 4:
    return Difficulty(difficulty, 20, 6, 1.8, 8, 3)
  if difficulty == 5:
    return Difficulty(difficulty, 20, 6, 1.5, 9, 4)
  if difficulty == 6:
    return Difficulty(difficulty, 20, 5, 1.2, 9, 4)
  if difficulty == 7:
    return Difficulty(difficulty, 26, 4, 1.2, 9, 4)
  if difficulty == 8:
    return Difficulty(difficulty, 26, 4, 1.1, 9, 5)
  if difficulty == 9:
    return Difficulty(difficulty, 26, 4, 1.0, 9, 5)
  if difficulty == 10:
    return Difficulty(difficulty, 26, 3, 1.0, 9, 5)
  raise NoDifficultyError('That difficulty does not exist')
