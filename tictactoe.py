ROWS = 3
COLUMNS = 3


# takes 2 coordinates for a move,
# returns corresponding 1 coordinate in the list
def coordinate(c, r):
    new_c = c - 1
    new_r = ROWS - r
    return new_r * COLUMNS + new_c


# takes list with symbols, prints out the battlefield
def print_field(l):
    print("---------")
    for i in range(ROWS):
        print("|", " ".join(l[i * ROWS:i * ROWS + COLUMNS]), "|")
    print("---------")


# creates the nested list with three-in-a-row combinations
def three_rows(l):
    rows = [l[i:COLUMNS*i] for i in range(COLUMNS)]
    columns = [l[0:7:3], l[1:8:3], l[2:9:3]]
    diagonals = [l[0:9:4], l[2:7:2]]
    three = [rows, columns, diagonals]
    return three


# game set up: prints out empty fields, creates variable
field_list = list(' ' * 9)
print_field(field_list)
move_counter = 0
game_finished = False

while not game_finished:

    # prompts the user to give coordinates for a move until valid
    valid_input = False
    valid_numbers = ['1', '2', '3']
    move = -1
    while not valid_input:
        move_coordinates = input("Enter the coordinates: ").split()
        if len(move_coordinates) != 2:
            print("Enter exactly two numbers!")
        elif not move_coordinates[0].isnumeric() or not move_coordinates[1].isnumeric():
            print("You should enter numbers!")
        elif move_coordinates[0] not in valid_numbers or move_coordinates[1] not in valid_numbers:
            print("Coordinates should be from 1 to 3!")
        else:
            col, row = [int(i) for i in move_coordinates]
            move = coordinate(col, row)
            if field_list[move] not in [' ', '_']:
                print("This cell is occupied! Choose another one!")
            else:
                valid_input = True
                move_counter += 1

    # writes user's move into the field list and outputs new field
    if move_counter % 2 == 1:
        field_list[move] = 'X'
    else:
        field_list[move] = 'O'
    print_field(field_list)

    # generates three-in-a-row combinations
    three_in_a_row = three_rows(field_list)

    # checks if input contains empty cells
    empty_cells = False
    for symbol in field_list:
        if symbol in [' ', '_']:
            empty_cells = True

    # counts 3 in a row combinations for Xs and Os
    winning = [['X'] * 3, ['O'] * 3]
    x_three, o_three = 0, 0

    for element in three_in_a_row:
        for i in element:
            if i == winning[0]:
                x_three += 1
            if i == winning[1]:
                o_three += 1

    # Prints game states
    if x_three > 0 and o_three == 0:
        print("X wins")
        game_finished = True
    elif o_three > 0 and x_three == 0:
        print("O wins")
        game_finished = True
    elif (x_three == 0 and o_three ==0) and not empty_cells:
        print("Draw")
        game_finished = True
