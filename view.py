import tkinter as tk

initial_highlight_color = "#FF0000"
initial_background_color = "#000000"
initial_tile_color = "#FFFFFF"

class View:
    def __init__(self):
        self.tile_color = initial_tile_color
        self.background_color = initial_background_color
        self.highlight_color = initial_highlight_color

        self.window = tk.Tk()
        self.board = {}
        self.canvas = None
        self.controller = None

    def init_window(self, game, width, height, scale):
        """Initializes window. Fills with all necessary stuff"""
        self.controller = game
        self.window.geometry("{0}x{1}".format((width * scale)+5, (height * scale)+5))
        self.window.resizable(False, False)

        self.canvas = tk.Canvas(self.window, width=width * scale, height=height * scale)
        self.canvas.grid(row=0, column=0, sticky="nesw")

        self.draw_grid(width, height, scale)

        self.window.bind("<Button-1>", lambda a: game.toggle_onclick(a))
        self.window.bind("<B1-Motion>", lambda a: game.toggle_onclick(a))
        self.window.bind("<space>", lambda a: game.toggle_pause())
        self.window.bind("<Return>", lambda a: game.do_step())
        self.window.bind("<BackSpace>", lambda a: game.reset())
        self.set_menu()

    def draw_grid(self, width, height, scale):
        """Prints Game board"""
        for x in range(0, width):
            for y in range(0, height):
                self.board[(x, y)] = self.canvas.create_rectangle(x * scale, y * scale,
                                                                  (x * scale) + scale,
                                                                  (y * scale) + scale,
                                                                  fill=self.background_color,
                                                                  activefill=self.highlight_color)

    def update_title(self, paused, mode, width, height):
        """Reset window title"""
        state = "Paused" if paused else ""
        mode_title = "Normal" if mode == 1 else "Spherical"
        self.window.wm_title("{}x{} | {} Mode | {}".format(width, height, mode_title, state))

    def reset(self, width, height):
        """Reset board, perform reseting animation"""
        for x in range(width):
            for y in range(height):
                self.canvas.itemconfig(self.board[(x, y)], fill=self.highlight_color)
            self.canvas.update()

        for x in range(width):
            for y in range(height):
                self.canvas.itemconfig(self.board[(x, y)], fill=self.background_color)
            self.canvas.update()

    def change_color(self, x, y, state):
        """change color of a tile by state"""
        if state == 1:
            color = self.tile_color
        else:
            color = self.background_color
        self.canvas.itemconfig(self.board[(x, y)], fill=color)

    def set_color(self, background_color, color):
        """Reset tile color scheme"""
        self.background_color = background_color
        self.tile_color = color
        self.controller.refresh_board()

    def set_menu(self):
        """Inits Menu bar"""
        menubar = tk.Menu(self.window)
        grid_size = tk.Menu(menubar, tearoff=0)
        grid_size.add_command(label="50x50", command= lambda: self.controller.change_grid_size(50, 50))
        grid_size.add_command(label="75x75", command= lambda: self.controller.change_grid_size(75, 75))
        grid_size.add_command(label="100x100", command= lambda: self.controller.change_grid_size(100, 100))
        grid_size.add_command(label="125x125", command= lambda: self.controller.change_grid_size(125, 125))
        grid_size.add_command(label="150x150", command= lambda: self.controller.change_grid_size(150, 150))
        menubar.add_cascade(label="Grid Size", menu=grid_size)

        pattern = tk.Menu(menubar, tearoff=0)
        pattern.add_command(label="0% Living", command= lambda: self.controller.update_filling(0))
        pattern.add_command(label="10% Living", command=lambda: self.controller.update_filling(0.1))
        pattern.add_command(label="20% Living", command=lambda: self.controller.update_filling(0.2))
        pattern.add_command(label="30% Living", command=lambda: self.controller.update_filling(0.3))
        pattern.add_command(label="40% Living", command=lambda: self.controller.update_filling(0.4))
        pattern.add_command(label="50% Living", command=lambda: self.controller.update_filling(0.5))
        pattern.add_command(label="60% Living", command=lambda: self.controller.update_filling(0.6))
        pattern.add_command(label="70% Living", command=lambda: self.controller.update_filling(0.7))
        pattern.add_command(label="80% Living", command=lambda: self.controller.update_filling(0.8))
        pattern.add_command(label="90% Living", command=lambda: self.controller.update_filling(0.9))
        menubar.add_cascade(label="Start Pattern", menu=pattern)

        color = tk.Menu(menubar, tearoff=0)
        color.add_command(label="Black & White", command= lambda: self.set_color("Black","White"))
        color.add_command(label="Black & Blue", command= lambda: self.set_color("Black","Blue"))
        color.add_command(label="White & Black", command=lambda: self.set_color("White", "Black"))
        color.add_command(label="White & Blue", command=lambda: self.set_color("White", "Blue"))
        menubar.add_cascade(label="Color", menu=color)

        method = tk.Menu(menubar, tearoff=0)
        method.add_command(label="Normal", command= lambda: self.controller.set_mode(1))
        method.add_command(label="Spherical", command= lambda: self.controller.set_mode(0))
        menubar.add_cascade(label="Method", menu=method)

        controls = tk.Menu(menubar, tearoff=0)
        controls.add_command(label="Play / Pause [Space]", command= lambda: self.controller.toggle_pause())
        controls.add_command(label="Reset [Return]", command= lambda: self.controller.reset())
        controls.add_command(label="Step [Enter]", command= lambda: self.controller.do_step())
        menubar.add_cascade(label="Controls", menu=controls)
        self.window.config(menu=menubar)
