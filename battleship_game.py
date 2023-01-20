from game_files.player import Player
from game_files.computer_player import ComputerPlayer
from game_files.from_square_name_to_position import from_square_name_to_position
from game_files.game_settings import board_size, list_of_ships_length
from game_files.defined_enumerations import Course, Keys
import curses
from curses import wrapper
from curses.textpad import Textbox
import time


def update_window(window, text):
    """Clear given window and write given text."""
    window.clear()
    window.addstr(text)
    window.refresh()


def show_not_placed_ship(window, ship):
    """Overwrite player_board_win to show ship that was't placed yet."""
    for position in ship.positions():
        row, column = position
        window.addstr(row + 1, (2*column) + 3, 'O ')
    window.refresh()


def get_key(stdcsr):
    """Get key from keyboard if key defined else wait."""
    while True:
        try:
            key = Keys(stdcsr.getkey())
            return key
        except ValueError:
            pass


size = board_size


def main(stdcsr):
    """
    Initialize game

    - Initialize game window
    - Place computer ships
    - Allow player to place ships
    - Allow player to guess squares
    - Guess player's squares
    - Repeat two last ones until player or computer has no ships
    """
    stdcsr.clear()

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    RED_AND_BLACK = curses.color_pair(1)
    title = "Battleship Game"
    stdcsr.addstr(1, 2 * size - 1, title, RED_AND_BLACK | curses.A_BOLD)

    stdcsr.refresh()

    computer = ComputerPlayer(size, list_of_ships_length)
    for ship_length in list_of_ships_length:
        computer.place_ship(ship_length)

    player = Player(size, list_of_ships_length)

    player_board_win = curses.newwin(size + 4, 2*size+3, 6, 1)
    update_window(player_board_win, str(player.player_board()))

    guess_board_win = curses.newwin(size + 4, 2*size+3, 6, 2*size+6)
    update_window(guess_board_win, str(player.player_guess_board()))

    output_win = curses.newwin(1, 150, 3, 1)
    update_window(output_win, "Game starts!")

    input_win = curses.newwin(1, 4, 4, 1)
    text_box = Textbox(input_win)

    time.sleep(1)

    for ship_length in list_of_ships_length:
        message = "Use arrows to move ship, v to rotate and x to place."
        update_window(output_win, message)
        ship = player.place_ship(ship_length)
        update_window(player_board_win, str(player.player_board()))
        key = get_key(stdcsr)
        if key != Keys.EXIT:
            player._player_board.remove_ship(ship)
        board_size = player._player_board.size()
        while key != Keys.EXIT:
            if key == Keys.LEFT:
                update_window(player_board_win, str(player.player_board()))
                ship.move_ship(Course.west, board_size)
                show_not_placed_ship(player_board_win, ship)
            elif key == Keys.UP:
                update_window(player_board_win, str(player.player_board()))
                ship.move_ship(Course.north, board_size)
                show_not_placed_ship(player_board_win, ship)
            elif key == Keys.RIGHT:
                update_window(player_board_win, str(player.player_board()))
                ship.move_ship(Course.east, board_size)
                show_not_placed_ship(player_board_win, ship)
            elif key == Keys.DOWN:
                update_window(player_board_win, str(player.player_board()))
                ship.move_ship(Course.south, board_size)
                show_not_placed_ship(player_board_win, ship)
            elif key == Keys.ROTATE:
                update_window(player_board_win, str(player.player_board()))
                ship.rotate_ship(board_size)
                show_not_placed_ship(player_board_win, ship)
            key = get_key(stdcsr)
            if key == Keys.EXIT:
                if player._player_board.can_place_ship(ship):
                    player._player_board.place_ship(ship)
                else:
                    message = "Ship can't be placed here! Try to meve it."
                    update_window(output_win, message)
                    key = get_key(stdcsr)

    while player.player_board().has_ship() and computer.computer_board().has_ship():
        update_window(output_win, "Write position where you want to shoot: ")
        correct_square = False
        while not correct_square:
            text_box.edit()
            square_name = text_box.gather().strip().upper()
            input_win.clear()
            try:
                attacked_position = from_square_name_to_position[square_name]
                player.guess(computer.computer_board(), attacked_position)
                correct_square = True
            except KeyError:
                update_window(output_win, "Wrong position. Try again: ")
        update_window(guess_board_win, str(player.player_guess_board()))
        if not computer.computer_board().has_ship():
            message = "Congratulations. You have won! Click any key to exit"
            update_window(output_win, message)
        else:
            computer.guess(player.player_board())
            update_window(player_board_win, str(player.player_board()))
            if not player.player_board().has_ship():
                message = "Unfortunately, you have lost. Click any key to exit"
                update_window(output_win, message)

    stdcsr.refresh()
    stdcsr.getch()


wrapper(main)
