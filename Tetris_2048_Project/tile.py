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

   color_key = {
         2: Color(238, 228, 218),   # Skin color
         4: Color(236, 224, 199),   # Shade of red
         8: Color(243, 177, 120),   # Shade of red
         16: Color(244, 150, 100),  # Shade of red
         32: Color(249, 123, 98),    # Shade of red
         64: Color(237, 97, 86),
         128: Color(250, 69, 56),
         256: Color(255, 60, 48),
         512: Color(255, 90, 11),
         1024: Color(233, 103, 189),
         2048: Color(233, 149, 112),    # Shade of red
         4096: Color(0, 0, 0)       # Black
      }

   # A constructor that creates a tile with 2 as the number on it
   def __init__(self):
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


      self.change_color()



   def change_color(self):
      if self.number in self.color_key:
         self.background_color = self.color_key[self.number]
      else:
         self.background_color = Color(238,228,218)


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

