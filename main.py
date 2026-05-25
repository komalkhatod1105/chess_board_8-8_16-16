import tkinter as tk
from tkinter import messagebox

# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()

root.title("Chess Game")
root.geometry("1600x1000")

# =========================
# VARIABLES
# =========================

board_size = 8
selected = None
current_player = "WHITE"

buttons = []
board_data = []

white_captured = []
black_captured = []

# =========================
# FRAMES
# =========================

top_frame = tk.Frame(root)
top_frame.pack(pady=10)

status_label = tk.Label(
    root,
    text="WHITE TURN",
    font=("Arial", 18, "bold")
)

status_label.pack()

white_label = tk.Label(
    root,
    text="WHITE CAPTURED: ",
    font=("Arial", 14)
)

white_label.pack()

black_label = tk.Label(
    root,
    text="BLACK CAPTURED: ",
    font=("Arial", 14)
)

black_label.pack()

board_frame = tk.Frame(root)
board_frame.pack(pady=20)

# =========================
# PIECES
# =========================

white_pieces = [
    "♖","♘","♗","♕",
    "♔","♗","♘","♖"
]

black_pieces = [
    "♜","♞","♝","♛",
    "♚","♝","♞","♜"
]

# =========================
# CREATE BOARD DATA
# =========================

def get_board(size):

    board = [["" for _ in range(size)] for _ in range(size)]

    # =====================
    # 8 x 8
    # =====================

    if size == 8:

        board[0] = black_pieces
        board[1] = ["♟"] * 8

        board[6] = ["♙"] * 8
        board[7] = white_pieces

    # =====================
    # 16 x 16
    # =====================

    else:

        top16 = [
            "♜","♞","♝","♛",
            "♚","♝","♞","♜",
            "♜","♞","♝","♛",
            "♚","♝","♞","♜"
        ]

        bottom16 = [
            "♖","♘","♗","♕",
            "♔","♗","♘","♖",
            "♖","♘","♗","♕",
            "♔","♗","♘","♖"
        ]

        board[0] = top16
        board[1] = ["♟"] * 16

        board[14] = ["♙"] * 16
        board[15] = bottom16

    return board

# =========================
# DRAW BOARD
# =========================

def draw_board():

    for widget in board_frame.winfo_children():
        widget.destroy()

    buttons.clear()

    # board settings

    if board_size == 8:

        width = 3
        height = 1
        font_size = 16

    else:

        width = 2
        height = 1
        font_size = 12

    # draw board

    for row in range(board_size):

        row_buttons = []

        for col in range(board_size):

            color = "#F0D9B5"

            if (row + col) % 2 == 0:
                color = "#B58863"

            piece = board_data[row][col]

            fg_color = "black"

            if piece in [
                "♙","♖","♘",
                "♗","♕","♔"
            ]:
                fg_color = "blue"

            btn = tk.Button(
                board_frame,
                text=piece,
                font=("Arial", font_size, "bold"),
                bg=color,
                fg=fg_color,
                width=width,
                height=height,
                relief="raised",
                bd=2,
                command=lambda r=row,c=col:
                    click_cell(r,c)
            )

            btn.grid(row=row,column=col)

            row_buttons.append(btn)

        buttons.append(row_buttons)

# =========================
# CHECK WINNER
# =========================

def check_winner():

    white_king = False
    black_king = False

    for row in board_data:

        for piece in row:

            if piece == "♔":
                white_king = True

            if piece == "♚":
                black_king = True

    if not white_king:

        messagebox.showinfo(
            "Winner",
            "BLACK WINS"
        )

        return True

    if not black_king:

        messagebox.showinfo(
            "Winner",
            "WHITE WINS"
        )

        return True

    return False

# =========================
# VALID MOVE
# =========================

def valid_move(piece, fr, fc, tr, tc):

    # same position

    if fr == tr and fc == tc:
        return False

    # board limit

    if tr < 0 or tr >= board_size:
        return False

    if tc < 0 or tc >= board_size:
        return False

    white_set = [
        "♙","♖","♘",
        "♗","♕","♔"
    ]

    black_set = [
        "♟","♜","♞",
        "♝","♛","♚"
    ]

    target = board_data[tr][tc]

    # same team

    if piece in white_set and target in white_set:
        return False

    if piece in black_set and target in black_set:
        return False

    return True

# =========================
# CLICK CELL
# =========================

def click_cell(row, col):

    global selected
    global current_player

    piece = board_data[row][col]

    # =====================
    # FIRST CLICK
    # =====================

    if selected is None:

        if piece == "":
            return

        # white turn

        if current_player == "WHITE":

            if piece not in [
                "♙","♖","♘",
                "♗","♕","♔"
            ]:

                messagebox.showerror(
                    "Wrong Turn",
                    "WHITE TURN"
                )

                return

        # black turn

        else:

            if piece not in [
                "♟","♜","♞",
                "♝","♛","♚"
            ]:

                messagebox.showerror(
                    "Wrong Turn",
                    "BLACK TURN"
                )

                return

        selected = (row,col)

        buttons[row][col].config(bg="yellow")

    # =====================
    # SECOND CLICK
    # =====================

    else:

        fr, fc = selected

        moving_piece = board_data[fr][fc]

        if valid_move(
            moving_piece,
            fr, fc,
            row, col
        ):

            # capture

            captured_piece = board_data[row][col]

            if captured_piece != "":

                # white captured

                if captured_piece in [
                    "♙","♖","♘",
                    "♗","♕","♔"
                ]:

                    white_captured.append(
                        captured_piece
                    )

                    white_label.config(
                        text=
                        "WHITE CAPTURED: "
                        + " ".join(white_captured)
                    )

                # black captured

                else:

                    black_captured.append(
                        captured_piece
                    )

                    black_label.config(
                        text=
                        "BLACK CAPTURED: "
                        + " ".join(black_captured)
                    )

            # move piece

            board_data[row][col] = moving_piece

            board_data[fr][fc] = ""

            # switch player

            if current_player == "WHITE":

                current_player = "BLACK"

                status_label.config(
                    text="BLACK TURN"
                )

            else:

                current_player = "WHITE"

                status_label.config(
                    text="WHITE TURN"
                )

            draw_board()

            check_winner()

        else:

            messagebox.showerror(
                "Invalid Move",
                "Wrong Move"
            )

            draw_board()

        selected = None

# =========================
# CREATE BOARD
# =========================

def create_board(size):

    global board_size
    global board_data
    global selected
    global current_player
    global white_captured
    global black_captured

    selected = None

    current_player = "WHITE"

    white_captured.clear()
    black_captured.clear()

    white_label.config(
        text="WHITE CAPTURED: "
    )

    black_label.config(
        text="BLACK CAPTURED: "
    )

    status_label.config(
        text="WHITE TURN"
    )

    board_size = size

    board_data = get_board(size)

    draw_board()

# =========================
# TOP BUTTONS
# =========================

btn8 = tk.Button(
    top_frame,
    text="8 x 8 Chess",
    font=("Arial",14),
    command=lambda: create_board(8)
)

btn8.grid(row=0,column=0,padx=20)

btn16 = tk.Button(
    top_frame,
    text="16 x 16 Chess",
    font=("Arial",14),
    command=lambda: create_board(16)
)

btn16.grid(row=0,column=1,padx=20)

# =========================
# START GAME
# =========================

create_board(8)

# =========================
# MAIN LOOP
# =========================

root.mainloop()