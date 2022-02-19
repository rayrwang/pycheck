# Jan 24, 2022

# Modules required:
# graphics.py: http://www.cs.uky.edu/~keen/help/Zelle-graphics-reference.pdf

import graphics as gr
import random
from collections import deque

# The game board
win = gr.GraphWin("Checkers AI", 650, 500, autoflush=False)


def initialize_board():
    # Draw the rows of the game board
    rows = []
    for row_coordinates in range(50, 500, 50):
        new_row = gr.Line(gr.Point(50, row_coordinates), gr.Point(450, row_coordinates))
        rows.append(new_row)
    for row in rows:
        row.draw(win)

    # Draw the columns
    columns = []
    for column_coordinates in range(50, 500, 50):
        new_columns = gr.Line(gr.Point(column_coordinates, 50), gr.Point(column_coordinates, 450))
        columns.append(new_columns)
    for column in columns:
        column.draw(win)

    del rows, columns

    # Text that says "Debug"
    debug_heading = gr.Text(gr.Point(575, 25), "Debug")
    debug_heading.setSize(18)
    debug_heading.setStyle("bold")
    debug_heading.draw(win)

    divider = gr.Line(gr.Point(500, 0), gr.Point(500, 500))
    divider.draw(win)

    # This code will generate the connections between the squares on the board
    # This can be done manually, but it's arguably more interesting to do it algorithmically

    # connections_dict is nested dictionary with {square <tuple>: {connection type <int>: connected square <tuple>}}
    # Squares and connected squares are tuples specified with row and pos (position in row), (row, pos): 1 to 8, 1 to 4
    # Connection type ranges from 0 to 3: top right, bottom right, bottom left, top left: from perspective of self
    connections_dict = {}
    # Give an index for each square
    for row in range(1, 9):
        for position_in_row in range(1, 5):
            connections_dict[(row, position_in_row)] = {}

    # There are 8 types of squares: Those on each of the 4 edges,
    # upper right and lower left corners, and the middle ones on even and odd rows

    for square in connections_dict:
        row = square[0]
        pos = square[1]  # Position in row
        # Upper edge squares (excluding top right)
        if row == 1 and pos in (1, 2, 3):
            connections_dict[square] = {0: None,
                                        1: (row + 1, pos + 1),
                                        2: (row + 1, pos),
                                        3: None}
        # Top right square
        if row == 1 and pos == 4:
            connections_dict[square] = {0: None,
                                        1: None,
                                        2: (row + 1, pos),
                                        3: None}
        # Left edge excluding bottom left
        if row in (2, 4, 6) and pos == 1:
            connections_dict[square] = {0: (row - 1, pos),
                                        1: (row + 1, pos),
                                        2: None,
                                        3: None}
        # Center squares on even rows
        if row in (2, 4, 6) and pos in (2, 3, 4):
            connections_dict[square] = {0: (row - 1, pos),
                                        1: (row + 1, pos),
                                        2: (row + 1, pos - 1),
                                        3: (row - 1, pos - 1)}
        # Center squares on odd rows
        if row in (3, 5, 7) and pos in (1, 2, 3):
            connections_dict[square] = {0: (row - 1, pos + 1),
                                        1: (row + 1, pos + 1),
                                        2: (row + 1, pos),
                                        3: (row - 1, pos)}
        # Right edge
        if row in (3, 5, 7) and pos == 4:
            connections_dict[square] = {0: None,
                                        1: None,
                                        2: (row + 1, pos),
                                        3: (row - 1, pos)}
        # Bottom left square
        if row == 8 and pos == 1:
            connections_dict[square] = {0: (row - 1, pos),
                                        1: None,
                                        2: None,
                                        3: None}
        # Bottom row
        if row == 8 and pos in (2, 3, 4):
            connections_dict[square] = {0: (row - 1, pos),
                                        1: None,
                                        2: None,
                                        3: (row - 1, pos - 1)}

    # Initialize and draw the starting pieces
    for piece_row in range(1, 4):
        for piece_pos in range(1, 5):
            piece = Piece(False, piece_row, piece_pos)
            pieces.append(piece)
    for piece_row in range(4, 6):
        for piece_pos in range(1, 5):
            pieces.append(None)
    for piece_row in range(6, 9):
        for piece_pos in range(1, 5):
            piece = Piece(True, piece_row, piece_pos)
            pieces.append(piece)

    # Initialize the squares, the squares are drawn in Square.__init__ since the square background never changes
    for square_row in range(1, 9):
        for square_pos in range(1, 5):
            square = Square(square_row, square_pos,
                            connections_dict[(square_row, square_pos)], pieces[square_row * 4 - 5 + square_pos])
            squares[square_row - 1].append(square)


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
        else:  # If piece is on rows 2, 4, 6, 8
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
        else:  # If piece is on rows 2, 4, 6, 8
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


# I guess this function is kind of like deepcopy, but I couldn't figure out how to make deepcopy work
def duplicate(squares_list):
    virtual_squares = [[[], [], [], []],
                       [[], [], [], []],
                       [[], [], [], []],
                       [[], [], [], []],
                       [[], [], [], []],
                       [[], [], [], []],
                       [[], [], [], []],
                       [[], [], [], []]]
    for i, row in enumerate(squares_list):
        for j, square in enumerate(row):
            if square.piece is not None:
                virtual_piece = Piece(square.piece.color, square.piece.row, square.piece.pos,
                                      square.piece.king, square.piece.highlight)
                virtual_squares[i][j] = Square(square.row, square.pos, square.connections,
                                               virtual_piece, square.highlight)
            else:
                virtual_squares[i][j] = Square(square.row, square.pos, square.connections,
                                               None, square.highlight)
    return virtual_squares


# Finds all the possible moves for a certain side (red or black), from a certain board position (squares_list)
def find_moves(squares_list, side=False):
    # Figure out if there are any force jumps, and what they are
    force_jumps = []
    for row in squares_list:
        for square in row:
            if square.piece is not None:
                # Only need to check for available jumps for the color whose turn it is
                if square.piece.color == side:
                    for captured_list in search(square, squares_list).values():
                        if captured_list != [None]:  # If there are possible captures for the piece on this square
                            force_jumps.append(square)
                            break

    moves = []
    if force_jumps:
        for square in force_jumps:
            moves.append([square, search(square, squares_list)])
    else:
        for row in squares_list:
            for square in row:
                if square.piece is not None:
                    if square.piece.color == side:
                        if search(square, squares_list) != {}:
                            moves.append([square, search(square, squares_list)])

    # Flatten the list of possible moves (so it's easier to work with)
    moves_flat = []
    for whole_move in moves:
        start = whole_move[0]
        end_and_captured = whole_move[1]
        for end in end_and_captured:
            captured = end_and_captured[end]
            moves_flat.append([start, end, captured])

    return moves_flat


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
        else:
            pos = x / 2
    else:
        if x % 2 == 1:
            pos = (x + 1) / 2
        else:
            return None

    return row, int(pos)


# Finds all the possible moves for the piece on a certain square
def search(start, squares_list):
    # square_list is whether searching "squares" or "virtual_squares"

    # start is which square <Square> to start the search from
    # search() outputs dictionary {possible_move_1 <Square>: [captured pieces <Square>, ...], ...}

    # Stores the possible moves as they're discovered: [{possible_move_1 <Square>: captured pieces <Square>}, ...]
    moves = {}

    # Make sure that if the piece isn't a king, that it doesn't jump backwards
    # Only need to check this extra thing if the piece isn't a king
    if start.piece.king is False:
        # If the piece is red
        if start.piece.color is False:
            # Can only jump downwards (forwards from red's perspective)
            allowed_jumps = [1, 2]
        # If the piece is black
        else:
            # Can only jump upwards (forwards from black's perspective)
            allowed_jumps = [0, 3]
    else:
        allowed_jumps = [0, 1, 2, 3]

    # Search for all possible moves
    # Loop through all the possible connections of the highlighted square ("start")
    for connection_type in start.connections:
        if connection_type in allowed_jumps:
            connection = start.connections[connection_type]
            if connection is not None:
                connection_square = squares_list[connection[0] - 1][connection[1] - 1]
                # If there is no piece on the connected square, it is a possible move
                if connection_square.piece is None:
                    moves.update({connection_square: [None]})
                # if there is a piece, check if it's of the opposite color
                elif connection_square.piece.color is not start.piece.color:
                    # Reuse the previous connection direction so it only tries to capture in a straight line
                    other_side = connection_square.connections[connection_type]
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
                                for connection_type in start_from.connections:
                                    if connection_type in allowed_jumps:
                                        end_reached = False
                                        all_captured = previous_captured.copy()
                                        new_connection = start_from.connections[connection_type]
                                        if new_connection is not None:
                                            new_connection_square = squares_list[new_connection[0] - 1] \
                                                [new_connection[1] - 1]
                                            if new_connection_square not in visited:
                                                if new_connection_square.piece is not None:
                                                    if new_connection_square.piece.color is not start.piece.color:
                                                        new_other_side = new_connection_square.connections[
                                                            connection_type]
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
                                        # Recursion if needed
                                        find_all_jumps(new_other_side_square, all_captured)

                            find_all_jumps(other_side_square, [connection_square])

    # Implement the force jump rule for each piece (also need implementation for all pieces, to see if any of them
    # have an opportunity to jump), this is done elsewhere
    jump_available = False
    for any_captured in moves.values():
        if any_captured != [None]:
            jump_available = True
            break
    if jump_available:
        for move in moves.copy():
            if moves[move] == [None]:
                moves.pop(move)

    # search() outputs dictionary {possible_move_1 <Square>: [captured pieces <Square>, ...], ...}
    return moves


# Move a piece from the old square to the new square
def move_piece(old_square, new_square, captured, squares_list):
    # Figure out which squares in squares_list are representative of the squares to be moved
    # This means find squares which aren't necessarily the same object, but have the same attributes (row and position)
    captured_copy = []
    for row in squares_list:
        for square in row:
            if square.row == old_square.row and square.pos == old_square.pos:
                old_square = square
                continue
            if square.row == new_square.row and square.pos == new_square.pos:
                new_square = square
                continue
            if captured != [None]:
                for captured_square in captured:
                    if square.row == captured_square.row and square.pos == captured_square.pos:
                        captured_copy.append(square)
                        continue

    if captured_copy is not None:
        for captured_square in captured_copy:
            if captured_square is not None:
                if captured_square.piece is not None:
                    captured_square.piece.undraw_piece()
                    captured_square.piece = None

    new_square.piece = old_square.piece
    new_square.piece.row = new_square.row
    new_square.piece.pos = new_square.pos

    old_square.piece = None


# Computer makes a move (with intelligence)
def computer_move():
    # Essentially, this algorithm checks for each move the computer might do right now, what is the average number
    # of pieces that the computer could gain / lose

    # These are all the possible moves that the computer must look at:
    # moves = [[start_square, end_square, [captured, ...]], ...]
    moves = find_moves(squares)

    moves_scored = []  # Holds a score for how good a move is
    # Initialize moves_scored (basically sort of flatten moves list)
    # moves_scored = [[[start_square, end_square, [captured, ...]], [score, total]], ...]
    for move in moves:
        moves_scored.append([move, [0, 0]])

    # TODO Minimax algorithm? So computer also takes into account what the player will probably do, not just assigning
    # TODO equal probability to each move

    # This is the basic object that the computer uses to look into possible futures
    class Position:
        def __init__(self, move_index, virtual_squares, turn, depth):
            self.move_index = move_index  # Which original move's tree is this node part of?
            self.board = virtual_squares
            self.depth = depth
            self.turn = turn
            self.moves = find_moves(virtual_squares, turn)

    # Search into the future to see how good a move is, communicate by updating moves_scored
    to_search = deque()
    # Start by populating the search deque with the moves that the computer can make right now
    for move_index, starting_move in enumerate(moves_scored):
        new_virtual_squares = duplicate(squares)
        move_piece(starting_move[0][0], starting_move[0][1], starting_move[0][2], new_virtual_squares)
        to_search.append(Position(move_index, new_virtual_squares, True, 1))

    while True:
        if len(to_search) == 0:
            break

        # Start searching through the deque
        current = to_search.popleft()

        # Analyze the current board situation and adjust moves_scored accordingly
        # Looking for how many pieces each side has, and has one side lost yet

        red_pieces_count = 0
        black_pieces_count = 0
        for row in current.board:
            for square in row:
                if square.piece is not None:
                    if square.piece.color is False:
                        if square.piece.king is True:
                            red_pieces_count += 4
                        else:
                            red_pieces_count += 1
                    if square.piece.color is True:
                        if square.piece.king is True:
                            black_pieces_count += 4
                        else:
                            black_pieces_count += 1

        # Update score
        moves_scored[current.move_index][1][0] += (red_pieces_count - black_pieces_count)
        # Increment total # of scores (for calculating average later)
        moves_scored[current.move_index][1][1] += 1

        # If there are captures, these need to be looked at, even if the default search depth is exceeded
        # Otherwise the results will be skewed since a capture may be detected, but not the recapture afterwards
        capturing = False
        for move in current.moves:
            if move[2] != [None]:
                capturing = True
                break

        # Only generate more moves if certain depth hasn't been reached yet:
        if current.depth <= 1 or capturing:
            # Generate the child positions:
            for move in current.moves:
                new_virtual_squares = duplicate(current.board)
                move_piece(move[0], move[1], move[2], new_virtual_squares)
                to_search.append(Position(current.move_index, new_virtual_squares,
                                          not current.turn, current.depth + 1))

        # FIXME Fix high memory usage, need to deallocate objects somehow?
        # TODO ^ Is it a memory leak, or just a function of rising board complexity? Do testing

        # TODO Use multiprocessing and algorithm optimization to search more efficiently / deeper

    # Calculate averages
    for move in moves_scored:
        score, total = move[1].copy()
        move[1] = score / total

    # Display moves_scored
    for move in moves_display:
        if move is not None:
            move.undraw()

    moves_display.clear()
    line = 60
    for move in moves_scored:
        text = gr.Text(gr.Point(575, line), f"{move[0][0].row} {move[0][0].pos} to "
                                            f"{move[0][1].row} {move[0][1].pos} : {move[1]:.2f}")
        text.setSize(10)
        moves_display.append(text)
        line += 15
    for move in moves_display:
        move.draw(win)

    # Pick out the move(s) with the highest score in moves_scored, and pick random move from the move(s)
    highest = None
    best_moves = []
    for i, move in enumerate(moves_scored):
        if highest is None:
            highest = moves_scored[i][1]
            best_moves.append(move)
        else:
            if moves_scored[i][1] == highest:
                best_moves.append(move)
            elif moves_scored[i][1] > highest:
                highest = moves_scored[i][1]
                best_moves.clear()
                best_moves.append(move)

    move_chosen = best_moves[random.randrange(0, len(best_moves))]
    start_square = move_chosen[0][0]
    end_square = move_chosen[0][1]
    captured = move_chosen[0][2]

    move_piece(start_square, end_square, captured, squares)

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

moves_display = []

player_won, computer_won = False, False

# Black moves first
turn = True
# TODO Make color selection functionality
# Main game loop
count = 0
while True:
    # Erase old highlights and displayed connections (from last loop)
    for row in squares:
        for square in row:
            if square is not None:
                square.highlight = False
                if square.piece is not None:
                    square.piece.highlight = False

    # Update the drawing of everything in between mouse clicks
    for row in squares:
        for square in row:
            square.draw_square()
            if square.piece is not None:
                square.piece.draw_piece()
    win.update()

    # See if any jumps are available (for force jump rule)
    squares_with_jump = []
    for row in squares:
        for square in row:
            if square.piece is not None:
                # Only need to check for available jumps for the color whose turn it is
                if square.piece.color == turn:
                    for captured_list in search(square, squares).values():
                        if captured_list != [None]:  # If there are possible captures for the piece on this square
                            squares_with_jump.append(square)
                            break

    # If it's the player's turn
    if turn is True:
        # Check if the player is able to move
        able = False
        for row in squares:
            for square in row:
                if square.piece is not None:
                    if square.piece.color is True:
                        if search(square, squares) != {}:
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
                        for move in possible_moves:
                            move.highlight = True

                        # Update the drawing of everything in between mouse clicks
                        for row in squares:
                            for square in row:
                                square.draw_square()
                                if square.piece is not None:
                                    square.piece.draw_piece()
                        win.update()

                        # Detect whether / where to move the selected piece
                        second_click = win.getMouse()
                        second_click_square_coordinates = click_get_square(second_click)
                        if second_click_square_coordinates is not None:
                            second_click_square_object = \
                                squares[second_click_square_coordinates[0] - 1][second_click_square_coordinates[1] - 1]
                            if second_click_square_object in possible_moves:
                                move_piece(click_square_object, second_click_square_object,
                                           possible_moves[second_click_square_object], squares)

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
        for row in squares:
            for square in row:
                if square.piece is not None:
                    if square.piece.color is False:
                        if search(square, squares) != {}:
                            able = True
                            break

        if able is False:
            player_won = True
            break

        computer_move()

        # Flip whose turn it is
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
