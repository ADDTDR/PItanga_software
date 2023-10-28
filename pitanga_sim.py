import time
import pygame
import numpy as np 
from ht16k33 import Pitanga

from bluetooth_bitmap import bluetooth_bitmap
# from pikachu import pikachu as pikachu_bitmap

COLOR_GRID = (40, 40, 40)
COLOR_ACTIVE = (106, 215, 90)
COLOR_PASSIVE = (4, 12, 5)
CELL_PX_SIZE = 15

def main():
    pitanga = Pitanga()
    running = False
    pygame.init()
    height_px = 7 
    width_px = 30
    screen = pygame.display.set_mode((width_px * CELL_PX_SIZE, height_px * CELL_PX_SIZE))
    screen.fill(COLOR_GRID)
    bitmap = bluetooth_bitmap
    
    cells = np.zeros((7, 30))
    pattern = np.array([
                        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,1],
                        [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0],
                        [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,1],
                        [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1],
                        [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0] 
                        ]
                        )
    pos = (0, 0)
    #Fill the pattern to cell date 
    # cells[pos[0]:pos[0]+pattern.shape[0], pos[1]:pos[1]+pattern.shape[1]] = pattern

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
            bitmap = bitmap[1:] + bitmap[:1]  
            bitmap_slice = bitmap[:7]  
            cells[pos[0]:pos[0]+7, pos[1]:pos[1]+30] = bitmap_slice

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