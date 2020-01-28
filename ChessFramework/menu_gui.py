import tkinter as tk
from tkinter.font import Font

import Strategies
from Move import *
from Piece import Piece, Player
from Position import Position
from Board import Board
from game import PvAI_Game

from tkinter import ttk
from ttkthemes import ThemedTk

APPNAME = "Savvy Chess"
FONTSIZE = 12

class GUI:

    def __init__(self):
        self.main_window=None
        self.THEME = "equilux"

    def popup(self, text):
        win = tk.Toplevel()
        win.wm_title("Error!")
        l = ttk.Label(win, text=text)
        l.grid(row=0, column=0)
        b = ttk.Button(win, text="Ok", command=win.destroy)
        b.grid(row=1, column=0)

    def classic_button_function(self):
        self.exit_button_function()

        root = ThemedTk(theme=self.THEME)
        root.title(APPNAME)
        ws = root.winfo_screenwidth() / 2
        hs = root.winfo_screenheight() / 2
        root.geometry('%dx%d+%d+%d' % (580, 614, ws - 290, hs - 307))
        root.resizable(0, 0)


        game = PvAI_Game(Board(), Strategies.Minimax(2, Player.BLACK, Player.WHITE), root, width=592, height=618)
        game.pack(side="top", fill="both", expand="true")
        game.draw_pieces()

        root.mainloop()

    def custom_button_function(self):
        self.exit_button_function()
        all_movements_list = []

        moves = []
        attacks = []

        custom_window = ThemedTk(theme=self.THEME)
        custom_window.title(APPNAME + ': Define custom movements')
        custom_window.geometry('470x750')
        ws = custom_window.winfo_screenwidth() / 2
        hs = custom_window.winfo_screenheight() / 2
        custom_window.geometry('%dx%d+%d+%d' % (470, 750, ws - 235, hs - 375))
        custom_window.resizable(0, 0)
        
        def add_move():
            try:
                x = int(x_move.get())
                y = int(y_move.get())
            except ValueError:
                return False

            moves.append((x, y))

        def add_attack():
            try:
                x = int(x_attack.get())
                y = int(y_attack.get())
            except ValueError:
                return False

            attacks.append((x, y))

        def add_new_movement():
            new_movement = CustomMovement()

            new_movement.set_name(move_name.get())
            new_movement.set_vacant(vacant_flag.get())

            str_moves = ""
            for move in moves:
                str_moves += '(' + str(move[0]) + ', ' + str(move[1]) + ') ' 
                new_movement.add_custom_movement(move[0], move[1])

            str_attacks = ""
            for attack in attacks:
                str_attacks += '(' + str(attack[0]) + ', ' + str(attack[1]) + ') ' 
                new_movement.add_custom_attack(attack[0], attack[1])

            moves.clear()
            attacks.clear()
            all_movements_list.append(new_movement)
            tv.insert("", 0, text=move_name.get(), values=(str_moves, str_attacks))
        
        move_name = tk.StringVar()
        x_move = tk.StringVar()
        y_move = tk.StringVar()
        x_attack = tk.StringVar()
        y_attack = tk.StringVar()
        vacant_flag = tk.BooleanVar()


        style = ttk.Style(custom_window)
        font = Font(size=FONTSIZE)
        style.configure("TButton", font=font)
     
        subtitle_font = Font(size=60, weight='bold')
        frame = ttk.Frame(custom_window, width=470, height=750)
        frame.grid(row=0, columnspan=3)
        frame.pack(fill="both", expand=1)

        pb_label = ttk.Label(frame, text="Progress:")
        pb_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        pb = ttk.Progressbar(frame, orient="horizontal", length=200, mode="determinate")
        pb.grid(row=0, column=1, padx=10, pady=10, sticky=tk.E)
        pb["maximum"] = 8
        pb["value"] = 1

        name_label = ttk.Label(frame, text="Set movement rule name:")
        name_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        move_name_entry = ttk.Entry(frame, textvariable=move_name)
        move_name_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        move_x_label = ttk.Label(frame, text="Move on X:")
        move_x_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

        move_x = ttk.Entry(frame, textvariable=x_move, width=5)
        move_x.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

        move_y_label = ttk.Label(frame, text="Move on Y:")
        move_y_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)

        move_y = ttk.Entry(frame, textvariable=y_move, width=5)
        move_y.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)
        
        add_move_button = ttk.Button(frame, text="Add new move", command=add_move)
        add_move_button.grid(row=5, columnspan=3, padx=10, pady=10)

        attack_x_label = ttk.Label(frame, text="Attack on X:")
        attack_x_label.grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)

        attack_x = ttk.Entry(frame, textvariable=x_attack, width=5)
        attack_x.grid(row=7, column=1, padx=10, pady=5, sticky=tk.W)

        attack_y_label = ttk.Label(frame, text="Attack on Y:")
        attack_y_label.grid(row=8, column=0, padx=10, pady=5, sticky=tk.W)

        attack_y = ttk.Entry(frame, textvariable=y_attack, width=5)
        attack_y.grid(row=8, column=1, padx=10, pady=5, sticky=tk.W)

        add_attack_button = ttk.Button(frame, text="Add new attack", command=add_attack)
        add_attack_button.grid(row=9, columnspan=3, padx=10, pady=10)

        set_vacant_label = ttk.Label(frame, text="Move on vacant squares:")
        set_vacant_label.grid(row=11, column=0, padx=10, pady=10, sticky=tk.W)

        set_vacant_checkbox = ttk.Checkbutton(frame, variable=vacant_flag)
        set_vacant_checkbox.grid(row=11, column=1, padx=10, pady=10, sticky=tk.W)

        add_button = ttk.Button(frame, text="Add new movement", command=add_new_movement)
        add_button.grid(row=12, columnspan=3, padx=10, pady=10)

        
        tv = ttk.Treeview(frame)
        tv['columns'] = ('moves', 'attacks')
        tv.heading("#0", text='Movement', anchor='w')
        tv.column("#0", anchor="w")
        tv.heading('moves', text='Moves')
        tv.column('moves', anchor='center', width=100)
        tv.heading('attacks', text='Attacks')
        tv.column('attacks', anchor="e", width=100)
        tv.grid(rowspan=8, columnspan=3, padx=20, pady=10, sticky = (tk.N, tk.S, tk.W, tk.E))
    
        add_button = ttk.Button(frame, text="Next step", command=custom_window.destroy)
        add_button.grid(row=22, columnspan=3, padx=10, pady=10)
        custom_window.mainloop()
        
        all_movements_list.append(HorizontalMovement())
        all_movements_list.append(LimitedDiagonalMovement())
        all_movements_list.append(LimitedHorizontalMovement())
        all_movements_list.append(LimitedVerticalMovement())
        all_movements_list.append(DiagonalMovement())
        all_movements_list.append(HorizontalMovement())
        all_movements_list.append(VerticalMovement())
        all_movements_list.append(PawnMovement())
        all_movements_list.append(HorseMovement())

        pieces = ['Pawn', 'Horse', 'Bishop', 'Rook', 'Queen', 'King']
        pieces_movement_flags = []

        def submit_check():
            for val in result:
                if val.get():
                    custom_window.destroy()
                    return
            self.popup("Check at least one movement for the piece!")

        cnt = 1
        for piece in pieces:
            custom_window = ThemedTk(theme=self.THEME)
            custom_window.title(APPNAME + ': Customize piece movements')
            ws = custom_window.winfo_screenwidth() / 2
            hs = custom_window.winfo_screenheight() / 2
            custom_window.geometry('%dx%d+%d+%d' % (470, 750, ws - 235, hs - 375))
            custom_window.resizable(0, 0)

            frame = ttk.Frame(custom_window, width=470, height=750)
            frame.grid(row=0, columnspan=3, sticky="nsew")
            frame.pack(fill="both", expand=1)

            pb_label = ttk.Label(frame, text="Progress:", font=subtitle_font)
            pb_label.grid(row=0, column=0, padx=30, pady=10, sticky=tk.W)

            pb = ttk.Progressbar(frame, orient="horizontal", length=200, mode="determinate")
            pb.grid(row=0, column=0, padx=140, pady=10, sticky=tk.W)
            pb["maximum"] = 8
            pb["value"] = 1 + cnt
            
            cnt += 1
            
            piece_label = ttk.Label(frame, text=piece, font=subtitle_font)
            piece_label.grid(row=1, column=0, columnspan=3, padx=30, pady=30, sticky="nsew")
            
            count = 0
            result = []
            for movement in all_movements_list:
                if piece=='King' and 'Limited' in movement.name:
                        result.append(tk.BooleanVar(value=True))
                elif piece=='Bishop' and movement.name=='Diagonal movement':
                        result.append(tk.BooleanVar(value=True))
                elif piece=='Queen' and (movement.name=='Horizontal movement' or movement.name=='Vertical movement' or movement.name=='Diagonal movement'):
                        result.append(tk.BooleanVar(value=True))
                elif piece=='Rook' and (movement.name=='Horizontal movement' or movement.name=='Vertical movement'):
                        result.append(tk.BooleanVar(value=True))
                elif piece =='Horse' and movement.name=='Horse movement':
                        result.append(tk.BooleanVar(value=True))
                elif piece=='Pawn' and movement.name=='Pawn movement':
                        result.append(tk.BooleanVar(value=True))
                else:
                    result.append(tk.BooleanVar(value=False))
                ttk.Checkbutton(frame,
                               text=movement.name,
                               variable=result[count]).grid(row=count+2, column=0, padx=50, pady=10, sticky=tk.W)
                
                
                count += 1

            add_button = ttk.Button(frame, text="Next step", command=submit_check)
            add_button.grid(row=22, columnspan=3, padx=30, pady=30, sticky=tk.S)
            custom_window.mainloop()

            pieces_movement_flags.append(result)
        custom_window = ThemedTk(theme=self.THEME)
        custom_window.title(APPNAME + ': Custom locations')
        ws = custom_window.winfo_screenwidth() / 2
        hs = custom_window.winfo_screenheight() / 2
        custom_window.geometry('%dx%d+%d+%d' % (660, 750, ws - 330, hs - 375))
        custom_window.resizable(0, 0)

        frame = ttk.Frame(custom_window, width=660, height=750)
        frame.pack(fill="both", expand=1)
        frame.grid(row=0, column=0, columnspan=6)
        
        pb_label = ttk.Label(frame, text="Progress:", font=subtitle_font)
        pb_label.grid(row=0, column=0, padx=30, pady=10, sticky=tk.W)

        pb = ttk.Progressbar(frame, orient="horizontal", length=200, mode="determinate")
        pb.grid(row=0, column=1, columnspan=5, padx=30, pady=10, sticky=tk.W)
        pb["maximum"] = 8
        pb["value"] = 8

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
            logs.insert(tk.END, "\nAdded " + piece_to_add.name + " at position " + str(Position(column.get(), row.get())) + ".")

        piece_selection_label = ttk.Label(frame, text='Piece selection', font=subtitle_font)
        piece_selection_label.grid(row=1, column=0, padx=30, pady=30)

        count = 0
        piece_name = tk.IntVar()
        for piece in pieces:
            ttk.Radiobutton(frame,
                           text=piece,
                           variable=piece_name,
                           value=count).grid(row=count+2, column=0, padx=30, pady=10, sticky=tk.W)
            count += 1
        sep = ttk.Separator(frame, orient="vertical")
        sep.grid(column=1, row=1, rowspan=10, pady=20, sticky="ns")

        piece_location_label = ttk.Label(frame, text='Piece location', font=subtitle_font)
        piece_location_label.grid(row=1, column=2, columnspan=2, padx=30, pady=30)

        piece_location_description_label = ttk.Label(frame, text='Select the row\n(first is the closest)')
        piece_location_description_label.grid(row=2, column=2, columnspan=2, padx=10, pady=10)

        row = tk.IntVar(value=1)
        ttk.Radiobutton(frame, text='First row', variable=row, value=1).grid(row=3, column=2, columnspan=2, sticky=tk.W, padx=20)
        ttk.Radiobutton(frame, text='Second row', variable=row, value=2).grid(row=4, column=2, columnspan=2, sticky=tk.W, padx=20)
        piece_location_description_label = ttk.Label(frame, text='Select the column\n(from left to right)')
        piece_location_description_label.grid(row=5, column=2, columnspan=2, padx=10, pady=10)

        column = tk.IntVar(value=1)
        for i in range(4):
            ttk.Radiobutton(frame, text=str(i + 1), variable=column, value=i + 1).grid(row=6+i, column=2, padx=40, pady=10, sticky=tk.W)
            ttk.Radiobutton(frame, text=str(i + 5), variable=column, value=i+5).grid(row=6+i, column=3, padx=40, pady=10, sticky=tk.E)
        sep2 = ttk.Separator(frame, orient="vertical")
        sep2.grid(column=4, row=1, rowspan=12, pady=20, sticky="ns")
        add_button = ttk.Button(frame, text="Add", command=add_piece_to_game, width=20, style="TButton")
        add_button.grid(row=1, rowspan=11, column=5, sticky="nsew", padx=20, pady=240)
       
        logs = tk.Text(frame, height=8)
        logs.grid(row=13, column=0, columnspan=6, rowspan=1, padx=10, pady=5)
        logs.insert(tk.END, "Try adding pieces to the board!")
       
        play_button = ttk.Button(frame, text="Play", command=custom_window.destroy, width=30, style="TButton")
        play_button.grid(row=14, column=0, columnspan=7, sticky="nsew", padx=10, pady=10)
        
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

        root = ThemedTk(theme=self.THEME)
        root.title(APPNAME)
        ws = root.winfo_screenwidth() / 2
        hs = root.winfo_screenheight() / 2
        root.geometry('%dx%d+%d+%d' % (580, 614, ws - 290, hs - 307))
        root.resizable(0, 0)

        game = PvAI_Game(custom_board, Strategies.MinimaxRandomSample(Player.BLACK, Player.WHITE, 2, 10, 10), root, custom_flag=True, width=592, height=618)
        game.pack(side="top", fill="both", expand="true")
        game.draw_pieces()

        root.mainloop()

    def exit_button_function(self):
        self.main_window.destroy()

    def change_theme(self):
        if self.THEME == 'equilux':
            self.THEME = 'radiance'
        else:
            self.THEME = 'equilux'

        self.main_window.destroy()
        self.init_GUI()


    def init_GUI(self):
        self.main_window = ThemedTk(theme=self.THEME)
        self.main_window.set_theme(self.THEME)
        self.main_window.title(APPNAME)

        self.main_window.geometry('400x300')
        ws = self.main_window.winfo_screenwidth() / 2
        hs = self.main_window.winfo_screenheight() / 2
        self.main_window.geometry('%dx%d+%d+%d' % (400, 300, ws - 200, hs - 150))
        self.main_window.resizable(0, 0)


        style = ttk.Style(self.main_window)
        font = Font(size=12)
        style.configure("TButton", font=font)
     
        frame = ttk.Frame(self.main_window, width = 400, height=300)
        frame.pack(fill="both", expand=1)

        classic_button = ttk.Button(frame, text='Classic', style="TButton", command=self.classic_button_function)
        classic_button.pack(padx=100, pady=20)

        custom_button = ttk.Button(frame, text='Custom', style="TButton", command=self.custom_button_function)
        custom_button.pack(padx=100, pady=20)

        if self.THEME == 'equilux':
            t = 'light'
        else:
            t = 'dark'
        change_theme = ttk.Button(frame, text='Use  ' + t + ' theme', style="TButton", command=self.change_theme)
        change_theme.pack(padx=100, pady=20)

        exit_button = ttk.Button(frame, text='Exit', style="TButton", command=self.exit_button_function)
        exit_button.pack(padx=100, pady=20)


        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(4, weight=1)
        self.main_window.mainloop()


test = GUI()
test.init_GUI()
