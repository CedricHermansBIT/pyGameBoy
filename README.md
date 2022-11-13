# Gameboy emulator written in Python

## Requirements

- Python 3.11 (tested)
- Pygame
- Threading

## Usage

In config.txt, set the first line to the path of the ROM you want to run.

Run the read_gb.py program from within the directory that contains the python scripts and DMG_ROM.bin

```bash
python3 read_gb.py
```

## Controls

Arrow keys + A, S (would be B on gameboy), ENTER, BACKSPACE

## Notes

At the moment, only ROMS without memory banking or memory bank controller 3 (kinda) work.
No sound yet.

## TODO

- Add sound
- Add memory banking for other mbcs
- Add save states
- Check what is wrong with specific ROMs

## Working ROMs (Tested, might still contain bugs, but they are playable)

- Dr. Mario (World).gb
