import random
import copy
import time

class Model:
    def __init__(self):
        self.controller = None

    def fill_grid(self, width, height, perc_alive):
        """Initially fills Grid with certain percentage of alive cells"""
        tot_size = width * height
        alive = int(tot_size * perc_alive)
        board = [True] * alive + (tot_size - alive) * [False]
        random.shuffle(board)
        board = [board[i:i + width] for i in range(0, tot_size, height)]

        for row in range(height):
            for column in range(width):
                self.controller.change_color(row, column, board[row][column])

        return board

    def set_controller(self, controller):
        """Defines the controller object from outside"""
        self.controller = controller

    def toggle_onclick(self, event, fullstop, paused, width, height, scale, table):
        """Toggles the State of a cell after click event"""
        if (not fullstop) and paused:
            x = int(event.x / scale)
            y = int(event.y / scale)
            if x >= 0 and x < width and y >= 0 and y < height:
                table[x][y] = not table[x][y]
                if table[x][y]:
                    self.controller.change_color(x, y, 1)
                else:
                    self.controller.change_color(x, y, 0)
        return table

    def calc_next_gen(self, grid, mode):
        """Returns a Grid of alive cell after applying Conway's rules"""
        #before = time.time()
        rows = len(grid)
        columns = len(grid[0])
        next_gen = copy.deepcopy(grid)

        for row in range(rows):
            for column in range(columns):

                # Count Alive Neighbours
                alive_neighbours = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):

                        # Dont count itself
                        if not (i == 0 and j == 0):
                            # Apply Normal Rules with fix grid borders
                            if mode == 1:
                                if (row + i) in range(0, rows) and (column + j) in range(0, columns):
                                    alive_neighbours += grid[row+i][column+j]
                            # Apply Spherical rules
                            else:
                                alive_neighbours += grid[((row + i) % rows)][((column + j) % columns)]

                if grid[row][column] == False and alive_neighbours == 3:
                    next_gen[row][column] = True
                    self.controller.change_color(row, column, 1)
                if grid[row][column] == True and (alive_neighbours < 2 or alive_neighbours > 3):
                    next_gen[row][column] = False
                    self.controller.change_color(row, column, 0)
        self.controller.apply_changes()
        #print(time.time()-before)
        return next_gen