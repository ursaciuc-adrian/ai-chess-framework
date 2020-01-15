import tkinter as tk

import Strategies
from Move import *
from Piece import Piece, Player
from Position import Position
from Board import Board
from game import PvAI_Game


class GUI:
    main_window = tk.Tk()
    main_window.title('Chess Menu')
    main_window.geometry('400x300')
    ws = main_window.winfo_screenwidth() / 2
    hs = main_window.winfo_screenheight() / 2
    main_window.geometry('%dx%d+%d+%d' % (400, 300, ws - 200, hs - 150))
    main_window.resizable(0, 0)

    def classic_button_function(self):
        self.exit_button_function()
        print('classic button')

        root = tk.Tk()
        root.title("Simple Python Chess")

        game = PvAI_Game(Board(), Strategies.Minimax(2, Player.BLACK, Player.WHITE), root)
        game.pack(side="top", fill="both", expand="true", padx=4, pady=4)
        game.draw_pieces()

        root.mainloop()

    def custom_button_function(self):
        self.exit_button_function()
        all_movements_list = []

        moves = []
        attacks = []

        custom_window = tk.Tk()
        custom_window.title('Custom movements')
        custom_window.geometry('800x750')
        ws = custom_window.winfo_screenwidth() / 2
        hs = custom_window.winfo_screenheight() / 2
        custom_window.geometry('%dx%d+%d+%d' % (800, 750, ws - 400, hs - 375))
        custom_window.resizable(0, 0)

        def add_move():
            try:
                x = int(x_move.get())
                y = int(y_move.get())
            except ValueError:
                return False

            moves.append((x, y))
            print('added move')

        def add_attack():
            try:
                x = int(x_attack.get())
                y = int(y_attack.get())
            except ValueError:
                return False

            attacks.append((x, y))
            print('added attack')

        def add_new_movement():
            new_movement = CustomMovement()

            new_movement.set_name(move_name.get())
            new_movement.set_vacant(vacant_flag.get())

            for move in moves:
                new_movement.add_custom_movement(move[0], move[1])

            for attack in attacks:
                new_movement.add_custom_attack(attack[0], attack[1])

            moves.clear()
            attacks.clear()
            all_movements_list.append(new_movement)

            print('added movement')

        move_name = tk.StringVar()
        x_move = tk.StringVar()
        y_move = tk.StringVar()
        x_attack = tk.StringVar()
        y_attack = tk.StringVar()
        vacant_flag = tk.BooleanVar()

        name_label = tk.Label(custom_window, text="Enter your new move name:", font=("Courier", 20))
        name_label.place(x=40, y=30)

        move_name_entry = tk.Entry(custom_window, textvariable=move_name, width=30, font=("Courier", 15))
        move_name_entry.place(x=40, y=80)

        move_label = tk.Label(custom_window, text="Add moves:", font=("Courier", 20))
        move_label.place(x=40, y=120)

        move_x_label = tk.Label(custom_window, text="X", font=("Courier", 20))
        move_x_label.place(x=50, y=200)

        move_x = tk.Entry(custom_window, textvariable=x_move, width=5, font=("Courier", 15))
        move_x.place(x=72, y=204)

        move_y_label = tk.Label(custom_window, text="Y:", font=("Courier", 20))
        move_y_label.place(x=150, y=200)

        move_y = tk.Entry(custom_window, textvariable=y_move, width=5, font=("Courier", 15))
        move_y.place(x=172, y=204)

        add_move_button = tk.Button(custom_window, text="Add new move", command=add_move, font=("Courier", 15))
        add_move_button.place(x=300, y=198)

        attack_label = tk.Label(custom_window, text="Add attacks:", font=("Courier", 20))
        attack_label.place(x=40, y=280)

        attack_x_label = tk.Label(custom_window, text="X", font=("Courier", 20))
        attack_x_label.place(x=50, y=360)

        attack_x = tk.Entry(custom_window, textvariable=x_attack, width=5, font=("Courier", 15))
        attack_x.place(x=72, y=364)

        attack_y_label = tk.Label(custom_window, text="Y:", font=("Courier", 20))
        attack_y_label.place(x=150, y=360)

        attack_y = tk.Entry(custom_window, textvariable=y_attack, width=5, font=("Courier", 15))
        attack_y.place(x=172, y=364)

        add_attack_button = tk.Button(custom_window, text="Add new attack", command=add_attack, font=("Courier", 15))
        add_attack_button.place(x=300, y=358)

        set_vacant_label = tk.Label(custom_window, text="Set vacant(default is False):", font=("Courier", 20))
        set_vacant_label.place(x=40, y=450)

        set_vacant_checkbox = tk.Checkbutton(custom_window, variable=vacant_flag, font=("Courier", 20))
        set_vacant_checkbox.place(x=515, y=448)

        add_button = tk.Button(custom_window, text="Add new movement", command=add_new_movement, font=("Courier", 20))
        add_button.place(x=40, y=520)

        logs = tk.Text(custom_window, height=4, width=90)
        logs.place(x=40, y=620)
        logs.insert(tk.END, "Just a text Widget\nin two lines\n")

        add_button = tk.Button(custom_window, text="Next step", command=custom_window.destroy, font=("Courier", 20))
        add_button.place(x=590, y=695)

        custom_window.mainloop()

        all_movements_list.append(HorizontalMovement())
        all_movements_list.append(LimitedDiagonalMovement())
        all_movements_list.append(LimitedHorizontalMovement())
        all_movements_list.append(LimitedVerticalMovement())
        all_movements_list.append(DiagonalMovement())
        all_movements_list.append(HorizontalMovement())
        all_movements_list.append(VerticalMovement())
        all_movements_list.append(PawnMovement())

        pieces = ['Pawn', 'Knight', 'Bishop', 'Rook', 'Queen', 'King']
        pieces_movement_flags = []

        def submit_check():
            for val in result:
                if val.get():
                    custom_window.destroy()
                    return

            print('at least one')

        for piece in pieces:
            custom_window = tk.Tk()
            custom_window.title('Custom movements')
            ws = custom_window.winfo_screenwidth() / 2
            hs = custom_window.winfo_screenheight() / 2
            custom_window.geometry('%dx%d+%d+%d' % (800, 800, ws - 400, hs - 400))
            custom_window.resizable(0, 0)

            piece_label = tk.Label(custom_window, text=piece, font=("Courier", 50))
            piece_label.place(x=100, y=15)

            count = 0
            result = []
            for movement in all_movements_list:
                result.append(tk.BooleanVar())
                tk.Checkbutton(custom_window,
                               text=movement.name,
                               padx=20,
                               variable=result[count],
                               font=("Courier", 15)).place(x=140, y=100 + count * 40)

                count += 1

            add_button = tk.Button(custom_window, text="Next step", command=submit_check, font=("Courier", 20))
            add_button.place(x=590, y=720)

            custom_window.mainloop()

            pieces_movement_flags.append(result)

        custom_window = tk.Tk()
        custom_window.title('Custom locations')
        ws = custom_window.winfo_screenwidth() / 2
        hs = custom_window.winfo_screenheight() / 2
        custom_window.geometry('%dx%d+%d+%d' % (800, 800, ws - 400, hs - 400))
        custom_window.resizable(0, 0)

        pieces_for_game = []

        def add_piece_to_game():
            flag_count = 0
            piece_to_add = Piece(pieces[piece_name.get()], pieces[piece_name.get()][0])

            for flag in pieces_movement_flags[piece_name.get()]:
                if flag.get():
                    piece_to_add.add_movement(all_movements_list[flag_count])

                flag_count += 1

            piece_to_add.set_position(Position(column.get(), row.get()))
            pieces_for_game.append(piece_to_add)

        piece_selection_label = tk.Label(custom_window, text='Piece selection', font=("Courier", 20))
        piece_selection_label.place(x=20, y=15)

        count = 0
        piece_name = tk.IntVar()
        for piece in pieces:
            tk.Radiobutton(custom_window,
                           text=piece,
                           padx=20,
                           variable=piece_name,
                           value=count,
                           font=("Courier", 15)).place(x=70, y=70 + count * 50)

            count += 1

        piece_location_label = tk.Label(custom_window, text='Piece location', font=("Courier", 20))
        piece_location_label.place(x=320, y=15)

        piece_location_description_label = tk.Label(custom_window, text='Select the row\n(first is the closest)',
                                                    font=("Courier", 15))
        piece_location_description_label.place(x=300, y=70)

        row = tk.IntVar(value=1)
        tk.Radiobutton(custom_window, text='First row', padx=20, variable=row, value=1,
                       font=("Courier", 15)).place(x=340, y=130)
        tk.Radiobutton(custom_window, text='Second row', padx=20, variable=row, value=2,
                       font=("Courier", 15)).place(x=340, y=170)

        piece_location_description_label = tk.Label(custom_window, text='Select the column\n(from left to right)',
                                                    font=("Courier", 15))
        piece_location_description_label.place(x=312, y=220)

        column = tk.IntVar(value=1)
        for i in range(8):
            tk.Radiobutton(custom_window, text=str(i + 1), padx=20, variable=column, value=i + 1,
                           font=("Courier", 15)).place(x=360 + i // 4 * 70, y=290 + i % 4 * 30)

        add_button = tk.Button(custom_window, text="Add", command=add_piece_to_game, font=("Courier", 20))
        add_button.place(x=655, y=190)

        play_button = tk.Button(custom_window, text="Play", command=custom_window.destroy, font=("Courier", 20))
        play_button.place(x=655, y=720)

        canvas1 = tk.Canvas(custom_window, width=2, height=430)
        canvas1.create_line(2, 10, 2, 1600)
        canvas1.place(x=280, y=5)

        canvas2 = tk.Canvas(custom_window, width=2, height=430)
        canvas2.create_line(2, 10, 2, 1600)
        canvas2.place(x=580, y=5)

        canvas3 = tk.Canvas(custom_window, width=800, height=2)
        canvas3.create_line(2, 2, 1600, 2)
        canvas3.place(x=10, y=55)

        canvas4 = tk.Canvas(custom_window, width=800, height=2)
        canvas4.create_line(2, 2, 1600, 2)
        canvas4.place(x=10, y=440)

        logs = tk.Text(custom_window, height=1, width=90)
        logs.place(x=40, y=680)
        logs.insert(tk.END, "Just a text Widgetin two lines")

        custom_window.mainloop()

        custom_board = Board()
        custom_board.board = [[None for j in range(custom_board.SIZE)] for i in range(custom_board.SIZE)]

        for el in pieces_for_game:
            # x coloana, y randul
            el_pos_x_w = el.position.x - 1
            el_pos_y_w = el.position.y - 1

            el_pos_x_b = 7 - el_pos_x_w

            if el_pos_y_w == 0:
                el_pos_y_b = 7
            else:
                el_pos_y_b = 6

            custom_board.add_piece(el, Position(el_pos_y_w, el_pos_x_w), Player.WHITE)
            custom_board.add_piece(el, Position(el_pos_y_b, el_pos_x_b), Player.BLACK)

        root = tk.Tk()
        root.title("Simple Python Chess")

        game = PvAI_Game(custom_board, Strategies.Minimax(2, Player.BLACK, Player.WHITE), root, custom_flag=True)
        game.pack(side="top", fill="both", expand="true", padx=4, pady=4)
        game.draw_pieces()

        root.mainloop()

    def exit_button_function(self):
        self.main_window.destroy()

    def init_GUI(self):
        classic_button = tk.Button(self.main_window, text='Classic', width=25, command=self.classic_button_function)
        classic_button.place(height=50, width=200, relx=0.5, rely=0.2, anchor=tk.CENTER)

        custom_button = tk.Button(self.main_window, text='Custom', width=25, command=self.custom_button_function)
        custom_button.place(height=50, width=200, relx=0.5, rely=0.5, anchor=tk.CENTER)

        exit_button = tk.Button(self.main_window, text='Exit', width=25, command=self.exit_button_function)
        exit_button.place(height=50, width=200, relx=0.5, rely=0.8, anchor=tk.CENTER)

        self.main_window.mainloop()


test = GUI()
test.init_GUI()
