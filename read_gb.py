#import threading
import time
import pygame
from threading import Thread

from graphics import PPU_THREAD
from interrupts import handle_interrupts, handle_timer
from memory_control import readMem, writeMem
from opcodes import extra_opcodes, opcodes
from cpu import handle_opcode
from events import handle_events

log = 1
ppu = 1


A, B, C, D, E, H, L = 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
F = [0, 0, 0, 0, 0, 0, 0, 0]
SP = 0x0000
MEMORY = [0]*0x100
IME = False
HALT = 0

MAXCYCLE = 69905


if log:
    disassembled_file = open("disassembled.txt", "w")


def runCode(pointer):
    global A, B, C, D, E, F, H, L, SP, MEMORY, IME, HALT



    #pygame
    pygame.init()
    pygame.display.set_caption("Gameboy Emulator")
    #resizable
    screen = pygame.display.set_mode((160*4, 144*4), pygame.RESIZABLE)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    # keys
    keys={"LEFT": 1, "RIGHT": 1, "UP": 1, "DOWN": 1, "A": 1, "B": 1, "SELECT": 1, "START": 1}

    # get current time
    dt = time.time()
    counter = 0
    cycles = 0
    boot = True
    
    # spawn ppu thread
    stop=False
    ppu_thread = Thread(target=PPU_THREAD, args=(lambda: MEMORY,screen,lambda: stop))
    ppu_thread.start()

    while True:
        keys = handle_events(keys, MEMORY)
        if keys==True:
            stop=True
            ppu_thread.join()
            pygame.quit()
            return True


        if time.time() - dt > 1.0/60.0:
            if MEMORY[0xFF40] & 0x80:
                counter = 0
                MEMORY[0xFF44] = 0x90
                MEMORY[0xFF0F] |= 0x01
                dt = time.time()
            cycles = 0
        else:
            if MEMORY[0xFF40] & 0x80:
                counter += 1
                if counter >= 0x90:
                    MEMORY[0xFF44] += 1
                if MEMORY[0xFF44] >= 153:
                    MEMORY[0xFF44] = 0
            if cycles >= MAXCYCLE:
                continue

        if len(MEMORY) <= pointer:
            print(f"End of file reached, pointer: {pointer}")
            break
        code = readMem(MEMORY, pointer)
        if not HALT:
            ctime=time.time()

            if log:
                disassembled_file.write(f"PC: {pointer:04x}\t{opcodes[code]:<8} {extra_opcodes[readMem(MEMORY,pointer+1)] if opcodes[code]=='PREFCB' else '':<8}\tCode: {code:02x}\tPC+1: {readMem(MEMORY,pointer+1):02x}\tPC+2: {readMem(MEMORY,pointer+2):02x}")
            
            A, B, C, D, E, H, L, F, SP, IME, MEMORY, pointer, cycle, HALT = handle_opcode(code,A,B,C,D,E,H,L,F,SP,IME,MEMORY,pointer,keys)
            
            if log:
                disassembled_file.write(
                    f"\tAF: {A:02x}{int(''.join([str(x) for x in F[::-1]]),2):02x}\tBC: {B:02x}{C:02x}\tDE: {D:02x}{E:02x}\tHL: {H:02x}{L:02x}\tSP: {SP:04x}\tF: {F}\tIME: {IME}\tSP: {SP:04x}\tTime taken: {time.time()-ctime}\n")
        else:
            print("Halting!")
            cycle = 1

        cycles += cycle
        handle_timer(cycle, MEMORY)
        pointer, MEMORY, IME, SP, HALT = handle_interrupts(MEMORY, pointer, IME, SP, HALT)

        # print(f"F: {F}")
        if pointer == 0x100 and boot:
            boot = False
            # copy the interupt table to the beginning of the memory
            MEMORY[0:0x100] = game[0:0x100]


f = open("DMG_ROM.bin", "rb")
content = f.read()
f.close()
# print(content)
MEMORY[0x0:0x100] = content

#f = open("Dr. Mario (World).gb", "rb")
with open("config.txt", "r") as f:
    config=f.read().splitlines()

# NOTE: should probably do this differently
f=open(config[0].split("=")[1], "rb")
game = f.read()
f.close()
MEMORY += game[0x100:0x8000]
if len(MEMORY) < 0x10000:
    MEMORY += [0]*(0x10000-len(MEMORY))
if __name__=="__main__":
    runCode(0x0)
