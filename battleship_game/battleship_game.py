from player import Player
from computer_player import ComputerPlayer
from from_square_name_to_position import from_square_name_to_position
from game_settings import board_size, list_of_ships_length
import curses
from curses import wrapper
from curses.textpad import Textbox
import time


def update_window(window, text):
    window.clear()
    window.addstr(text)
    window.refresh()


def show_not_placed_ship(window, ship):
    for position in ship.positions():
        row, column = position
        window.addstr(row + 1, (2*column) + 3, 'O ')
    window.refresh()


size = board_size


def main(stdcsr):
    stdcsr.clear()

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    RED_AND_BLACK = curses.color_pair(1)
    stdcsr.addstr(1, 2 * size - 1, "Battleship Game", RED_AND_BLACK | curses.A_BOLD)

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
        update_window(output_win, "Use arrows to move ship, v to rotate and x to place.")
        ship = player.place_ship(ship_length)
        update_window(player_board_win, str(player.player_board()))
        key = stdcsr.getkey()
        if key != 'x':
            player._player_board.remove_ship(ship)
        board_size = player._player_board.size()
        while key != 'x':
            if key == 'KEY_LEFT':
                update_window(player_board_win, str(player.player_board()))
                ship.move_ship('w', board_size)
                show_not_placed_ship(player_board_win, ship)
            elif key == 'KEY_UP':
                update_window(player_board_win, str(player.player_board()))
                ship.move_ship('n', board_size)
                show_not_placed_ship(player_board_win, ship)
            elif key == 'KEY_RIGHT':
                update_window(player_board_win, str(player.player_board()))
                ship.move_ship('e', board_size)
                show_not_placed_ship(player_board_win, ship)
            elif key == 'KEY_DOWN':
                update_window(player_board_win, str(player.player_board()))
                ship.move_ship('s', board_size)
                show_not_placed_ship(player_board_win, ship)
            elif key == 'v':
                update_window(player_board_win, str(player.player_board()))
                ship.rotate_ship(board_size)
                show_not_placed_ship(player_board_win, ship)
            key = stdcsr.getkey()
            if key == 'x':
                if player._player_board.can_place_ship(ship):
                    player._player_board.place_ship(ship)
                else:
                    update_window(output_win, "Ship can't be placed here! Try to meve it.")
                    key = 'z'

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
            update_window(output_win, "Congratulations. You have won! Click any key to exit")
        else:
            computer.guess(player.player_board())
            update_window(player_board_win, str(player.player_board()))
            if not player.player_board().has_ship():
                update_window(output_win, "Unfortunately, you have lost. Click any key to exit")

    stdcsr.refresh()
    stdcsr.getch()


wrapper(main)
