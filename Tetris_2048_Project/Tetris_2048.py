################################################################################
#                                                                              #
# The main program of Tetris 2048 Base Code                                    #
#                                                                              #
################################################################################

import lib.stddraw as stddraw  # for creating an animation with user interactions
from lib.picture import Picture  # used for displaying an image on the game menu
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid  # the class for modeling the game grid
from tetromino import Tetromino  # the class for modeling the tetrominoes
import random  # used for creating tetrominoes with random types (shapes)

# The main function where this program starts execution
def start(startup):
   # set the dimensions of the game grid
   grid_h, grid_w= 20, 12
   right_panel_width = 5
   # set the size of the drawing canvas (the displayed window)
   canvas_h, canvas_w = 40 * grid_h, 40 * (grid_w + right_panel_width)
   # only set stddraw window on startup
   if startup:
      stddraw.setCanvasSize(canvas_w, canvas_h)
      # set the scale of the coordinate system for the drawing canvas
      stddraw.setXscale(-0.5, grid_w + right_panel_width - 0.5)
      stddraw.setYscale(-0.5, grid_h - 0.5)

   # set the game grid dimension values stored and used in the Tetromino class
   Tetromino.grid_height = grid_h
   Tetromino.grid_width = grid_w
   # create the game grid
   grid = GameGrid(grid_h, grid_w, right_panel_width)
   # create the first tetromino to enter the game grid
   # by using the create_tetromino function defined below
   current_tetromino = create_tetromino()
   grid.current_tetromino = current_tetromino
   #creates the next tetromino
   next_tetro = create_tetromino()

   # display a simple menu before opening the game
   # by using the display_game_menu function defined below
   display_game_menu(grid_h, grid_w + right_panel_width)

   # display a simple menu for speed selection
   display_speed_menu(grid_h, grid_w + right_panel_width, grid)

   # the main game loop
   while True:
      # check for any user interaction via the keyboard
      if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
         key_typed = stddraw.nextKeyTyped()  # the most recently pressed key
         # if the left arrow key has been pressed
         if key_typed == "left":
            # move the active tetromino left by one
            current_tetromino.move(key_typed, grid)
         # if the right arrow key has been pressed
         elif key_typed == "right":
            # move the active tetromino right by one
            current_tetromino.move(key_typed, grid)
         # if the down arrow key has been pressed
         elif key_typed == "down":
            # move the active tetromino down by one
            # (soft drop: causes the tetromino to fall down faster)
            current_tetromino.move(key_typed, grid)
         elif key_typed == "space": # it rotates the the tetraminos by clockwise
            current_tetromino.rotate_clockwise(grid)   
            # if the right arrow key has been pressed
         elif key_typed == "p": # opens pause menu
            display_pause_menu(grid_h, grid_w)
            # if the right arrow key has been pressed
         elif key_typed == "h":
            # hard drop the active tetromino 
            current_tetromino.move(key_typed, grid,hard_drop=True)
         # clear the queue of the pressed keys for a smoother interaction
         stddraw.clearKeysTyped()

      # move the active tetromino down by one at each iteration (auto fall)
      success = current_tetromino.move("down", grid)
      # lock the active tetromino onto the grid when it cannot go down anymore
      if not success:
         # get the tile matrix of the tetromino without empty rows and columns
         # and the position of the bottom left cell in this matrix
         tiles, pos = current_tetromino.get_min_bounded_tile_matrix(True)
         # update the game grid by locking the tiles of the landed tetromino
         game_over = grid.update_grid(tiles, pos)
         game_win = grid.win
         # end the main game loop if the game is over
         # show victory message if game is won
         if game_over and game_win:
            display_gameover_menu(grid_h, grid_w, "You won the game!", grid.score)
            break
         # show lose mesage if game is lost
         elif game_over and not game_win:
            display_gameover_menu(grid_h, grid_w, "Game over, you lost!", grid.score)
            break

         # updates to the next tetromino, after locking the current tetromino
         current_tetromino = next_tetro
         grid.current_tetromino = current_tetromino

         # creates the 'next' next tetromino
         next_tetro = create_tetromino()

      # display the game grid with the current tetromino
      grid.display(next_tetro)

# A function for creating random shaped tetrominoes to enter the game grid
def create_tetromino():
   # the type (shape) of the tetromino is determined randomly
   tetromino_types = ['I', 'O', 'Z','J', 'L', 'S','T']
   random_index = random.randint(0, len(tetromino_types) - 1)
   random_type = tetromino_types[random_index]
   # create and return the tetromino
   tetromino = Tetromino(random_type)
   return tetromino

# A function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width):
   # the colors used for the menu
   background_color = Color(42, 69, 99)
   button_color = Color(238, 228, 218)
   text_color = Color(31, 160, 239)
   # clear the background drawing canvas to background_color
   stddraw.clear(background_color)
   # get the directory in which this python code file is placed
   current_dir = os.path.dirname(os.path.realpath(__file__))
   # compute the path of the image file
   img_file = current_dir + "/images/menu_image.png"
   # the coordinates to display the image centered horizontally
   img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
   # the image is modeled by using the Picture class
   image_to_display = Picture(img_file)
   # add the image to the drawing canvas
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # the dimensions for the start game button
   button_w, button_h = grid_width - 1.5, 2
   # the coordinates of the bottom left corner for the start game button
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
   # add the start game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   # add the text on the start game button
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   text_to_display = "Click Here to Start the Game"
   stddraw.text(img_center_x, 5, text_to_display)
   # the user interaction loop for the simple menu
   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked on the start game button
      if stddraw.mousePressed():
         # get the coordinates of the most recent location at which the mouse
         # has been left-clicked
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the button
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               break  # break the loop to end the method and start the game

# A function for displaying a simple menu for game speed selection
def display_speed_menu(grid_height, canvas_width, grid):
   # Adjust colors for speed menu screen
   stddraw.clear(Color(187, 182, 165))

   # Showing game title image
   current_dir = os.path.dirname(os.path.realpath(__file__))
   img_file = current_dir + "/images/menu_image.png"
   img_center_x, img_center_y = (canvas_width - 1) / 2, grid_height - 7
   image_to_display = Picture(img_file)
   stddraw.picture(image_to_display, img_center_x, img_center_y)

   # Creating general button dimensions
   button_w, button_h = canvas_width - 1.5, 2
   # Creating general button horizontal position
   button_blc_x = img_center_x - button_w / 2

   # "Slow" button creation with given dimensions, positions, and text
   stddraw.setPenColor(Color(238,228,218))
   stddraw.filledRectangle(button_blc_x, 1, button_w, button_h)
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(Color(160, 109, 130))
   text_to_display = "Slow"
   stddraw.text(img_center_x, 2, text_to_display)

   # "Medium" button creation with given dimensions, positions, and text
   stddraw.setPenColor(Color(238,228,218))
   stddraw.filledRectangle(button_blc_x, 4, button_w, button_h)
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(Color(160, 109, 130))
   text_to_display = "Medium"
   stddraw.text(img_center_x, 5, text_to_display)

   # "Fast" button creation with given dimensions, positions, and text
   stddraw.setPenColor(Color(238,228,218))
   stddraw.filledRectangle(button_blc_x, 7, button_w, button_h)
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(Color(160, 109, 130))
   text_to_display = "Fast"
   stddraw.text(img_center_x, 8, text_to_display)

   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked on a button
      if stddraw.mousePressed():
         # set mouse click positions
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # Check if mouse click is on the Slow button
         if button_blc_x <= mouse_x <= button_blc_x + button_w and 1 <= mouse_y <= 1 + button_h:
            grid.set_speed(275)
            break
         # Check if mouse click is on the Medium button
         elif button_blc_x <= mouse_x <= button_blc_x + button_w and 4 <= mouse_y <= 4 + button_h:
            grid.set_speed(175)
            break
         # Check if mouse click is on the Fast button
         elif button_blc_x <= mouse_x <= button_blc_x + button_w and 7 <= mouse_y <= 7 + button_h:
            grid.set_speed(100)
            break

# A function for displaying a simple pause menu
def display_pause_menu(grid_height, grid_width):
   # the colors used for the menu
   background_color = Color(42, 69, 99)
   button_color = Color(25, 255, 228)
   text_color = Color(31, 160, 239)
   # clear the background drawing canvas to background_color
   stddraw.clear(background_color)
   # the dimensions for the continue game button
   button_w, button_h = grid_width - 1.5, 2
   # the coordinates of the bottom left corner for the continue game button
   button_blc_x, button_blc_y = 5 - button_w / 2, 4
   # add the continue game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x + 3, button_blc_y, button_w, button_h)
   # add the text on the continue game button
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   text_to_display = "Continue"
   stddraw.text(8, 5, text_to_display)
   # add the back to menu game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x + 3, button_blc_y + 3, button_w, button_h)
   # add the text on the back to menu game button
   stddraw.setPenColor(text_color)
   text_to_display = "Back to Main Menu"
   stddraw.text(8, 8, text_to_display)
   # add the pause text
   stddraw.setFontSize(45)
   text_to_display = "Game Paused"
   stddraw.text(8, 15, text_to_display)
   # check if the mouse has been left-clicked on the continue game button
   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked on a button
      if stddraw.mousePressed():
         # get the coordinates of the most recent location at which the mouse
         # has been left-clicked
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the button (Continue)
         if mouse_x >= button_blc_x + 3 and mouse_x <= button_blc_x + button_w + 3:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               break  # break the loop to end the method and start the game
         # check if these coordinates are inside the button (Back to main menu)
         if mouse_x >= button_blc_x + 3 and mouse_x <= button_blc_x + button_w + 3:
            if mouse_y >= button_blc_y + 3 and mouse_y <= button_blc_y + 3 + button_h:
               start(False)

# A method for displaying a simple game over menu with different messages depending on win/lose        
def display_gameover_menu(grid_height, grid_width, message, final_score):
   # the colors used for the menu
   background_color = Color(42, 69, 99)
   button_color = Color(25, 255, 228)
   text_color = Color(31, 160, 239)
   # clear the background drawing canvas to background_color
   stddraw.clear(background_color)
   # the dimensions for the continue game button
   button_w, button_h = grid_width - 1.5, 2
   # the coordinates of the bottom left corner for the continue game button
   button_blc_x, button_blc_y = 5 - button_w / 2, 4
   # add the quit game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x + 3, button_blc_y, button_w, button_h)
   # add the text on the quit game button
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   text_to_display = "Exit Game"
   stddraw.text(8, 5, text_to_display)
   # add the back to menu game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x + 3, button_blc_y + 3, button_w, button_h)
   # add the text on the back to menu game button
   stddraw.setPenColor(text_color)
   text_to_display = "Return to Main Menu"
   stddraw.text(8, 8, text_to_display)
   # add the game over text
   stddraw.setFontSize(50)
   text_to_display = message
   stddraw.text(8, 15, text_to_display)
   # add the final score
   stddraw.setFontSize(35)
   text_to_display = "Score: " + str(final_score)
   stddraw.text(8, 13, text_to_display)
   # check if the mouse has been left-clicked on the continue game button
   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked on a button
      if stddraw.mousePressed():
         # get the coordinates of the most recent location at which the mouse
         # has been left-clicked
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the button
         if mouse_x >= button_blc_x + 3 and mouse_x <= button_blc_x + button_w + 3:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               break  # break the loop to end the method and start the game
         if mouse_x >= button_blc_x + 3 and mouse_x <= button_blc_x + button_w + 3:
            if mouse_y >= button_blc_y + 3 and mouse_y <= button_blc_y + 3 + button_h:
               start(False)

# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__ == '__main__':
   start(True)
