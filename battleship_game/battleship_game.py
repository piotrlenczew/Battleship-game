from player import Player
from computer_player import ComputerPlayer
from from_square_name_to_position import from_square_name_to_position
import curses
from curses import wrapper
from curses.textpad import Textbox
import time


def update_window(window, text):
    window.clear()
    window.addstr(text)
    window.refresh()


def main(stdcsr):
    stdcsr.clear()

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    RED_AND_BLACK = curses.color_pair(1)
    stdcsr.addstr(1, 17, "Battleship Game", RED_AND_BLACK | curses.A_BOLD)

    stdcsr.refresh()

    list_of_ships_length = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]

    computer = ComputerPlayer(10, list_of_ships_length)
    for ship_length in list_of_ships_length:
        computer.place_ship(ship_length)

    player = Player(10, list_of_ships_length)

    player_board_win = curses.newwin(12, 23, 6, 1)
    update_window(player_board_win, str(player.player_board()))

    guess_board_win = curses.newwin(12, 23, 6, 27)
    update_window(guess_board_win, str(player.player_guess_board()))

    output_win = curses.newwin(1, 150, 3, 1)
    update_window(output_win, "Game starts!")

    input_win = curses.newwin(1, 4, 4, 1)
    text_box = Textbox(input_win)

    time.sleep(1)

    update_window(output_win, "Use arrows to move ship, v to rotate and x to place.")

    for ship_length in list_of_ships_length:
        ship = player.place_ship(ship_length)
        update_window(player_board_win, str(player.player_board()))
        key = stdcsr.getkey()
        while key != 'x':
            if key == 'KEY_LEFT':
                ship = player.move_ship(ship, 'w')
            elif key == 'KEY_UP':
                ship = player.move_ship(ship, 'n')
            elif key == 'KEY_RIGHT':
                ship = player.move_ship(ship, 'e')
            elif key == 'KEY_DOWN':
                ship = player.move_ship(ship, 's')
            elif key == 'v':
                ship = player.rotate_ship(ship)
            update_window(player_board_win, str(player.player_board()))
            key = stdcsr.getkey()

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
