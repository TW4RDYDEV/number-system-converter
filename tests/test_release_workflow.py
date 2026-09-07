from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_release_workflow_builds_versioned_windows_exe():
    workflow = (ROOT / ".github/workflows/build-release.yml").read_text(encoding="utf-8")
    assert "windows-latest" in workflow
    assert "pytest -q" in workflow
    assert "pyinstaller" in workflow
    assert "NumberSystemConverter-${{ github.ref_name }}-Windows-x64.exe" in workflow
    assert "Get-FileHash" in workflow
    assert "softprops/action-gh-release@v2" in workflow


def test_readme_points_users_to_latest_release():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "releases/latest" in readme
    assert "No Python installation or dependency setup is required." in readme
    assert "Build the Windows executable locally:" not in readme
