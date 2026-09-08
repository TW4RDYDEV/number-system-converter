<div align="center">

<img src="assets/banner.svg" alt="Number System Converter" width="100%">

<br>

![Version](https://img.shields.io/badge/version-1.0.0-79FFA8?style=flat-square&labelColor=11151B)
![Python](https://img.shields.io/badge/Python-3.11%2B-79FFA8?style=flat-square&labelColor=11151B)
![PySide6](https://img.shields.io/badge/UI-PySide6%20%2B%20QML-79FFA8?style=flat-square&labelColor=11151B)
![Platform](https://img.shields.io/badge/release-Windows%20x64-79FFA8?style=flat-square&labelColor=11151B)
![License](https://img.shields.io/badge/license-source--available-79FFA8?style=flat-square&labelColor=11151B)

[![Download Latest Release](https://img.shields.io/badge/Download-Latest%20Release-79FFA8?style=for-the-badge&labelColor=11151B)](https://github.com/TW4RDYDEV/number-system-converter/releases/latest)

**Binary · Octal · Decimal · Hexadecimal**

A polished desktop utility for developers, students, networking labs, and anyone working with integer representations.

</div>

---

## Overview

**Number System Converter** converts integers between binary, octal, decimal, and hexadecimal while exposing the bit-level information behind each value.

Version `1.0.0` is a complete rebuild of the original Tkinter project using **Python, PySide6, and QML**.

The application provides live multi-base conversion, signed and unsigned interpretation, fixed-width integer modes, two's-complement support, persistent history, export tools, configurable appearance, and a redesigned desktop interface.

## Features

- Binary, octal, decimal, and hexadecimal conversion
- Automatic base detection for `0b`, `0o`, and `0x` prefixes
- Live conversion while typing
- All four number-system representations displayed simultaneously
- 8-bit, 16-bit, 32-bit, 64-bit, and Auto width modes
- Signed and unsigned integer interpretation
- Two's-complement interpretation for fixed-width bit patterns
- Automatic signed interpretation for non-decimal values in Auto mode
- Negative decimal support in Signed mode
- Binary digit grouping
- Uppercase and lowercase hexadecimal formatting
- Number inspector with:
  - bit length
  - bytes required
  - parity
  - sign
  - decimal digit count
  - hexadecimal digit count
- Persistent local conversion history
- TXT and CSV history export
- Dark, light, and system appearance modes
- Copy-to-clipboard actions
- Keyboard shortcuts
- Automated test suite
- Automated Windows release builds through GitHub Actions
- SHA-256 checksums for published Windows executables

## Preview

![Number System Converter Preview](assets/preview.png)

## Supported Input

| System | Base | Examples |
|---|---:|---|
| Binary | 2 | `101010`, `0b101010`, `1111 0000` |
| Octal | 8 | `755`, `0o755` |
| Decimal | 10 | `415`, `-42` |
| Hexadecimal | 16 | `F3C`, `0xDEADBEEF`, `ff` |

Spaces and underscores may be used as visual separators.

## Auto Detection

Auto mode intentionally avoids aggressive guessing.

- `0b...` → Binary
- `0o...` → Octal
- `0x...` → Hexadecimal
- Values containing `A-F` → Hexadecimal
- Digits-only values → Decimal

This prevents ambiguous values such as `10`, `100`, or `1010` from being silently interpreted as binary.

## Signed Mode

`Signed` controls whether a value may be interpreted as a signed integer.

With a fixed width (`8/16/32/64-bit`), binary, octal, and hexadecimal inputs use two's-complement interpretation.

When `Auto` width is selected, signed non-decimal inputs automatically use the smallest whole-byte width required to represent the value.

Example:

```text
1111 1111 + Signed + Auto  → -1 (8-bit)
1111 1111 + Unsigned       → 255
0x80 + Signed + Auto       → -128 (8-bit)
0x7F + Signed + Auto       → 127 (8-bit)
```

Decimal input remains intentionally conservative in Auto mode to avoid ambiguous interpretation.

## Fixed-Width Integer Modes

Choose `8-bit`, `16-bit`, `32-bit`, or `64-bit` to inspect a value using a specific integer width.

Example:

```text
Input: FF
Input base: Hexadecimal
Width: 8-bit
Mode: Signed

Decimal:      -1
Binary:       1111 1111
Octal:        377
Hexadecimal:  FF

Unsigned interpretation: 255
Signed interpretation:   -1
```

## Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl + L` | Focus the input field |
| `Ctrl + R` | Reset converter |
| `Ctrl + C` | Copy decimal result |
| `Esc` | Clear/reset input |
| `Enter` | Convert and add to history |

## Download

The recommended way to use Number System Converter is the official standalone Windows release.

### Windows

1. Open the **[Latest Release](https://github.com/TW4RDYDEV/number-system-converter/releases/latest)**.
2. Download:

```text
NSC-v1.0.0.exe
```

3. Run the executable.

No Python installation or dependency setup is required.

A SHA-256 checksum is published alongside the executable:

```text
NSC-v1.0.0.exe.sha256
```

### Verify the Download

On Windows, verify the executable with PowerShell:

```powershell
Get-FileHash .\NSC-v1.0.0.exe -Algorithm SHA256
```

Compare the resulting hash with the value stored in:

```text
NSC-v1.0.0.exe.sha256
```

## Windows SmartScreen

The Windows executable is currently distributed without a commercial code-signing certificate.

Because of this, Microsoft Defender SmartScreen may display an **"unrecognized app"** warning when the application is launched for the first time.

Official builds are distributed only through this repository's **GitHub Releases**, and every release includes a SHA-256 checksum for verification.

Code signing may be added to future releases.

## Run from Source

Developers who prefer to run the application directly from source can clone the repository:

```bash
git clone https://github.com/TW4RDYDEV/number-system-converter.git
cd number-system-converter
```

Create a virtual environment:

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install runtime dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

## Development

Install development dependencies:

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

Run the complete test suite:

```bash
pytest -q
```

Windows executables are built automatically through GitHub Actions. Local users do not need to build the packaged release themselves.

## Project Structure

```text
number-system-converter/
├── main.py
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
│
├── app/
│   ├── __init__.py
│   ├── backend.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── converter.py
│   │   ├── detector.py
│   │   └── formatter.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── history.py
│   │   └── settings.py
│   │
│   └── ui/
│       ├── Main.qml
│       │
│       ├── components/
│       │   ├── AppButton.qml
│       │   ├── ResultCard.qml
│       │   ├── StyledComboBox.qml
│       │   ├── StyledTextField.qml
│       │   └── ToggleSwitch.qml
│       │
│       └── pages/
│           ├── ConverterPage.qml
│           └── SettingsPage.qml
│
├── tests/
│   ├── test_converter.py
│   ├── test_detector.py
│   ├── test_formatter.py
│   ├── test_qml_signal_handlers.py
│   ├── test_release_sanity.py
│   └── test_release_workflow.py
│
├── assets/
│   ├── banner.svg
│   ├── icon.ico
│   ├── icon.png
│   └── preview.png
│
├── .github/
│   └── workflows/
│       └── build-release.yml
│
├── .gitattributes
├── .gitignore
├── CHANGELOG.md
├── RELEASE_NOTES_v1.0.0.md
├── LICENSE
└── README.md
```

## Release Automation

Windows releases are built automatically using **GitHub Actions** on a Windows runner.

When a version tag such as:

```bash
git tag v1.1.0
git push origin v1.1.0
```

is pushed, the workflow automatically:

1. checks out the repository,
2. configures Python,
3. installs project dependencies,
4. runs the automated test suite,
5. builds the standalone Windows executable,
6. generates a SHA-256 checksum,
7. uploads the build artifact, and
8. publishes the GitHub Release.

Release files follow the naming format:

```text
NSC-v1.0.0.exe
NSC-v1.0.0.exe.sha256
```

Future versions automatically inherit the corresponding version tag:

```text
NSC-v1.1.0.exe
NSC-v2.0.0.exe
```

## License

This project is **source-available**, not OSI-approved open source.

Personal, educational, evaluation, and other non-commercial use is permitted under the included license.

**Commercial use, resale, monetization, paid hosting, or inclusion in a commercial product or service requires prior written permission from TW4RDYDEV.**

Redistributions must retain the original copyright, license, and attribution notices.

The original TW4RDYDEV attribution may not be removed, obscured, or falsified.

See [`LICENSE`](LICENSE) for the complete terms.

## Author

**TW4RDYDEV**

Cybersecurity · Networking · Software Development

---

<div align="center">

Built with Python + PySide6/QML.

</div>