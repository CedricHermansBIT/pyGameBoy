# Gameboy emulator written in Python

## Requirements

- Python 3.11 (tested)
- Pygame
- Threading

## Usage

Within read_gb.py, change the path to the ROM you want to play on line 202

Run the program from within the directory that contains the python scripts and DMG_ROM.bin

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
- Fix halt bug for 02-interrupts.gb
- Add save states
