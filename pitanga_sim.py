import time
import random 
import pygame
import numpy as np 
from datetime import datetime
from ht16k33 import Pitanga, JOKES_FILE
from font5x7 import Font5x7_full as Font5x7

from bluetooth_bitmap import bluetooth_bitmap
# from pikachu import pikachu as pikachu_bitmap

COLOR_GRID = (40, 40, 40)
COLOR_ACTIVE = (106, 215, 90)
COLOR_PASSIVE = (4, 12, 5)
CELL_PX_SIZE = 15

def main():
    
    with open(JOKES_FILE, 'r') as file:
        # Read all the lines into a list
        lines = file.readlines()

    display_string = random.choice(lines)
    display_string = display_string.replace('\n', '')

    pitanga = Pitanga()
    running = False
    pygame.init()
    height_px = 7 
    width_px = 30
    screen = pygame.display.set_mode((width_px * CELL_PX_SIZE, height_px * CELL_PX_SIZE))
    screen.fill(COLOR_GRID)

    cells = np.zeros((7, 30))
    pos = (0, 0)


    # Update plot 
    for row, col in np.ndindex(cells.shape):
        color = COLOR_ACTIVE if cells[row, col] == 1 else COLOR_PASSIVE
        pygame.draw.rect(screen, color, (col * CELL_PX_SIZE, row * CELL_PX_SIZE, CELL_PX_SIZE - 1, CELL_PX_SIZE - 1))


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Wipe out pitanga display 
                bit_map_list = np.zeros((7, 30)).astype(int).tolist()
                pitanga.display_bitmap(bit_map_list)
                # Pygame quit 
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running

            # Mouse right button click 
            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                cells[mouse_pos[1] // CELL_PX_SIZE, mouse_pos[0] // CELL_PX_SIZE] = 1 


            # Mouse left button click 
            if pygame.mouse.get_pressed()[2]:
                mouse_pos = pygame.mouse.get_pos()
                cells[mouse_pos[1] // CELL_PX_SIZE, mouse_pos[0] // CELL_PX_SIZE] = 0


        if running is True:
            # bitmap = bitmap[1:] + bitmap[:1]  
            # bitmap_slice = bitmap[:7]  
            # cells[pos[0]:pos[0]+7, pos[1]:pos[1]+30] = bitmap_slice
            display_string = display_string[1:] + display_string[:1]
            # pitanga.display_print(Font5x7, display_string[:6], show_decimals=False)
            current_time = datetime.now().strftime("%H%M%SS")
            raw_data = pitanga.display_print(Font5x7, display_string[:6], show_decimals=False, decimal_dots=0xf00, update_leds=False)
            cells[pos[0]:pos[0]+7, pos[1]:pos[1]+30] = np.hstack((raw_data[5], raw_data[4], raw_data[3], raw_data[2], raw_data[1], raw_data[0]))
            time.sleep(0.1)


        # Fill the data 
        for row, col in np.ndindex(cells.shape):
            color = COLOR_ACTIVE if cells[row, col] == 1 else COLOR_PASSIVE
            pygame.draw.rect(screen, color, (col * CELL_PX_SIZE, row * CELL_PX_SIZE, CELL_PX_SIZE - 1, CELL_PX_SIZE - 1))    

        # Update pitanga
        bit_map_list = cells.astype(int).tolist()
        pitanga.display_bitmap(bit_map_list)

        pygame.display.update()
        time.sleep(0.01)

        
if __name__ == '__main__':
    main()