import string

letters = string.ascii_uppercase[:8]
print(f"letters = \"{letters}\"")


def validate_input():
    while True:
        user_input = input('type 2 symbols that represent cell position on the chessboard: ').upper()
        if len(user_input) == 2 \
                and user_input[0].upper() in letters \
                and (user_input[1].isdigit() and int(user_input[1]) in range(9)):
            print(f"Input \"{user_input.upper()}\" is valid. Continue...")
            return user_input
        else:
            print(f'Sorry "{user_input}" is not valid chess position. Try again.')


def convert_to_numbers(pos: str) -> (int, int):
    x = letters.index(pos[0]) + 1
    y = int(pos[1])
    print(f'Converting "{pos.upper()}" to numeric values: x={x} y={y}')
    return x, y


position: str = validate_input()
numeric_pos = convert_to_numbers(position)

print('Answer: Position cell color is ', end='')
if numeric_pos[0] % 2 == numeric_pos[1] % 2:
    print('Black')
else:
    print('White')
