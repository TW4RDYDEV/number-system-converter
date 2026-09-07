# Changelog

All notable changes to Number System Converter are documented here.

## [1.0.0] - 2026-09-07

### Added

- Added null-safe shutdown bindings to prevent harmless end-of-process QML TypeErrors.
- Improved backend lifetime management during QML shutdown.
- Switched Qt Quick Controls to the customizable Basic style to eliminate native-style customization warnings.
- Remember-history disabled state now prevents history from persisting between launches.
- Conversion-affecting settings now refresh live results automatically.
- Default bit-width setting now immediately synchronizes with the converter.
- Responsive Settings cards so controls remain inside their sections.
- Unified styling for the converter value field and dropdown controls.
- Complete PySide6/QML interface rebuild.
- Binary, octal, decimal, and hexadecimal conversion.
- Conservative automatic number-system detection.
- Live multi-base conversion.
- 8-bit, 16-bit, 32-bit, 64-bit, and automatic width modes.
- Signed and unsigned integer interpretation.
- Auto-width signed interpretation for non-decimal two's-complement input.
- Two's-complement interpretation for binary, octal, and hexadecimal bit patterns.
- Negative decimal support in Signed mode.
- Number inspector with bit length, byte requirement, parity, sign, and digit counts.
- Persistent conversion history.
- TXT and CSV history export.
- Dark, light, and system appearance settings.
- Uppercase/lowercase hexadecimal preference.
- Binary grouping preference.
- Keyboard shortcuts.
- Windows executable build and tagged-release GitHub Actions workflow.
- Automated core conversion tests.
- TW4RDYDEV source-available licensing.
