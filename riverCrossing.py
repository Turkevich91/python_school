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
aliases = {'goat': '🐐',
           'wolf': '🐺',
           'cabbage': '🥬'}


# functions
def input_handler(available_entities):
    """
    Ensure user input is correct and entity available
    :param available_entities: available entities in current coast
    :return:
    """

    while True:

        user_input = input('Type who do you want to take: ')

        if user_input == '':
            print(f'you decided to float alone')
            return user_input
        elif user_input in available_entities:
            print(f'you took: {user_input}')
            return user_input
        else:
            for alias in aliases.keys():
                if alias.startswith(user_input.lower()):
                    passenger = aliases[alias]
                    if passenger in available_entities:
                        print(f'you took: {passenger}')
                        return passenger
                    else:
                        print(f'you took a {passenger} but it not present on the current coast.')
                        break
            print('incorrect input, try again')


def take_passenger():
    """
    This function took 1 passenger from current coast
    """
    cur_position = board['position']  # we figured out our board current position
    current_island_passengers = coasts[cur_position]  # get available passengers from the current coast
    passenger = input_handler(current_island_passengers)  # chose the passenger we want to take
    board['passenger'] = passenger
    if passenger:
        current_island_passengers.remove(passenger)  # delete passenger from the coast


def float_board():
    board['position'] = 'left' if board['position'] == 'right' else 'right'
    board['trips'] += 1


def drop_passenger():
    """
    This function depart 1 passenger to the recently arrived coast
    """
    cur_position = board['position']
    passenger = board['passenger']
    if passenger:
        current_island_passengers = coasts[cur_position]
        #         print(current_island_passengers)
        current_island_passengers.add(passenger)


def check_rule():
    """
    check out entities not to eat each others
    :return:
    """
    if not board['trips']:
        return True

    uncontrollable_coast_entities = coasts['left' if board['position'] == 'right' else 'right']

    for rule in prohibitions:
        if uncontrollable_coast_entities.issuperset(rule):
            print(f'FAIL! {rule[1]} have been eaten by {rule[0]} while you been away')
            print(' GAME OVER '.center(22, '🥺'))
            return False

    if not coasts['left']:
        display_current_state()
        print(' YOU WIN '.center(22, '👑'))
        return False
    return True


def display_current_state():
    current_position = board['position']
    left_passengers = ''.join(coasts['left']).center(5, ' ')
    right_passengers = ''.join(coasts['right']).center(5, ' ')

    # drawing information
    print('You are now at the ' + current_position + ' coast')
    if current_position == 'left':
        print(f"🏝️{left_passengers}🏝️🚤➡️           🏝️{right_passengers}🏝️")
    elif current_position == 'right':
        print(f"🏝️{left_passengers}🏝️           ⬅️🚤🏝️{right_passengers}🏝️")


def main():
    print('available aliases: {0}or push Enter to depart alone'
          .format(''.join([f"\'{k}\': {v}, " for k, v in aliases.items()])))
    while True:
        if not check_rule():
            break
        display_current_state()
        take_passenger()
        float_board()
        drop_passenger()

        # change variables and start again


main()
