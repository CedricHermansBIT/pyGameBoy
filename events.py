import pygame
from memory_control import readMem, writeMem
def handle_events(keys, MEMORY):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return keys,True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                keys["RIGHT"] = 0
            elif event.key == pygame.K_LEFT:
                keys["LEFT"] = 0
            elif event.key == pygame.K_UP:
                keys["UP"] = 0
            elif event.key == pygame.K_DOWN:
                keys["DOWN"] = 0
            elif event.key == pygame.K_a:
                keys["A"] = 0
            elif event.key == pygame.K_s:
                keys["B"] = 0
            elif event.key == pygame.K_RETURN:
                keys["START"] = 0
            elif event.key == pygame.K_BACKSPACE:
                keys["SELECT"] = 0
            # set interupt
            writeMem(MEMORY, 0xFF0F, readMem(MEMORY, 0xFF0F) | 0x10)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                keys["RIGHT"] = 1
            elif event.key == pygame.K_LEFT:
                keys["LEFT"] = 1
            elif event.key == pygame.K_UP:
                keys["UP"] = 1
            elif event.key == pygame.K_DOWN:
                keys["DOWN"] = 1
            elif event.key == pygame.K_a:
                keys["A"] = 1
            elif event.key == pygame.K_s:
                keys["B"] = 1
            elif event.key == pygame.K_RETURN:
                keys["START"] = 1
            elif event.key == pygame.K_BACKSPACE:
                keys["SELECT"] = 1
    return keys,False