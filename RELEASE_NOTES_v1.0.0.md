# Number System Converter v1.0.0

The first official release of the rebuilt **Number System Converter**.

Version `1.0.0` replaces the original Tkinter implementation with a redesigned desktop application built using **Python, PySide6, and QML**.

## Highlights

- Complete desktop UI rebuild with PySide6 + QML
- Binary, octal, decimal, and hexadecimal conversion
- Automatic prefix-aware number-system detection
- Live multi-base conversion
- 8-bit, 16-bit, 32-bit, 64-bit, and Auto width modes
- Signed and unsigned integer interpretation
- Two's-complement support
- Automatic signed interpretation for non-decimal Auto mode
- Negative integer support in Signed mode
- Number inspector with bit, byte, sign, parity, and representation details
- Persistent local conversion history
- TXT and CSV history export
- Dark, light, and system appearance modes
- Keyboard shortcuts and copy-to-clipboard actions
- Automated test suite
- Automated Windows build pipeline through GitHub Actions
- SHA-256 release verification

## Windows

Download:

```text
NSC-v1.0.0.exe
```

No Python installation or dependency setup is required.

A SHA-256 checksum is provided alongside the executable:

```text
NSC-v1.0.0.exe.sha256
```

## Windows SmartScreen

The executable is currently distributed without a commercial code-signing certificate.

Because of this, Microsoft Defender SmartScreen may display an **"unrecognized app"** warning when the application is launched for the first time.

Official builds are distributed only through this repository's GitHub Releases. The included SHA-256 checksum can be used to verify the downloaded executable.

## Source

Developers can also run the application directly from source using Python 3.11+ and PySide6.

See the repository README for setup, architecture, usage, and development information.

---

Built by **TW4RDYDEV**.