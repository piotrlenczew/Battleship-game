from_square_name_to_position = {}

for row, number in enumerate(range(1, 11)):
    for column, letter_ascii in enumerate(range(ord('A'), ord('K'))):
        square_name = chr(letter_ascii) + str(number)
        from_square_name_to_position[square_name] = (row, column)
