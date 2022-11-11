from opcodes import opcodes


def getChecksum(data):
    checksum = 0
    for byte in data:
        checksum = checksum - byte - 1
    return checksum & 0xFF


def read_header(content):
    ENTRY_POINT = content[0x100:0x104]
    print(f"Entry point: {ENTRY_POINT}")
    NINTENDO_LOGO = content[0x104:0x134]
    print(f"Nintendo logo: {NINTENDO_LOGO.hex()}")
    TITLE = content[0x134:0x143]
    print(f"Title: {TITLE.decode('ascii')}")
    MANUFACTURER_CODE = content[0x13F:0x143]
    print(f"Manufacturer code: {MANUFACTURER_CODE.hex()}")
    CGB_FLAG = content[0x143:0x144]
    print(f"CGB flag: {CGB_FLAG}")
    NEW_LICENSEE_CODE = content[0x144:0x146]
    print(f"New licensee code: {NEW_LICENSEE_CODE.decode('ascii')}")
    SGB_FLAG = content[0x146:0x147]
    print(f"SGB flag: {SGB_FLAG}")
    CARTRIDGE_TYPE = content[0x147:0x148]
    print(f"Cartridge type: {CARTRIDGE_TYPE}")
    ROM_SIZE = content[0x148:0x149]
    print(f"ROM size: {ROM_SIZE.hex()}")
    RAM_SIZE = content[0x149:0x14A]
    print(f"RAM size: {RAM_SIZE}")
    DESTINATION_CODE = content[0x14A:0x14B]
    print(f"Destination code: {DESTINATION_CODE}")
    OLD_LICENSEE_CODE = content[0x14B:0x14C]
    print(f"Old licensee code: {OLD_LICENSEE_CODE.hex()}")
    MASK_ROM_VERSION_NUMBER = content[0x14C:0x14D]
    print(f"Mask ROM version number: {MASK_ROM_VERSION_NUMBER}")
    HEADER_CHECKSUM = content[0x14D:0x14E]
    print(f"Header checksum: {HEADER_CHECKSUM.hex()}")
    calculatedCheckSum = getChecksum(
        content[0x134:0x14D]).to_bytes(1, 'little').hex()
    print(
        f"Calculated header checksum: {calculatedCheckSum}")
    if HEADER_CHECKSUM == calculatedCheckSum:
        print("Header checksum is correct")
    else:
        print("Header checksum is incorrect!")

    GLOBAL_CHECKSUM = content[0x14E:0x150]
    print(f"Global checksum: {GLOBAL_CHECKSUM.hex()}")

    for n in range(len(ENTRY_POINT)):
        print(instruction := opcodes[ENTRY_POINT[n]])
        if instruction == "NOP":
            continue
        elif instruction == "JP":
            print(ENTRY_POINT[n+1:n+3].hex())
            break
    return ENTRY_POINT[n+1:n+3]

if __name__ == "__main__":
    with open("Pokemon - Red Version.gb", "rb") as f:
        content = f.read()
    read_header(content)
