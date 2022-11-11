from utils import signed
import pygame

# BW color palette
COLORS = {0: (255, 255, 255), 1: (192, 192, 192), 2: (96, 96, 96), 3: (0, 0, 0)}
# Greenish color palette
COLORS = {0: (255, 255, 255), 1: (0, 255, 0), 2: (0, 128, 0), 3: (0, 0, 0)}


def draw_sprite(screen: pygame.Surface, tile, x, y, flags, CURRENT_PALETTE, MEMORY):
    if y!=-16 and x!=-8 and y<144 and x<160:
        for r in range(0, 8):
            for c in range(0, 8):
                # the pixels are rendered per row
                # In memory it looks like this
                # tile1-row1 tile1-row1 tile1-row2 tile1-row2 tile1-row3 tile1-row3 tile1-row4 tile1-row4 tile1-row5 tile1-row5 tile1-row6 tile1-row6 tile1-row7 tile1-row7 tile1-row8 tile1-row8 tile2-row1 tile2-row1 tile2-row2 tile2-row2 tile2-row3 tile2-row3 tile2-row4 tile2-row4 tile2-row5 tile2-row5 tile2-row6 tile2-row6 tile2-row7 tile2-row7 tile2-row8 tile2-row8 ...
                # Render just the tileset
                offset = tile*16 + r % 8*2
                b1 = MEMORY[0x8000+offset]
                b2 = MEMORY[0x8000+offset+1]
                # b1= 0b12345678 b2=0b12345678, if i=0 then 0b11, if i=1 then 0b22, if i=2 then 0b33, if i=3 then 0b44, if i=4 then 0b55, if i=5 then 0b66, if i=6 then 0b77, if i=7 then 0b88
                b1sel = ((b1 >> (7-c)) & 1) << 1
                b2sel = (b2 >> (7-c)) & 1
                color = b1sel | b2sel
                if color != 0:
                    if flags & 0x20:
                        c = 7-c
                    if flags & 0x40:
                        r = 7-r
                    pygame.draw.rect(screen, COLORS[CURRENT_PALETTE[color]], (screen.get_width()/160*(x+c), screen.get_height()/144*(y+r), screen.get_width()/160 + 1, screen.get_height()/144 + 1))


def RENDER_VRAM(MEMORY, screen: pygame.Surface):
    settings = MEMORY[0xFF40]
    # TILEMAP = 0x9C00 if settings & 0x08 else 0x9800
    TILESET = 0x8000 if settings & 0x10 else 0x8800
    # current palette is mapping 0xff47 to PALLETTE
    colorsettings = MEMORY[0xFF47]

    CURRENT_PALETTE = {3: colorsettings >> 6 & 3, 2: colorsettings >>
                        4 & 3, 1: colorsettings >> 2 & 3, 0: colorsettings & 3}
    # 144 rows and 160 columns, however it is in 8x8 tiles
    for r in range(0, 144):
        for c in range(0, 130//8):
            # the pixels are rendered per row
            # In memory it looks like this
            # tile1-row1 tile1-row1 tile1-row2 tile1-row2 tile1-row3 tile1-row3 tile1-row4 tile1-row4 tile1-row5 tile1-row5 tile1-row6 tile1-row6 tile1-row7 tile1-row7 tile1-row8 tile1-row8 tile2-row1 tile2-row1 tile2-row2 tile2-row2 tile2-row3 tile2-row3 tile2-row4 tile2-row4 tile2-row5 tile2-row5 tile2-row6 tile2-row6 tile2-row7 tile2-row7 tile2-row8 tile2-row8 ...
            # Render just the tileset
            tile = r//8*130//8+c
            offset = tile*16 + r % 8*2
            for i in range(0, 8):
                b1 = MEMORY[TILESET+offset]
                b2 = MEMORY[TILESET+offset+1]
                # b1= 0b12345678 b2=0b12345678, if i=0 then 0b11, if i=1 then 0b22, if i=2 then 0b33, if i=3 then 0b44, if i=4 then 0b55, if i=5 then 0b66, if i=6 then 0b77, if i=7 then 0b88
                b1sel = ((b1 >> (7-i)) & 1) << 1
                b2sel = (b2 >> (7-i)) & 1
                color = b1sel | b2sel
                pygame.draw.rect(screen, COLORS[CURRENT_PALETTE[color]], (screen.get_width()/130*(c*8+i), screen.get_height()/144*r, screen.get_width()/130+1, screen.get_height()/144+1))
    pygame.display.flip()


def PPU(MEMORY, screen: pygame.Surface):
    #global PCOL
    settings = MEMORY[0xFF40]
    yOffset = MEMORY[0xFF42]
    xOffset = MEMORY[0xFF43]
    if settings & 0x80:
        TILEMAP = 0x9C00 if (settings >> 3) &1 else 0x9800
        TILESET = 0x8000 if (settings >> 4) &1 else 0x8800
        colorsettings = MEMORY[0xFF47]
        # print("Draw")
        CURRENT_PALETTE = {3: colorsettings >> 6 & 3, 2: colorsettings >>
                            2 & 3, 1: colorsettings >> 4 & 3, 0: colorsettings >> 0 & 3}
        MEMORY[0xFF44] = 0
        # 144 rows and 160 columns, however it is in 8x8 tiles

        #Background
        for r in range(0, 144):
            for c in range(0, 160):
                # the pixels are rendered per row
                # In memory it looks like this
                # tile1-row1 tile1-row1 tile1-row2 tile1-row2 tile1-row3 tile1-row3 tile1-row4 tile1-row4 tile1-row5 tile1-row5 tile1-row6 tile1-row6 tile1-row7 tile1-row7 tile1-row8 tile1-row8 tile2-row1 tile2-row1 tile2-row2 tile2-row2 tile2-row3 tile2-row3 tile2-row4 tile2-row4 tile2-row5 tile2-row5 tile2-row6 tile2-row6 tile2-row7 tile2-row7 tile2-row8 tile2-row8 ...
                # Render just the tileset
                dx=(c+xOffset)&0xff
                dy=(r+yOffset)&0xff
                tile = MEMORY[TILEMAP+(dy)//8*32+(dx)//8]
                if TILESET == 0x8800:
                    offset = (signed(tile)+128)*16 + (dy) % 8*2
                else:
                    offset = tile*16 + (dy) % 8*2
                # for i in range(0, 8):
                b1 = MEMORY[TILESET+offset]
                b2 = MEMORY[TILESET+offset+1]
                # b1= 0b12345678 b2=0b12345678, if i=0 then 0b11, if i=1 then 0b22, if i=2 then 0b33, if i=3 then 0b44, if i=4 then 0b55, if i=5 then 0b66, if i=6 then 0b77, if i=7 then 0b88
                b1sel = ((b1 >> (7-dx % 8)) & 1) << 1
                b2sel = (b2 >> (7-dx % 8)) & 1
                color = b1sel | b2sel
                pygame.draw.rect(screen, COLORS[CURRENT_PALETTE[color]], (screen.get_width()/160*c, screen.get_height()/144*r, screen.get_width()/160 + 1, screen.get_height()/144 + 1))


        #Window
        if settings & 0x20:
            TILEMAP=0x9C00 if (settings>>6)&1 else 0x9800
            TILESET=0x8000 if (settings>>4)&1 else 0x8800
            wx=MEMORY[0xFF4B]-7
            wy=MEMORY[0xFF4A]
            if wx>0 and wx<166 and wy>0 and wy<143:
                for r in range(0,144-wy):
                    for c in range(0,160-wx):
                        dx=(c+xOffset)&0xff
                        dy=(r+yOffset)&0xff
                        tile=MEMORY[TILEMAP+(dy)//8*32+(dx)//8]
                        if TILESET==0x8800:
                            offset=(signed(tile)+128)*16+(dy)%8*2
                        else:
                            offset=tile*16+(dy)%8*2
                        #for i in range(0,8):
                        b1=MEMORY[TILESET+offset]
                        b2=MEMORY[TILESET+offset+1]
                        #b1= 0b12345678 b2=0b12345678, if i=0 then 0b11, if i=1 then 0b22, if i=2 then 0b33, if i=3 then 0b44, if i=4 then 0b55, if i=5 then 0b66, if i=6 then 0b77, if i=7 then 0b88
                        b1sel=((b1>>(7-dx%8))&1)<<1
                        b2sel=(b2>>(7-dx%8))&1
                        color=b1sel|b2sel
                        pygame.draw.rect(screen,COLORS[CURRENT_PALETTE[color]],(screen.get_width()/160*(c+wx),screen.get_height()/144*(r+wy),screen.get_width()/160+1,screen.get_height()/144+1))


        #Sprites
        mode=MEMORY[0xFF40]>>2&1
        for i in range(0, 40):
            offset = 0xFE00 + i*4
            y = MEMORY[offset] - 16
            x = MEMORY[offset + 1] - 8
            flags = MEMORY[offset + 3]
            tile = MEMORY[offset + 2]
            if mode == 0:
                draw_sprite(screen, tile, x, y, flags, CURRENT_PALETTE, MEMORY)
            else:
                draw_sprite(screen, tile&0xFE, x, y, flags, CURRENT_PALETTE, MEMORY)
                draw_sprite(screen, tile|1, x, y+8, flags, CURRENT_PALETTE, MEMORY)
            
        pygame.display.flip()

import time
def PPU_THREAD(MEMORY,screen: pygame.Surface,stop):
    ptime=time.time()
    while not stop():
        if time.time()-ptime>1/60:
            ptime=time.time()
            #global PCOLORS
            settings = MEMORY()[0xFF40]
            yOffset = MEMORY()[0xFF42]
            xOffset = MEMORY()[0xFF43]
            if settings & 0x80:
                TILEMAP = 0x9C00 if (settings >> 3) &1 else 0x9800
                TILESET = 0x8000 if (settings >> 4) &1 else 0x8800
                colorsettings = MEMORY()[0xFF47]
                # print("Draw")
                CURRENT_PALETTE = {3: colorsettings >> 6 & 3, 2: colorsettings >>
                                    2 & 3, 1: colorsettings >> 4 & 3, 0: colorsettings >> 0 & 3}
                MEMORY()[0xFF44] = 0
                # 144 rows and 160 columns, however it is in 8x8 tiles

                #Background
                for r in range(0, 144):
                    for c in range(0, 160):
                        # the pixels are rendered per row
                        # In MEMORY() it looks like this
                        # tile1-row1 tile1-row1 tile1-row2 tile1-row2 tile1-row3 tile1-row3 tile1-row4 tile1-row4 tile1-row5 tile1-row5 tile1-row6 tile1-row6 tile1-row7 tile1-row7 tile1-row8 tile1-row8 tile2-row1 tile2-row1 tile2-row2 tile2-row2 tile2-row3 tile2-row3 tile2-row4 tile2-row4 tile2-row5 tile2-row5 tile2-row6 tile2-row6 tile2-row7 tile2-row7 tile2-row8 tile2-row8 ...
                        # Render just the tileset
                        dx=(c+xOffset)&0xff
                        dy=(r+yOffset)&0xff
                        tile = MEMORY()[TILEMAP+(dy)//8*32+(dx)//8]
                        if TILESET == 0x8800:
                            offset = (signed(tile)+128)*16 + (dy) % 8*2
                        else:
                            offset = tile*16 + (dy) % 8*2
                        # for i in range(0, 8):
                        b1 = MEMORY()[TILESET+offset]
                        b2 = MEMORY()[TILESET+offset+1]
                        # b1= 0b12345678 b2=0b12345678, if i=0 then 0b11, if i=1 then 0b22, if i=2 then 0b33, if i=3 then 0b44, if i=4 then 0b55, if i=5 then 0b66, if i=6 then 0b77, if i=7 then 0b88
                        b1sel = ((b1 >> (7-dx % 8)) & 1) << 1
                        b2sel = (b2 >> (7-dx % 8)) & 1
                        color = b1sel | b2sel
                        pygame.draw.rect(screen, COLORS[CURRENT_PALETTE[color]], (screen.get_width()/160*c, screen.get_height()/144*r, screen.get_width()/160 + 1, screen.get_height()/144 + 1))


                #Window
                if settings & 0x20:
                    TILEMAP=0x9C00 if (settings>>6)&1 else 0x9800
                    TILESET=0x8000 if (settings>>4)&1 else 0x8800
                    wx=MEMORY()[0xFF4B]-7
                    wy=MEMORY()[0xFF4A]
                    if wx>0 and wx<166 and wy>0 and wy<143:
                        for r in range(0,144-wy):
                            for c in range(0,160-wx):
                                dx=(c+xOffset)&0xff
                                dy=(r+yOffset)&0xff
                                tile=MEMORY()[TILEMAP+(dy)//8*32+(dx)//8]
                                if TILESET==0x8800:
                                    offset=(signed(tile)+128)*16+(dy)%8*2
                                else:
                                    offset=tile*16+(dy)%8*2
                                #for i in range(0,8):
                                b1=MEMORY()[TILESET+offset]
                                b2=MEMORY()[TILESET+offset+1]
                                #b1= 0b12345678 b2=0b12345678, if i=0 then 0b11, if i=1 then 0b22, if i=2 then 0b33, if i=3 then 0b44, if i=4 then 0b55, if i=5 then 0b66, if i=6 then 0b77, if i=7 then 0b88
                                b1sel=((b1>>(7-dx%8))&1)<<1
                                b2sel=(b2>>(7-dx%8))&1
                                color=b1sel|b2sel
                                pygame.draw.rect(screen,COLORS[CURRENT_PALETTE[color]],(screen.get_width()/160*(c+wx),screen.get_height()/144*(r+wy),screen.get_width()/160+1,screen.get_height()/144+1))


                #Sprites
                mode=MEMORY()[0xFF40]>>2&1
                for i in range(0, 40):
                    offset = 0xFE00 + i*4
                    y = MEMORY()[offset] - 16
                    x = MEMORY()[offset + 1] - 8
                    flags = MEMORY()[offset + 3]
                    tile = MEMORY()[offset + 2]
                    if mode == 0:
                        draw_sprite(screen, tile, x, y, flags, CURRENT_PALETTE, MEMORY())
                    else:
                        draw_sprite(screen, tile&0xFE, x, y, flags, CURRENT_PALETTE, MEMORY())
                        draw_sprite(screen, tile|1, x, y+8, flags, CURRENT_PALETTE, MEMORY())
                    
                pygame.display.flip()