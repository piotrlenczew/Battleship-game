from classes import Ship, Player, ComputerPlayer, IncorrectDirectionError
from classes import CanNotPlaceShipError, NegativeDimensionError
from from_square_name_to_position import from_square_name_to_position
import curses
from curses import wrapper
from curses.textpad import Textbox
import time


def update_window(window, text):
    window.clear()
    window.addstr(text)
    window.refresh()


def main(stdscr):
    stdscr.clear()

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    RED_AND_BLACK = curses.color_pair(1)
    stdscr.addstr(1, 17, "Battleship Game", RED_AND_BLACK | curses.A_BOLD)

    stdscr.refresh()

    list_of_ship_lengths = [2, 3, 3, 4, 5]

    computer = ComputerPlayer(10, list_of_ship_lengths)
    for ship_length in list_of_ship_lengths:
        computer.place_ship(ship_length)

    player = Player(10)

    player_board_win = curses.newwin(12, 23, 6, 1)
    update_window(player_board_win, str(player.player_board()))

    guess_board_win = curses.newwin(12, 23, 6, 27)
    update_window(guess_board_win, str(player.player_guess_board()))

    output_win = curses.newwin(1, 100, 3, 1)
    update_window(output_win, "Game starts!")

    input_win = curses.newwin(1, 4, 4, 1)
    text_box = Textbox(input_win)

    time.sleep(2)

    for ship_length in list_of_ship_lengths:
        main_message = f"Place ship of {ship_length} length. "
        add_message = "Write first position of ship: "
        update_window(output_win, main_message + add_message)
        can_place_ship = False
        while not can_place_ship:
            correct_square_name = False
            while not correct_square_name:
                text_box.edit()
                square_name = text_box.gather().strip().upper()
                input_win.clear()
                try:
                    position = from_square_name_to_position[square_name]
                    correct_square_name = True
                except KeyError:
                    main_message = "Position was incorrect. "
                    update_window(output_win, main_message + add_message)
            main_message = f"Place ship of {ship_length} length. "
            add_message = "Write direction of ship [n/e/s/w]: "
            update_window(output_win, main_message + add_message)
            correct_direction = False
            ship = Ship((0, 0), 's', 20)
            while not correct_direction or not ship.fits_in_board(10):
                text_box.edit()
                direction = text_box.gather().strip()
                input_win.clear()
                try:
                    ship = Ship(position, direction, ship_length)
                    correct_direction = True
                except IncorrectDirectionError:
                    message = 'Can only use n-north, e-east, s-south, w-west. '
                    main_message = "Direction was incorrect." + message
                    update_window(output_win, main_message + add_message)
                except NegativeDimensionError:
                    main_message = f"There's not enough space in {direction} direction. "
                    update_window(output_win, main_message + add_message)
                if not ship.fits_in_board(10):
                    main_message = f"There's not enough space in {direction} direction. "
                    update_window(output_win, main_message + add_message)
            try:
                player.place_ship(ship)
                can_place_ship = True
            except CanNotPlaceShipError:
                main_message = f"Ship of {ship_length} length interferes with another ship. "
                add_message = "Write first position of ship: "
                update_window(output_win, main_message + add_message)
        update_window(player_board_win, str(player.player_board()))

    while player.player_board().has_ship() and computer.computer_board().has_ship():
        update_window(output_win, "Write position where you want to shoot: ")
        correct_square = False
        while not correct_square:
            text_box.edit()
            square_name = text_box.gather().strip().upper()
            input_win.clear()
            correct_square = True
            try:
                attacked_position = from_square_name_to_position[square_name]
            except KeyError:
                update_window(output_win, "Wrong position. Try again: ")
        player.guess(computer.computer_board(), attacked_position)
        update_window(guess_board_win, str(player.player_guess_board()))
        if not computer.computer_board().has_ship():
            update_window(output_win, "Congratulations. You have won!")
        else:
            computer.guess(player.player_board())
            update_window(player_board_win, str(player.player_board()))
            if not player.player_board().has_ship():
                update_window(output_win, "Unfortunately, you have lost.")

    stdscr.refresh()
    stdscr.getch()


wrapper(main)
