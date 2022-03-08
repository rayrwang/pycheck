# Jan 24, 2022

# Modules required:
# graphics.py: http://www.cs.uky.edu/~keen/help/Zelle-graphics-reference.pdf

import graphics as gr
import random

# The game board
game_board = gr.GraphWin("Checkers AI", 650, 500, autoflush=False)


def initialize_board():
    # Draw the rows of the game board
    rows = []
    for row_coordinates in range(50, 500, 50):
        new_row = gr.Line(gr.Point(50, row_coordinates), gr.Point(450, row_coordinates))
        rows.append(new_row)
    for row in rows:
        row.draw(game_board)

    # Draw the columns
    columns = []
    for column_coordinates in range(50, 500, 50):
        new_columns = gr.Line(gr.Point(column_coordinates, 50), gr.Point(column_coordinates, 450))
        columns.append(new_columns)
    for column in columns:
        column.draw(game_board)

    # Text that says "Debug"
    debug_heading = gr.Text(gr.Point(575, 25), "Debug")
    debug_heading.setSize(18)
    debug_heading.setStyle("bold")
    debug_heading.draw(game_board)

    debug_info = gr.Text(gr.Point(550, 445),
                         '''
                         row column to row column : score
                         
                         rows numbered 1 to 8, top to bottom
                         
                         columns numbered 1 to 4,
                         left to right,
                         for each playable (gray) square
                         
                         score is from the player's perspective
                         (+ = player is winning)
                         ''')
    debug_info.setSize(6)
    debug_info.draw(game_board)

    divider = gr.Line(gr.Point(500, 0), gr.Point(500, 500))
    divider.draw(game_board)

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

    pieces = []
    # If the player is playing red
    if player_color is False:
        # Initialize and draw the starting pieces
        for piece_row in range(1, 4):
            for piece_pos in range(1, 5):
                piece = Piece(True, piece_row, piece_pos, real=True)
                pieces.append(piece)
        for piece_row in range(4, 6):
            for piece_pos in range(1, 5):
                pieces.append(None)
        for piece_row in range(6, 9):
            for piece_pos in range(1, 5):
                piece = Piece(False, piece_row, piece_pos, real=True)
                pieces.append(piece)
    # If the player is playing black
    if player_color is True:
        # Initialize and draw the starting pieces
        for piece_row in range(1, 4):
            for piece_pos in range(1, 5):
                piece = Piece(False, piece_row, piece_pos, real=True)
                pieces.append(piece)
        for piece_row in range(4, 6):
            for piece_pos in range(1, 5):
                pieces.append(None)
        for piece_row in range(6, 9):
            for piece_pos in range(1, 5):
                piece = Piece(True, piece_row, piece_pos, real=True)
                pieces.append(piece)

    # Initialize the squares, the squares are drawn in Square.__init__ since the square background never changes
    for square_row in range(1, 9):
        for square_pos in range(1, 5):
            square = Square(square_row, square_pos, connections_dict[(square_row, square_pos)],
                            pieces[square_row * 4 - 5 + square_pos], real=True)
            squares[square_row - 1].append(square)


class Piece:
    def __init__(self, color, row, pos, king=False, highlight=False, real=False):
        # "color": False = red, True = Black
        # "row": Rows are numbered 1 to 8, top to bottom
        # "pos": Square in each row, 1 to 4, left to right
        # "highlight": Whether the player has highlighted the piece (about to move it)
        # "real': Whether the piece is on the real board, or is just part of the computer's thinking process

        self.color = color
        self.row = row
        self.pos = pos
        self.king = king
        self.highlight = highlight
        self.real = real

        # Only generate the graphics objects if the piece is real, otherwise unnecessary and takes up too much memory
        if self.real:
            # Initialize the templates for the three parts of a piece:
            # the piece itself, and symbols for king or highlighted

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
        self.piece_template.draw(game_board)

        if self.king:
            self.king_template.undraw()
            self.king_template.draw(game_board)
        if not self.king:
            self.king_template.undraw()

        if self.highlight:
            self.highlight_template.undraw()
            self.highlight_template.draw(game_board)
        if not self.highlight:
            self.highlight_template.undraw()

    def undraw_piece(self):
        self.piece_template.undraw()
        self.king_template.undraw()
        self.highlight_template.undraw()


class Square:
    def __init__(self, row, pos, connections, piece, highlight=False, real=False):
        # row and pos specify position of square (same convention as position of piece)
        # highlight shows if square is highlighted, this is used when a piece is clicked, to show possible moves
        # connections is dictionary with {connection type <int>: connected square <tuple>}
        # connected squares are tuples specified with row and pos (position in row); (row, pos): 1 to 8, 1 to 4
        # Connection type ranges from 0 to 3: top right, bottom right, bottom left, top left: from perspective of self
        # piece is which piece currently occupies this square
        # real is whether the square is part of the board that is being played on, or is just in the computer's thoughts

        self.row = row
        self.pos = pos
        self.highlight = highlight
        self.connections = connections
        self.piece = piece

        # Only generate the graphics objects if the square is real, otherwise unnecessary and takes up too much memory
        if real:
            if self.row % 2 == 1:  # If square is on rows 1, 3, 5, 7
                self.position = gr.Point(self.pos * 100 + 25, self.row * 50 + 25)
            elif self.row % 2 == 0:  # If square is on rows 2, 4, 6, 8
                self.position = gr.Point(self.pos * 100 - 25, self.row * 50 + 25)

            shading = gr.Rectangle(gr.Point(self.position.getX() - 25, self.position.getY() - 25),
                                   gr.Point(self.position.getX() + 25, self.position.getY() + 25))
            shading.setFill("grey")
            shading.draw(game_board)

            # Initialize the highlight template for future use
            self.highlight_template = gr.Circle(self.position, 3)
            self.highlight_template.setWidth(6)
            self.highlight_template.setOutline("gold")

    def draw_square(self):
        # Need to draw highlight on square (if there is one)

        if self.highlight:
            self.highlight_template.undraw()
            self.highlight_template.draw(game_board)
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
def find_moves(squares_list, side):
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


# fixme Rearrange the order of the functions to make more sense
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
        # If the piece is at the top of the board
        if start.piece.color is not player_color:
            # Can only jump downwards (forwards from red's perspective)
            allowed_jumps = [1, 2]
        # If the piece is at the bottom of the board  # todo check all comments make sense with updated code
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
                    # Reuse the previous connection direction, so it only tries to capture in a straight line
                    other_side = connection_square.connections[connection_type]
                    # If there is a square on the other side (not reached edge of board)
                    if other_side is not None:
                        other_side_square = squares_list[other_side[0] - 1][other_side[1] - 1]
                        # And check if the square on the other side is empty, to be able to jump it
                        if other_side_square.piece is None:

                            # Figure out the rest of the possible jumps (similar to the main for loop, but only looking
                            # for jumps, not regular moves)

                            visited = []

                            def find_all_jumps(start_from, previous_captured):
                                end_reached_overall = True
                                for connection_type in start_from.connections:
                                    all_captured = previous_captured.copy()
                                    end_reached = False
                                    if connection_type in allowed_jumps:
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

                                # If no more moves in each of the 4 directions
                                if end_reached_overall:
                                    moves.update({start_from: previous_captured})

                            find_all_jumps(other_side_square, [connection_square])

    # Implement the force jump rule for each piece,
    # meaning that if a piece has available jumps, it must take one of them, rather than an ordinary move
    jump_available = False
    for any_captured in moves.values():
        if any_captured != [None]:
            jump_available = True
            break
    if jump_available:
        for move in moves.copy():
            if moves[move] == [None]:
                moves.pop(move)

    # todo Add ambiguous jump handling

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
                    if captured_square.piece.real:
                        captured_square.piece.undraw_piece()
                    captured_square.piece = None

    new_square.piece = old_square.piece
    new_square.piece.row = new_square.row
    new_square.piece.pos = new_square.pos

    old_square.piece = None

    # Check to make the piece king if necessary
    # If piece is computer's
    if new_square.piece.color is not player_color:
        if new_square.row == 8:
            new_square.piece.king = True
    # If piece is player's
    if new_square.piece.color is player_color:
        if new_square.row == 1:
            new_square.piece.king = True


def player_move():
    # Get the coordinates of mouse click, and converts it to square on board, <None> if not on a playable square
    click = game_board.getMouse()
    click_square_coordinates = click_get_square(click)

    # Draw the new connections and highlights
    if click_square_coordinates is not None:
        # Read the connections associated with the square
        click_square_object = squares[click_square_coordinates[0] - 1][click_square_coordinates[1] - 1]

        # Find which moves are possible from the current position
        allowed_moves = find_moves(squares, turn)
        allowed_starts = []
        for move in allowed_moves:
            allowed_starts.append(move[0])

        # If there are any squares with jumps available, they are the only allowed moves,
        # otherwise if no jumps available, all moves allowed
        if click_square_object in allowed_starts:
            allowed = True
        else:
            allowed = False

        if allowed:
            # Highlight the piece on the square that was clicked (only if there is a piece present)
            if click_square_object.piece is not None:
                # Check if the piece clicked is of the color whose turn it is to move
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
                    game_board.update()

                    # Detect whether / where to move the selected piece
                    second_click = game_board.getMouse()
                    second_click_square_coordinates = click_get_square(second_click)
                    if second_click_square_coordinates is not None:
                        second_click_square_object = \
                            squares[second_click_square_coordinates[0] - 1][second_click_square_coordinates[1] - 1]
                        if second_click_square_object in possible_moves:
                            move_piece(click_square_object, second_click_square_object,
                                       possible_moves[second_click_square_object], squares)

                            # Tell the program that the player has actually made a move
                            # (rather than clicked on illegal square)
                            return True


# Computer makes a move (with intelligence)
def computer_move():
    # The computer uses the minimax algorithm to decide how to move next
    # Basically, the algorithm makes a tree with all possible future moves as deep as possible, limited by
    # processing power and memory
    # Then it evaluates each of these end positions (not every position along the way, just the end positions)
    # The criteria used right now is counting pieces, regular pieces worth 1 and kings worth 3
    # Maybe other more advanced evaluation criteria later
    # Let the score be positive if it thinks the player is winning
    # Now, for the layer one shallower than the one with the scores, for each position node on that layer,
    # if (for the positions on that layer) it's red (the computer's) turn, each position node will take on
    # the maximum score of its child nodes
    # This is because were the game to reach that position, red (the computer) would play the move that maximizes
    # the score
    # Conversely, if the layer is black (the player's) turn, then the parent node will take on the minimum value
    # of its child nodes
    # Since the player would want to minimize the advantage for the computer, which meaning maximizing the advantage
    # for the player
    # Repeat this process until the layer below the current position has numerical scores
    # Then the computer makes the move with the maximum score
    # Now let's implement this in code:

    # These are all the possible moves that the computer must look at:
    # moves = [[start_square, end_square, [captured, ...]], ...]
    moves = find_moves(squares, not player_color)

    moves_scored = []  # Holds a score for how good a move is
    # Initialize moves_scored
    # moves_scored = [[[start_square, end_square, [captured, ...]], score], ...]
    for move in moves:
        moves_scored.append([move, 0])

    # Recursive algorithm to do minimax
    def minimax(board, turn, depth, moves, end_piece_moved, search_depth=4):
        # end_piece_moved is whether a piece in the end-zone move last move, if yes, must continue this branch

        # If there are captures, these need to be looked at, even if the default search depth is exceeded
        # Otherwise the results will be skewed since a capture may be detected, but not the recapture afterwards
        capturing = False
        for move in moves:
            if move[2] != [None]:
                capturing = True
                break

        # Check if reached end of branch (certain depth reached and no further captures, or no more possible moves)
        if depth > search_depth and not capturing and not end_piece_moved or moves == []:
            # Analyze the current board situation to give it a score
            # Looking for how many pieces each side has

            # FIXME Flaw with algorithm? Will sacrifice pieces to try to prevent king (maybe)

            # TODO Add endgame strategy algorithm
            # TODO Add king chasing down opponent pieces and cornering opponent king feature

            # TODO Add piece formation and overextension evaluation

            # TODO Use multiprocessing and algorithm optimization to search more efficiently / deeper
            # todo Change program into C++ to run faster

            # TODO Add repetition escape feature if computer is winning
            # TODO Add start using the king more if one side has a king and the other side doesn't

            # TODO Add more advanced king detection, where there are no pieces blocking it, not just nearing end-zone

            # TODO Use neural nets to play better

            # If there are no more possible moves
            if not moves:
                # If it's the computer's turn, and it can't move
                if turn is not player_color:
                    return 1_000_000
                # If it's the player's turn, and they can't move
                if turn is player_color:
                    return -1_000_000

            # Current scoring scheme:
            # 1 for normal piece, 3 for king
            # +0.1 if it's in the center 4x4
            # an additional +0.05 on top of that if it's in the center 2x2

            # +0.5 bonus if it's a normal piece, and it's on one of the two back row squares
            # that control the whole back area
            computer_pieces_score = 0
            player_pieces_score = 0
            for row in board:
                for square in row:
                    if square.piece is not None:
                        if square.piece.color is not player_color:
                            # Check if piece is in center of board, slightly better position
                            if square.piece.row in [3, 4, 5, 6] and square.piece.pos in [2, 3]:
                                computer_pieces_score += 0.1
                            if square.piece.row == 4 and square.piece.pos == 3 or \
                                    square.piece.row == 5 and square.piece.pos == 2:
                                computer_pieces_score += 0.05

                            if square.piece.king is True:
                                computer_pieces_score += 3
                            else:
                                computer_pieces_score += 1
                                # Check for the back row pieces
                                if square.piece.row == 1 and square.piece.pos in [1, 3]:
                                    computer_pieces_score += 0.5

                        if square.piece.color is player_color:
                            # Check if piece is in center of board, slightly better position
                            if square.piece.row in [3, 4, 5, 6] and square.piece.pos in [2, 3]:
                                player_pieces_score += 0.1
                            if square.piece.row == 4 and square.piece.pos == 3 or \
                                    square.piece.row == 5 and square.piece.pos == 2:
                                player_pieces_score += 0.05

                            if square.piece.king is True:
                                player_pieces_score += 3
                            else:
                                player_pieces_score += 1
                                # Check for the back row pieces
                                if square.piece.row == 8 and square.piece.pos in [2, 4]:
                                    player_pieces_score += 0.5

            score = player_pieces_score - computer_pieces_score
            return score

        # Dynamically adjust the search depth depending on how complex the board position is
        new_search_depth = 4
        if not capturing:  # If there are force jumps, the complexity would appear artificially low
            moves_count = len(moves)
            if moves_count in [4, 5]:
                new_search_depth = 5
            elif moves_count == 3:
                new_search_depth = 6
            elif moves_count == 2:
                new_search_depth = 8
            elif moves_count == 1:
                new_search_depth = 12

        # fixme The king (end-zone) detection turns out to not work that well, as well as being slow, improve it
        # If it's the computer's turn
        if turn is not player_color:
            min_value = None
            for move in moves:
                # See if this move will move a piece to the end-zone, to decide if this branch must be continued
                new_end_piece_moved = False
                # If the piece is from the side at the top of the board
                if move[0].piece.color is not player_color:
                    if move[0].piece.king is False:
                        if move[1].row in [6, 7]:
                            new_end_piece_moved = True
                # If the piece is from the side at the bottom of the board
                if move[0].piece.color is player_color:
                    if move[0].piece.king is False:
                        if move[1].row in [2, 3]:
                            new_end_piece_moved = True

                new_virtual_squares = duplicate(board)
                move_piece(move[0], move[1], move[2], new_virtual_squares)
                new_value = minimax(new_virtual_squares, not turn, depth + 1,
                                    find_moves(new_virtual_squares, not turn), new_end_piece_moved, new_search_depth)
                if min_value is None:
                    min_value = new_value
                else:
                    if new_value < min_value:
                        min_value = new_value
            return min_value

        # If it's the player's turn
        if turn is player_color:
            max_value = None
            for move in moves:
                # See if this move will move a piece to the end-zone, to decide if this branch must be continued
                new_end_piece_moved = False
                # If the piece is from the side at top of board
                if move[0].piece.color is not player_color:
                    if move[0].piece.king is False:
                        if move[1].row in [6, 7]:
                            new_end_piece_moved = True
                # If the piece is from the side at bottom of board
                if move[0].piece.color is player_color:
                    if move[0].piece.king is False:
                        if move[1].row in [1, 2]:
                            new_end_piece_moved = True

                new_virtual_squares = duplicate(board)
                move_piece(move[0], move[1], move[2], new_virtual_squares)
                new_value = minimax(new_virtual_squares, not turn, depth + 1,
                                    find_moves(new_virtual_squares, not turn), new_end_piece_moved, new_search_depth)
                if max_value is None:
                    max_value = new_value
                else:
                    if new_value > max_value:
                        max_value = new_value
            return max_value

    for move in moves_scored:
        new_virtual_squares = duplicate(squares)
        move_piece(move[0][0], move[0][1], move[0][2], new_virtual_squares)
        move[1] = minimax(new_virtual_squares, player_color, 1, find_moves(new_virtual_squares, player_color), False)

    # Pick out the move(s) with the lowest score in moves_scored (meaning worst for player, best for computer),
    # and pick random move from the move(s)
    lowest = None
    best_moves = []
    for i, move in enumerate(moves_scored):
        if lowest is None:
            lowest = moves_scored[i][1]
            best_moves.append(move)
        else:
            if moves_scored[i][1] == lowest:
                best_moves.append(move)
            elif moves_scored[i][1] < lowest:
                lowest = moves_scored[i][1]
                best_moves.clear()
                best_moves.append(move)

    move_chosen = best_moves[random.randrange(0, len(best_moves))]
    start_square = move_chosen[0][0]
    end_square = move_chosen[0][1]
    captured = move_chosen[0][2]

    move_piece(start_square, end_square, captured, squares)

    # Display moves_scored
    for move in moves_display:
        if move is not None:
            move.undraw()

    moves_display.clear()
    line = 60
    for move in moves_scored:
        score = move[1]
        if score > 100_000:
            text = gr.Text(gr.Point(575, line), f"{move[0][0].row} {move[0][0].pos} to "
                                                f"{move[0][1].row} {move[0][1].pos} : Player win")
        elif score < -100_000:
            text = gr.Text(gr.Point(575, line), f"{move[0][0].row} {move[0][0].pos} to "
                                                f"{move[0][1].row} {move[0][1].pos} : Computer win")
        else:
            text = gr.Text(gr.Point(575, line), f"{move[0][0].row} {move[0][0].pos} to "
                                                f"{move[0][1].row} {move[0][1].pos} : {score:.2f}")
        text.setSize(10)
        moves_display.append(text)
        line += 15
    for move in moves_display:
        move.draw(game_board)

    return True


# Initialize game
squares = [[],
           [],
           [],
           [],
           [],
           [],
           [],
           []]

# Player select player color
color_selector = gr.GraphWin("Select Color", 350, 200)
black_box = gr.Circle(gr.Point(100, 100), 50)
black_box.setFill("black")
black_box.draw(color_selector)
red_box = gr.Circle(gr.Point(250, 100), 50)
red_box.setFill("red3")
red_box.draw(color_selector)
while True:
    select = color_selector.getMouse()
    if 50 <= select.getX() <= 150 and 50 <= select.getY() <= 150:
        player_color = True
        break
    if 200 <= select.getX() <= 300 and 50 <= select.getY() <= 150:
        player_color = False
        break
color_selector.close()

initialize_board()

# Holds the moves displayed on the debug menu
moves_display = []

player_won, computer_won = False, False

# Black moves first
turn = True
# Main game loop
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
    game_board.update()

    # If it's the player's turn
    if turn is player_color:
        # Check if the player is able to move
        able = False
        for row in squares:
            for square in row:
                if square.piece is not None:
                    if square.piece.color is player_color:
                        if search(square, squares) != {}:
                            able = True
                            break

        if able is False:
            computer_won = True
            break

        moved = player_move()

    # If it's the computer's turn
    else:
        # Check if the computer is able to move
        able = False
        for row in squares:
            for square in row:
                if square.piece is not None:
                    if square.piece.color is not player_color:
                        if search(square, squares) != {}:
                            able = True
                            break

        if able is False:
            player_won = True
            break

        moved = computer_move()

    # Only flip whose turn it is if the player actually made a move
    if moved:
        # Flip whose turn it is
        turn = not turn

if player_won:
    player_won_text = gr.Text(gr.Point(250, 25), "Player Won")
    player_won_text.setSize(16)
    if player_color is False:
        player_won_text.setTextColor("red3")
    player_won_text.draw(game_board)
elif computer_won:
    computer_won_text = gr.Text(gr.Point(250, 25), "Computer Won")
    computer_won_text.setSize(16)
    if player_color is True:
        computer_won_text.setTextColor("red3")
    computer_won_text.draw(game_board)

game_board.getKey()
