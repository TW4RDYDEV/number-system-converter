# Number System Converter by TWARDY

A Python desktop application that converts numbers between **Decimal**, **Binary**, and **Hexadecimal** number systems.

This project was built using Python and Tkinter. It includes a clean graphical interface, live conversion, input validation, copy-to-clipboard support, conversion history, and dark/light mode switching.

## Features

- Convert between Decimal, Binary, and Hexadecimal
- Prevents converting a number system into the same type
- Live conversion while typing
- Copy the result by clicking on it
- Copy Result button
- Reset button
- Conversion history
- Save conversion history to a `.txt` file
- Clear history button
- Dark mode and light mode
- Supports binary prefixes like `0b1010`
- Supports hexadecimal prefixes like `0xF3C`
- Allows spaces and underscores in input for readability
- Displays extra number details:
  - Decimal value
  - Binary value
  - Grouped binary
  - Hexadecimal value
  - Bit length
- Better error messages for invalid input

## Supported Conversions

|    From     |     To      |
|-------------|-------------|
| Decimal     | Binary      |
| Decimal     | Hexadecimal |
| Binary      | Decimal     |
| Binary      | Hexadecimal |
| Hexadecimal | Decimal     |
| Hexadecimal | Binary      |

## Example Conversions

|   Input   |     From    |     To      |    Result    |
|-----------|-------------|-------------|--------------|
| 415       | Decimal     | Binary      | 110011111    |
| 415       | Decimal     | Hexadecimal | 19F          |
| 110011111 | Binary      | Decimal     | 415          |
| F3C       | Hexadecimal | Binary      | 111100111100 |
| 0xF3C     | Hexadecimal | Decimal     | 3900         |
| 0b101010  | Binary      | Decimal     | 42           |


## Requirements

This project does not require any external Python packages.

It only uses built-in Python libraries:

- `tkinter`
- `ttk`
- `messagebox`
- `filedialog`

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/TW4RDYDEV/number-system-converter.git
