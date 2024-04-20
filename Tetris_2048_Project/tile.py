import random
import lib.stddraw as stddraw  # used for drawing the tiles to display them
from lib.color import Color  # used for coloring the tiles

# A class for modeling numbered tiles as in 2048
class Tile:
   # Class variables shared among all Tile objects
   # ---------------------------------------------------------------------------
   # the value of the boundary thickness (for the boxes around the tiles)
   boundary_thickness = 0.004
   # font family and font size used for displaying the tile number
   font_family, font_size = "Arial", 14

   # A constructor that creates a tile with 2 as the number on it
   def __init__(self):
      self.is_merge_victim = False # if merge victim, tile shall fall until touching another or border
      self.is_merge_doer = False # if merge doer, tile shall delete tile below, then keep falling until touching another or border
      self.pos_y = 0
      self.pos_x = 0
      # set the number on this tile
      self.number = random.choice([2, 4]) #choose randomly between 2 and 4
      # set the colors of this tile
      self.background_color = Color(238,228,218)  # background (tile) color
      self.foreground_color = Color(159,149,138)  # foreground (number) color
      self.box_color = Color(143,134,125)  # box (boundary) color
      if self.number == 4:
         self.background_color = Color(236,224,200) 
          # darken the box color if the number is 4
      elif self.number == 2: 
         self.background_color = Color(238,228,218)   
         # light color of the box color if the number is 2 
   # A method for drawing this tile at a given position with a given length

   def draw(self, position, length=1):  # length defaults to 1
      # draw the tile as a filled square
      stddraw.setPenColor(self.background_color)
      stddraw.filledSquare(position.x, position.y, length / 2)
      # draw the bounding box around the tile as a square
      stddraw.setPenColor(self.box_color)
      stddraw.setPenRadius(Tile.boundary_thickness)
      stddraw.square(position.x, position.y, length / 2)
      stddraw.setPenRadius()  # reset the pen radius to its default value
      # draw the number on the tile
      stddraw.setPenColor(self.foreground_color)
      stddraw.setFontFamily(Tile.font_family)
      stddraw.setFontSize(Tile.font_size)
      stddraw.text(position.x, position.y, str(self.number))

   # A method for moving this tetromino in a given direction by 1 on the grid
   def fall(self, game_grid):
         while self.can_fall(game_grid):
            self.pos_y -= 1

   def can_fall(self, game_grid):
      # if the tile hit border
      if self.y == 0:
         return False  # this tile cannot be moved down
      # if the grid cell below any bottommost tile is occupied
      if game_grid.is_occupied(self.pos_y - 1, self.pos_x):
         return False  # this tile cannot be moved down
         # as the bottommost tile of the current row is checked
      # if this method does not end by returning False before this line
      return True  # this tile can be moved in the given direction