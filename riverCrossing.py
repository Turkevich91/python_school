# variables - place in memory where computer stores information. any variable has a name and type.
entities: set = {'🐐', '🐺', '🥬'}  # type = set
prohibitions = {('🐺', '🐐'), ('🐐', '🥬')}

movement_story = []

board = {  # dictionary
    'position': 'left',
    'passenger': None,
    'picture': '🚤',
    'trips': 0
}

coasts = {  # dictionary
    'left': set(entities),
    'right': set(),
}


# functions
def input_handler(available_entities):
    """
    Ensure user input is correct and entity available
    :param available_entities: available entities in current coast
    :return:
    """
    while True:
        aliases = {'goat': '🐐',
                   'g': '🐐',
                   'wolf': '🐺',
                   'w': '🐺',
                   'cabbage': '🥬',
                   'c': '🥬'}
        user_input = input('Type who do you want to take: ')

        if user_input in available_entities:
            print(f'you took: {user_input}')
            return user_input
        elif user_input in aliases.keys():
            print(f'you took: {aliases[user_input]}')
            return aliases[user_input]
        elif user_input == '':
            print(f'you decided to float alone')
            return user_input
        else:
            print('incorrect input, try again')


def take_passanger():
    """
    This function took 1 passanger from current coast
    """
    cur_position = board['position']  # we figured out our board current position
    current_island_passangers = coasts[cur_position]  # get available passangers from the current coast
    user_input = input_handler(current_island_passangers)  # chose the passanger we want to take
    taken_passanger = user_input  #
    board['passanger'] = taken_passanger
    if taken_passanger:
        current_island_passangers.remove(user_input)  # delete passanger from the coast


#     return taken_passanger, current_island_passangers

def float_board():
    board['position'] = 'left' if board['position'] == 'right' else 'right'


def drop_passanger():
    """
    This function depart 1 passanger to the recently arrived coast
    """
    cur_position = board['position']
    passanger = board['passanger']
    if passanger:
        current_island_passangers = coasts[cur_position]
        #         print(current_island_passangers)
        current_island_passangers.add(passanger)


def rule_checker():
    """
    check out entities not to eat each others
    :param coast_entities:
    :return:
    """
    coast_entities = coasts[board['position']]
    for rule in prohibitions:
        if coast_entities.issuperset(rule):
            print(f'FAIL! {rule[1]} have been eaten by {rule[0]} while you been away')
            print('game over')
            return False

    if len(coasts['left']) == 0:
        display_current_state()
        print('you win 👑')
        return False
    return True


def display_current_state():
    current_position = board['position']
    current_passanger = board['passenger']
    left_passangers = ''.join(coasts['left']).center(5, ' ')
    right_passangers = ''.join(coasts['right']).center(5, ' ')

    # drawing information
    print('You are now at the ' + current_position + ' coast')
    if current_position == 'left':
        print(f"🏝️{left_passangers}🏝️🚤➡️           🏝️{right_passangers}🏝️")
    elif current_position == 'right':
        print(f"🏝️{left_passangers}🏝️           ⬅️🚤🏝️{right_passangers}🏝️")


def main():
    while coasts['left']:  # продовжувати гру поки на лівому березі хтось є
        display_current_state()

        # define start and destination positions
        cur_coast = board['position']  # left or right

        # take someone before left
        take_passanger()
        if not rule_checker(): break
        float_board()
        drop_passanger()

        # change variables and start again


main()
