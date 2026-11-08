# AutoClick AC

**A lightweight, free and open-source autoclicker for Windows, developed by JakkByte.**

AutoClick AC is a simple and easy-to-use Windows application that automates mouse clicks with adjustable speed and convenient keyboard shortcuts.

## Features

- Five adjustable clicking speed levels
- Left and right mouse button support
- Global F6 shortcut to start or stop clicking
- Speed control using arrow keys or the numeric keypad
- Minimize to the Windows system tray
- Lightweight interface with JakkByte's dark theme
- Standalone Windows executable
- Free and open-source software

## Download

The Windows executable will be available in the [Releases](https://github.com/JakkByte/AutoClick-AC/releases) section.

Once released, download `AutoClick-AC.exe` and run it. No Python installation is required.

## Keyboard Shortcuts

| Key | Action |
|---|---|
| F6 | Start / Stop automatic clicking |
| Up Arrow | Increase clicking speed (arrow mode) |
| Down Arrow | Decrease clicking speed (arrow mode) |
| Numpad 1–5 | Select a speed level (numpad mode) |
| ESC | Close the application |

## Clicking Speeds

| Level | Interval |
|---|---|
| 1 | 500 ms |
| 2 | 250 ms |
| 3 | 100 ms |
| 4 | 50 ms |
| 5 | 20 ms |

## Run from Source

Install Python and the required dependencies:

```bash
python -m pip install pillow pystray
```

Then run:

```bash
python main.py
```

**Note:** AutoClick AC is designed for Windows.

## License

This project is licensed under the [MIT License](LICENSE).

## Developer

**JakkByte**

Building useful apps and tools, one byte at a time.

[GitHub Profile](https://github.com/JakkByte)
