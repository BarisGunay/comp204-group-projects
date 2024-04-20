import lib.stddraw as stddraw  # used for displaying the game grid
from lib.color import Color  # used for coloring the game grid
from point import Point  # used for tile positions
import numpy as np  # fundamental Python module for scientific computing

# A class for modeling the game grid
class GameGrid:
   # A constructor for creating the game grid based on the given arguments
   def __init__(self, grid_h, grid_w):
      # set the dimensions of the game grid as the given arguments
      self.grid_height = grid_h
      self.grid_width = grid_w
      # create a tile matrix to store the tiles locked on the game grid
      self.tile_matrix = np.full((grid_h, grid_w), None)
      # create the tetromino that is currently being moved on the game grid
      self.current_tetromino = None
      # the game_over flag shows whether the game is over or not
      self.game_over = False
      # set the color used for the empty grid cells
      self.empty_cell_color = Color(206, 195, 181)
      # set the colors used for the grid lines and the grid boundaries
      self.line_color = Color(185,171,158)
      self.boundary_color = Color(132, 122, 113)
      # thickness values used for the grid lines and the grid boundaries
      self.line_thickness = 0.002
      self.box_thickness = 10 * self.line_thickness

   # A method for displaying the game grid
   def display(self):
      # clear the background to empty_cell_color
      stddraw.clear(self.empty_cell_color)
      # draw the game grid
      self.draw_grid()
      # draw the current/active tetromino if it is not None
      # (the case when the game grid is updated)
      if self.current_tetromino is not None:
         self.current_tetromino.draw()
      # draw a box around the game grid
      self.draw_boundaries()
      # show the resulting drawing with a pause duration = 250 ms
      stddraw.show(250)

   # A method for drawing the cells and the lines of the game grid
   def draw_grid(self):
      self.find_positions()
      # for each cell of the game grid
      for row in range(self.grid_height):
         for col in range(self.grid_width):
            current_tile = self.tile_matrix[row][col]
            # if the current grid cell is occupied by a tile
            if current_tile is not None:
               # draw this tile
               current_tile.draw(current_tile.position)
      # draw the inner lines of the game grid
      stddraw.setPenColor(self.line_color)
      stddraw.setPenRadius(self.line_thickness)
      # x and y ranges for the game grid
      start_x, end_x = -0.5, self.grid_width - 0.5
      start_y, end_y = -0.5, self.grid_height - 0.5
      for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
         stddraw.line(x, start_y, x, end_y)
      for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
         stddraw.line(start_x, y, end_x, y)
      stddraw.setPenRadius()  # reset the pen radius to its default value

   # A method for drawing the boundaries around the game grid
   def draw_boundaries(self):
      # draw a bounding box around the game grid as a rectangle
      stddraw.setPenColor(self.boundary_color)  # using boundary_color
      # set the pen radius as box_thickness (half of this thickness is visible
      # for the bounding box as its lines lie on the boundaries of the canvas)
      stddraw.setPenRadius(self.box_thickness)
      # the coordinates of the bottom left corner of the game grid
      pos_x, pos_y = -0.5, -0.5
      stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
      stddraw.setPenRadius()  # reset the pen radius to its default value

   # A method used checking whether the grid cell with the given row and column
   # indexes is occupied by a tile or not (i.e., empty)
   def is_occupied(self, row, col):
      # considering the newly entered tetrominoes to the game grid that may
      # have tiles with position.y >= grid_height
      if not self.is_inside(row, col):
         return False  # the cell is not occupied as it is outside the grid
      # the cell is occupied by a tile if it is not None
      return self.tile_matrix[row][col] is not None

   # A method for checking whether the cell with the given row and col indexes
   # is inside the game grid or not
   def is_inside(self, row, col):
      if row < 0 or row >= self.grid_height:
         return False
      if col < 0 or col >= self.grid_width:
         return False
      return True
    # A method for clearing full lines in the game grid
   def clear_full_lines(self):
      rows_to_clear = []  # list to store the row indexes of full rows
      for row in range(self.grid_height):
         # check if all cells in the current row are occupied
         if all(self.tile_matrix[row]):
            rows_to_clear.append(row)  # add the index of the full row to the list
      # remove the full rows from the grid
      for row in rows_to_clear:
         self.tile_matrix = np.delete(self.tile_matrix, row, axis=0)
         # add a new empty row at the top of the grid
         new_row = np.full((1, self.grid_width), None)
         self.tile_matrix = np.concatenate((self.tile_matrix, new_row), axis=0)
   # A method that locks the tiles of a landed tetromino on the grid checking
   # if the game is over due to having any tile above the topmost grid row.
   # (This method returns True when the game is over and False otherwise.)
   def update_grid(self, tiles_to_lock, blc_position):
      # necessary for the display method to stop displaying the tetromino
      self.current_tetromino = None
      # lock the tiles of the current tetromino (tiles_to_lock) on the grid
      n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
      for col in range(n_cols):
         for row in range(n_rows):
            # place each tile (occupied cell) onto the game grid
            if tiles_to_lock[row][col] is not None:
               # compute the position of the tile on the game grid
               pos = Point()
               pos.x = blc_position.x + col
               pos.y = blc_position.y + (n_rows - 1) - row
               if self.is_inside(pos.y, pos.x):
                  self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
               # the game is over if any placed tile is above the game grid
               else:
                  self.game_over = True
      # clear full lines in the game grid
      self.clear_full_lines()
      # return the value of the game_over flag
      return self.game_over

   def find_positions(self):
      # scan the grid
      for col in range(self.grid_width):
         for row in range(self.grid_height):
            if self.tile_matrix[row][col] is not None:
               self.tile_matrix[row][col].position.move(col, row)

   def merge_tiles(self):
      self.find_positions()
      merge_count, new_count = 0, 0
      while(new_count == merge_count):
      # scan the grid
         for col in range(self.grid_width):
            for row in range(1, self.grid_height - 1):
               next_tile = self.tile_matrix[row - 1][col]

               if self.tile_matrix[row][col] is None or next_tile is None:
                  continue
               
               if self.tile_matrix[row][col].number == next_tile.number:
                  self.tile_matrix[row][col].double()
                  self.tile_matrix[row - 1][col] = None
                  self.fall(self.tile_matrix[row][col])
                  merge_count += 1
                  # + Update color needed

               if self.tile_matrix[row][col] in self.current_tetromino.tile_matrix:
                  for tile in self.current_tetromino.tile_matrix:
                     self.fall(tile)
         new_count += 1

   # A method for moving this tetromino in a given direction by 1 on the grid
   def fall(self, tile):
         while self.can_fall(tile):
            tile.position.translate(0, -1)
   
   def can_fall(self, tile):
      # if the tile hit border
      if tile.position.y == 0:
         return False  # this tile cannot be moved down
      # if the grid cell below any bottommost tile is occupied
      if self.is_occupied(tile.position.y - 1, tile.position.x):
         return False  # this tile cannot be moved down
         # as the bottommost tile of the current row is checked
      # if this method does not end by returning False before this line
      return True  # this tile can be moved in the given direction