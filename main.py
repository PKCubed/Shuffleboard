import pygame
from time import sleep
import numpy

pygame.init()
clock = pygame.time.Clock()



# Options

screen_width = 600
screen_height = 800
fps = 60

background_color = (92, 78, 55)

board_color = (189, 159, 111)
board_width = 400
board_height = screen_height

stone_color = (128, 128, 128)
stone_width = 50
stone_height = 50
stone_start_x = board_width/2 - stone_width/2
stone_start_y = screen_height - 100
stone_x = stone_start_x
stone_y = stone_start_y
stone_move = False
stone_speed = 4
stone_vel_x = 0
stone_vel_y = 0
stone_stop_vel = 0.01

friction = 0.008 # (Change this variable when sweeping in front of the stone) For curling, not shuffleboard

# These variables control the spin aspect of the puck
stone_spin_speed = 1.2
stone_spin_friction = 0.003
stone_spin_div = 35





screen = pygame.display.set_mode((screen_width,screen_height))


stone_spin_vel = 0 
clicking = False
running = True
while running: # Main game loop
    clock.tick(fps) # Tick the clock for a constant frame rate
    for event in pygame.event.get(): # Iterate through each pygame event
        if event.type == pygame.QUIT: # If the X is pressed
            running = False # Stop the main loop
        elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(num_buttons=3)[0] == True: # If any mouse button is pressed
            clicking = True
            mouse_start_x, mouse_start_y = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            if clicking:
                mouse_end_x, mouse_end_y = pygame.mouse.get_pos()

                spin = mouse_end_x - mouse_start_x # Get the spin value from the users mouse locations
                print(spin)
                spin /= stone_spin_div
                print(spin)


                if stone_move == False: # If the mouse has not already been pressed
                    mouse_x, mouse_y = mouse_start_x, mouse_start_y # Assign the mouse's position to the mouse_x and y variables

                    stone_move = True # Trigger the stone to move

                    stone_center_x = stone_x + stone_width/2 # Define the center of the stone and not the top left corner
                    stone_center_y = stone_y + stone_height/2

                    try: # Catch divide by zero when user clicks on the same y level as the stone
                        slope = (mouse_x - stone_center_x)/(mouse_y - stone_center_y) # Get slope
                    except:
                        stone_move = False # ignore click

                    # Reduce slope to a constant size
                    angle = numpy.arctan(slope) # Get arc-tan of the slope
                    stone_vel_x = numpy.sin(angle) * stone_speed # Get the slope from the angle and multiply it by the speed setting
                    stone_vel_y = numpy.cos(angle) * stone_speed

                    stone_spin_vel = (stone_speed - stone_vel_y) * -spin / 10 * stone_spin_speed # Define the spin velocity based on the spin value. Just make it a more reasonable number.

                    # The stone_speed variable should be controlled by the length of the user's click

            

    
    # Update
    if stone_move: # If the user clicked on the screen and triggered the stone to be moved

        

        print(stone_spin_vel)


        stone_x -= stone_vel_x + stone_spin_vel # Subtract the velocity from the stone's location to move the stone.
        stone_y -= stone_vel_y
        if abs(stone_vel_y) >= stone_stop_vel or abs(stone_vel_x) >= stone_stop_vel: # If the stone's velocity is lower than the stop velocity, stop it from moving forever
            stone_vel_x /= friction + 1
            stone_vel_y /= friction + 1
            stone_spin_vel /= (stone_spin_friction) + 1
        elif abs(stone_spin_vel) >= stone_stop_vel:
            stone_spin_vel /= (friction + 1)
        else:
            stone_vel_x = 0 # Set the velocity to 0 to stop the stone from moving
            stone_vel_y = 0
            stone_move = False # Disable stone movement so we can click again to curl the stone
            sleep(1)
            stone_x = stone_start_x
            stone_y = stone_start_y


    # Draw

    screen.fill(background_color) # Draw Background
    pygame.draw.rect(screen, board_color, (0,0,board_width, board_height)) # Draw board
    pygame.draw.ellipse(screen, stone_color, (stone_x, stone_y, stone_width, stone_height)) # Draw curling stone

    pygame.display.update() # Update the screen with the new frame