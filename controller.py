import threading
import time

# Initial Parameters
initial_width = 75
initial_height = 75
initial_scale = 5
initial_delay = 0.000000001
initial_mode = 0
initial_filling = 0.3

class Controller:
    def __init__(self, view, model):
        self.model = model
        self.view = view

        # Sizing Params
        self.width = initial_width
        self.height = initial_height
        self.scale = initial_scale
        self.delay = initial_delay
        self.mode = initial_mode
        self.filling = initial_filling
        self.generation = 0
        self.living = 0

        # Play Params
        self.fullstop = False
        self.paused = True

        # Game Board
        self.table = None

        # Initialize
        self.view.init_window(self, self.width, self.height, self.scale)
        self.model.set_controller(self)
        self.view.update_title(self.paused, self.mode, self.width, self.height)
        self.table = self.model.fill_grid(self.width, self.height, self.filling)

    def start(self):
        """Starts the Main Loop in a new thread"""
        thread = threading.Thread(target=self.clock)
        thread.start()

    def clock(self):
        """The Main Loop. Initializes a new step each run"""
        while True:
            if (not self.paused) and (not self.fullstop):
                self.table = self.model.calc_next_gen(self.table, self.mode)
            time.sleep(self.delay)

    def reset(self):
        """Resets the board and initially fills it with certain amount of living cells"""
        if not self.fullstop:
            self.fullstop = True
            self.view.reset(self.width, self.height)
            self.table = self.model.fill_grid(self.width, self.height, self.filling)
            self.fullstop = False
            if not self.paused:
                self.toggle_pause()
            self.view.update_title(self.paused, self.mode, self.width, self.height)

    def apply_changes(self):
        """Triggers window update"""
        self.view.window.update()

    def refresh_board(self):
        """Resets the whole window to apply new board size"""
        rows = len(self.table)
        columns = len(self.table[0])
        for row in range(rows):
            for column in range(columns):
                self.change_color(row, column, self.table[row][column])

    # Control Actions -------------------------------------------------------
    def toggle_pause(self):
        """Toggles pause state and updates title"""
        if not self.fullstop:
            self.paused = not self.paused
            self.view.update_title(self.paused, self.mode, self.width, self.height)

    def do_step(self):
        """Do a single run"""
        self.paused = True
        self.table = self.model.calc_next_gen(self.table, self.mode)

    def update_filling(self, filling):
        """Updates amount of living cells in start state"""
        self.filling = filling
        self.reset()

    def change_grid_size(self, width, height):
        """Changes grid size and inits board reset"""
        self.height = height
        self.width = width
        self.view.init_window(self, self.width, self.height, self.scale)
        self.reset()

    def toggle_onclick(self,event):
        """toggles cell state after click event"""
        self.table = self.model.toggle_onclick(event, self.fullstop, self.paused,
                                               self.width, self.height, self.scale, self.table)

    # Mode 1 = Normal, Mode 0 = Spherical
    def set_mode(self, mode):
        """Resets Game mode"""
        self.mode = mode
        self.view.update_title(self.paused, self.mode, self.width, self.height)

    def change_color(self, x, y, state):
        """Triggers view to change color of a tile"""
        self.view.change_color(x, y, state)