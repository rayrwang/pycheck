# Jan 24, 2022

# Modules required:
# graphics.py: http://www.cs.uky.edu/~keen/help/Zelle-graphics-reference.pdf

import graphics as gr
import random
import copy
from collections import deque

# The game board
win = gr.GraphWin("Checkers AI", 500, 500, autoflush=False)


def initialize_board():
    # Draw the rows of the game board
    rows = []
    for i in range(50, 500, 50):
        new_row = gr.Line(gr.Point(50, i), gr.Point(450, i))
        rows.append(new_row)
    for i in rows:
        i.draw(win)

    # Draw the columns
    columns = []
    for i in range(50, 500, 50):
        new_columns = gr.Line(gr.Point(i, 50), gr.Point(i, 450))
        columns.append(new_columns)
    for i in columns:
        i.draw(win)

    del rows, columns

    # This code will generate the connections between the squares on the board
    # This can be done manually, but it's arguably more interesting to do it algorithmically

    # connections_dict is nested dictionary with {square <tuple>: {connection type <int>: connected square <tuple>}}
    # Squares and connected squares are tuples specified with row and pos (position in row), (row, pos): 1 to 8, 1 to 4
    # Connection type ranges from 0 to 3: top right, bottom right, bottom left, top left: from perspective of self
    connections_dict = {}
    # Give an index for each square
    for i in range(1, 9):
        for j in range(1, 5):
            connections_dict[(i, j)] = {}

    # There are 8 types of squares: Those on each of the 4 edges,
    # upper right and lower left corners, and the middle ones on even and odd rows

    for i in connections_dict:
        row = i[0]
        pos = i[1]
        # Upper edge squares (excluding top right)
        if row == 1 and pos in (1, 2, 3):
            connections_dict[i] = {0: None,
                                   1: (row + 1, pos + 1),
                                   2: (row + 1, pos),
                                   3: None}
        # Top right square
        if row == 1 and pos == 4:
            connections_dict[i] = {0: None,
                                   1: None,
                                   2: (row + 1, pos),
                                   3: None}
        # Left edge excluding bottom left
        if row in (2, 4, 6) and pos == 1:
            connections_dict[i] = {0: (row - 1, pos),
                                   1: (row + 1, pos),
                                   2: None,
                                   3: None}
        # Center squares on even rows
        if row in (2, 4, 6) and pos in (2, 3, 4):
            connections_dict[i] = {0: (row - 1, pos),
                                   1: (row + 1, pos),
                                   2: (row + 1, pos - 1),
                                   3: (row - 1, pos - 1)}
        # Center squares on odd rows
        if row in (3, 5, 7) and pos in (1, 2, 3):
            connections_dict[i] = {0: (row - 1, pos + 1),
                                   1: (row + 1, pos + 1),
                                   2: (row + 1, pos),
                                   3: (row - 1, pos)}
        # Right edge
        if row in (3, 5, 7) and pos == 4:
            connections_dict[i] = {0: None,
                                   1: None,
                                   2: (row + 1, pos),
                                   3: (row - 1, pos)}
        # Bottom left square
        if row == 8 and pos == 1:
            connections_dict[i] = {0: (row - 1, pos),
                                   1: None,
                                   2: None,
                                   3: None}
        # Bottom row
        if row == 8 and pos in (2, 3, 4):
            connections_dict[i] = {0: (row - 1, pos),
                                   1: None,
                                   2: None,
                                   3: (row - 1, pos - 1)}

    # Initialize and draw the starting pieces
    for i in range(1, 4):
        for j in range(1, 5):
            piece = Piece(False, i, j)
            pieces.append(piece)
    for i in range(4, 6):
        for j in range(1, 5):
            pieces.append(None)
    for i in range(6, 9):
        for j in range(1, 5):
            piece = Piece(True, i, j)
            pieces.append(piece)

    # Initialize the squares, the squares are drawn in Square.__init__ since the square background never changes
    for i in range(1, 9):
        for j in range(1, 5):
            square = Square(i, j, connections_dict[(i, j)], pieces[i * 4 - 5 + j])
            squares[i - 1].append(square)

    for i in squares:
        for j in i:
            if j.piece is not None:
                j.piece.draw_piece()


class Piece:
    def __init__(self, color, row, pos, king=False, highlight=False):
        # "color": False = red, True = Black
        # "row": Rows are numbered 1 to 8, top to bottom
        # "pos": Square in each row, 1 to 4, left to right
        # "highlight": Whether or not the player has highlighted the piece (about to move it)

        self.color = color
        self.row = row
        self.pos = pos
        self.king = king
        self.highlight = highlight

        # Initialize the templates for the three parts of a piece: the piece itself, and symbols for king or highlighted

        if self.row % 2 == 1:  # If piece is on rows 1, 3, 5, 7
            piece_position = gr.Point(self.pos * 100 + 25, self.row * 50 + 25)
        elif self.row % 2 == 0:  # If piece is on rows 2, 4, 6, 8
            piece_position = gr.Point(self.pos * 100 - 25, self.row * 50 + 25)
        self.piece_template = (gr.Circle(piece_position, 20))

        self.king_template = gr.Text(piece_position, "K")
        self.king_template.setTextColor("gold")
        self.king_template.setSize(27)
        self.king_template.setStyle("bold")

        self.highlight_template = gr.Circle(piece_position, 22)
        self.highlight_template.setWidth(4)
        self.highlight_template.setOutline("gold")

    def draw_piece(self):
        # Update the templates for the three parts of a piece: the piece itself, and symbols for king or highlighted

        self.piece_template.undraw()
        self.king_template.undraw()
        self.highlight_template.undraw()

        if self.row % 2 == 1:  # If piece is on rows 1, 3, 5, 7
            piece_position = gr.Point(self.pos * 100 + 25, self.row * 50 + 25)
        elif self.row % 2 == 0:  # If piece is on rows 2, 4, 6, 8
            piece_position = gr.Point(self.pos * 100 - 25, self.row * 50 + 25)
        self.piece_template = (gr.Circle(piece_position, 20))

        self.king_template = gr.Text(piece_position, "K")
        self.king_template.setTextColor("gold")
        self.king_template.setSize(27)
        self.king_template.setStyle("bold")

        self.highlight_template = gr.Circle(piece_position, 22)
        self.highlight_template.setWidth(4)
        self.highlight_template.setOutline("gold")

        # Converts piece attributes into graphics.py objects and draws them

        if self.color is False:
            self.piece_template.setFill("red3")
        elif self.color is True:
            self.piece_template.setFill("Black")
        self.piece_template.undraw()
        self.piece_template.draw(win)

        if self.king:
            self.king_template.undraw()
            self.king_template.draw(win)
        if not self.king:
            self.king_template.undraw()

        if self.highlight:
            self.highlight_template.undraw()
            self.highlight_template.draw(win)
        if not self.highlight:
            self.highlight_template.undraw()

    def undraw_piece(self):
        self.piece_template.undraw()
        self.king_template.undraw()
        self.highlight_template.undraw()


class Square:
    def __init__(self, row, pos, connections, piece, highlight=False):
        # row and pos specify position of square (same convention as position of piece)
        # highlight shows if square is highlighted, this is used when a piece is clicked, to show possible moves
        # connections is dictionary with {connection type <int>: connected square <tuple>}
        # connected squares are tuples specified with row and pos (position in row); (row, pos): 1 to 8, 1 to 4
        # Connection type ranges from 0 to 3: top right, bottom right, bottom left, top left: from perspective of self
        # piece is which piece currently occupies this square

        self.row = row
        self.pos = pos
        self.highlight = highlight
        self.connections = connections
        self.piece = piece

        if self.row % 2 == 1:  # If square is on rows 1, 3, 5, 7
            self.position = gr.Point(self.pos * 100 + 25, self.row * 50 + 25)
        elif self.row % 2 == 0:  # If square is on rows 2, 4, 6, 8
            self.position = gr.Point(self.pos * 100 - 25, self.row * 50 + 25)

        shading = gr.Rectangle(gr.Point(self.position.getX() - 25, self.position.getY() - 25),
                               gr.Point(self.position.getX() + 25, self.position.getY() + 25))
        shading.setFill("grey")
        shading.draw(win)

        # Initialize the highlight template for future use
        self.highlight_template = gr.Circle(self.position, 3)
        self.highlight_template.setWidth(6)
        self.highlight_template.setOutline("gold")

    def draw_square(self):
        # Need to draw highlight on square (if there is one)

        if self.highlight:
            self.highlight_template.undraw()
            self.highlight_template.draw(win)
        else:
            self.highlight_template.undraw()


def click_get_square(point):
    # Figure out which square was clicked from coordinates of mouse click
    # Returns square as tuple: row, pos (same convention as piece position)

    x = point.getX()
    y = point.getY()

    # check if coordinates are in board
    if not (50 < x < 450 and 50 < y < 450):
        return None

    # Convert coordinates to sections (50 x 50 area of board), then convert to row and position in row
    x = round((x / 50) - 0.5)
    y = round((y / 50) - 0.5)

    row = y
    if row % 2 == 1:
        if x % 2 == 1:
            return None
        if x % 2 == 0:
            pos = x / 2
    if row % 2 == 0:
        if x % 2 == 1:
            pos = (x + 1) / 2
        if x % 2 == 0:
            return None

    return row, int(pos)


def search(start, squares_list):
    # square_list is whether searching "squares" or "virtual_squares"

    # start is which square <Square> to start the search from
    # search() outputs dictionary {possible_move_1 <Square>: [captured pieces <Square>, ...], ...}

    # Stores the possible moves as they're discovered: [{possible_move_1 <Square>: captured pieces <Square>}, ...]
    moves = {}

    # Make sure that if the piece isn't a king, that it doesn't jump backwards in the middle of
    # a series of jumps
    # Only need to check this extra thing if the piece isn't a king
    if start.piece.king is False:
        # If the piece is red
        if start.piece.color is False:
            # Can only jump downwards (forwards from red's perspective)
            allowed_jumps = [1, 2]
        # If the piece is black
        if start.piece.color is True:
            # Can only jump upwards (forwards from black's perspective)
            allowed_jumps = [0, 3]
    else:
        allowed_jumps = [0, 1, 2, 3]

    # Search for all possible moves
    # Loop through all the possible connections of the highlighted square ("start")
    for i in start.connections:
        if i in allowed_jumps:
            connection = start.connections[i]
            if connection is not None:
                connection_square = squares_list[connection[0] - 1][connection[1] - 1]
                # If there is no piece on the connected square, it is a possible move
                if connection_square.piece is None:
                    moves.update({connection_square: [None]})
                # if there is a piece, check if it's of the opposite color
                elif connection_square.piece.color is not start.piece.color:
                    # Reuse the previous connection direction so it only tries to capture in a straight line
                    other_side = connection_square.connections[i]
                    # If there is a square on the other side (not reached edge of board)
                    if other_side is not None:
                        other_side_square = squares_list[other_side[0] - 1][other_side[1] - 1]
                        # And check if the square on the other side is empty, to be able to jump it
                        if other_side_square.piece is None:
                            moves.update({other_side_square: [connection_square]})

                            # Figure out the rest of the possible jumps (similar to the main for loop, but only looking
                            # for jumps, not regular moves)

                            visited = []

                            def find_all_jumps(start_from, previous_captured):
                                end_reached_overall = True
                                for i in start_from.connections:
                                    if i in allowed_jumps:
                                        end_reached = False
                                        all_captured = previous_captured.copy()
                                        new_connection = start_from.connections[i]
                                        if new_connection is not None:
                                            new_connection_square = squares_list[new_connection[0] - 1] \
                                                [new_connection[1] - 1]
                                            if new_connection_square not in visited:
                                                if new_connection_square.piece is not None:
                                                    if new_connection_square.piece.color is not start.piece.color:
                                                        new_other_side = new_connection_square.connections[i]
                                                        if new_other_side is not None:
                                                            new_other_side_square = \
                                                                squares_list[new_other_side[0] - 1] \
                                                                    [new_other_side[1] - 1]
                                                            if new_other_side_square.piece is None:
                                                                all_captured.append(new_connection_square)
                                                                moves.update({new_other_side_square: all_captured})
                                                                visited.append(new_connection_square)
                                                            else:
                                                                end_reached = True
                                                        else:
                                                            end_reached = True
                                                    else:
                                                        end_reached = True
                                                else:
                                                    end_reached = True
                                            else:
                                                end_reached = True
                                        else:
                                            end_reached = True
                                    else:
                                        end_reached = True

                                    if end_reached is False:
                                        end_reached_overall = False
                                        # Recursion if needed
                                        find_all_jumps(new_other_side_square, all_captured)
                                if end_reached_overall:
                                    return

                            find_all_jumps(other_side_square, [connection_square])

    # Make sure the possible moves are limited based on whether the piece is a king, and which color the piece is
    if start.piece.king is False:
        # If the piece is red
        if start.piece.color is False:
            for i in moves.copy():
                if i.row < start.row:
                    moves.pop(i)

        # If the piece is black
        if start.piece.color is True:
            for i in moves.copy():
                if i.row > start.row:
                    moves.pop(i)

    # Implement the force jump rule for each piece (also need implementation for all pieces, to see if any of them
    # have an opportunity to jump), this is done elsewhere
    jump_available = False
    for i in moves.values():
        if i != [None]:
            jump_available = True
            break
    if jump_available:
        for i in moves.copy():
            if moves[i] == [None]:
                moves.pop(i)

    # search() outputs dictionary {possible_move_1 <Square>: [captured pieces <Square>, ...], ...}
    return moves


# Move a piece from the old square to the new square
def move(old_square, new_square, captured):
    if captured is not None:
        for i in captured:
            if i is not None:
                if i.piece is not None:
                    i.piece.undraw_piece()
                    i.piece = None

    new_square.piece = old_square.piece
    new_square.piece.row = new_square.row
    new_square.piece.pos = new_square.pos

    old_square.piece = None


# Computer makes a move
def computer_move(have_to_move):
    # If there are force jumps, pick the one that captures the most pieces
    if have_to_move:
        # best_jumps = [[start_square, {end_square: [captured, ...]}], ...]
        best_jumps = []
        # Default only expect jumps with 1 captured piece
        most_jump_length = 1

        for start_square in have_to_move:
            options = search(start_square, squares)
            for end_square in options:
                if len(options[end_square]) == most_jump_length:
                    best_jumps.append([start_square, {end_square: options[end_square]}])
                elif len(options[end_square]) > most_jump_length:
                    most_jump_length = len(options[end_square])
                    best_jumps.clear()
                    best_jumps.append([start_square, {end_square: options[end_square]}])

        jump_chosen = random.randrange(0, len(best_jumps))
        start_square = best_jumps[jump_chosen][0]
        end_and_captured = list(best_jumps[jump_chosen][1].items())
        end_square = end_and_captured[0][0]
        captured = end_and_captured[0][1]

    # If no force jumps, use this algorithm to figure out how to move
    # Essentially, this algorithm checks for each move the computer might do right now, what is the average number
    # of pieces that the computer could gain / lose
    # TODO Make sure the computer only stops looking forward on a move that has no captures, to account for sets of
    # TODO captures and capture backs, otherwise the evaluation of the moves will be skewed
    else:
        # These are all the possible moves that the computer must look at:
        # moves = [[start_square, {end_square: [captured, ...], ...}], ...]
        moves = []
        for row in squares:
            for square in row:
                if square.piece is not None:
                    if square.piece.color is False:
                        if search(square, squares) != {}:
                            moves.append([square, search(square, squares)])

        # Check for possible captures that are 1 move away (first step in intelligence)
        to_delete = []  # Delete them because they allow a capture by the opponent
        for i, whole_move in enumerate(moves):
            start_square = whole_move[0]
            for j, end_square in enumerate(whole_move[1]):
                # Generate the virtual objects (objects that are manipulated to see what happens)
                virtual_squares = [[[], [], [], []],
                                   [[], [], [], []],
                                   [[], [], [], []],
                                   [[], [], [], []],
                                   [[], [], [], []],
                                   [[], [], [], []],
                                   [[], [], [], []],
                                   [[], [], [], []]]
                for virt_i, row in enumerate(squares):
                    for virt_j, square in enumerate(row):
                        if square.piece is not None:
                            virtual_piece = Piece(square.piece.color, square.piece.row, square.piece.pos,
                                                  square.piece.king, square.piece.highlight)
                            virtual_squares[virt_i][virt_j] = Square(square.row, square.pos, square.connections,
                                                                     virtual_piece, square.highlight)
                        else:
                            virtual_squares[virt_i][virt_j] = Square(square.row, square.pos, square.connections,
                                                                     None, square.highlight)
                virtual_moves = []
                for virtual_row in virtual_squares:
                    for virtual_square in virtual_row:
                        if virtual_square.piece is not None:
                            if virtual_square.piece.color is False:
                                if search(virtual_square, virtual_squares) != {}:
                                    virtual_moves.append([virtual_square, search(virtual_square, virtual_squares)])

                virtual_start = virtual_moves[i][0]
                virtual_end = list(virtual_moves[i][1].keys())[j]
                virtual_captured = list(virtual_moves[i][1].values())[j]
                move(virtual_start, virtual_end, virtual_captured)
                # Figure out if the move is good or not (does it let opponent capture a piece?)
                for virtual_row in virtual_squares:
                    for virtual_square in virtual_row:
                        if virtual_square.piece is not None:
                            if virtual_square.piece.color is True:
                                opponent_moves = search(virtual_square, virtual_squares)
                                for opponent_move in opponent_moves:
                                    if opponent_moves[opponent_move] != [None]:
                                        to_delete.append((start_square, end_square))

        num_possible_moves = 0
        for whole_move in moves:
            num_possible_moves += len(whole_move[1])

        # If there are any moves possible that don't result in a capture
        if len(to_delete) < num_possible_moves:
            for bad_start, bad_end in to_delete:
                for whole_move in moves:
                    if whole_move[0].row == bad_start.row and whole_move[0].pos == bad_start.pos:
                        for i, end_square in enumerate(whole_move[1].copy()):
                            if end_square.row == bad_end.row and end_square.pos == bad_end.pos:
                                whole_move[1].pop(end_square)

        # Pick random move of out ones that survived search
        piece_has_moves = False
        while piece_has_moves is False:
            move_chosen = random.randrange(0, len(moves))
            if moves[move_chosen][1] != {}:
                piece_has_moves = True
        start_square = moves[move_chosen][0]
        possible_end_and_captured = moves[move_chosen][1]
        possible_end_squares = list(possible_end_and_captured.keys())
        end_square = possible_end_squares[random.randrange(0, len(possible_end_squares))]
        captured = possible_end_and_captured[end_square]

    move(start_square, end_square, captured)

    # Check to make the piece king if necessary
    # If piece is red
    if end_square.piece.color is False:
        if end_square.row == 8:
            end_square.piece.king = True
    # If piece is black
    if end_square.piece.color is True:
        if end_square.row == 1:
            end_square.piece.king = True


# Initialize game
# squares list is actively used, pieces array is for initialization purposes only
squares = [[],
           [],
           [],
           [],
           [],
           [],
           [],
           []]

pieces = []
initialize_board()

player_won, computer_won = False, False

# Black moves first
turn = True

# Main game loop
while True:
    # Erase old highlights and displayed connections (from last loop)
    for i in squares:
        for j in i:
            if j is not None:
                j.highlight = False
                if j.piece is not None:
                    j.piece.highlight = False

    # Update the drawing of everything in between mouse clicks
    for i in squares:
        for j in i:
            j.draw_square()
            if j.piece is not None:
                j.piece.draw_piece()

    # See if any jumps are available (for force jump rule)
    squares_with_jump = []
    for i in squares:
        for j in i:
            if j.piece is not None:
                # Only need to check for available jumps for the color who's turn it is
                if j.piece.color == turn:
                    check_possible_moves = search(j, squares)
                    for i in check_possible_moves.values():
                        if i != [None]:
                            squares_with_jump.append(j)
                            break

    # If it's the player's turn
    if turn is True:
        # Check if the player is able to move
        able = False
        for i in squares:
            for j in i:
                if j.piece is not None:
                    if j.piece.color is True:
                        if search(j, squares) != {}:
                            able = True
                            break

        if able is False:
            computer_won = True
            break

        # Get the coordinates of mouse click, and converts it to square on board, <None> if not on a playable square
        click = win.getMouse()
        click_square_coordinates = click_get_square(click)

        # Draw the new connections and highlights
        if click_square_coordinates is not None:
            # Read the connections associated with the square
            click_square_object = squares[click_square_coordinates[0] - 1][click_square_coordinates[1] - 1]

            # If there are any squares with jumps available, they are the only allowed moves,
            # otherwise if no jumps available, all moves allowed
            if squares_with_jump:
                if click_square_object in squares_with_jump:
                    allowed = True
                else:
                    allowed = False
            else:
                allowed = True

            if allowed:
                # Highlight the piece on the square that was clicked (only if there is a piece present)
                if click_square_object.piece is not None:
                    # Check if the piece clicked is of the color who's turn it is to move
                    if click_square_object.piece.color == turn:
                        click_square_object.piece.highlight = True

                        # Highlight all the possible moves
                        possible_moves = search(click_square_object, squares)
                        for i in possible_moves:
                            i.highlight = True

                        # Update the drawing of everything on between mouse clicks
                        for i in squares:
                            for j in i:
                                j.draw_square()
                                if j.piece is not None:
                                    j.piece.draw_piece()

                        # Detect whether / where to move the selected piece
                        second_click = win.getMouse()
                        second_click_square_coordinates = click_get_square(second_click)
                        if second_click_square_coordinates is not None:
                            second_click_square_object = \
                                squares[second_click_square_coordinates[0] - 1][second_click_square_coordinates[1] - 1]
                            if second_click_square_object in possible_moves:
                                move(click_square_object, second_click_square_object,
                                     possible_moves[second_click_square_object])

                                # Flip who's turn it is
                                turn = not turn

                                # Check to make the piece king if necessary
                                # If piece is red
                                if second_click_square_object.piece.color is False:
                                    if second_click_square_object.row == 8:
                                        second_click_square_object.piece.king = True
                                # If piece is black
                                if second_click_square_object.piece.color is True:
                                    if second_click_square_object.row == 1:
                                        second_click_square_object.piece.king = True
    # If it's the computer's turn
    else:
        # Check if the computer is able to move
        able = False
        for i in squares:
            for j in i:
                if j.piece is not None:
                    if j.piece.color is False:
                        if search(j, squares) != {}:
                            able = True
                            break

        if able is False:
            player_won = True
            break

        computer_move(squares_with_jump)

        # Flip who's turn it is
        turn = not turn

if player_won:
    player_won_text = gr.Text(gr.Point(250, 25), "Player Won")
    player_won_text.setSize(16)
    player_won_text.draw(win)
elif computer_won:
    computer_won_text = gr.Text(gr.Point(250, 25), "Computer Won")
    computer_won_text.setSize(16)
    computer_won_text.setTextColor("red3")
    computer_won_text.draw(win)

win.getKey()
