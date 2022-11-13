from memory_control import *


def handle_interrupts(MEMORY: list, PC: int, IME: int, SP: int, HALT: int) -> tuple:
    if IME:
        #print(f"IER: {hex(MEMORY[0xffff])} IF: {hex(MEMORY[0xff0f])}")
        #0xFFFF is the interrupt enable register and 0xFF0F is the interrupt flag register
        if readMem(MEMORY, 0xFFFF) & readMem(MEMORY, 0xFF0F):
            if readMem(MEMORY, 0xFFFF) & 0x01 and readMem(MEMORY, 0xFF0F) & 0x01:
                #print("VBLANK")
                IME = False
                writeMem(MEMORY, 0xFF0F, readMem(MEMORY, 0xFF0F) & 0xFE)
                # print(MEMORY[0xFF0F])
                SP-=1
                writeMem(MEMORY, SP, (PC>>8) & 0xFF)
                SP-=1
                writeMem(MEMORY, SP, PC & 0xFF)
                #print(hex(MEMORY[SP]),hex(MEMORY[SP+1]))
                HALT=False
                return 0x0040, MEMORY, IME, SP, HALT
            elif readMem(MEMORY, 0xFFFF) & 0x02 and readMem(MEMORY, 0xFF0F) & 0x02:
                #print("LCD STAT")
                IME = False
                writeMem(MEMORY, 0xFF0F, readMem(MEMORY, 0xFF0F) & 0xFD)
                SP-=1
                writeMem(MEMORY, SP, (PC>>8) & 0xFF)
                SP-=1
                writeMem(MEMORY, SP, PC & 0xFF)
                HALT=False
                return 0x0048 , MEMORY, IME, SP, HALT
            elif readMem(MEMORY, 0xFFFF) & 0x04 and readMem(MEMORY, 0xFF0F) & 0x04:
                #print("TIMER")
                IME = False
                writeMem(MEMORY, 0xFF0F, readMem(MEMORY, 0xFF0F) & 0xFB)
                SP-=1
                writeMem(MEMORY, SP, (PC>>8) & 0xFF)
                SP-=1
                writeMem(MEMORY, SP, PC & 0xFF)
                HALT=False
                return 0x0050, MEMORY, IME, SP, HALT
            elif readMem(MEMORY, 0xFFFF) & 0x08 and readMem(MEMORY, 0xFF0F) & 0x08:
                #print("SERIAL")
                IME = False
                writeMem(MEMORY, 0xFF0F, readMem(MEMORY, 0xFF0F) & 0xF7)
                SP-=1
                writeMem(MEMORY, SP, (PC>>8) & 0xFF)
                SP-=1
                writeMem(MEMORY, SP, PC & 0xFF)
                HALT=False
                return 0x0058, MEMORY, IME, SP, HALT
            elif readMem(MEMORY, 0xFFFF) & 0x10 and readMem(MEMORY, 0xFF0F) & 0x10:
                print("JOYPAD")
                IME = False
                writeMem(MEMORY, 0xFF0F, readMem(MEMORY, 0xFF0F) & 0xEF)
                SP-=1
                writeMem(MEMORY, SP, (PC>>8) & 0xFF)
                SP-=1
                writeMem(MEMORY, SP, PC & 0xFF)
                HALT=False
                return 0x0060, MEMORY, IME, SP, HALT
    return PC, MEMORY, IME, SP, HALT

CLOCKSUM = 0
TIMER_CLOCKSUM = 0

def handle_timer(cycle, MEMORY):
    global CLOCKSUM
    global TIMER_CLOCKSUM
    CLOCKSUM+=cycle
    if CLOCKSUM>=256:
        CLOCKSUM-=256
        MEMORY[0xff04] += 1 & 0xff
    if MEMORY[0xff07] & 0x04:
        TIMER_CLOCKSUM+=cycle*4
        freq=4096
        if MEMORY[0xff07] & 0x03 == 0x01:
            freq=262144
        elif MEMORY[0xff07] & 0x03 == 0x02:
            freq=65536
        elif MEMORY[0xff07] & 0x03 == 0x03:
            freq=16384
        while TIMER_CLOCKSUM>=(4194304/freq):
            MEMORY[0xff05] = (MEMORY[0xff05]+1)
            if MEMORY[0xff05] > 0xff:
                MEMORY[0xff05] = MEMORY[0xff06]
                MEMORY[0xff0f] |= 0x04
            TIMER_CLOCKSUM-=(4194304/freq)
    
