import string

letters = string.ascii_uppercase[:8]
chessdesk = {f'{x}{number + 1}' for x in letters for number in range(8)}


def nums_to_pos(x, y):
    return f'{letters[x - 1]}{y}'


def pos_to_nums(pos):
    return letters.index(pos[0]) + 1, int(pos[1])


def occupied(position):
    letter, number = position[0], int(position[1])
    occupied = set()

    # Horizontally and Vertically
    for l in letters:
        occupied.add(f"{l}{number}")
    for n in range(1, 9):
        occupied.add(f"{letter}{n}")

    # Diagonally
    for i in range(-7, 8):
        if 0 < number + i <= 8 and letters.index(letter) + i >= 0 and letters.index(letter) + i < 8:
            occupied.add(f"{letters[letters.index(letter) + i]}{number + i}")
        if 0 < number - i <= 8 and letters.index(letter) + i >= 0 and letters.index(letter) + i < 8:
            occupied.add(f"{letters[letters.index(letter) + i]}{number - i}")

    # Remove the current position as it's not "occupied" by another piece
    occupied.remove(position)

    return occupied


def place_eight_queens(occupied_positions, figures, combinations=set()):
    if len(figures) == 8 and figures not in combinations:
        print(figures)
        combinations.add(frozenset(figures))
        return

    vacant = chessdesk - (occupied_positions.union(figures))

    for pos in vacant:
        current_occupied = occupied_positions.union(occupied(pos))
        if pos not in current_occupied:
            place_eight_queens(current_occupied, figures.union({pos}), combinations)


occupied_positions = set()
figures = set()
place_eight_queens(occupied_positions, figures)
