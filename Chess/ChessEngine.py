
class GameState:
    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]
        self.move_functions = {'P': self.check_pawn_moves, 'B': self.check_bishop_moves, 'R': self.check_rock_moves,
                               'Q': self.check_queen_moves, 'N': self.check_knight_moves, 'K': self.check_king_moves}
        self.move_log = []
        self.white_move = True
        self.selected_figure = '--'
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)

    def make_move(self, move):
        self.board[move.start_move_row][move.start_move_col] = '--'
        self.board[move.end_move_row][move.end_move_col] = move.figure_moved
        self.move_log.append(move)
        self.white_move = not self.white_move
        if move.figure_moved == 'wK':
            self.white_king_location = (move.end_move_row, move.end_move_col)
        elif move.figure_moved == 'bK':
            self.white_king_location = (move.end_move_row, move.end_move_col)

    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_move_row][move.start_move_col] = move.figure_moved
            self.board[move.end_move_row][move.end_move_col] = move.figure_captured
            self.white_move = not self.white_move
            if move.figure_moved == 'wK':
                self.white_king_location = (move.end_move_row, move.end_move_col)
            elif move.figure_moved == 'bK':
                self.white_king_location = (move.end_move_row, move.end_move_col)

    def get_valid_moves(self):
        return self.generate_all_possible_moves()

    def generate_all_possible_moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if self.white_move and turn == 'w':
                    peace = self.board[r][c][1]
                    self.move_functions[peace](r, c, moves, turn)

                elif not self.white_move and turn == 'b':
                    peace = self.board[r][c][1]
                    self.move_functions[peace](r, c, moves, turn)
        return moves

    def check_pawn_moves(self, r, c, moves, turn):
        if turn == 'w':
            if r > 0:
                if self.board[r-1][c] == '--':
                    moves.append(Move((r, c), (r-1, c), self.board))
                    if r == 6 and self.board[r - 2][c] == '--':
                        moves.append(Move((r, c), (r - 2, c), self.board))
                if c > 0:
                    if self.board[r-1][c-1][0] != turn:
                        moves.append(Move((r, c), (r-1, c-1), self.board))
                if c < 7:
                    if self.board[r-1][c+1][0] != turn:
                        moves.append(Move((r, c), (r-1, c+1), self.board))
        else:
            if r < 7:
                if self.board[r+1][c] == '--':
                    moves.append(Move((r, c), (r+1, c), self.board))
                    if r == 1 and self.board[r+2][c] == '--':
                        moves.append(Move((r, c), (r+2, c), self.board))
                if c > 0:
                    if self.board[r+1][c-1][0] != turn:
                        moves.append(Move((r, c), (r+1, c-1), self.board))
                if c < 7:
                    if self.board[r+1][c+1][0] != turn:
                        moves.append(Move((r, c), (r+1, c+1), self.board))

    def check_bishop_moves(self, r, c, moves, turn):
        directions = ((-1, -1), (1, -1), (-1, 1), (1, 1))
        for d in directions:
            for i in range(1, 8):
                r_end = r + d[0] * i
                c_end = c + d[1] * i
                if 0 <= r_end < 8 and 0 <= c_end < 8:
                    endpiece = self.board[r_end][c_end]
                    if endpiece == '--':
                        moves.append(Move((r, c), (r_end, c_end), self.board))
                    elif endpiece[0] != turn:
                        moves.append(Move((r, c), (r_end, c_end), self.board))
                        break
                    else:
                        break
                else:
                    break

    def check_rock_moves(self, r, c, moves, turn):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        for d in directions:
            for i in range(1, 8):
                r_end = r + d[0] * i
                c_end = c + d[1] * i
                if 0 <= r_end < 8 and 0 <= c_end < 8:
                    endpiece = self.board[r_end][c_end]
                    if endpiece == '--':
                        moves.append(Move((r, c), (r_end, c_end), self.board))
                    elif endpiece[0] != turn:
                        moves.append(Move((r, c), (r_end, c_end), self.board))
                        break
                    else:
                        break
                else:
                    break

    def check_queen_moves(self, r, c, moves, turn):
        self.check_bishop_moves(r, c, moves, turn)
        self.check_rock_moves(r, c, moves, turn)

    def check_knight_moves(self, r, c, moves, turn):
        directions = ((-2, -1), (-2, 1), (2, -1), (2, 1), (-1, 2), (1, 2), (-1, -2), (1, -2))
        for d in directions:
            r_end = r + d[0]
            c_end = c + d[1]
            if 0 <= r_end < 8 and 0 <= c_end < 8:
                endpiece = self.board[r_end][c_end]
                if endpiece == '--':
                    moves.append(Move((r, c), (r_end, c_end), self.board))
                elif endpiece[0] != turn:
                    moves.append(Move((r, c), (r_end, c_end), self.board))

    def check_king_moves(self, r, c, moves, turn):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1))
        for d in directions:
            r_end = r + d[0]
            c_end = c + d[1]
            if 0 <= r_end < 8 and 0 <= c_end < 8:
                endpiece = self.board[r_end][c_end]
                if endpiece[0] != turn:
                    moves.append(Move((r, c), (r_end, c_end), self.board))


class Move:
    ranks_to_rows = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_moves, end_moves, board):
        self.start_move_row = start_moves[0]
        self.start_move_col = start_moves[1]
        self.end_move_row = end_moves[0]
        self.end_move_col = end_moves[1]
        self.figure_moved = board[start_moves[0]][start_moves[1]]
        self.figure_captured = board[end_moves[0]][end_moves[1]]
        self.id = self.start_move_row * 1000 + self.start_move_col * 100 + self.end_move_row * 10 + self.end_move_col

    def __eq__(self, other):
        if isinstance(other, Move):
            if self.id == other.id:
                return True

    def get_chess_notation(self):
        return self.get_rank_file(self.start_move_row, self.start_move_col) + \
               self.get_rank_file(self.end_move_row, self.end_move_col)

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]




