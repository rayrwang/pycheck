#include <iostream>
#include <SFML/Graphics.hpp>
#include <map>
#include <vector>
#include <array>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <string>
#include <sstream>
#include <iomanip>

using namespace sf;
using namespace std;

class Piece {
    public:
        bool color;
        int row;
        int pos;
        RenderWindow* gameBoard;
        bool king;
        bool highlight;
        bool real;
        bool noPiece;

        int position[2];
        CircleShape* pieceTemplate = new CircleShape(40);
        Font* font = new Font();
        Text* kingTemplate = new Text();
        CircleShape* highlightTemplate = new CircleShape(40);

        Piece() = default;

        Piece(bool p_color, int p_row, int p_pos, RenderWindow& p_gameBoard,
            bool p_king, bool p_highlight, bool p_real, bool p_noPiece) {

            color = p_color;
            row = p_row;
            pos = p_pos;
            
            king = p_king;
            highlight = p_highlight;
            real = p_real;
            noPiece = p_noPiece;

            if (real) {
                gameBoard = &p_gameBoard;

                if (row % 2 == 1) {
                    position[0] = pos * 200 + 50;
                    position[1] = row * 100 + 50;
                }
                else if (row % 2 == 0) {
                    position[0] = pos * 200 - 50;
                    position[1] = row * 100 + 50;
                }

                pieceTemplate->setPosition(position[0], position[1]);
                
                font->loadFromFile("Helvetica.ttf");
                kingTemplate->setFont(*font);
                kingTemplate->setString("K");
                kingTemplate->setStyle(Text::Bold);
                kingTemplate->setFillColor(Color(255, 215, 0));
                kingTemplate->setCharacterSize(70);

                highlightTemplate->setFillColor(Color::Transparent);
                highlightTemplate->setOutlineThickness(8);
                highlightTemplate->setOutlineColor(Color(255, 215, 0));
            }
        }

        ~Piece() {

        }

        void drawPiece() {
            if (row % 2 == 1) {
                position[0] = pos * 200 + 50;
                position[1] = row * 100 + 50;
            }
            else if (row % 2 == 0) {
                position[0] = pos * 200 - 50;
                position[1] = row * 100 + 50;
            }

            pieceTemplate->setPosition(position[0] - 40, position[1] - 40);
            gameBoard->draw(*pieceTemplate);

            kingTemplate->setPosition(position[0] - 25, position[1] - 44);
            highlightTemplate->setPosition(position[0] - 40, position[1] - 40);

            if (color == false) {
                pieceTemplate->setFillColor(Color(127, 0, 0));
                pieceTemplate->setOutlineColor(Color(127, 0, 0));
            }
            else if (color == true) {
                pieceTemplate->setFillColor(Color::Black);
                pieceTemplate->setOutlineColor(Color::Black);
            }
            gameBoard->draw(*pieceTemplate);

            if (king) {
                gameBoard->draw(*kingTemplate);
            }

            if (highlight) {
                gameBoard->draw(*highlightTemplate);
            }
        }
};

class Square {
    public:
        int row;
        int pos;
        Piece* piece;
        RenderWindow* gameBoard;
        bool highlight;
        bool real;
        
        map<int, vector<int>> connections;

        int position[2];
        CircleShape* highlightTemplate = new CircleShape(12);
        RectangleShape* shading = new RectangleShape(Vector2f(101, 101));

        Square() = default;

        Square(int p_row, int p_pos, Piece* p_piece, RenderWindow& p_gameBoard,
            bool p_real, bool p_highlight) {

            row = p_row;
            pos = p_pos;
            piece = p_piece;
            gameBoard = &p_gameBoard;
            highlight = p_highlight;
            real = p_real;

            // Figure out this square's connections
            if (row == 1 && (pos == 1 || pos == 2 || pos == 3)) {
                vector<int> c0{ 0, 0 };
                vector<int> c1{ row + 1, pos + 1 };
                vector<int> c2{ row + 1, pos };
                vector<int> c3{ 0, 0 };

                connections[0] = c0;
                connections[1] = c1;
                connections[2] = c2;
                connections[3] = c3;
            }
            if (row == 1 && pos == 4) {
                vector<int> c0{ 0, 0 };
                vector<int> c1{ 0, 0 };
                vector<int> c2{ row + 1, pos };
                vector<int> c3{ 0, 0 };

                connections[0] = c0;
                connections[1] = c1;
                connections[2] = c2;
                connections[3] = c3;
            }
            if ((row == 2 || row == 4 || row == 6) && pos == 1) {
                vector<int> c0{ row - 1, pos };
                vector<int> c1{ row + 1, pos };
                vector<int> c2{ 0, 0 };
                vector<int> c3{ 0, 0 };

                connections[0] = c0;
                connections[1] = c1;
                connections[2] = c2;
                connections[3] = c3;
            }
            if ((row == 2 || row == 4 || row == 6) && (pos == 2 || pos == 3 || pos == 4)) {
                vector<int> c0{ row - 1, pos };
                vector<int> c1{ row + 1, pos };
                vector<int> c2{ row + 1, pos - 1 };
                vector<int> c3{ row - 1, pos - 1 };

                connections[0] = c0;
                connections[1] = c1;
                connections[2] = c2;
                connections[3] = c3;
            }
            if ((row == 3 || row == 5 || row == 7)  && (pos == 1 || pos == 2 || pos == 3)) {
                vector<int> c0{ row - 1, pos + 1 };
                vector<int> c1{ row + 1, pos + 1 };
                vector<int> c2{ row + 1, pos };
                vector<int> c3{ row - 1, pos };

                connections[0] = c0;
                connections[1] = c1;
                connections[2] = c2;
                connections[3] = c3;
            }
            if ((row == 3 || row == 5 || row == 7) && pos == 4) {
                vector<int> c0{ 0, 0 };
                vector<int> c1{ 0, 0 };
                vector<int> c2{ row + 1, pos };
                vector<int> c3{ row - 1, pos };

                connections[0] = c0;
                connections[1] = c1;
                connections[2] = c2;
                connections[3] = c3;
            }
            if (row == 8 && pos == 1) {
                vector<int> c0{ row - 1, pos };
                vector<int> c1{ 0, 0 };
                vector<int> c2{ 0, 0 };
                vector<int> c3{ 0, 0 };

                connections[0] = c0;
                connections[1] = c1;
                connections[2] = c2;
                connections[3] = c3;
            }
            if (row == 8 && (pos == 2 || pos == 3 || pos == 4)) {
                vector<int> c0{ row - 1, pos };
                vector<int> c1{ 0, 0 };
                vector<int> c2{ 0, 0 };
                vector<int> c3{ row - 1, pos - 1 };

                connections[0] = c0;
                connections[1] = c1;
                connections[2] = c2;
                connections[3] = c3;
            }

            if (real) {
                if (row % 2 == 1) {
                    position[0] = pos * 200 + 50;
                    position[1] = row * 100 + 50;
                }
                else if (row % 2 == 0) {
                    position[0] = pos * 200 - 50;
                    position[1] = row * 100 + 50;
                }

                highlightTemplate->setPosition(position[0] - 13, position[1] - 11);
                highlightTemplate->setFillColor(Color(255, 215, 0));
            }
        }

        ~Square() {
            
        }

        void drawSquare() {
            shading->setPosition(position[0] - 51, position[1] - 50);
            shading->setFillColor(Color(127, 127, 127));
            gameBoard->draw(*shading);

            if (piece->noPiece == false) {
                piece->drawPiece();
            }

            if (highlight) {
                gameBoard->draw(*highlightTemplate);
            }
        }
};

void drawBackground(RenderWindow& gameBoard) {
    // Draw the row dividers
    VertexArray top(Lines, 2);
    top[0].position = Vector2f(99, 99);
    top[1].position = Vector2f(901, 99);
    top[0].color = Color::Black;
    top[1].color = Color::Black;
    gameBoard.draw(top);

    // Draw the row dividers
    VertexArray bottom(Lines, 2);
    bottom[0].position = Vector2f(99, 901);
    bottom[1].position = Vector2f(901, 901);
    bottom[0].color = Color::Black;
    bottom[1].color = Color::Black;
    gameBoard.draw(bottom);

    // Draw the column dividers
    VertexArray left(Lines, 2);
    left[0].position = Vector2f(99, 99);
    left[1].position = Vector2f(99, 901);
    left[0].color = Color::Black;
    left[1].color = Color::Black;
    gameBoard.draw(left);

    VertexArray right(Lines, 2);
    right[0].position = Vector2f(901, 99);
    right[1].position = Vector2f(901, 901);
    right[0].color = Color::Black;
    right[1].color = Color::Black;
    gameBoard.draw(right);

    // Draw the text that says "Debug"
    Font font;
    font.loadFromFile("helvetica.ttf");

    Text debugHeading;
    debugHeading.setFont(font);
    debugHeading.setString("Debug");
    debugHeading.setCharacterSize(36);
    debugHeading.setFillColor(Color::Black);
    debugHeading.setStyle(Text::Bold);
    debugHeading.setPosition(1090, 24);
    gameBoard.draw(debugHeading);

    // Draw text explaining debug output
    Text debugInfo1;
    Text debugInfo2;
    Text debugInfo3;
    Text debugInfo4;
    Text debugInfo5;
    Text debugInfo6;

    debugInfo1.setFont(font);
    debugInfo1.setString("row column to row column : score");
    debugInfo2.setFont(font);
    debugInfo2.setString("columns numbered 1 to 4,");
    debugInfo3.setFont(font);
    debugInfo3.setString("left to right,");
    debugInfo4.setFont(font);
    debugInfo4.setString("for each playable (gray) square");
    debugInfo5.setFont(font);
    debugInfo5.setString("score is from the player's perspective");
    debugInfo6.setFont(font);
    debugInfo6.setString("(+ = player is winning)");

    debugInfo1.setCharacterSize(12);
    debugInfo1.setFillColor(Color::Black);
    debugInfo1.setPosition(1060, 900);
    debugInfo2.setCharacterSize(12);
    debugInfo2.setFillColor(Color::Black);
    debugInfo2.setPosition(1080, 916);
    debugInfo3.setCharacterSize(12);
    debugInfo3.setFillColor(Color::Black);
    debugInfo3.setPosition(1120, 932);
    debugInfo4.setCharacterSize(12);
    debugInfo4.setFillColor(Color::Black);
    debugInfo4.setPosition(1070, 948);
    debugInfo5.setCharacterSize(12);
    debugInfo5.setFillColor(Color::Black);
    debugInfo5.setPosition(1055, 964);
    debugInfo6.setCharacterSize(12);
    debugInfo6.setFillColor(Color::Black);
    debugInfo6.setPosition(1090, 980);

    gameBoard.draw(debugInfo1);
    gameBoard.draw(debugInfo2);
    gameBoard.draw(debugInfo3);
    gameBoard.draw(debugInfo4);
    gameBoard.draw(debugInfo5);
    gameBoard.draw(debugInfo6);

    // Draw the line separating game board from debug scores output
    VertexArray newColumn(Lines, 2);

    newColumn[0].position = Vector2f(1000, 0);
    newColumn[1].position = Vector2f(1000, 1000);

    newColumn[0].color = Color::Black;
    newColumn[1].color = Color::Black;

    gameBoard.draw(newColumn);
}

void drawBoard(RenderWindow& gameBoard, Square* squares[8][4],
    map< tuple<Square*, Square*, vector<Square*>* >*, double>* previousScores, bool noPreviousScores = false) {
    // This draws the current squares and pieces
    gameBoard.clear(Color::White);
    drawBackground(gameBoard);
    for (int row = 1; row <= 8; row++) {
        for (int pos = 1; pos <= 4; pos++) {
            squares[row - 1][pos - 1]->drawSquare();  // Drawing the pieces is included in drawSquare()
        }
    }

    /*if (noPreviousScores == false) {
        int line = 100;
        Font font;
        font.loadFromFile("Helvetica.ttf");
        for (auto move = previousScores->begin(); move != previousScores->end(); move++) {
            Text text;
            text.setFont(font);

            string startRow = to_string(get<0>(*move->first)->row);
            string startPos = to_string(get<0>(*move->first)->pos);
            string endRow = to_string(get<1>(*move->first)->row);
            string endPos = to_string(get<1>(*move->first)->pos);

            stringstream stream;
            stream << fixed << setprecision(2) << move->second;
            string score = stream.str();

            text.setString(startRow + " " + startPos + " to " + endRow + " " + endPos + " : " + score);
            text.setFillColor(Color::Black);
            text.setPosition(1075, line);
            text.setCharacterSize(20);
            gameBoard.draw(text);
            line += 30;
        }
    }*/
    gameBoard.display();
}

void initializeBoard(bool playerColor, Square* squares[8][4], RenderWindow& gameBoard) {
    drawBackground(gameBoard);

    Piece* pieces[8][4];
    if (playerColor == true) {
        for (int pieceRow = 1; pieceRow <= 3; pieceRow++) {
            for (int piecePos = 1; piecePos <= 4; piecePos++) {
                Piece* piece = new Piece(false, pieceRow, piecePos, gameBoard, false, false, true, false);
                pieces[pieceRow - 1][piecePos - 1] = piece;
            }
        }
        for (int pieceRow = 4; pieceRow <= 5; pieceRow++) {
            for (int piecePos = 1; piecePos <= 4; piecePos++) {
                Piece* piece = new Piece(false, pieceRow, piecePos, gameBoard, false, false, true, true);
                pieces[pieceRow - 1][piecePos - 1] = piece;
            }
        }
        for (int pieceRow = 6; pieceRow <= 8; pieceRow++) {
            for (int piecePos = 1; piecePos <= 4; piecePos++) {
                Piece* piece = new Piece(true, pieceRow, piecePos, gameBoard, false, false, true, false);
                pieces[pieceRow - 1][piecePos - 1] = piece;
            }
        }
    }

    for (int squareRow = 1; squareRow <= 8; squareRow++) {
        for (int squarePos = 1; squarePos <= 4; squarePos++) {
            Square* square = new Square(squareRow, squarePos, pieces[squareRow - 1][squarePos - 1],
                gameBoard, true, false);
            squares[squareRow - 1][squarePos - 1] = square;
        }
    }
}

void movePiece(Square& oldSquare, Square& newSquare, vector<Square*>* captured, Square* squaresList[8][4], bool playerColor) {
    Square* newOldSquare = NULL;
    Square* newNewSquare = NULL;
    vector<Square*> capturedCopy;
    for (int i = 0; i <= 7; i++) {
        for (int j = 0; j <= 3; j++) {
            Square& square = *squaresList[i][j];
            if (square.row == oldSquare.row && square.pos == oldSquare.pos) {
                newOldSquare = &square;
                continue;
            }
            if (square.row == newSquare.row && square.pos == newSquare.pos) {
                newNewSquare = &square;
                continue;
            }
            for (auto& capturedSquare : *captured) {
                if (square.row == capturedSquare->row && square.pos == capturedSquare->pos) {
                    capturedCopy.push_back(&square);
                }
            }
        }
    }

    for (auto& square : capturedCopy) {
        square->piece->noPiece = true;
    }
    
    newNewSquare->piece->color = newOldSquare->piece->color;
    newNewSquare->piece->king = newOldSquare->piece->king;

    newNewSquare->piece->noPiece = false;

    newOldSquare->piece->noPiece = true;

    if (newNewSquare->piece->color != playerColor) {
        if (newNewSquare->row == 8) {
            newNewSquare->piece->king = true;
        }
    }
    else if (newNewSquare->piece->color == playerColor) {
        if (newNewSquare->row == 1) {
            newNewSquare->piece->king = true;
        }
    }
}

bool findAllJumps(Square* startFrom, vector<Square*>* previousCaptured,
    vector<int>& allowedJumps, Square* squaresList[8][4], vector<Square*>& visited, Square& start, map<Square*, vector<Square*>* >* moves, bool firstJump) {
    bool endReachedOverall = true;
    for (int connectionType = 0; connectionType <= 3; connectionType++) {
        Square* newStartFrom = NULL;

        vector<Square*>* allCaptured = new vector<Square*>;
        *allCaptured = *previousCaptured;
        bool endReached = false;
        if (count(allowedJumps.begin(), allowedJumps.end(), connectionType)) {
            vector<int> newConnection = startFrom->connections[connectionType];
            vector<int> noConnection = { 0, 0 };
            if (newConnection != noConnection) {
                Square& newConnectionSquare = *squaresList[newConnection[0] - 1][newConnection[1] - 1];
                if (count(visited.begin(), visited.end(), &newConnectionSquare) == false) {
                    if (newConnectionSquare.piece->noPiece == false) {
                        if (newConnectionSquare.piece->color != start.piece->color) {
                            vector<int> newOtherSide = newConnectionSquare.connections[connectionType];
                            if (newOtherSide != noConnection) {
                                Square& newOtherSideSquare = *squaresList[newOtherSide[0] - 1][newOtherSide[1] - 1];
                                if (newOtherSideSquare.piece->noPiece) {
                                    newStartFrom = &newOtherSideSquare;

                                    allCaptured->push_back(&newConnectionSquare);
                                    visited.push_back(&newConnectionSquare);
                                }
                                else {
                                    endReached = true;
                                }
                            }
                            else {
                                endReached = true;
                            }
                        }
                        else {
                            endReached = true;
                        }
                    }
                    else {
                        endReached = true;
                    }
                }
                else {
                    endReached = true;
                }
            }
            else {
                endReached = true;
            }
        }
        else {
            endReached = true;
        }

        if (endReached == false) {
            endReachedOverall = false;

            bool endReachedOnNextIter = false;
            endReachedOnNextIter = findAllJumps(newStartFrom, allCaptured, allowedJumps, squaresList, visited, start, moves, false);
            if (!endReachedOnNextIter) {
                delete allCaptured;  // Only delete captured vector if it won't be used in the final possible moves
            }
        }
    }
    
    if (endReachedOverall) {
        //if (!firstJump) {
        moves->operator[](startFrom) = previousCaptured;
        //
        
        return true;
    }
}

map<Square*, vector<Square*>* >* search(Square& start, Square* squaresList[8][4], bool playerColor) {
    map<Square*, vector<Square*>* >* moves = new map<Square*, vector<Square*>* >;

    vector<int> allowedJumps;
    if (start.piece->king == false) {
        if (start.piece->color != playerColor) {
            allowedJumps.push_back(1);
            allowedJumps.push_back(2);
        }
        else {
            allowedJumps.push_back(0);
            allowedJumps.push_back(3);
        }
    }
    else {
        allowedJumps.push_back(0);
        allowedJumps.push_back(1);
        allowedJumps.push_back(2);
        allowedJumps.push_back(3);
    }
    
    for (int connectionType = 0; connectionType < 4; connectionType++) {
        if (count(allowedJumps.begin(), allowedJumps.end(), connectionType)) {
            vector<int> connection = start.connections[connectionType];
            vector<int> noConnection{ 0, 0 };
            if (connection != noConnection) {
                Square& connectionSquare = *squaresList[connection[0] - 1][connection[1] - 1];
                if (connectionSquare.piece->noPiece) {
                    vector<Square*>* captured = new vector<Square*>;
                    captured->push_back({ &start }) ;  // Meaning no captured
                    moves->operator[](&connectionSquare) = captured;
                }
                else if (connectionSquare.piece->color != start.piece->color) {
                    vector<int> otherSide = connectionSquare.connections[connectionType];
                    if (otherSide != noConnection) {
                        Square& otherSideSquare = *squaresList[otherSide[0] - 1][otherSide[1] - 1];
                        if (otherSideSquare.piece->noPiece == true) {
                            vector<Square*> visited;            
                            vector<Square*>* startingCaptured = new vector<Square*>;
                            startingCaptured->push_back(&connectionSquare);
                            bool noMoreJumps = false;
                            noMoreJumps = findAllJumps(&otherSideSquare, startingCaptured, allowedJumps, squaresList, visited, start, moves, true);
                            if (noMoreJumps) {
                                // delete startingCaptured;
                            }
                        }
                    }
                }
            }
        }
    }

    bool jumpAvailable = false;
    for (auto i = moves->begin(); i != moves->end(); i++) {
        // If the captured pieces vector (i->second) doesn't only contains the starting square, this means no captures
        if (!((*i->second)[0]->row == start.row && (*i->second)[0]->pos == start.pos)) {
            jumpAvailable = true;
            break;
        }
    }
    if (jumpAvailable) {
        map<Square*, vector<Square*>* > movesCopy = *moves;
        for (auto i = movesCopy.begin(); i != movesCopy.end(); i++) {
            if ((*i->second)[0]->row == start.row && (*i->second)[0]->pos == start.pos) {
                for (auto toErase = moves->begin(); toErase != moves->end(); toErase++) {
                    if ((*toErase->second)[0]->row == start.row && (*toErase->second)[0]->pos == start.pos) {
                        moves->erase(toErase);
                        break;
                    }
                }
            }
        }
    }

    return moves;
}

vector< tuple<Square*, Square*, vector<Square*>* >* >* findMoves(Square* squaresList[8][4], bool side, bool playerColor) {
    vector<Square*> forceJumps;
    bool anyCaptured = false;
    for (int i = 0; i <= 7; i++) {
        auto& row = squaresList[i];
        for (auto& square : row) {
            if (square->piece->noPiece == false) {
                if (square->piece->color == side) {
                    map<Square*, vector<Square*>* >* moves = search(*square, squaresList, playerColor);
                    vector<Square*> noCaptured = { square };
                    for (auto i = moves->begin(); i != moves->end(); i++) {
                        if (*i->second != noCaptured) {
                            forceJumps.push_back(square);
                            anyCaptured = true;
                            delete i->second;
                            break;
                        }
                    }
                    delete moves;
                }
            }
        }
    }

    map<Square*, map<Square*, vector<Square*>* >* > allMoves;
    if (anyCaptured) {
        for (auto& square : forceJumps) {
            map<Square*, vector<Square*>* >* moves = search(*square, squaresList, playerColor);
            allMoves[square] = moves;
        }
    }
    else {
        for (int i = 0; i <= 7; i++) {
            auto& row = squaresList[i];
            for (auto& square : row) {
                if (square->piece->noPiece == false) {
                    if (square->piece->color == side) {
                        map<Square*, vector<Square*>* >* moves = search(*square, squaresList, playerColor);
                        if (!moves->empty()) {
                            allMoves[square] = moves;
                        }
                    }
                }
            }
        }
    }

    vector< tuple<Square*, Square*, vector<Square*>* >* >* movesFlat = new vector< tuple<Square*, Square*, vector<Square*>* >* >;
    for (auto wholeMove = allMoves.begin(); wholeMove != allMoves.end(); wholeMove++) {
        Square* start = wholeMove->first;
        for (auto endAndCaptured = (wholeMove->second)->begin(); endAndCaptured != (wholeMove->second)->end(); endAndCaptured++) {
            Square* end = endAndCaptured->first;
            vector<Square*>* captured = endAndCaptured->second;
            
            tuple<Square*, Square*, vector<Square*>* >* move = new tuple<Square*, Square*, vector<Square*>* >;
            *move = make_tuple(start, end, captured);
            movesFlat->push_back(move);
        }
        delete wholeMove->second;
    }

    return movesFlat;
}

array<int, 2> waitClick(RenderWindow& gameBoard) {
    array<int, 2> clickSquareCoordinates;
    Event event;
    while (gameBoard.waitEvent(event)) {
        switch (event.type) {
        case Event::Closed:
            gameBoard.close();
            break;
        case Event::MouseButtonPressed:
            Vector2i mousePosition;
            mousePosition = Mouse::getPosition(gameBoard);

            // Figure out what square was clicked from the click's coordinates
            int x = mousePosition.x;
            int y = mousePosition.y;
            if (!(x > 100 && x < 900 && y > 100 && y < 900)) {
                clickSquareCoordinates[0] = 0;
                clickSquareCoordinates[1] = 0;

                return clickSquareCoordinates;
            }

            x = round((x / 100) - 0.5);
            y = round((y / 100) - 0.5);

            int row = y;
            int pos;

            if (row % 2 == 1) {
                if (x % 2 == 1) {
                    clickSquareCoordinates[0] = 0;
                    clickSquareCoordinates[1] = 0;

                    return clickSquareCoordinates;
                }
                else {
                    pos = x / 2;
                }
            }

            else {
                if (x % 2 == 1) {
                    pos = (x + 1) / 2;
                }
                else {
                    clickSquareCoordinates[0] = 0;
                    clickSquareCoordinates[1] = 0;

                    return clickSquareCoordinates;
                }
            }

            clickSquareCoordinates[0] = row;
            clickSquareCoordinates[1] = pos;

            return clickSquareCoordinates;
        }
    }
}

bool playerMove(bool turn, Square* squares[8][4], bool playerColor, RenderWindow& gameBoard,
    map< tuple<Square*, Square*, vector<Square*>* >*, double>* previousScores, bool noPreviousScores) {
    array<int, 2> clickSquare = waitClick(gameBoard);

    array<int, 2> noClick = { 0, 0 };
    if (clickSquare != noClick) {
        Square* clickSquareObject = squares[clickSquare[0] - 1][clickSquare[1] - 1];

        vector< tuple<Square*, Square*, vector<Square*>* >* >* allowedMoves = findMoves(squares, turn, playerColor);
        vector<Square*> allowedStarts;
        for (auto& move : *allowedMoves) {
            allowedStarts.push_back(get<0>(*move));
        }

        if (count(allowedStarts.begin(), allowedStarts.end(), clickSquareObject)) {
            clickSquareObject->piece->highlight = true;
            
            map<Square*, vector<Square*>* >* possibleMoves;
            possibleMoves = search(*clickSquareObject, squares, playerColor);
            for (auto i = possibleMoves->begin(); i != possibleMoves->end(); i++) {
                i->first->highlight = true;
            }

            drawBoard(gameBoard, squares, previousScores, noPreviousScores);

            array<int, 2> secondClickSquare = waitClick(gameBoard);
            if (secondClickSquare != noClick) {
                Square* secondClickSquareObject = squares[secondClickSquare[0] - 1][secondClickSquare[1] - 1];
                bool clickIsLegal = false;
                vector<Square*>* captured = {};
                for (auto i = possibleMoves->begin(); i != possibleMoves->end(); i++) {
                    if (i->first == secondClickSquareObject) {
                        captured = i->second;
                        clickIsLegal = true;
                        break;
                    }
                }
                if (clickIsLegal) {
                    movePiece(*clickSquareObject, *secondClickSquareObject, captured, squares, playerColor);
                    return true;
                }
            }
        }
    }
    return false;
}

void duplicate(Square* oldSquares[8][4], Square* newSquares[8][4]) {
    for (int i = 0; i <= 7; i++) {
        for (int j = 0; j <= 3; j++) {
            Square& oldSquare = *oldSquares[i][j];

            // these pieces and squares all have real = false
            Piece* newPiece = new Piece(oldSquare.piece->color, oldSquare.piece->row, oldSquare.piece->pos, *oldSquare.piece->gameBoard, oldSquare.piece->king,
                false, false, oldSquare.piece->noPiece);
            Square* newSquare = new Square(oldSquare.row, oldSquare.pos, newPiece, *oldSquare.gameBoard, false, false);
            newSquares[i][j] = newSquare;
        }
    }
}

double minimax(Square* board[8][4], bool turn, int depth, bool endPieceMoved, int searchDepth, bool playerColor) {
    vector< tuple<Square*, Square*, vector<Square*>* >* >* moves = findMoves(board, turn, playerColor);
    
    int computerPiecesScore = 0;
    int playerPiecesScore = 0;
    if (depth >= searchDepth) {
        for (int i = 0; i <= 7; i++) {
            for (int j = 0; j <= 3; j++) {
                Square& square = *board[i][j];
                if (square.piece->noPiece == false) {
                    if (square.piece->color != playerColor) {
                        if (square.piece->king) {
                            computerPiecesScore += 3;
                        }
                        else {
                            computerPiecesScore += 1;
                        }
                    }

                    else {
                        if (square.piece->king) {
                            playerPiecesScore += 3;
                        }
                        else {
                            playerPiecesScore += 1;
                        }
                    }
                }
            }
        }
        double score = playerPiecesScore - computerPiecesScore;

        // Deallocate memory used by moves and board
        for (auto& move : *moves) {
            delete get<2>(*move);
            delete move;
        }
        delete moves;

        for (int i = 0; i <= 7; i++) {
            for (int j = 0; j <= 3; j++) {
                delete board[i][j]->piece->pieceTemplate;
                delete board[i][j]->piece->font;
                delete board[i][j]->piece->kingTemplate;
                delete board[i][j]->piece->highlightTemplate;
                delete board[i][j]->piece;

                delete board[i][j]->highlightTemplate;
                delete board[i][j]->shading;
                delete board[i][j];
            }
        }

        return score;
    }

    int newSearchDepth = 6;
    if (turn != playerColor) {
        double minValue;
        bool minValueExist = false;

        for (auto& move : *moves) {
            bool newEndPieceMoved = false;
            Square* newVirtualSquares[8][4];
            duplicate(board, newVirtualSquares);

            Square* startSquare = get<0>(*move);
            Square* endSquare = get<1>(*move);
            vector<Square*>* captured = get<2>(*move);

            movePiece(*startSquare, *endSquare, captured, newVirtualSquares, playerColor);
            double newValue = minimax(newVirtualSquares, !turn, depth + 1, newEndPieceMoved,
                newSearchDepth, playerColor);

            if (minValueExist == false) {
                minValue = newValue;
                minValueExist = true;
            }
            else {
                if (newValue < minValue) {
                    minValue = newValue;
                }
            }
        }

        // Deallocate memory used by moves and board
        for (auto& move : *moves) {
            delete get<2>(*move);
            delete move;
        }
        delete moves;

        for (int i = 0; i <= 7; i++) {
            for (int j = 0; j <= 3; j++) {
                delete board[i][j]->piece->pieceTemplate;
                delete board[i][j]->piece->font;
                delete board[i][j]->piece->kingTemplate;
                delete board[i][j]->piece->highlightTemplate;
                delete board[i][j]->piece;

                delete board[i][j]->highlightTemplate;
                delete board[i][j]->shading;
                delete board[i][j];
            }
        }

        return minValue;
    }
    else {
        double maxValue;
        bool maxValueExist = false;

        for (auto& move : *moves) {
            bool newEndPieceMoved = false;
            Square* newVirtualSquares[8][4];
            duplicate(board, newVirtualSquares);

            Square* startSquare = get<0>(*move);
            Square* endSquare = get<1>(*move);
            vector<Square*>* captured = get<2>(*move);

            movePiece(*startSquare, *endSquare, captured, newVirtualSquares, playerColor);
            double newValue = minimax(newVirtualSquares, !turn, depth + 1, newEndPieceMoved,
                newSearchDepth, playerColor);
            
            if (maxValueExist == false) {
                maxValue = newValue;
                maxValueExist = true;
            }
            else {
                if (newValue > maxValue) {
                    maxValue = newValue;
                }
            }
        }

        // Deallocate memory used by moves and board
        for (auto& move : *moves) {
            delete get<2>(*move);
            delete move;
        }
        delete moves;

        for (int i = 0; i <= 7; i++) {
            for (int j = 0; j <= 3; j++) {
                delete board[i][j]->piece->pieceTemplate;
                delete board[i][j]->piece->font;
                delete board[i][j]->piece->kingTemplate;
                delete board[i][j]->piece->highlightTemplate;
                delete board[i][j]->piece;

                delete board[i][j]->highlightTemplate;
                delete board[i][j]->shading;
                delete board[i][j];
            }
        }

        return maxValue;
    }
}

bool computerMove(Square* squares[8][4], bool playerColor, RenderWindow& gameBoard, map< tuple<Square*, Square*, vector<Square*>* >*, double>* previousScores) {
    vector< tuple<Square*, Square*, vector<Square*>* >* >* moves = findMoves(squares, !playerColor, playerColor);
    
    map< tuple<Square*, Square*, vector<Square*>* >*, double>* movesScored = new map< tuple<Square*, Square*, vector<Square*>* >*, double>;
    for (auto& move : *moves) {
        movesScored->operator[](move) = 0;
    }

    // todo: win detection & AI

    // Figure out the scores for each move
    for (auto move = movesScored->begin(); move != movesScored->end(); move++) {
        Square* newVirtualSquares[8][4];
        duplicate(squares, newVirtualSquares);

        Square* startSquare = get<0>(*move->first);
        Square* endSquare = get<1>(*move->first);
        vector<Square*>* captured = get<2>(*move->first);

        movePiece(*startSquare, *endSquare, captured, newVirtualSquares, playerColor);
        move->second = minimax(newVirtualSquares, playerColor, 1, false, 6, playerColor);
    }

    for (auto i = movesScored->begin(); i != movesScored->end(); i++) {
        i->second = (round(i->second * 100)) / 100;
    }

    // Figure out which move to take, will chose one of the moves with the lowest scores from the player's perspective
    int lowest;
    bool lowestExist = false;
    vector< tuple<Square*, Square*, vector<Square*>* >* > bestMoves;

    for (auto i = movesScored->begin(); i != movesScored->end(); i++) {
        if (!lowestExist) {
            lowest = i->second;
            bestMoves.push_back(i->first);
            lowestExist = true;
        }
        else {
            if (i->second == lowest) {
                bestMoves.push_back(i->first);
            }
            else if (i->second < lowest) {
                lowest = i->second;
                bestMoves.clear();
                bestMoves.push_back(i->first);
            }
        }
    }

    srand(time(0));
    int moveIndex = rand() % bestMoves.size();
    tuple <Square*, Square*, vector<Square*>* >* moveChosen = bestMoves[moveIndex];
    Square* startSquare = get<0>(*moveChosen);
    Square* endSquare = get<1>(*moveChosen);
    vector<Square*>* captured = get<2>(*moveChosen);
    movePiece(*startSquare, *endSquare, captured, squares, playerColor);

    previousScores = movesScored;

    return true;
}

int main()
{
    bool turn = true;
    bool playerColor = true;
    
    // Initialize the game window
    RenderWindow gameBoard(VideoMode(1300, 1000), "Checkers AI");
    
    // Initialize the board at the start of a game
    gameBoard.clear(Color::White);
    Square* squares[8][4];
    initializeBoard(true, squares, gameBoard);
    gameBoard.display();

    // Initialize the map with the scores for the computer's last move, so they're available during the player's current mvoe
    map< tuple<Square*, Square*, vector<Square*>* >*, double>* previousScores = {};
    bool noPreviousScores = true;

    while (gameBoard.isOpen()) {
        Event event;
        while (gameBoard.pollEvent(event)) {
            if (event.type == Event::Closed) {
                gameBoard.close();
            }
        }

        // At the start of every loop clear the last loop's highlights
        for (auto& row : squares) {
            for (auto& square : row) {
                square->highlight = false;
                square->piece->highlight = false;
            }
        }

        bool moved = false;
        if (turn == playerColor) {
            drawBoard(gameBoard, squares, previousScores, noPreviousScores);
            moved = playerMove(turn, squares, playerColor, gameBoard, previousScores, noPreviousScores);
            drawBoard(gameBoard, squares, previousScores, noPreviousScores);
        }
        else {
            drawBoard(gameBoard, squares, previousScores, noPreviousScores);
            moved = computerMove(squares, playerColor, gameBoard, previousScores);
            noPreviousScores = false;
            //moved = playerMove(turn, squares, playerColor, gameBoard);
            drawBoard(gameBoard, squares, previousScores);
        }

        if (moved) {
            turn = !turn;
        }
    }

    return 0;
}
