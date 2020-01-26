import random
import time
from copy import deepcopy

from Piece import Player
from Board import Board
import tkinter as tk
from PIL import Image
from Position import Position
from tkinter import ttk

class PvAI_Game(ttk.Frame):
    def __init__(self, board: Board, ai_strategy, parent, width, height, square_size=64, custom_flag=False):
        self.board = board
        if not custom_flag:
            self.board.init_board()
        self.turn = Player.WHITE

        self.strategy = ai_strategy

        self.square_size = square_size
        self.parent = parent

        canvas_width = self.columns * square_size
        canvas_height = self.rows * square_size

        ttk.Frame.__init__(self, parent, width=width, height=height)

        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height, background="grey")
        self.canvas.pack(side="top", fill="both", anchor="c", expand=True)

        self.canvas.bind("<Configure>", self.refresh)
        self.canvas.bind("<Button-1>", self.click)

        self.statusbar = ttk.Frame(self)
        self.label_status = ttk.Label(self.statusbar, text="   White's turn  ")
        self.label_status.pack(side=tk.LEFT, expand=0, in_=self.statusbar)

        self.button_quit = ttk.Button(self.statusbar, text="Quit", command=self.parent.destroy)
        self.button_quit.pack(side=tk.RIGHT, in_=self.statusbar)
        self.statusbar.pack(expand=False, fill="x", side='bottom')

    pieces = {}
    selected = None
    selected_piece = None
    highlighted = None
    icons = {}

    color1 = "NavajoWhite2"
    color2 = "NavajoWhite4"

    rows = 8
    columns = 8

    axis_y = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
    axis_x = tuple(range(1, 9))  # (1,2,3,...8)

    @property
    def canvas_size(self):
        return self.columns * self.square_size, self.rows * self.square_size

    def number_notation(self, coord):
        return coord.x, coord.y

    def click(self, event):
        if self.turn == Player.WHITE:
            print('CLICK')

            col_size = row_size = event.widget.master.square_size

            current_column = event.x // col_size
            current_row = 7 - (event.y // row_size)

            position = Position(current_column, current_row)
            print(self.board.board[current_row][current_column])

            if self.selected_piece:
                print('AL DOILEA PAS')
                if self.move(self.selected_piece, position):
                    self.selected_piece = None
                    self.highlighted = None
                    self.selected = None
                    self.pieces = {}
                    self.refresh()
                    self.draw_pieces()

                    time.sleep(random.randint(1, 3))
                    self.turn = Player.BLACK
                    if not self.board.is_check_mate(self.turn) and not self.board.is_draw():
                        ai_move = self.strategy.take_decision(self.board)
                        self.board.move(ai_move[0], ai_move[1])
                        self.turn = Player.WHITE
                        self.refresh()
                        self.draw_pieces()

                    self.refresh()
                    if self.board.is_check_mate(self.turn) and not self.board.is_draw():
                        self.label_status["text"] = "Player " + str(self.turn) + " lost."
                        self.parent.destroy()
                    elif self.board.is_draw('all'):
                        self.label_status["text"] = "It's a draw."
                        time.sleep(5)
                        exit(0)
                else:
                    self.selected = None
                    self.selected_piece = None
                    self.highlighted = None
                    self.refresh()

            else:
                self.highlight(position)
            self.refresh()

    def move(self, p1, p2):
        aux = p2.x
        p2.x = p2.y
        p2.y = aux

        if self.board.can_move(p1.position, p2) or self.board.can_attack(p1.position, p2):
            self.board.move(p1.position, p2)
            self.label_status["text"] = p1.player.name.capitalize() + " moved piece " + str(p1.name) + " on " + str(p2) + '.'
            return True
        else:
            self.label_status["text"] = "Cannot move " + str(p1.name) + " to " + str(p2)+ '.'
            return False

    def highlight(self, pos):
        piece = self.board.board[pos.y][pos.x]

        if piece is not None and (piece.player.name == self.turn.name):
            self.selected_piece = piece
            self.highlighted = []
            l1 = self.board.available_piece_moves(piece)
            for el in l1:
                if self.board.can_move(piece.position, el):
                    self.highlighted.append(el)

            l1 = self.board.available_piece_moves(piece, attack=True)
            for el in l1:
                if self.board.can_attack(piece.position, el):
                    self.highlighted.append(el)

            if not self.highlighted:
                self.selected = None
                self.selected_piece = None
                self.highlighted = None
                self.refresh()

    def add_piece(self, name, image, row=0, column=0):
        self.canvas.create_image(0, 0, image=image, tags=(name, "piece"), anchor="c")
        self.place_piece(name, row, column)

    def place_piece(self, name, row, column):
        self.pieces[name] = (row, column)
        x0 = (column * self.square_size) + int(self.square_size / 2)
        y0 = ((7 - row) * self.square_size) + int(self.square_size / 2)
        self.canvas.coords(name, x0, y0)

    def refresh(self, event={}):
        print('refresh')
        if event:
            xsize = int((event.width - 1) / self.columns)
            ysize = int((event.height - 1) / self.rows)
            self.square_size = min(xsize, ysize)

        self.canvas.delete("square")
        color = self.color2

        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.square_size)
                y1 = ((7 - row) * self.square_size)
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size

                aux_pos = Position(row, col)

                if (self.selected is not None) and aux_pos == self.selected:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="orange", tags="square")
                elif self.highlighted is not None and aux_pos in self.highlighted:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="spring green", tags="square")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2

        for name in self.pieces:
            self.place_piece(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")

    def draw_pieces(self):
        self.canvas.delete("piece")
        for piece in self.board.get_pieces():
            x, y = piece.position.x, piece.position.y
            if piece is not None:
                filename = "img/%s%s.png" % (piece.player.name, piece.id)
                piecename = "%s%s%s" % (piece.id, x, y)

                if filename not in self.icons:
                    self.icons[filename] = tk.PhotoImage(file=filename.lower(), width=64, height=64)

                self.add_piece(piecename, self.icons[filename], x, y)
                self.place_piece(piecename, x, y)


class PvP_Game:
    def __init__(self, board):
        self.board = board
        self.board.init_board()

    def play(self):
        self.board.display_board()

        turn = Player.WHITE

        while True:
            if not self.board.is_check_mate(turn) and not self.board.is_draw():
                from_pos = input("from: ").split()
                to_pos = input("to: ").split()

                correct_input = False
                while not correct_input:
                    try:
                        from_pos = Position(int(from_pos[0]), int(from_pos[1]))
                        to_pos = Position(int(to_pos[0]), int(to_pos[1]))
                        correct_input = True
                    except:
                        print('An input pair should look like this: "1 0", where x = 1, y = 0.')
                        correct_input = False

                if self.board.get_player_from_pos(from_pos) != turn:
                    print('This is the other player turn')
                else:
                    correct_move = self.board.move(from_pos, to_pos)
                    self.board.display_board()

                    if correct_move is not None:
                        continue

                    if turn == Player.WHITE:
                        turn = Player.BLACK
                    else:
                        turn = Player.WHITE
            if self.board.is_draw():
                print("It's a draw.")
                break


class AIvAI_Game:
    def __init__(self, board: Board, ai_strategy1, ai_strategy2):
        self.board = board
        self.board.init_board()

        self.strategy1 = ai_strategy1
        self.strategy2 = ai_strategy2

    def play(self):
        self.board.display_board()

        turn = Player.WHITE

        while True:
            if not self.board.is_check_mate(turn) and not self.board.is_draw('all'):
                copy = deepcopy(self.board)
                if turn == Player.BLACK:
                    ai_move = self.strategy1.take_decision(copy)
                    if self.board.move(ai_move[0], ai_move[1]) is False:
                        return
                    self.board.display_board()
                    turn = Player.WHITE
                    continue
                elif turn == Player.WHITE:
                    ai_move = self.strategy2.take_decision(copy)
                    if self.board.move(ai_move[0], ai_move[1]) is False:
                        return
                    self.board.display_board()
                    turn = Player.BLACK
                    continue
            if self.board.is_draw('all'):
                print("It's a draw.")
                break


if __name__ == '__main__':
    print('main')
    # game = PvAI_Game(Board(), Strategies.Minimax(2, Player.BLACK, Player.WHITE))
    # game = PvAI_Game(Board(), Strategies.MinimaxRandomSample(3, 5, 5))
    # game = PvP_Game(Board())
    # game = AIvAI_Game(Board(), Strategies.MinimaxRandomSample(Player.BLACK, Player.WHITE, 3, 5, 5),
    # Strategies.MinimaxRandomSample(Player.WHITE, Player.BLACK, 3, 5, 5))
    # game = AIvAI_Game(Board(), Strategies.Minimax(3, Player.BLACK, Player.WHITE),
    #                   Strategies.Minimax(3, Player.WHITE, Player.BLACK))
    # game.play()
