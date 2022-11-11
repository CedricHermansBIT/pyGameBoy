
def signed(unsigned):
    return unsigned-256 if unsigned > 127 else unsigned

def unsigned(signed):
    return signed+256 if signed < 0 else signed

def splitHex(hex):
    return (hex >> 8), (hex & 0xFF)

def joinHex(high, low):
    return (high << 8) | low

def BIT(n, b, F):
    F[7] = int((n & (1 << b)) == 0)
    F[5:7] = [1, 0]
    return F

def SLA(n, F):
    F[4] = int((n & (1 << 7)) != 0)
    n = (n << 1) & 0xff
    F[7] = int(n == 0)
    F[5:7] = [0, 0]
    return n, F

def SRA(n, F):
    F[4] = int((n & 1) != 0)
    n = (n&(1<<7))|(n >> 1) 
    F[7] = int(n == 0)
    F[5:7] = [0, 0]
    return n, F

def SWAP(n, F):
    n = ((n & 0x0f) << 4) | ((n & 0xf0) >> 4)
    F[7] = int(n == 0)
    F[4:7] = [0, 0, 0]
    return n, F

def SRL(n, F):
    F[4] = int((n & 1) != 0)
    n = (n >> 1) & 0x7f
    F[7] = int(n == 0)
    F[5:7] = [0, 0]
    return n, F

def RES(n, b):
    n &= ~(1 << b)
    return n

def SET(n, b):
    n |= (1 << b)
    return n

def ADDAR8(a, b, F):
    tmp= a + b
    F[7] = int((tmp & 0xFF) == 0)
    F[6] = 0
    F[5] = int((((a&0xF)+(b&0xF))&0x10)==0x10)
    F[4] = int(tmp>0xFF)
    return tmp & 0xFF, F

def ADCAR8(a, b, F):
    tmp = a + b + F[4]
    F[7] = int((tmp & 0xFF) == 0)
    F[6] = 0
    F[5] = int((((a&0xF)+(b&0xF)+F[4])&0x10)==0x10)
    F[4] = int(tmp>0xFF)
    return tmp & 0xFF, F

def SUBAR8(a, b, F):
    tmp = a - b
    F[7] = int((tmp & 0xFF) == 0)
    F[6] = 1
    F[5] = int((((a&0xF)-(b&0xF))&0x10)==0x10)
    F[4] = int(tmp<0)
    return tmp & 0xFF, F

def SBCAR8(a, b, F):
    tmp = a - b - F[4]
    F[7] = int((tmp & 0xFF) == 0)
    F[6] = 1
    F[5] = int((((a&0xF)-(b&0xF)-F[4])&0x10)==0x10)
    F[4] = int(tmp<0)
    return tmp & 0xFF, F

def RLC(n, F):
    F[4] = int((n & (1 << 7)) == (1 << 7))
    n = ((n << 1) & 0xff) | F[4]
    F[7] = int(n == 0)
    F[5:7] = [0, 0]
    return n, F

def RRC(n, F):
    F[4] = int((n & 1) == 1)
    n = (n >> 1) | (F[4] << 7)
    F[7] = int(n == 0)
    F[5:7] = [0, 0]
    return n, F

def RL(n, F):
    tmp = int((n & (1 << 7)) == (1 << 7))
    n = ((n << 1) & 0xff) | F[4]
    F[4] = tmp
    F[7] = int(n == 0)
    F[5:7] = [0, 0]
    return n, F

def RR(n, F):
    tmp = int((n & 1) == 1)
    n = (n >> 1) | (F[4] << 7)
    F[4] = tmp
    F[7] = int(n == 0)
    F[5:7] = [0, 0]
    return n, F