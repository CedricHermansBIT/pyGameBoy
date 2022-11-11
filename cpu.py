from opcodes import *
from utils import *
from memory_control import *




def handle_opcode(code,A,B,C,D,E,H,L,F,SP,IME,MEMORY,pointer,bank_controller,keys):
    prefix = False
    match opcodes[code]:
        case "NOP":
            # print("NOP")
            pointer += 1
            cycle = 1
        case "LDBCA16":
            # print("LDBCA16")
            B = readMem(MEMORY, pointer+2, bank_controller)
            C = readMem(MEMORY, pointer+1, bank_controller)
            pointer += 3
            cycle = 3
        case "LDHBCA":
            # print("LDHBCA")
            writeMem(MEMORY, joinHex(B, C), A, bank_controller)
            pointer += 1
            cycle = 2
        case "INCBC":
            # print("INCBC")
            B,C = splitHex((joinHex(B,C) + 1) & 0xffff)
            pointer += 1
            cycle = 2
        case "INCB":
            # print("INCB")
            # F[5] if overflow of BIT 3
            F[5] = 0 if (B & 0x7) + 1 <= 0x7 else 1
            B = (B + 1) & 0xFF
            F[7] = int(B == 0)
            F[6] = 0
            pointer += 1
            cycle = 1
        case "DECB":
            # print("DECB")
            F[5] = int((B & 0x7) - 1 < 0)
            B = (B - 1) & 0xFF
            # print(B)
            F[7] = int(B == 0)
            F[6] = 1
            pointer += 1
            cycle = 1
        case "LDB":
            # print("LDB")
            B = readMem(MEMORY, pointer+1, bank_controller)
            pointer += 2
            cycle = 2
        case "RLCA":
            # Rotate left through carry
            # print("RLCA")
            A,F=RLC(A,F)
            F[7] = 0
            pointer += 1
            cycle = 1
        case "LDA16SP":
            # print("LDA16SP")
            a16=joinHex(readMem(MEMORY, pointer+2, bank_controller), readMem(MEMORY, pointer+1, bank_controller))
            writeMem(MEMORY, a16, SP & 0xFF, bank_controller)
            writeMem(MEMORY, a16+1, SP>>8 , bank_controller)
            pointer += 3
            cycle = 5
        case "ADDHLBC":
            # print("ADDHLBC")
            F[5] = 1 if (joinHex(H,L) & 0x7FF) + \
                (joinHex(B, C) & 0x7FF) > 0x7FF else 0
            F[4] = int(joinHex(H,L) + joinHex(B, C) > 0xFFFF)
            h, l = splitHex(joinHex(H,L) + joinHex(B, C))
            F[6] = 0
            H = h & 0xFF
            L = l & 0xFF
            pointer += 1
            cycle = 2
        case "LDABC":
            # print("LDABC")
            A = readMem(MEMORY, joinHex(B, C), bank_controller)
            pointer += 1
            cycle = 2
        case "DECBC":
            # print("DECBC")
            B, C = splitHex((joinHex(B, C) - 1) & 0xFFFF)
            pointer += 1
            cycle = 2
        case "INCC":
            # Increment register C
            # print("INCC")
            F[5] = 0 if (C & 0x7) + 1 <= 0x7 else 1
            C = (C + 1) & 0xFF
            F[7] = int(C == 0)
            F[6] = 0
            pointer += 1
            cycle = 1
        case "DECC":
            # print("DECC")
            F[5] = int((C & 0x7) - 1 < 0)
            C = (C - 1) & 0xFF
            F[7] = int(C == 0)
            F[6] = 1
            pointer += 1
            cycle = 1
        case "LDC":
            # print("LDC")
            C = readMem(MEMORY, pointer+1, bank_controller)
            pointer += 2
            cycle = 2
        case "RRCA":
            # Rotate right through carry
            # print("RRCA")
            A,F=RRC(A,F)
            F[7] = 0
            pointer += 1
            cycle = 1
        case "STOP0":
            # print("STOP0")
            pointer += 2
            cycle = 0
        case "LDDED16":
            # print("LDDED16")
            D = readMem(MEMORY, pointer+2, bank_controller)
            E = readMem(MEMORY, pointer+1, bank_controller)
            pointer += 3
            cycle = 3
        case "LDHDEA":
            # print("LDHDEA")
            writeMem(MEMORY, joinHex(D,E), A, bank_controller)
            pointer += 1
            cycle = 2
        case "INCDE":
            # print("INCDE")
            D, E = splitHex((joinHex(D,E) + 1 ) & 0xFFFF)
            pointer += 1
            cycle = 3
        case "INCD":
            # print("INCD")
            F[5] = 0 if (D & 0x7) + 1 <= 0x7 else 1
            D = (D + 1) & 0xFF
            F[7] = int(D == 0)
            F[6] = 0
            pointer += 1
            cycle = 1
        case "DECD":
            # print("DECD")
            F[5] = int((D & 0x7) - 1 < 0)
            D = (D - 1) & 0xFF
            F[7] = int(D == 0)
            F[6] = 1
            pointer += 1
            cycle = 1
        case "LDD":
            # print("LDD")
            D = readMem(MEMORY, pointer+1, bank_controller)
            pointer += 2
            cycle = 2
        case "RLA":
            # print("RLA")
            tmp = F[4]
            F[4] = (A & 0x80) >> 7
            A = (A << 1) & 0xFF
            A = A | tmp
            F[7] = 0
            F[5:7] = [0, 0]
            # disassembled_file.write(
            #    f"carry: {hex(F[4])}, prev carry: {tmp}, A: {A}\n")
            pointer += 1
            cycle = 1
        case "JR":
            # print("JR")
            pointer += signed(readMem(MEMORY,
                                pointer+1, bank_controller)) + 2
            cycle = 3
        case "ADDHLDE":
            # print("ADDHLDE")
            F[5] = 1 if (joinHex(H,L) & 0x7FF) + \
                (joinHex(D,E) & 0x7FF) > 0x7FF else 0
            F[4] = int(joinHex(H,L) + joinHex(D,E) > 0xFFFF)
            h, l = splitHex(joinHex(H,L) + joinHex(D,E))
            F[6] = 0
            # prevent overflow
            H = h & 0xFF
            L = l & 0xFF
            pointer += 1
            cycle = 2
        case "LDADE":
            # print("LDADE")
            A = readMem(MEMORY, joinHex(D,E), bank_controller)
            # input()
            pointer += 1
            cycle = 2
        case "DECDE":
            # print("DECDE")
            D, E = splitHex((joinHex(D,E) - 1) & 0xFFFF)
            pointer += 1
            cycle = 2
        case "INCE":
            # print("INCE")
            F[5] = 0 if (E & 0x7) + 1 <= 0x7 else 1
            E = (E + 1) & 0xFF
            F[7] = int(E == 0)
            F[6] = 0
            pointer += 1
            cycle = 1
        case "DECE":
            # print("DECE")
            F[5] = int((E & 0x7) - 1 < 0)
            E = (E - 1) & 0xFF
            F[7] = int(E == 0)
            F[6] = 1
            pointer += 1
            cycle = 1
        case "LDE":
            # print("LDE")
            E = readMem(MEMORY, pointer+1, bank_controller)
            pointer += 2
            cycle = 2
        case "RRA":
            # print("RRA")
            tmp = F[4]
            F[4] = A & 0x01
            A = (A >> 1) & 0xFF
            A = A | (tmp << 7)
            F[7] = 0
            F[5:7] = [0, 0]
            pointer += 1
            cycle = 1
        case "JRNZ":
            # print("JRNZ")
            pointer,cycle = (pointer+signed(readMem(MEMORY,pointer+1,bank_controller))+2,3) if F[7]==0 else (pointer+2,2)
        case "LDHL16":
            # print("LDHL16")
            H = readMem(MEMORY, pointer+2, bank_controller)
            L = readMem(MEMORY, pointer+1, bank_controller)
            pointer += 3
            cycle = 3
        case "LDHL+A":
            # print("LDHL+A")
            writeMem(MEMORY, joinHex(H,L), A, bank_controller)
            H, L = splitHex(joinHex(H,L) + 1)
            pointer += 1
            cycle = 2
        case "INCHL":
            # print("INCHL")
            H, L = splitHex((joinHex(H,L) + 1) & 0xFFFF)
            pointer += 1
            cycle = 3
        case "INCH":
            # print("INCH")
            F[5] = 0 if (H & 0x7) + 1 <= 0x7 else 1
            H = (H + 1) & 0xFF
            F[7] = int(H == 0)
            F[6] = 0
            pointer += 1
            cycle = 1
        case "DECH":
            # print("DECH")
            F[5] = int((H & 0x7) - 1 < 0)
            H = (H - 1) & 0xFF
            F[7] = int(H == 0)
            F[6] = 1
            pointer += 1
            cycle = 1
        case "LDHA8":
            # print("LDHA8")
            H = readMem(MEMORY, pointer+1, bank_controller)
            pointer += 2
            cycle = 2
        case "DAA":
            # print("DAA")
            # print(pointer)
            # // note: assumes a is a uint8_t and wraps from 0xff to 0
            # if (!n_flag) {  // after an addition, adjust if (half-)carry occurred or if result is out of bounds
            # if (c_flag || a > 0x99) { a += 0x60; c_flag = 1; }
            # if (h_flag || (a & 0x0f) > 0x09) { a += 0x6; }
            # } else {  // after a subtraction, only adjust if (half-)carry occurred
            # if (c_flag) { a -= 0x60; }
            # if (h_flag) { a -= 0x6; }
            # }
            # // these flags are always updated
            # z_flag = (a == 0); // the usual z flag
            # h_flag = 0; // h flag is always cleared
            if F[6] == 0:
                if F[4] or A > 0x99:
                    A = (A + 0x60) & 0xFF
                    F[4] = 1
                if F[5] or (A & 0x0F) > 0x09:
                    A = (A + 0x6) & 0xFF
            else:
                if F[4]:
                    A = (A - 0x60) & 0xFF
                if F[5]:
                    A = (A - 0x6) & 0xFF
            F[5] = 0
            F[7] = int(A == 0)
            pointer += 1
            cycle = 1

            # if A&0x0F >9 and (A&0xF0)>>4 >9:
            #     A = (A + 0x66) & 0xFF
            #     F[4] = 1
            # else:
            #     if A&0x0F > 9:
            #         A = (A + 0x6)
            #     if ((A&0xF0)>>4) > 9:
            #         A = (A + 0x60) & 0xFF
            #         F[4] = 1
            # F[7] = int(A==0)
            # F[5] = 0
            # pointer += 1
            # cycle=1
        case "JRZ":
            # print("JRZ")
            if F[7] == 1:
                pointer += signed(readMem(MEMORY,
                                    pointer+1, bank_controller)) + 2
                cycle = 3
                # print(hex(pointer))
                # pointer += MEMORY[pointer+1] + 1
            else:
                pointer += 2
                cycle = 2
        case "ADDHLHL":
            # print("ADDHLHL")
            F[5] = 1 if (joinHex(H,L) & 0x7FF) + \
                (joinHex(H,L) & 0x7FF) > 0x7FF else 0
            F[4] = int(joinHex(H,L) + joinHex(H,L) > 0xFFFF)
            H, L = splitHex(joinHex(H,L) + joinHex(H,L))
            F[6] = 0
            H = H & 0xFF
            L = L & 0xFF
            pointer += 1
            cycle = 2
        case "LDAHL+":
            # print("LDAHL+")
            # print(joinHex(H,L))
            A = readMem(MEMORY, joinHex(H,L), bank_controller)
            H, L = splitHex(joinHex(H,L) + 1)
            pointer += 1
            cycle = 2
        case "DECHL":
            # print("DECHL")
            H, L = splitHex((joinHex(H,L) - 1) & 0xFFFF)
            pointer += 1
            cycle = 3
        case "INCL":
            # print("INCL")
            F[5] = 0 if (L & 0x7) + 1 <= 0x7 else 1
            L = (L + 1) & 0xFF
            F[7] = int(L == 0)
            F[6] = 0
            pointer += 1
            cycle = 1
        case "DECL":
            # print("DECL")
            F[5] = int((L & 0x7) - 1 < 0)
            L = (L - 1) & 0xFF
            F[7] = int(L == 0)
            F[6] = 1

            pointer += 1
            cycle = 1
        case "LDL":
            # print("LDL")
            L = readMem(MEMORY, pointer+1, bank_controller)
            pointer += 2
            cycle = 2
        case "CPLM":
            # print("CPL")
            A = A ^ 0xFF
            F[6] = 1
            F[5] = 1

            pointer += 1
            cycle = 1
        case "JRNCR8":
            # print("JRNCR8")
            if F[4] == 0:
                pointer += signed(readMem(MEMORY,
                                    pointer+1, bank_controller)) + 2
                cycle = 3
            else:
                pointer += 2
                cycle = 2
        case "LDSP16":
            # print("LDSP16")
            SP = readMem(
                MEMORY, pointer+2, bank_controller) << 8 | readMem(MEMORY, pointer+1, bank_controller)
            pointer += 3
            cycle = 3
        case "LDHL-A":
            # print("LDHL-A")
            writeMem(MEMORY, joinHex(H,L), A, bank_controller)
            H, L = splitHex(joinHex(H,L) - 1)
            pointer += 1
            cycle = 2
        case "INCSP":
            # print("INCSP")
            SP = (SP + 1) & 0xFFFF
            pointer += 1
            cycle = 2
        case "INCHHL":
            # print("INCHL")
            F[5] = 0 if (
                readMem(MEMORY, joinHex(H,L), bank_controller) & 0x7) + 1 <= 0x7 else 1
            writeMem(MEMORY, joinHex(H,L), (readMem(MEMORY, joinHex(H,L),
                        bank_controller) + 1) & 0xFF, bank_controller)
            F[7] = int(readMem(MEMORY, joinHex(H,L), bank_controller) == 0)
            F[6] = 0
            pointer += 1
            cycle = 3
        case "DECHHL":
            # print("DECHL")
            writeMem(MEMORY, joinHex(H,L), (readMem(MEMORY, joinHex(H,L),
                        bank_controller) - 1) & 0xFF, bank_controller)
            F[5] = int((readMem(MEMORY, joinHex(H,L), bank_controller)&0xf)==0xf)
            F[7] = int(readMem(MEMORY, joinHex(H,L), bank_controller) == 0)
            F[6] = 1
            pointer += 1
            cycle = 3
        case "LDHLA8":
            # print("LDHLA8")
            writeMem(MEMORY, joinHex(H,L), readMem(
                MEMORY, pointer+1, bank_controller), bank_controller)
            pointer += 2
            cycle = 3
        case "SCF":
            # print("SCF")
            F[4] = 1
            F[5] = 0
            F[6] = 0
            pointer += 1
            cycle = 1
        case "JRCR8":
            # print("JRCR8")
            if F[4] == 1:
                pointer += signed(readMem(MEMORY,
                                    pointer+1, bank_controller)) + 2
                cycle = 3
            else:
                pointer += 2
                cycle = 2
        case "ADDHLSP":
            # print("ADDHLSP")
            F[5] = 1 if (joinHex(H,L) & 0x7FF) + \
                (SP & 0x7FF) > 0x7FF else 0
            H, L = splitHex(joinHex(H,L) + SP)
            F[4] = int(joinHex(H,L) + SP > 0xFFFF)
            F[6] = 0
            pointer += 1
            cycle = 2
        case "LDAHL-":
            # print("LDAHL-")
            A = readMem(MEMORY, joinHex(H,L), bank_controller)
            hl = joinHex(H,L)
            hl -= 1
            H = (hl >> 8) & 0xFF
            L = hl & 0xFF
            pointer += 1
            cycle = 2
        case "DECSP":
            # print("DECSP")
            SP = (SP - 1) & 0xFFFF
            pointer += 1
            cycle = 2
        case "INCA":
            # Increment register A
            # print("INCA")
            F[5] = 0 if (A & 0x7) + 1 <= 0x7 else 1
            A = (A + 1) & 0xFF
            F[7] = int(A == 0)
            F[6] = 0
            pointer += 1
            cycle = 1
        case "DECA":
            # print("DECA")
            F[5] = int((A & 0x7) - 1 < 0)
            A = (A - 1) & 0xFF
            F[7] = int(A == 0)
            F[6] = 1
            pointer += 1
            cycle = 1
        case "LDA":
            # print("LDA")
            A = readMem(MEMORY, pointer+1, bank_controller)
            pointer += 2
            cycle = 2
        case "CCF":
            # print("CCF")
            F[4] = int(F[4] == 0)
            F[5] = 0
            F[6] = 0
            pointer += 1
            cycle = 1
        case "LDBB":
            # print("LDBB")
            B = B
            pointer += 1
            cycle = 1
        case "LDBC":
            # print("LDBC")
            B = C
            pointer += 1
            cycle = 1
        case "LDBD":
            # print("LDBD")
            B = D
            pointer += 1
            cycle = 1
        case "LDBE":
            # print("LDBE")
            B = E
            pointer += 1
            cycle = 1
        case "LDBH":
            # print("LDBH")
            B = H
            pointer += 1
            cycle = 1
        case "LDBL":
            # print("LDBL")
            B = L
            pointer += 1
            cycle = 1
        case "LDBHL":
            # print("LDBHL")
            B = readMem(MEMORY, joinHex(H,L), bank_controller)
            pointer += 1
            cycle = 2
        case "LDBA":
            # print("LDBA")
            B = A
            pointer += 1
            cycle = 1
        case "LDCB":
            # print("LDCB")
            C = B
            pointer += 1
            cycle = 1
        case "LDCC":
            # print("LDCC")
            C = C
            pointer += 1
            cycle = 1
        case "LDCD":
            # print("LDCD")
            C = D
            pointer += 1
            cycle = 1
        case "LDCE":
            # print("LDCE")
            C = E
            pointer += 1
            cycle = 1
        case "LDCH":
            # print("LDCH")
            C = H
            pointer += 1
            cycle = 1
        case "LDCL":
            # print("LDCL")
            C = L
            pointer += 1
            cycle = 1
        case "LDCHL":
            # print("LDCHL")
            C = readMem(MEMORY, joinHex(H,L), bank_controller)
            pointer += 1
            cycle = 2
        case "LDCA":
            # print("LDCA")
            C = A
            pointer += 1
            cycle = 1
        case "LDDB":
            # print("LDDB")
            D = B
            pointer += 1
            cycle = 1
        case "LDDC":
            # print("LDDC")
            D = C
            pointer += 1
            cycle = 1
        case "LDDD":
            # print("LDDD")
            D = D
            pointer += 1
            cycle = 1
        case "LDDE":
            # print("LDDE")
            D = E
            pointer += 1
            cycle = 1
        case "LDDH":
            # print("LDDH")
            D = H
            pointer += 1
            cycle = 1
        case "LDDL":
            # print("LDDL")
            D = L
            pointer += 1
            cycle = 1
        case "LDDHL":
            # print("LDDHL")
            D = readMem(MEMORY, joinHex(H,L), bank_controller)
            pointer += 1
            cycle = 2
        case "LDDA":
            D = A
            pointer += 1
            cycle = 1
        case "LDEB":
            # print("LDEB")
            E = B
            pointer += 1
            cycle = 1
        case "LDEC":
            # print("LDEC")
            E = C
            pointer += 1
            cycle = 1
        case "LDED":
            # print("LDED")
            E = D
            pointer += 1
            cycle = 1
        case "LDEE":
            # print("LDEE")
            E = E
            pointer += 1
            cycle = 1
        case "LDEH":
            # print("LDEH")
            E = H
            pointer += 1
            cycle = 1
        case "LDEL":
            # print("LDEL")
            E = L
            pointer += 1
            cycle = 1
        case "LDEHL":
            # print("LDEHL")
            E = readMem(MEMORY, joinHex(H,L), bank_controller)
            pointer += 1
            cycle = 2
        case "LDEA":
            # print("LDEA")
            E = A
            pointer += 1
            cycle = 1
        case "LDHB":
            # print("LDHB")
            H = B
            pointer += 1
            cycle = 1
        case "LDHC":
            # print("LDHC")
            H = C
            pointer += 1
            cycle = 1
        case "LDHD":
            # print("LDHD")
            H = D
            pointer += 1
            cycle = 1
        case "LDHE":
            # print("LDHE")
            H = E
            pointer += 1
            cycle = 1
        case "LDHH":
            # print("LDHH")
            H = H
            pointer += 1
            cycle = 1
        case "LDHL":
            # print("LDHL")
            H = L
            pointer += 1
            cycle = 1
        case "LDHHL":
            # print("LDHHL")
            H = readMem(MEMORY, joinHex(H,L), bank_controller)
            pointer += 1
            cycle = 2
        case "LDHA":
            # print("LDHA")
            H = A
            # print(H)
            pointer += 1
            cycle = 1
        case "LDLB":
            # print("LDLB")
            L = B
            pointer += 1
            cycle = 1
        case "LDLC":
            # print("LDLC")
            L = C
            pointer += 1
            cycle = 1
        case "LDLD":
            # print("LDLD")
            L = D
            pointer += 1
            cycle = 1
        case "LDLE":
            # print("LDLE")
            L = E
            pointer += 1
            cycle = 1
        case "LDLH":
            # print("LDLH")
            L = H
            pointer += 1
            cycle = 1
        case "LDLL":
            # print("LDLL")
            L = L
            pointer += 1
            cycle = 1
        case "LDLHL":
            # print("LDLHL")
            L = readMem(MEMORY, joinHex(H,L), bank_controller)
            pointer += 1
            cycle = 2
        case "LDLA":
            # load register A into L
            # print("LDLA")
            L = A
            pointer += 1
            cycle = 1
        case "LDHLB":
            # print("LDHLB")
            writeMem(MEMORY, joinHex(H,L), B, bank_controller)
            pointer += 1
            cycle = 2
        case "LDHLC":
            # print("LDHLC")
            writeMem(MEMORY, joinHex(H,L), C, bank_controller)
            pointer += 1
            cycle = 2
        case "LDHLD":
            # print("LDHLD")
            writeMem(MEMORY, joinHex(H,L), D, bank_controller)
            pointer += 1
            cycle = 2
        case "LDHLE":
            # print("LDHLE")
            writeMem(MEMORY, joinHex(H,L), E, bank_controller)
            pointer += 1
            cycle = 2
        case "LDHLH":
            # print("LDHLH")
            writeMem(MEMORY, joinHex(H,L), H, bank_controller)
            pointer += 1
            cycle = 2
        case "LDHLL":
            # print("LDHLL")
            writeMem(MEMORY, joinHex(H,L), L, bank_controller)
            pointer += 1
            cycle = 2
        case "HALT":
            # print("HALT")
            if IME:
                HALT = True
                pointer += 1
            else:
                if MEMORY[0xFFFF] or MEMORY[0xFF0F]:
                    pointer += 1

            cycle = 1
        case "LDHLA":
            # Store value in A into memory address HL
            # print("LDHLA")
            writeMem(MEMORY, joinHex(H,L), A, bank_controller)
            pointer += 1
            cycle = 2
        case "LDAB":
            # print("LDAB")
            A = B
            pointer += 1
            cycle = 1
        case "LDAC":
            # print("LDAC")
            A = C
            pointer += 1
            cycle = 1
        case "LDAD":
            # print("LDAD")
            A = D
            pointer += 1
            cycle = 1
        case "LDAE":
            # print("LDAE")
            A = E
            pointer += 1
            cycle = 1
        case "LDAH":
            # print("LDAH")
            A = H
            pointer += 1
            cycle = 1
        case "LDAL":
            # print("LDAL")
            A = L
            pointer += 1
            cycle = 1
        case "LDAHL":
            # Load value into A from memory address HL
            # print("LDAHL")
            A = readMem(MEMORY, joinHex(H,L), bank_controller)
            pointer += 1
            cycle = 2
        case "LDAA":
            # print("LDAA")
            A = A
            pointer += 1
            cycle = 1
        case "ADDAB":
            # print("ADDAB")
            A,F=ADDAR8(A,B,F)
            pointer += 1
            cycle = 1
        case "ADDAC":
            # print("ADDAC")
            A,F=ADDAR8(A,C,F)
            pointer += 1
            cycle = 1
        case "ADDAD":
            # print("ADDAD")
            A,F=ADDAR8(A,D,F)
            pointer += 1
            cycle = 1
        case "ADDAE":
            # print("ADDAE")
            A,F=ADDAR8(A,E,F)
            pointer += 1
            cycle = 1
        case "ADDAH":
            # print("ADDAH")
            A,F=ADDAR8(A,H,F)
            pointer += 1
            cycle = 1
        case "ADDAL":
            # print("ADDAL")
            A,F=ADDAR8(A,L,F)
            pointer += 1
            cycle = 1
        case "ADDAHL":
            # print("ADDAHL")
            A,F=ADDAR8(A,readMem(MEMORY, joinHex(H,L), bank_controller),F)
            pointer += 1
            cycle = 2
        case "ADDAA":
            # print("ADDAA")
            A,F=ADDAR8(A,A,F)
            pointer += 1
            cycle = 1
        case "ADCAB":
            # print("ADCAB")
            A,F=ADCAR8(A,B,F)
            pointer += 1
            cycle = 1
        case "ADCAC":
            # print("ADCAC")
            A,F=ADCAR8(A,C,F)
            pointer += 1
            cycle = 1
        case "ADCAD":
            # print("ADCAD")
            A,F=ADCAR8(A,D,F)
            pointer += 1
            cycle = 1
        case "ADCAE":
            # print("ADCAE")
            A,F=ADCAR8(A,E,F)
            pointer += 1
            cycle = 1
        case "ADCAH":
            # print("ADCAH")
            A,F=ADCAR8(A,H,F)
            pointer += 1
            cycle = 1
        case "ADCAL":
            # print("ADCAL")
            A,F=ADCAR8(A,L,F)
            pointer += 1
            cycle = 1
        case "ADCAHL":
            # print("ADCAHL")
            A,F=ADCAR8(A,readMem(MEMORY, joinHex(H,L), bank_controller),F)
            pointer += 1
            cycle = 2
        case "ADCAA":
            # print("ADCAA")
            A,F=ADCAR8(A,A,F)
            pointer += 1
            cycle = 1
        case "SUBB":
            # print("SUBB")
            A,F=SUBAR8(A,B,F)
            pointer += 1
            cycle = 1
        case "SUBC":
            # print("SUBC")
            A,F=SUBAR8(A,C,F)
            pointer += 1
            cycle = 1
        case "SUBD":
            # print("SUBD")
            A,F=SUBAR8(A,D,F)
            pointer += 1
            cycle = 1
        case "SUBE":
            # print("SUBE")
            A,F=SUBAR8(A,E,F)
            pointer += 1
            cycle = 1
        case "SUBH":
            # print("SUBH")
            A,F=SUBAR8(A,H,F)
            pointer += 1
            cycle = 1
        case "SUBL":
            # print("SUBL")
            A,F=SUBAR8(A,L,F)
            pointer += 1
            cycle = 1
        case "SUBHL":
            # print("SUBHL")
            A,F=SUBAR8(A,readMem(MEMORY, joinHex(H,L), bank_controller),F)
            pointer += 1
            cycle = 2
        case "SUBA":
            # print("SUBA")
            A,F=SUBAR8(A,A,F)
            pointer += 1
            cycle = 1
        case "SBCAB":
            # print("SBCAB")
            A,F=SBCAR8(A,B,F)
            pointer += 1
            cycle = 1
        case "SBCAC":
            # print("SBCAC")
            A,F=SBCAR8(A,C,F)
            pointer += 1
            cycle = 1
        case "SBCAD":
            # print("SBCAD")
            A,F=SBCAR8(A,D,F)
            pointer += 1
            cycle = 1
        case "SBCAE":
            # print("SBCAE")
            A,F=SBCAR8(A,E,F)
            pointer += 1
            cycle = 1
        case "SBCAH":
            # print("SBCAH")
            A,F=SBCAR8(A,H,F)
            pointer += 1
            cycle = 1
        case "SBCAL":
            # print("SBCAL")
            A,F=SBCAR8(A,L,F)
            pointer += 1
            cycle = 1
        case "SBCAHL":
            # print("SBCAHL")
            A,F=SBCAR8(A,readMem(MEMORY, joinHex(H,L), bank_controller),F)
            pointer += 1
            cycle = 2
        case "SBCAA":
            # print("SBCAA")
            A,F=SBCAR8(A,A,F)
            pointer += 1
            cycle = 1
        case "ANDB":
            # print("ANDB")
            A = (A & B) & 0xFF
            F[7] = int(A == 0)
            F[4:7] = [0, 1, 0]
            pointer += 1
            cycle = 1
        case "ANDC":
            # print("ANDC")
            A = A & C
            F[7] = int(A == 0)
            F[4:7] = [0, 1, 0]
            pointer += 1
            cycle = 1
        case "ANDD":
            # print("ANDD")
            A = A & D
            F[7] = int(A == 0)
            F[4:7] = [0, 1, 0]
            pointer += 1
            cycle = 1
        case "ANDE":
            # print("ANDE")
            A = A & E
            F[7] = int(A == 0)
            F[4:7] = [0, 1, 0]
            pointer += 1
            cycle = 1
        case "ANDH":
            # print("ANDH")
            A = A & H
            F[7] = int(A == 0)
            F[4:7] = [0, 1, 0]
            pointer += 1
            cycle = 1
        case "ANDL":
            # print("ANDL")
            A = A & L
            F[7] = int(A == 0)
            F[4:7] = [0, 1, 0]
            pointer += 1
            cycle = 1
        case "ANDHL":
            # print("ANDHL")
            A = A & readMem(MEMORY, joinHex(H,L), bank_controller)
            F[7] = int(A == 0)
            F[4:7] = [0, 1, 0]
            pointer += 1
            cycle = 2
        case "ANDA":
            # print("ANDA")
            A = A & A
            F[7] = int(A == 0)
            F[4:7] = [0, 1, 0]
            pointer += 1
            cycle = 1
        case "XORB":
            # print("XORB")
            A = A ^ B
            F[7] = int(A == 0)
            F[4:7] = [0, 0, 0]
            pointer += 1
            cycle = 1
        case "XORC":
            # print("XORC")
            A = A ^ C
            F[7] = int(A == 0)
            F[4:7] = [0, 0, 0]
            pointer += 1
            cycle = 1
        case "XORD":
            # print("XORD")
            A = A ^ D
            F[7] = int(A == 0)
            F[4:7] = [0, 0, 0]
            pointer += 1
            cycle = 1
        case "XORE":
            # print("XORE")
            A = A ^ E
            F[7] = int(A == 0)
            F[4:7] = [0, 0, 0]
            pointer += 1
            cycle = 1
        case "XORH":
            # print("XORH")
            A = A ^ H
            F[7] = int(A == 0)
            F[4:7] = [0, 0, 0]
            pointer += 1
            cycle = 1
        case "XORL":
            # print("XORL")
            A = A ^ L
            F[7] = int(A == 0)
            F[4:7] = [0, 0, 0]
            pointer += 1
            cycle = 1
        case "XORHL":
            # print("XORHL")
            A = A ^ readMem(MEMORY, joinHex(H,L), bank_controller)
            F[7] = int(A == 0)
            F[4:7] = [0, 0, 0]
            pointer += 1
            cycle = 2
        case "XORA":
            # print("XORA")
            A = A ^ A
            F[7] = int(A == 0)
            F[4:7] = [0, 0, 0]
            pointer += 1
            cycle = 1
        case "ORB":
            # print("ORB")
            A = A | B
            F[7] = int(A == 0)
            F[4:7] = [0, 0, 0]
            pointer += 1
            cycle = 1
        case "ORC":
            # print("ORC")
            A = A | C
            F[7] = int(A == 0)
            F[4:7] = [0, 0, 0]
            pointer += 1
            cycle = 1
        case "ORD":
            # print("ORD")
            A = A | D
            F[7] = int(A == 0)
            F[4:7] = [0, 0, 0]
            pointer += 1
            cycle = 1
        case "ORE":
            # print("ORE")
            A = A | E
            F[7] = int(A == 0)
            F[4:7] = [0, 0, 0]
            pointer += 1
            cycle = 1
        case "ORH":
            # print("ORH")
            A = A | H
            F[7] = int(A == 0)
            F[4:7] = [0, 0, 0]
            pointer += 1
            cycle = 1
        case "ORL":
            # print("ORL")
            A = A | L
            F[7] = int(A == 0)
            F[4:7] = [0, 0, 0]
            pointer += 1
            cycle = 1
        case "ORHL":
            # print("ORHL")
            A = A | readMem(MEMORY, joinHex(H,L), bank_controller)
            F[7] = int(A == 0)
            F[4:7] = [0, 0, 0]
            pointer += 1
            cycle = 2
        case "ORA":
            # print("ORA")
            A = A | A
            F[7] = int(A == 0)
            F[4:7] = [0, 0, 0]
            pointer += 1
            cycle = 1
        case "CPB":
            # print("CPB")
            F[7] = int(A == B)
            F[6] = 1
            F[5] = int((A & 0xF) < (B & 0xF))
            F[4] = int(A < B)
            pointer += 1
            cycle = 1
        case "CPC":
            # print("CPC")
            F[7] = int(A == C)
            F[6] = 1
            F[5] = int((A & 0xF) < (C & 0xF))
            F[4] = int(A < C)
            pointer += 1
            cycle = 1
        case "CPD":
            # print("CPD")
            F[7] = int(A == D)
            F[6] = 1
            F[5] = int((A & 0xF) < (D & 0xF))
            F[4] = int(A < D)
            pointer += 1
            cycle = 1
        case "CPE":
            # print("CPE")
            F[7] = int(A == E)
            F[6] = 1
            F[5] = int((A & 0xF) < (E & 0xF))
            F[4] = int(A < E)
            pointer += 1
            cycle = 1
        case "CPH":
            # print("CPH")
            F[7] = int(A == H)
            F[6] = 1
            F[5] = int((A & 0xF) < (H & 0xF))
            F[4] = int(A < H)
            pointer += 1
            cycle = 1
        case "CPL":
            # print("CPL")
            F[7] = int(A == L)
            F[6] = 1
            F[5] = int((A & 0xF) < (L & 0xF))
            F[4] = int(A < L)
            pointer += 1
            cycle = 1
        case "CPHL":
            # print("CPHL")
            F[7] = int(A == readMem(MEMORY, joinHex(H,L), bank_controller))
            F[6] = 1
            F[5] = int((A & 0xF) < (readMem(MEMORY, joinHex(H,L), bank_controller) & 0xF))
            F[4] = int(A < readMem(MEMORY, joinHex(H,L), bank_controller))
            pointer += 1
            cycle = 2
        case "CPA":
            # print("CPA")
            F[7] = int(A == A)
            F[6] = 1
            F[5] = 0
            F[4] = 0

            pointer += 1
            cycle = 1
        case "RETNZ":
            # print("RETNZ")
            if F[7] == 0:
                l = readMem(MEMORY, SP, bank_controller)
                SP += 1
                h = readMem(MEMORY, SP, bank_controller)
                SP += 1
                pointer = (h << 8) | l
                cycle = 5
            else:
                pointer += 1
                cycle = 2
        case "POPBC":
            # print("POPBC")
            C = readMem(MEMORY, SP, bank_controller)
            SP += 1
            B = readMem(MEMORY, SP, bank_controller)
            SP += 1
            pointer += 1
            cycle = 3
        case "JPNZA16":
            # print("JPNZA16")
            if F[7] == 0:
                pointer = (readMem(MEMORY, pointer+2, bank_controller)
                            << 8) | readMem(MEMORY, pointer+1, bank_controller)
                cycle = 4
            else:
                pointer += 3
                cycle = 3
        case "JP":
            # print("JP")
            h = readMem(MEMORY, pointer+1, bank_controller)
            l = readMem(MEMORY, pointer+2, bank_controller)
            # print(pointer)
            pointer = l << 8 | h
            cycle = 4
            #print(f"Jumped to {hex(pointer)}")
        case "CALLNZA16":
            # print("CALLNZA16")
            if F[7] == 0:
                SP -= 1
                writeMem(MEMORY, SP, (pointer+3)
                            >> 8, bank_controller)
                SP -= 1
                writeMem(MEMORY, SP, (pointer+3)
                            & 0xFF, bank_controller)
                # Jump to address
                pointer = (readMem(MEMORY, pointer+2, bank_controller)
                            << 8) | readMem(MEMORY, pointer+1, bank_controller)
                cycle = 6
            else:
                pointer += 3
                cycle = 3
        case "PUSHBC":
            # print("PUSHBC")
            SP -= 1
            writeMem(MEMORY, SP, B, bank_controller)
            SP -= 1
            writeMem(MEMORY, SP, C, bank_controller)
            pointer += 1
            cycle = 3
        case "ADDA8":
            # print("ADDA8")
            F[5] = 1 if (
                A & 0xF) + (readMem(MEMORY, pointer+1, bank_controller) & 0xF) > 0xF else 0
            F[4] = int(A + readMem(MEMORY, pointer +
                        1, bank_controller) > 0xFF)
            A = A + readMem(MEMORY, pointer+1,
                            bank_controller) & 0xFF
            F[7] = int(A == 0)
            F[6] = 0
            pointer += 2
            cycle = 2
        case "RST00H":
            # print("RST00H")
            SP -= 1
            writeMem(MEMORY, SP, (pointer+1) >> 8, bank_controller)
            SP -= 1
            writeMem(MEMORY, SP, (pointer+1)
                        & 0xFF, bank_controller)
            pointer = 0x00
            cycle = 4
        case "RETZ":
            # print("RETZ")
            if F[7] == 1:
                l = readMem(MEMORY, SP, bank_controller)
                SP += 1
                h = readMem(MEMORY, SP, bank_controller)
                SP += 1
                pointer = (h << 8) | l
                cycle = 5
            else:
                pointer += 1
                cycle = 2
        case "RET":
            # print("RET")
            # print VRAM
            # print(MEMORY[0x8000:0x8800])
            # exit()
            l = readMem(MEMORY, SP, bank_controller)
            SP += 1
            h = readMem(MEMORY, SP, bank_controller)
            SP += 1
            pointer = h << 8 | l
            cycle = 4
        case "JPZA16":
            # print("JPZA16")
            if F[7] == 1:
                pointer = (readMem(MEMORY, pointer+2, bank_controller)
                            << 8) | readMem(MEMORY, pointer+1, bank_controller)
                cycle = 4
            else:
                pointer += 3
                cycle = 3
        case "PREFCB":
            # print("PREFCB")
            prefix = True
            pointer += 1
            cycle = 2
        case "CALLZA16":
            # print("CALLZA16")
            if F[7] == 1:
                SP -= 1
                writeMem(MEMORY, SP, (pointer+3)
                            >> 8, bank_controller)
                SP -= 1
                writeMem(MEMORY, SP, (pointer+3)
                            & 0xFF, bank_controller)
                pointer = (readMem(MEMORY, pointer+2, bank_controller)
                            << 8) | readMem(MEMORY, pointer+1, bank_controller)
                cycle = 6
            else:
                pointer += 3
                cycle = 3
        case "CALLA16":
            # print("CALLA16")
            # Push address of next instruction to stack
            SP -= 1
            writeMem(MEMORY, SP, (pointer+3) >> 8, bank_controller)
            SP -= 1
            writeMem(MEMORY, SP, (pointer+3)
                        & 0xFF, bank_controller)
            # Jump to address
            h = readMem(MEMORY, pointer+1, bank_controller)
            l = readMem(MEMORY, pointer+2, bank_controller)
            pointer = l << 8 | h
            #print(f"Jumped to {hex(pointer)}")
            cycle = 6
        case "ADCAA8":
            #CEDE
            # print("ADDCAA8")
            tmp = A + readMem(MEMORY, pointer+1, bank_controller) + F[4]
            F[7] = int(tmp&0xff == 0)
            F[6] = 0
            F[5] = int(((A&0x07) + (readMem(MEMORY, pointer+1, bank_controller)&0x7) + F[4]) > 0x7)
            F[4] = int(tmp>0xff)
            A=tmp&0xff
            pointer += 2
            cycle = 2
        case "RST08H":
            # print("RST08H")
            SP -= 1
            writeMem(MEMORY, SP, (pointer+1) >> 8, bank_controller)
            SP -= 1
            writeMem(MEMORY, SP, (pointer+1)
                        & 0xFF, bank_controller)
            pointer = 0x08
            cycle = 4
        case "RETNC":
            # print("RETNC")
            if F[4] == 0:
                l = readMem(MEMORY, SP, bank_controller)
                SP += 1
                h = readMem(MEMORY, SP, bank_controller)
                SP += 1
                pointer = (h << 8) | l
                cycle = 5
            else:
                pointer += 1
                cycle = 2
        case "POPDE":
            # print("POPDE")
            E = readMem(MEMORY, SP, bank_controller)
            D = readMem(MEMORY, SP+1, bank_controller)
            SP += 2
            pointer += 1
            cycle = 3
        case "JPNCA16":
            # print("JPNCA16")
            if F[4] == 0:
                pointer = (readMem(MEMORY, pointer+2, bank_controller)
                            << 8) | readMem(MEMORY, pointer+1, bank_controller)
                cycle = 4
            else:
                pointer += 3
                cycle = 3
        case "CALLNCA16":
            # print("CALLNCA16")
            if F[4] == 0:
                SP -= 1
                writeMem(MEMORY, SP, (pointer+3)
                            >> 8, bank_controller)
                SP -= 1
                writeMem(MEMORY, SP, (pointer+3)
                            & 0xFF, bank_controller)
                pointer = (readMem(MEMORY, pointer+2, bank_controller)
                            << 8) | readMem(MEMORY, pointer+1, bank_controller)
                cycle = 6
            else:
                pointer += 3
                cycle = 3
        case "PUSHDE":
            # print("PUSHDE")
            SP -= 1
            writeMem(MEMORY, SP, D, bank_controller)
            SP -= 1
            writeMem(MEMORY, SP, E, bank_controller)
            pointer += 1
            cycle = 4
        case "SUBA8":
            # print("SUBA8")
            F[6] = 1
            F[5] = 1 if (
                (A & 0xF) - (readMem(MEMORY, pointer+1, bank_controller) & 0xF)) < 0 else 0
            F[4] = int(
                A - readMem(MEMORY, pointer+1, bank_controller) < 0)
            A = A - readMem(MEMORY, pointer+1,
                            bank_controller) & 0xFF
            F[7] = int(A == 0)
            pointer += 2
            cycle = 2
        case "RST10H":
            # print("RST10H")
            SP -= 1
            writeMem(MEMORY, SP, (pointer+1) >> 8, bank_controller)
            SP -= 1
            writeMem(MEMORY, SP, (pointer+1)
                        & 0xFF, bank_controller)
            pointer = 0x10
            cycle = 4
        case "RETC":
            # print("RETC")
            if F[4] == 1:
                l = readMem(MEMORY, SP, bank_controller)
                SP += 1
                h = readMem(MEMORY, SP, bank_controller)
                SP += 1
                pointer = (h << 8) | l
                cycle = 5
            else:
                pointer += 1
                cycle = 2
        case "RETI":
            # print("RETI")
            IME = True
            l = readMem(MEMORY, SP, bank_controller)
            SP += 1
            h = readMem(MEMORY, SP, bank_controller)
            SP += 1
            pointer = (h << 8) | l
            cycle = 4
            # print("RETI")
            #print("Pointer: ", hex(pointer))
        case "JPCA16":
            # print("JPCA16")
            if F[4] == 1:
                pointer = (readMem(MEMORY, pointer+2, bank_controller)
                            << 8) | readMem(MEMORY, pointer+1, bank_controller)
                cycle = 4
            else:
                pointer += 3
                cycle = 3
        case "CALLCA16":
            # print("CALLCA16")
            if F[4] == 1:
                SP -= 1
                writeMem(MEMORY, SP, (pointer+3)
                            >> 8, bank_controller)
                SP -= 1
                writeMem(MEMORY, SP, (pointer+3)
                            & 0xFF, bank_controller)
                pointer = (readMem(MEMORY, pointer+2, bank_controller)
                            << 8) | readMem(MEMORY, pointer+1, bank_controller)
                cycle = 6
            else:
                pointer += 3
                cycle = 3
        case "SBCA8":
            # print("SBCA8")
            tmp = A - readMem(MEMORY, pointer+1, bank_controller) - F[4]
            F[7] = int(tmp&0xff == 0)
            F[6] = 1
            F[5] = int(((A&0x07) - (readMem(MEMORY, pointer+1, bank_controller)&0x7) - F[4]) < 0)
            F[4] = int(tmp<0)
            A=tmp&0xff

            pointer += 2
            cycle = 2
        case "RST18H":
            # print("RST18H")
            SP -= 1
            writeMem(MEMORY, SP, (pointer+1) >> 8, bank_controller)
            SP -= 1
            writeMem(MEMORY, SP, (pointer+1)
                        & 0xFF, bank_controller)
            pointer = 0x18
            cycle = 4
        case "LDHA8A":
            # print("LDHA8A")
            writeMem(MEMORY, 0xFF00+readMem(MEMORY, pointer +
                        1, bank_controller), A, bank_controller)
            pointer += 2
            cycle = 3
        case "POPHL":
            # print("POPHL")
            L = readMem(MEMORY, SP, bank_controller)
            SP += 1
            H = readMem(MEMORY, SP, bank_controller)
            SP += 1
            pointer += 1
            cycle = 3
        case "LDHCA":
            # print("LDHCA")
            writeMem(MEMORY, 0xFF00+C, A, bank_controller)
            pointer += 1
            cycle = 2
        case "PUSHHL":
            # print("PUSHL")
            SP -= 1
            writeMem(MEMORY, SP, H, bank_controller)
            SP -= 1
            writeMem(MEMORY, SP, L, bank_controller)
            pointer += 1
            cycle = 4
        case "ANDA8":
            # print("ANDA8")
            F[4:7] = [0, 1, 0]
            A = A & readMem(MEMORY, pointer+1, bank_controller)
            F[7] = int(A == 0)
            pointer += 2
            cycle = 2
        case "RST20H":
            # print("RST20H")
            SP -= 1
            writeMem(MEMORY, SP, (pointer+1) >> 8, bank_controller)
            SP -= 1
            writeMem(MEMORY, SP, (pointer+1)
                        & 0xFF, bank_controller)
            pointer = 0x20
            cycle = 4
        case "ADDSPR8":
            # print("ADDSPR8")
            F[6:8] = [0, 0]
            F[5] = 1 if (
                SP & 0xF) + (readMem(MEMORY, pointer+1, bank_controller) & 0xF) > 0xF else 0
            F[4] = int(SP + readMem(MEMORY, pointer +
                        1, bank_controller) > 0xFF)
            SP = SP + \
                signed(readMem(MEMORY, pointer+1, bank_controller))
            pointer += 2
            cycle = 4
        case "JPHL":
            # print("JPHL")
            pointer = joinHex(H,L)
            cycle = 1
        case "LDA16A":
            # print("LDA16A")
            writeMem(MEMORY, (readMem(MEMORY, pointer+2, bank_controller) << 8)
                        | readMem(MEMORY, pointer+1, bank_controller), A, bank_controller)
            pointer += 3
            cycle = 2
        case "XORA8":
            # print("XORA8")
            F[4:7] = [0, 0, 0]
            A = A ^ readMem(MEMORY, pointer+1, bank_controller)
            F[7] = int(A == 0)
            pointer += 2
            cycle = 2
        case "RST28H":
            # print("RST28H")
            SP -= 1
            writeMem(MEMORY, SP, (pointer+1) >> 8, bank_controller)
            SP -= 1
            writeMem(MEMORY, SP, (pointer+1)
                        & 0xFF, bank_controller)
            pointer = 0x28
            cycle = 4
        case "LDHAA8":
            # print("LDHAA8")
            # print(MEMORY[0xFF00+MEMORY[pointer+1]])
            A = readMem(MEMORY, 0xFF00+readMem(MEMORY,
                        pointer+1, bank_controller), bank_controller,keys)
            pointer += 2
            cycle = 3
        case "POPAF":
            # print("POPAF")
            F = readMem(MEMORY, SP, bank_controller)
            F = [int(x) for x in list('{0:08b}'.format(F))]
            F = F[::-1]
            F[0:4] = [0, 0, 0, 0]
            SP += 1
            A = readMem(MEMORY, SP, bank_controller)
            SP += 1
            pointer += 1
            cycle = 3
        case "LDAHC":
            # print("LDAHC")
            A = readMem(MEMORY, 0xFF00+C, bank_controller)
            pointer += 1
            cycle = 2

        case "DI":
            # print("DI")
            IME = False
            pointer += 1
            cycle = 1
        case "PUSHAF":
            # print("PUSHAF")
            # F has to be converted to a byte
            SP -= 1
            writeMem(MEMORY, SP, A, bank_controller)
            SP -= 1
            # make sure F is 8 BITs and not true or false
            F = [int(x) for x in F]

            writeMem(MEMORY, SP, int(
                "".join([str(x) for x in F[::-1]]), 2), bank_controller)
            pointer += 1
            cycle = 4
        case "ORA8":
            # print("ORA8")
            A = A | readMem(MEMORY, pointer+1, bank_controller)
            F[7] = int(A == 0)
            F[4:7] = [0, 0, 0]
            pointer += 2
            cycle = 2
        case "RST30H":
            # print("RST30H")
            SP -= 1
            writeMem(MEMORY, SP, (pointer+1) >> 8, bank_controller)
            SP -= 1
            writeMem(MEMORY, SP, (pointer+1)
                        & 0xFF, bank_controller)
            pointer = 0x30
            cycle = 4
        case "LDHLSPR8":
            # print("LDHLSPR8")
            F[6:8] = [0, 0]
            F[5] = 1 if (
                SP & 0xF) + (readMem(MEMORY, pointer+1, bank_controller) & 0xF) > 0xF else 0
            F[4] = int(SP + readMem(MEMORY, pointer +
                        1, bank_controller) > 0xFF)
            L = (
                SP + signed(readMem(MEMORY, pointer+1, bank_controller))) & 0xFF
            H = (
                SP + signed(readMem(MEMORY, pointer+1, bank_controller))) >> 8
            pointer += 2
            cycle = 3
        case "LDSPHL":
            # print("LDSPHL")
            SP = joinHex(H,L)
            pointer += 1
            cycle = 2
        case "LDAA16":
            # print("LDAA16")
            l = readMem(MEMORY, pointer+1, bank_controller)
            h = readMem(MEMORY, pointer+2, bank_controller)
            A = readMem(MEMORY, int.from_bytes(
                [l, h], "little"), bank_controller)
            pointer += 3
            cycle = 2
        case "EI":
            # print("EI")
            IME = True
            pointer += 1
            cycle = 1
        case "CP":
            # print("CP")
            F[7] = int(A == readMem(MEMORY, pointer+1, bank_controller))
            F[6] = 1
            F[5] = int((A&0xf) < (readMem(MEMORY, pointer+1, bank_controller)&0xf))
            F[4] = int(A < readMem(MEMORY, pointer+1, bank_controller))
            pointer += 2
            cycle = 2
        case "RST38H":
            # print("RST38H")
            SP -= 1
            writeMem(MEMORY, SP, (pointer+1) >> 8, bank_controller)
            SP -= 1
            writeMem(MEMORY, SP, (pointer+1)
                        & 0xFF, bank_controller)
            pointer = 0x38
            cycle = 4

        case other:
            assert False, f"Unknown opcode: {code:02x}"
    return A, B, C, D, E, H, L, F, SP, IME, MEMORY, pointer, cycle, prefix

def handle_extra_opcodes(code,A,B,C,D,E,H,L,F,SP,IME,MEMORY,pointer,bank_controller):
    match extra_opcodes[code]:
        case "RLCB":
            # print("RLCB")
            B,F=RLC(B,F)
            pointer += 1
            cycle = 2
        case "RLCC":
            # print("RLC")
            C,F=RLC(C,F)
            pointer += 1
            cycle = 2
        case "RLCD":
            # print("RLCDE")
            D,F=RLC(D,F)
            pointer += 1
            cycle = 2
        case "RLCE":
            # print("RLCE")
            E,F=RLC(E,F)
            pointer += 1
            cycle = 2
        case "RLCH":
            # print("RLCH")
            H,F=RLC(H,F)
            pointer += 1
            cycle = 2
        case "RLCL":
            # print("RLCL")
            L,F=RLC(L,F)
            pointer += 1
            cycle = 2
        case "RLCHL":
            # print("RLCHL")
            val = readMem(MEMORY, joinHex(H,L), bank_controller)
            val,F=RLC(val,F)
            writeMem(MEMORY, joinHex(H,L), val, bank_controller)
            pointer += 1
            cycle = 2
        case "RLCA":
            # print("RLCA")
            A,F=RLC(A,F)
            pointer += 1
            cycle = 2
        case "RRCB":
            # print("RRCB")
            B,F=RRC(B,F)
            pointer += 1
            cycle = 2
        case "RRCC":
            # print("RRCC")
            C,F=RRC(C,F)
            pointer += 1
            cycle = 2
        case "RRCD":
            # print("RRCD")
            D,F=RRC(D,F)
            pointer += 1
            cycle = 2
        case "RRCE":
            # print("RRCE")
            E,F=RRC(E,F)
            pointer += 1
            cycle = 2
        case "RRCH":
            # print("RRCH")
            H,F=RRC(H,F)
            pointer += 1
            cycle = 2
        case "RRCL":
            # print("RRCL")
            L,F=RRC(L,F)
            pointer += 1
            cycle = 2
        case "RRCHL":
            # print("RRCHL")
            val = readMem(MEMORY, joinHex(H,L), bank_controller)
            val,F=RRC(val,F)
            writeMem(MEMORY, joinHex(H,L), val, bank_controller)
            pointer += 1
            cycle = 2
        case "RRCA":
            # print("RRCA")
            A,F=RRC(A,F)
            pointer += 1
            cycle = 2
        case "RLB":
            # print("RLB")
            B,F=RL(B,F)
            pointer += 1
            cycle = 2
        case"RLC":
            # Rotate left C
            # print("RLC")
            C,F=RL(C,F)
            pointer += 1
            cycle = 2
        case "RLD":
            # print("RLD")
            D,F=RL(D,F)
            pointer += 1
            cycle = 2
        case "RLE":
            # print("RLE")
            E,F=RL(E,F)
            pointer += 1
            cycle = 2
        case "RLH":
            # print("RLH")
            H,F=RL(H,F)
            pointer += 1
            cycle = 2
        case "RLL":
            # print("RLL")
            L,F=RL(L,F)
            pointer += 1
            cycle = 2
        case "RLHL":
            # print("RLHL")
            val = readMem(MEMORY, joinHex(H,L), bank_controller)
            val,F=RL(val,F)
            writeMem(MEMORY, joinHex(H,L), val, bank_controller)
            pointer += 1
            cycle = 2
        case "RLA":
            # print("RLA")
            A,F=RL(A,F)
            pointer += 1
            cycle = 2
        case "RRB":
            # print("RRB")
            B,F=RR(B,F)
            pointer += 1
            cycle = 2
        case "RRC":
            # print("RRC")
            C,F=RR(C,F)
            pointer += 1
            cycle = 2
        case "RRD":
            # print("RRD")
            D,F=RR(D,F)
            pointer += 1
            cycle = 2
        case "RRE":
            # print("RRE")
            E,F=RR(E,F)
            pointer += 1
            cycle = 2
        case "RRH":
            # print("RRH")
            H,F=RR(H,F)
            pointer += 1
            cycle = 2
        case "RRL":
            # print("RRL")
            L,F=RR(L,F)
            pointer += 1
            cycle = 2
        case "RRHL":
            # print("RRHL")
            val = readMem(MEMORY, joinHex(H,L), bank_controller)
            val,F=RR(val,F)
            writeMem(MEMORY, joinHex(H,L), val, bank_controller)
            pointer += 1
            cycle = 2
        case "RRA":
            # print("RRA")
            A,F=RR(A,F)
            pointer += 1
            cycle = 2
        case "SLAB":
            # print("SLAB")
            B,F=SLA(B,F)
            pointer += 1
            cycle = 2
        case "SLAC":
            # print("SLAC")
            C,F=SLA(C,F)
            pointer += 1
            cycle = 2
        case "SLAD":
            # print("SLAD")
            D,F=SLA(D,F)
            pointer += 1
            cycle = 2
        case "SLAE":
            # print("SLAE")
            E,F=SLA(E,F)
            pointer += 1
            cycle = 2
        case "SLAH":
            # print("SLAH")
            H,F=SLA(H,F)
            pointer += 1
            cycle = 2
        case "SLAL":
            # print("SLAL")
            L,F=SLA(L,F)
            pointer += 1
            cycle = 2
        case "SLAHL":
            # print("SLAHL")
            temp,F=SLA(readMem(MEMORY,joinHex(H,L),bank_controller),F)
            writeMem(MEMORY,joinHex(H,L),temp,bank_controller)
            pointer += 1
            cycle = 4
        case "SLAA":
            # print("SLAA")
            A,F=SLA(A,F)
            pointer += 1
            cycle = 2
        case "SRAB":
            # print("SRAB")
            B,F=SRA(B,F)
            pointer += 1
            cycle = 2
        case "SRAC":
            # print("SRAC")
            C,F=SRA(C,F)
            pointer += 1
            cycle = 2
        case "SRAD":
            # print("SRAD")
            D,F=SRA(D,F)
            pointer += 1
            cycle = 2
        case "SRAE":
            # print("SRAE")
            E,F=SRA(E,F)
            pointer += 1
            cycle = 2
        case "SRAH":
            # print("SRAH")
            H,F=SRA(H,F)
            pointer += 1
            cycle = 2
        case "SRAL":
            # print("SRAL")
            L,F=SRA(L,F)
            pointer += 1
            cycle = 2
        case "SRAHL":
            # print("SRAHL")
            temp,F=SRA(readMem(MEMORY,joinHex(H,L),bank_controller),F)
            writeMem(MEMORY,joinHex(H,L),temp,bank_controller)
            pointer += 1
            cycle = 4
        case "SRAA":
            # print("SRAA")
            A,F=SRA(A,F)
            pointer += 1
            cycle = 2
        case "SWAPB":
            # print("SWAPB")
            B,F=SWAP(B,F)
            pointer += 1
            cycle = 2
        case "SWAPC":
            # print("SWAPC")
            C,F=SWAP(C,F)
            pointer += 1
            cycle = 2
        case "SWAPD":
            # print("SWAPD")
            D,F=SWAP(D,F)
            pointer += 1
            cycle = 2
        case "SWAPE":
            # print("SWAPE")
            E,F=SWAP(E,F)
            pointer += 1
            cycle = 2
        case "SWAPH":
            # print("SWAPH")
            H,F=SWAP(H,F)
            pointer += 1
            cycle = 2
        case "SWAPL":
            # print("SWAPL")
            L,F=SWAP(L,F)
            pointer += 1
            cycle = 2
        case "SWAPHL":
            # print("SWAPHL")
            temp,F=SWAP(readMem(MEMORY,joinHex(H,L),bank_controller),F)
            writeMem(MEMORY,joinHex(H,L),temp,bank_controller)
            pointer += 1
            cycle = 4
        case "SWAPA":
            # print("SWAPA")
            A,F=SWAP(A,F)
            pointer += 1
            cycle = 2
        case "SRLB":
            # print("SRLB")
            B,F=SRL(B,F)
            pointer += 1
            cycle = 2
        case "SRLC":
            # print("SRLC")
            C,F=SRL(C,F)
            pointer += 1
            cycle = 2
        case "SRLD":
            # print("SRLD")
            D,F=SRL(D,F)
            pointer += 1
            cycle = 2
        case "SRLE":
            # print("SRLE")
            E,F=SRL(E,F)
            pointer += 1
            cycle = 2
        case "SRLH":
            # print("SRLH")
            H,F=SRL(H,F)
            pointer += 1
            cycle = 2
        case "SRLL":
            # print("SRLL")
            L,F=SRL(L,F)
            pointer += 1
            cycle = 2
        case "SRLHL":
            # print("SRLHL")
            temp,F=SRL(readMem(MEMORY,joinHex(H,L),bank_controller),F)
            writeMem(MEMORY,joinHex(H,L),temp,bank_controller)
            pointer += 1
            cycle = 4
        case "SRLA":
            # print("SRLA")
            A,F=SRL(A,F)
            pointer += 1
            cycle = 2
        case "BIT0B":
            # print("BIT0B")
            F=BIT(B,0,F)
            pointer += 1
            cycle = 2
        case "BIT0C":
            # print("BIT0C")
            F=BIT(C,0,F)
            pointer += 1
            cycle = 2
        case "BIT0D":
            # print("BIT0D")
            F=BIT(D,0,F)
            pointer += 1
            cycle = 2
        case "BIT0E":
            # print("BIT0E")
            F=BIT(E,0,F)
            pointer += 1
            cycle = 2
        case "BIT0H":
            # print("BIT0H")
            F=BIT(H,0,F)
            pointer += 1
            cycle = 2
        case "BIT0L":
            # print("BIT0L")
            F=BIT(L,0,F)
            pointer += 1
            cycle = 2
        case "BIT0HL":
            # print("BIT0HL")
            F=BIT(readMem(MEMORY, joinHex(H,L), bank_controller),0,F)
            pointer += 1
            cycle = 4
        case "BIT0A":
            # print("BIT0A")
            F=BIT(A,0,F)
            pointer += 1
            cycle = 2
        case "BIT1B":
            # print("BIT1B")
            F=BIT(B,1,F)
            pointer += 1
            cycle = 2
        case "BIT1C":
            # print("BIT1C")
            F=BIT(C,1,F)
            pointer += 1
            cycle = 2
        case "BIT1D":
            # print("BIT1D")
            F=BIT(D,1,F)
            pointer += 1
            cycle = 2
        case "BIT1E":
            # print("BIT1E")
            F=BIT(E,1,F)
            pointer += 1
            cycle = 2
        case "BIT1H":
            # print("BIT1H")
            F=BIT(H,1,F)
            pointer += 1
            cycle = 2
        case "BIT1L":
            # print("BIT1L")
            F=BIT(L,1,F)
            pointer += 1
            cycle = 2
        case "BIT1HL":
            # print("BIT1HL")
            F=BIT(readMem(MEMORY, joinHex(H,L), bank_controller),1,F)
            pointer += 1
            cycle = 4
        case "BIT1A":
            # print("BIT1A")
            F=BIT(A,1,F)
            pointer += 1
            cycle = 2
        case "BIT2B":
            # print("BIT2B")
            F=BIT(B,2,F)
            pointer += 1
            cycle = 2
        case "BIT2C":
            # print("BIT2C")
            F=BIT(C,2,F)
            pointer += 1
            cycle = 2
        case "BIT2D":
            # print("BIT2D")
            F=BIT(D,2,F)
            pointer += 1
            cycle = 2
        case "BIT2E":
            # print("BIT2E")
            F=BIT(E,2,F)
            pointer += 1
            cycle = 2
        case "BIT2H":
            # print("BIT2H")
            F=BIT(H,2,F)
            pointer += 1
            cycle = 2
        case "BIT2L":
            # print("BIT2L")
            F=BIT(L,2,F)
            pointer += 1
            cycle = 2
        case "BIT2HL":
            # print("BIT2HL")
            F=BIT(readMem(MEMORY, joinHex(H,L), bank_controller),2,F)
            pointer += 1
            cycle = 4
        case "BIT2A":
            # print("BIT2A")
            F=BIT(A,2,F)
            pointer += 1
            cycle = 2
        case "BIT3B":
            # print("BIT3B")
            F=BIT(B,3,F)
            pointer += 1
            cycle = 2
        case "BIT3C":
            # print("BIT3C")
            F=BIT(C,3,F)
            pointer += 1
            cycle = 2
        case "BIT3D":
            # print("BIT3D")
            F=BIT(D,3,F)
            pointer += 1
            cycle = 2
        case "BIT3E":
            # print("BIT3E")
            F=BIT(E,3,F)
            pointer += 1
            cycle = 2
        case "BIT3H":
            # print("BIT3H")
            F=BIT(H,3,F)
            pointer += 1
            cycle = 2
        case "BIT3L":
            # print("BIT3L")
            F=BIT(L,3,F)
            pointer += 1
            cycle = 2
        case "BIT3HL":
            # print("BIT3HL")
            F=BIT(readMem(MEMORY, joinHex(H,L), bank_controller),3,F)
            pointer += 1
            cycle = 4
        case "BIT3A":
            # print("BIT3A")
            F=BIT(A,3,F)
            pointer += 1
            cycle = 2
        case "BIT4B":
            # print("BIT4B")
            F=BIT(B,4,F)
            pointer += 1
            cycle = 2
        case "BIT4C":
            # print("BIT4C")
            F=BIT(C,4,F)
            pointer += 1
            cycle = 2
        case "BIT4D":
            # print("BIT4D")
            F=BIT(D,4,F)
            pointer += 1
            cycle = 2
        case "BIT4E":
            # print("BIT4E")
            F=BIT(E,4,F)
            pointer += 1
            cycle = 2
        case "BIT4H":
            # print("BIT4H")
            F=BIT(H,4,F)
            pointer += 1
            cycle = 2
        case "BIT4L":
            # print("BIT4L")
            F=BIT(L,4,F)
            pointer += 1
            cycle = 2
        case "BIT4HL":
            # print("BIT4HL")
            F=BIT(readMem(MEMORY, joinHex(H,L), bank_controller),4,F)
            pointer += 1
            cycle = 4
        case "BIT4A":
            # print("BIT4A")
            F=BIT(A,4,F)
            pointer += 1
            cycle = 2
        case "BIT5B":
            # print("BIT5B")
            F=BIT(B,5,F)
            pointer += 1
            cycle = 2
        case "BIT5C":
            # print("BIT5C")
            F=BIT(C,5,F)
            pointer += 1
            cycle = 2
        case "BIT5D":
            # print("BIT5D")
            F=BIT(D,5,F)
            pointer += 1
            cycle = 2
        case "BIT5E":
            # print("BIT5E")
            F=BIT(E,5,F)
            pointer += 1
            cycle = 2
        case "BIT5H":
            # print("BIT5H")
            F=BIT(H,5,F)
            pointer += 1
            cycle = 2
        case "BIT5L":
            # print("BIT5L")
            F=BIT(L,5,F)
            pointer += 1
            cycle = 2
        case "BIT5HL":
            # print("BIT5HL")
            F=BIT(readMem(MEMORY, joinHex(H,L), bank_controller),5,F)
            pointer += 1
            cycle = 4
        case "BIT5A":
            # print("BIT5A")
            F=BIT(A,5,F)
            pointer += 1
            cycle = 2
        case "BIT6B":
            # print("BIT6B")
            F=BIT(B,6,F)
            pointer += 1
            cycle = 2
        case "BIT6C":
            # print("BIT6C")
            F=BIT(C,6,F)
            pointer += 1
            cycle = 2
        case "BIT6D":
            # print("BIT6D")
            F=BIT(D,6,F)
            pointer += 1
            cycle = 2
        case "BIT6E":
            # print("BIT6E")
            F=BIT(E,6,F)
            pointer += 1
            cycle = 2
        case "BIT6H":
            # print("BIT6H")
            F=BIT(H,6,F)
            pointer += 1
            cycle = 2
        case "BIT6L":
            # print("BIT6L")
            F=BIT(L,6,F)
            pointer += 1
            cycle = 2
        case "BIT6HL":
            # print("BIT6HL")
            F=BIT(readMem(MEMORY, joinHex(H,L), bank_controller),6,F)
            pointer += 1
            cycle = 4
        case "BIT6A":
            # print("BIT6A")
            F=BIT(A,6,F)
            pointer += 1
            cycle = 2
        case "BIT7B":
            # print("BIT7B")
            F=BIT(B,7,F)
            pointer += 1
            cycle = 2
        case "BIT7C":
            # print("BIT7C")
            F=BIT(C,7,F)
            pointer += 1
            cycle = 2
        case "BIT7D":
            # print("BIT7D")
            F=BIT(D,7,F)
            pointer += 1
            cycle = 2
        case "BIT7E":
            # print("BIT7E")
            F=BIT(E,7,F)
            pointer += 1
            cycle = 2
        case "BIT7H":
            # print("BIT7H")
            F=BIT(H,7,F)
            pointer += 1
            cycle = 2
        case "BIT7L":
            # print("BIT7L")
            F=BIT(L,7,F)
            pointer += 1
            cycle = 2
        case "BIT7HL":
            # print("BIT7HL")
            F=BIT(readMem(MEMORY, joinHex(H,L), bank_controller),7,F)
            pointer += 1
            cycle = 4
        case "BIT7A":
            # print("BIT7A")
            F=BIT(A,7,F)
            pointer += 1
            cycle = 2
        case "RES0B":
            # print("RES0B")
            B=RES(B,0)
            pointer += 1
            cycle = 2
        case "RES0C":
            # print("RES0C")
            C=RES(C,0)
            pointer += 1
            cycle = 2
        case "RES0D":
            # print("RES0D")
            D=RES(D,0)
            pointer += 1
            cycle = 2
        case "RES0E":
            # print("RES0E")
            E=RES(E,0)
            pointer += 1
            cycle = 2
        case "RES0H":
            # print("RES0H")
            H=RES(H,0)
            pointer += 1
            cycle = 2
        case "RES0L":
            # print("RES0L")
            L=RES(L,0)
            pointer += 1
            cycle = 2
        case "RES0HL":
            # print("RES0HL")
            writeMem(MEMORY, joinHex(H,L), RES(readMem(MEMORY, joinHex(H,L), bank_controller),0), bank_controller)
            pointer += 1
            cycle = 4
        case "RES0A":
            # print("RES0A")
            A=RES(A,0)
            pointer += 1
            cycle = 2
        case "RES1B":
            # print("RES1B")
            B=RES(B,1)
            pointer += 1
            cycle = 2
        case "RES1C":
            # print("RES1C")
            C=RES(C,1)
            pointer += 1
            cycle = 2
        case "RES1D":
            # print("RES1D")
            D=RES(D,1)
            pointer += 1
            cycle = 2
        case "RES1E":
            # print("RES1E")
            E=RES(E,1)
            pointer += 1
            cycle = 2
        case "RES1H":
            # print("RES1H")
            H=RES(H,1)
            pointer += 1
            cycle = 2
        case "RES1L":
            # print("RES1L")
            L=RES(L,1)
            pointer += 1
            cycle = 2
        case "RES1HL":
            # print("RES1HL")
            writeMem(MEMORY, joinHex(H,L), RES(readMem(MEMORY, joinHex(H,L), bank_controller),1), bank_controller)
            pointer += 1
            cycle = 4
        case "RES1A":
            # print("RES1A")
            A=RES(A,1)
            pointer += 1
            cycle = 2
        case "RES2B":
            # print("RES2B")
            B=RES(B,2)
            pointer += 1
            cycle = 2
        case "RES2C":
            # print("RES2C")
            C=RES(C,2)
            pointer += 1
            cycle = 2
        case "RES2D":
            # print("RES2D")
            D=RES(D,2)
            pointer += 1
            cycle = 2
        case "RES2E":
            # print("RES2E")
            E=RES(E,2)
            pointer += 1
            cycle = 2
        case "RES2H":
            # print("RES2H")
            H=RES(H,2)
            pointer += 1
            cycle = 2
        case "RES2L":
            # print("RES2L")
            L=RES(L,2)
            pointer += 1
            cycle = 2
        case "RES2HL":
            # print("RES2HL")
            writeMem(MEMORY, joinHex(H,L), RES(readMem(MEMORY, joinHex(H,L), bank_controller),2), bank_controller)
            pointer += 1
            cycle = 4
        case "RES2A":
            # print("RES2A")
            A=RES(A,2)
            pointer += 1
            cycle = 2
        case "RES3B":
            # print("RES3B")
            B=RES(B,3)
            pointer += 1
            cycle = 2
        case "RES3C":
            # print("RES3C")
            C=RES(C,3)
            pointer += 1
            cycle = 2
        case "RES3D":
            # print("RES3D")
            D=RES(D,3)
            pointer += 1
            cycle = 2
        case "RES3E":
            # print("RES3E")
            E=RES(E,3)
            pointer += 1
            cycle = 2
        case "RES3H":
            # print("RES3H")
            H=RES(H,3)
            pointer += 1
            cycle = 2
        case "RES3L":
            # print("RES3L")
            L=RES(L,3)
            pointer += 1
            cycle = 2
        case "RES3HL":
            # print("RES3HL")
            writeMem(MEMORY, joinHex(H,L), RES(readMem(MEMORY, joinHex(H,L), bank_controller),3), bank_controller)
            pointer += 1
            cycle = 4
        case "RES3A":
            # print("RES3A")
            A=RES(A,3)
            pointer += 1
            cycle = 2
        case "RES4B":
            # print("RES4B")
            B=RES(B,4)
            pointer += 1
            cycle = 2
        case "RES4C":
            # print("RES4C")
            C=RES(C,4)
            pointer += 1
            cycle = 2
        case "RES4D":
            # print("RES4D")
            D=RES(D,4)
            pointer += 1
            cycle = 2
        case "RES4E":
            # print("RES4E")
            E=RES(E,4)
            pointer += 1
            cycle = 2
        case "RES4H":
            # print("RES4H")
            H=RES(H,4)
            pointer += 1
            cycle = 2
        case "RES4L":
            # print("RES4L")
            L=RES(L,4)
            pointer += 1
            cycle = 2
        case "RES4HL":
            # print("RES4HL")
            writeMem(MEMORY, joinHex(H,L), RES(readMem(MEMORY, joinHex(H,L), bank_controller),4), bank_controller)
            pointer += 1
            cycle = 4
        case "RES4A":
            # print("RES4A")
            A=RES(A,4)
            pointer += 1
            cycle = 2
        case "RES5B":
            # print("RES5B")
            B=RES(B,5)
            pointer += 1
            cycle = 2
        case "RES5C":
            # print("RES5C")
            C=RES(C,5)
            pointer += 1
            cycle = 2
        case "RES5D":
            # print("RES5D")
            D=RES(D,5)
            pointer += 1
            cycle = 2
        case "RES5E":
            # print("RES5E")
            E=RES(E,5)
            pointer += 1
            cycle = 2
        case "RES5H":
            # print("RES5H")
            H=RES(H,5)
            pointer += 1
            cycle = 2
        case "RES5L":
            # print("RES5L")
            L=RES(L,5)
            pointer += 1
            cycle = 2
        case "RES5HL":
            # print("RES5HL")
            writeMem(MEMORY, joinHex(H,L), RES(readMem(MEMORY, joinHex(H,L), bank_controller),5), bank_controller)
            pointer += 1
            cycle = 4
        case "RES5A":
            # print("RES5A")
            A=RES(A,5)
            pointer += 1
            cycle = 2
        case "RES6B":
            # print("RES6B")
            B=RES(B,6)
            pointer += 1
            cycle = 2
        case "RES6C":
            # print("RES6C")
            C=RES(C,6)
            pointer += 1
            cycle = 2
        case "RES6D":
            # print("RES6D")
            D=RES(D,6)
            pointer += 1
            cycle = 2
        case "RES6E":
            # print("RES6E")
            E=RES(E,6)
            pointer += 1
            cycle = 2
        case "RES6H":
            # print("RES6H")
            H=RES(H,6)
            pointer += 1
            cycle = 2
        case "RES6L":
            # print("RES6L")
            L=RES(L,6)
            pointer += 1
            cycle = 2
        case "RES6HL":
            # print("RES6HL")
            writeMem(MEMORY, joinHex(H,L), RES(readMem(MEMORY, joinHex(H,L), bank_controller),6), bank_controller)
            pointer += 1
            cycle = 4
        case "RES6A":
            # print("RES6A")
            A=RES(A,6)
            pointer += 1
            cycle = 2
        case "RES7B":
            # print("RES7B")
            B=RES(B,7)
            pointer += 1
            cycle = 2
        case "RES7C":
            # print("RES7C")
            C=RES(C,7)
            pointer += 1
            cycle = 2
        case "RES7D":
            # print("RES7D")
            D=RES(D,7)
            pointer += 1
            cycle = 2
        case "RES7E":
            # print("RES7E")
            E=RES(E,7)
            pointer += 1
            cycle = 2
        case "RES7H":
            # print("RES7H")
            H=RES(H,7)
            pointer += 1
            cycle = 2
        case "RES7L":
            # print("RES7L")
            L=RES(L,7)
            pointer += 1
            cycle = 2
        case "RES7HL":
            # print("RES7HL")
            writeMem(MEMORY, joinHex(H,L), RES(readMem(MEMORY, joinHex(H,L), bank_controller),7), bank_controller)
            pointer += 1
            cycle = 4
        case "RES7A":
            # print("RES7A")
            A=RES(A,7)
            pointer += 1
            cycle = 2
        case "SET0B":
            # print("SET0B")
            B=SET(B,0)
            pointer += 1
            cycle = 2
        case "SET0C":
            # print("SET0C")
            C=SET(C,0)
            pointer += 1
            cycle = 2
        case "SET0D":
            # print("SET0D")
            D=SET(D,0)
            pointer += 1
            cycle = 2
        case "SET0E":
            # print("SET0E")
            E=SET(E,0)
            pointer += 1
            cycle = 2
        case "SET0H":
            # print("SET0H")
            H=SET(H,0)
            pointer += 1
            cycle = 2
        case "SET0L":
            # print("SET0L")
            L=SET(L,0)
            pointer += 1
            cycle = 2
        case "SET0HL":
            # print("SET0HL")
            writeMem(MEMORY, joinHex(H,L), SET(readMem(MEMORY, joinHex(H,L), bank_controller),0), bank_controller)
            pointer += 1
            cycle = 4
        case "SET0A":
            # print("SET0A")
            A=SET(A,0)
            pointer += 1
            cycle = 2
        case "SET1B":
            # print("SET1B")
            B=SET(B,1)
            pointer += 1
            cycle = 2
        case "SET1C":
            # print("SET1C")
            C=SET(C,1)
            pointer += 1
            cycle = 2
        case "SET1D":
            # print("SET1D")
            D=SET(D,1)
            pointer += 1
            cycle = 2
        case "SET1E":
            # print("SET1E")
            E=SET(E,1)
            pointer += 1
            cycle = 2
        case "SET1H":
            # print("SET1H")
            H=SET(H,1)
            pointer += 1
            cycle = 2
        case "SET1L":
            # print("SET1L")
            L=SET(L,1)
            pointer += 1
            cycle = 2
        case "SET1HL":
            # print("SET1HL")
            writeMem(MEMORY, joinHex(H,L), SET(readMem(MEMORY, joinHex(H,L), bank_controller),1), bank_controller)
            pointer += 1
            cycle = 4
        case "SET1A":
            # print("SET1A")
            A=SET(A,1)
            pointer += 1
            cycle = 2
        case "SET2B":
            # print("SET2B")
            B=SET(B,2)
            pointer += 1
            cycle = 2
        case "SET2C":
            # print("SET2C")
            C=SET(C,2)
            pointer += 1
            cycle = 2
        case "SET2D":
            # print("SET2D")
            D=SET(D,2)
            pointer += 1
            cycle = 2
        case "SET2E":
            # print("SET2E")
            E=SET(E,2)
            pointer += 1
            cycle = 2
        case "SET2H":
            # print("SET2H")
            H=SET(H,2)
            pointer += 1
            cycle = 2
        case "SET2L":
            # print("SET2L")
            L=SET(L,2)
            pointer += 1
            cycle = 2
        case "SET2HL":
            # print("SET2HL")
            writeMem(MEMORY, joinHex(H,L), SET(readMem(MEMORY, joinHex(H,L), bank_controller),2), bank_controller)
            pointer += 1
            cycle = 4
        case "SET2A":
            # print("SET2A")
            A=SET(A,2)
            pointer += 1
            cycle = 2
        case "SET3B":
            # print("SET3B")
            B=SET(B,3)
            pointer += 1
            cycle = 2
        case "SET3C":
            # print("SET3C")
            C=SET(C,3)
            pointer += 1
            cycle = 2
        case "SET3D":
            # print("SET3D")
            D=SET(D,3)
            pointer += 1
            cycle = 2
        case "SET3E":
            # print("SET3E")
            E=SET(E,3)
            pointer += 1
            cycle = 2
        case "SET3H":
            # print("SET3H")
            H=SET(H,3)
            pointer += 1
            cycle = 2
        case "SET3L":
            # print("SET3L")
            L=SET(L,3)
            pointer += 1
            cycle = 2
        case "SET3HL":
            # print("SET3HL")
            writeMem(MEMORY, joinHex(H,L), SET(readMem(MEMORY, joinHex(H,L), bank_controller),3), bank_controller)
            pointer += 1
            cycle = 4
        case "SET3A":
            # print("SET3A")
            A=SET(A,3)
            pointer += 1
            cycle = 2
        case "SET4B":
            # print("SET4B")
            B=SET(B,4)
            pointer += 1
            cycle = 2
        case "SET4C":
            # print("SET4C")
            C=SET(C,4)
            pointer += 1
            cycle = 2
        case "SET4D":
            # print("SET4D")
            D=SET(D,4)
            pointer += 1
            cycle = 2
        case "SET4E":
            # print("SET4E")
            E=SET(E,4)
            pointer += 1
            cycle = 2
        case "SET4H":
            # print("SET4H")
            H=SET(H,4)
            pointer += 1
            cycle = 2
        case "SET4L":
            # print("SET4L")
            L=SET(L,4)
            pointer += 1
            cycle = 2
        case "SET4HL":
            # print("SET4HL")
            writeMem(MEMORY, joinHex(H,L), SET(readMem(MEMORY, joinHex(H,L), bank_controller),4), bank_controller)
            pointer += 1
            cycle = 4
        case "SET4A":
            # print("SET4A")
            A=SET(A,4)
            pointer += 1
            cycle = 2
        case "SET5B":
            # print("SET5B")
            B=SET(B,5)
            pointer += 1
            cycle = 2
        case "SET5C":
            # print("SET5C")
            C=SET(C,5)
            pointer += 1
            cycle = 2
        case "SET5D":
            # print("SET5D")
            D=SET(D,5)
            pointer += 1
            cycle = 2
        case "SET5E":
            # print("SET5E")
            E=SET(E,5)
            pointer += 1
            cycle = 2
        case "SET5H":
            # print("SET5H")
            H=SET(H,5)
            pointer += 1
            cycle = 2
        case "SET5L":
            # print("SET5L")
            L=SET(L,5)
            pointer += 1
            cycle = 2
        case "SET5HL":
            # print("SET5HL")
            writeMem(MEMORY, joinHex(H,L), SET(readMem(MEMORY, joinHex(H,L), bank_controller),5), bank_controller)
            pointer += 1
            cycle = 4
        case "SET5A":
            # print("SET5A")
            A=SET(A,5)
            pointer += 1
            cycle = 2
        case "SET6B":
            # print("SET6B")
            B=SET(B,6)
            pointer += 1
            cycle = 2
        case "SET6C":
            # print("SET6C")
            C=SET(C,6)
            pointer += 1
            cycle = 2
        case "SET6D":
            # print("SET6D")
            D=SET(D,6)
            pointer += 1
            cycle = 2
        case "SET6E":
            # print("SET6E")
            E=SET(E,6)
            pointer += 1
            cycle = 2
        case "SET6H":
            # print("SET6H")
            H=SET(H,6)
            pointer += 1
            cycle = 2
        case "SET6L":
            # print("SET6L")
            L=SET(L,6)
            pointer += 1
            cycle = 2
        case "SET6HL":
            # print("SET6HL")
            writeMem(MEMORY, joinHex(H,L), SET(readMem(MEMORY, joinHex(H,L), bank_controller),6), bank_controller)
            pointer += 1
            cycle = 4
        case "SET6A":
            # print("SET6A")
            A=SET(A,6)
            pointer += 1
            cycle = 2
        case "SET7B":
            # print("SET7B")
            B=SET(B,7)
            pointer += 1
            cycle = 2
        case "SET7C":
            # print("SET7C")
            C=SET(C,7)
            pointer += 1
            cycle = 2
        case "SET7D":
            # print("SET7D")
            D=SET(D,7)
            pointer += 1
            cycle = 2
        case "SET7E":
            # print("SET7E")
            E=SET(E,7)
            pointer += 1
            cycle = 2
        case "SET7H":
            # print("SET7H")
            H=SET(H,7)
            pointer += 1
            cycle = 2
        case "SET7L":
            # print("SET7L")
            L=SET(L,7)
            pointer += 1
            cycle = 2
        case "SET7HL":
            # print("SET7HL")
            writeMem(MEMORY, joinHex(H,L), SET(readMem(MEMORY, joinHex(H,L), bank_controller),7), bank_controller)
            pointer += 1
            cycle = 4
        case "SET7A":
            # print("SET7A")
            A=SET(A,7)
            pointer += 1
            cycle = 2
        case other:
            assert False, f"Unknown extra opcode: {code:02x}"
    return A, B, C, D, E, H, L, F, SP, IME, MEMORY, pointer, cycle