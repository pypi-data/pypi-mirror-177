from curses import wrapper, window as Window, curs_set, A_BOLD, A_DIM, COLOR_BLUE, COLOR_WHITE, init_pair, color_pair, newpad
from time import sleep
from typing import Union
import string

from . import Game, MAXIMUM_DIFFICULTY, MINIMUM_DIFFICULTY

game: Game = Game(MINIMUM_DIFFICULTY)
selected_elevator: Union[str, None] = None
auto_load = True

def game_loop():
  global game
  while True:
    difficulty = ''
    try:
      difficulty = input('Choose a difficulty({} - {}) or "exit" to quit: '.format(MINIMUM_DIFFICULTY, MAXIMUM_DIFFICULTY))
    except KeyboardInterrupt:
      print('')
      break
    if difficulty == 'exit':
      break
    difficulty_int = -1
    try:
      difficulty_int = int(difficulty)
    except:
      pass
    if difficulty_int < MINIMUM_DIFFICULTY or difficulty_int > MAXIMUM_DIFFICULTY:
      print('Invalid difficulty')
      continue

    game = Game(difficulty_int)
    try:
      wrapper(__play_game)
    except KeyboardInterrupt:
      pass
    print('You scored {:,.0f} on difficulty {}'.format(game.score, difficulty))

def __play_game(window: Window):
  global game
  global selected_elevator
  global auto_load
  init_pair(1, COLOR_WHITE, COLOR_BLUE)
  try:
    curs_set(False)
  except:
    pass
  window.nodelay(True)
  while not game.is_game_over:
    if game.tick_time_check():
      render(game, window)
      if auto_load:
        people_on_floors = game.get_people_on_floors()
        for elevator in game.get_elevators():
          if elevator.get_is_door_open():
            for person in people_on_floors[elevator.get_current_floor()]:
              game.load_or_unload_passenger(person.get_name())
    try:
      input = window.getkey()
      if input in string.ascii_lowercase:
        game.load_or_unload_passenger(input)
      elif input in string.ascii_uppercase:
        selected_elevator = input
      elif input in string.digits:
        if selected_elevator is not None:
          game.send_elevator_to_floor(selected_elevator, int(input))
      elif input == '!':
        if selected_elevator is not None:
          game.open_door(selected_elevator)
      render(game, window)
    except:
      pass
    sleep(1 / 24)

def render(game: Game, window: Window):
  global selected_elevator
  global auto_load
  
  window.clear()

  # Status bar
  window.move(1, 1)
  window.addstr('Time Passed ')
  window.addstr('{:3,}'.format(game.ticks_passed), A_BOLD)
  window.addstr(' | Score ')
  window.addstr('{:6,.0f}'.format(game.score), A_BOLD)
  window.addstr(' | People yet to arrive ')
  window.addstr('{:2,}'.format(game.people_to_arrive), A_BOLD)
  
  # Messages go to 2, 1
  
  # Elevator Header
  floor_start_row = 4
  window.move(floor_start_row, 1)
  window.addstr('Floor', A_DIM)
  for elevator in game.get_elevators():
    window.addstr(' ')
    if elevator.get_is_door_open():
      window.addstr('{}'.format(elevator.get_name()), color_pair(1))
    else:
      window.addstr('{}'.format(elevator.get_name()))
  
  # Floors
  floor_current_row = floor_start_row 
  for floor in range(game.number_of_floors, 0, -1):
    floor_current_row += 1
    window.move(floor_current_row, 1)
    window.addstr('{}'.format(floor))
    for elevator_index in range(len(game.get_elevators())):
      elevator = game.get_elevators()[elevator_index]
      if elevator.get_current_floor() == floor:
        window.move(floor_current_row, 6 + 2 * elevator_index)
        window.addstr('{:2.0f}'.format(len(elevator.get_passengers())))
  
  # People header
  person_start_column = 32
  person_current_row = floor_start_row
  window.move(person_current_row, person_start_column)
  window.addstr('Name Location Destination', A_DIM)
  
  LINES_BELOW_PEOPLE = 5
  
  # People on elevators
  for elevator in game.get_elevators():
    for person in elevator.get_passengers():
      if person_current_row + LINES_BELOW_PEOPLE > window.getmaxyx()[0]:
        break
      person_current_row += 1
      window.move(person_current_row, person_start_column)
      window.addstr('{}    {}({})     {}'.format(person.get_name(), elevator.get_name(), elevator.get_current_floor(), person.get_destination_floor()))

  # People on floorsA
  window.move(2, 1)
  for floor_index in range(1, game.number_of_floors + 1):
    floor = game.get_people_on_floors()[floor_index]
    for person in floor:
      if person_current_row + LINES_BELOW_PEOPLE > window.getmaxyx()[0]:
        break
      person_current_row += 1
      window.move(person_current_row, person_start_column)
      window.addstr('{}    {}        {}'.format(person.get_name(), floor_index, person.get_destination_floor()))

  # Commands
  commands_row = max(person_current_row, floor_current_row) + 2
  window.move(commands_row, 1)
  if selected_elevator is None:
    window.addstr('Uppercase letter to select an elevator', A_DIM)
  else:
    window.addstr('Elevator ', A_DIM)
    window.addstr('{}'.format(selected_elevator))
    window.addstr(' selected | Number to send elevator to floor | ! to open door', A_DIM)

  # Auto loading
  window.move(commands_row + 1, 1)
  if auto_load:
    window.addstr('Auto-load | @ to disable auto-loading elevators', A_DIM)
  else:
    window.addstr('@ to enable auto-loading elevators | Lowercase to manually load/unload person', A_DIM)

  window.move(3, 1)
