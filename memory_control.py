mbcRomNumber = 0

def readMem(Mem, adr, romtype, keys=0):
    global mbcRomNumber
    #special cases:
    # keys
    # keys is dict with keys: UP, DOWN, LEFT, RIGHT, A, B, START, SELECT
    if adr == 0xff00:
        if Mem[0xff00] & 0x20:
            #print(hex((Mem[0xff00] & 0xf0) | (keys['DOWN'] << 3) | (keys['UP'] << 2) | (keys['LEFT'] << 1) | keys['RIGHT'] | 1<<7 | 1<<6))
            return (Mem[0xff00] | (keys['DOWN'] << 3) | (keys['UP'] << 2) | (keys['LEFT'] << 1) | keys['RIGHT'] | 1<<7 | 1<<6)
        elif Mem[0xff00] & 0x10:
            return (Mem[0xff00] & 0xf0) | (keys['START'] << 3) | (keys['SELECT'] << 2) | (keys['B'] << 1) | keys['A'] | 1<<7 | 1<<6
        else:
            return Mem[0xff00]

    #	MBC1
    if (romtype == 1 and mbcRomNumber and (adr >= 0x4000 and adr < 0x8000)):
        adr = (adr - 0x4000) + (mbcRomNumber * 0x4000)
    #	MBC2
    elif romtype == 2:
        if (mbcRomNumber and (adr >= 0x4000 and adr < 0x8000)):
            adr = ((mbcRomNumber-1) * 0x4000) + (adr - 0x4000)
    elif romtype == 3:
        #mbcRomNumber = Mem[0x2000]
        if (mbcRomNumber and (adr >= 0x4000 and adr < 0x8000)):
            adr = (adr - 0x4000) + (mbcRomNumber * 0x4000)
            #print(adr, mbcRomNumber, hex(Mem[adr]))
    return Mem[adr]

mbcRamEnable = False
mbcRomMode = 0

def writeMem(Mem, adr, val, romtype):
    global mbcRamEnable
    global mbcRomNumber
    global mbcRomMode
    #special cases:
    # sound control
    if adr == 0xff26:
        if val:
            Mem[adr] = 0xff
        else:
            Mem[adr] = 0
        return
    # joypad
    if adr == 0xff00:
        Mem[adr] = 0xf0 & val
        return
    # OAM DMA
    if adr == 0xff46:
        for i in range(0xa0):
            Mem[0xfe00 + i] = Mem[(val << 8) + i]
        #print(f"OAM DMA: {[hex(Mem[0xfe00+i]) for i in range(0xa0)]}")
        return



    #	MBC1
    if romtype == 0:
        if adr >= 0x8000:
            Mem[adr] = val
    elif romtype == 1:
        if adr < 0x2000:
            mbcRamEnable = int(val==0x0a)
        elif adr < 0x4000:
            mbcRomNumber = mbcRomNumber | (val & 0x1f)
            if mbcRomNumber == 0 or mbcRomNumber == 0x20 or mbcRomNumber == 0x40 or mbcRomNumber == 0x60:
                mbcRomNumber += 1
        elif adr < 0x6000:
            if mbcRomMode == 0:
                mbcRomNumber |= ((val & 0x3) << 5)
            else:
                mbcRamNumber = val & 0x3
        elif adr < 0x8000:
            mbcRomMode = val > 0
        else:
            Mem[adr] = val
    #	MBC2
    elif romtype == 2:
        if adr < 0x2000:
            mbcRamEnable = val>0
        elif adr < 0x4000:
            mbcRomNumber = val & 0x1f
            if mbcRomNumber == 0 or mbcRomNumber == 0x20 or mbcRomNumber == 0x40 or mbcRomNumber == 0x60:
                mbcRomNumber += 1
        else:
            Mem[adr] = val
    elif romtype == 3:
        if adr < 0x2000:
            mbcRamEnable = val>0
        elif adr < 0x4000:
            mbcRomNumber = val & 0x1f
            if mbcRomNumber==0:
                mbcRomNumber+=1
        elif adr < 0x6000:
            if val < 0x8:
                mbcRamNumber = val & 0x3
            else:
                # TODO: RTC
                return
        elif adr < 0x8000:
            mbcRomMode = val > 0
        else:
            Mem[adr] = val
