#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
WINEPREFIX="$ROOT/.wine-krypt"; export WINEPREFIX
PYVER="3.12.10"
WROOT="$ROOT/.winpython"
mkdir -p "$WROOT"
if [ ! -f "$WROOT/python.exe" ]; then
  cd "$WROOT"
  wget -q --show-progress -O python.zip "https://www.python.org/ftp/python/${PYVER}/python-${PYVER}-embed-amd64.zip"
  unzip -q -o python.zip
  sed -i 's/^#import site/import site/' python312._pth
  wget -q -O get-pip.py https://bootstrap.pypa.io/get-pip.py
  wine python.exe get-pip.py
fi
cd "$ROOT"
wine "$WROOT/python.exe" -m pip install --upgrade pyinstaller
rm -rf "$ROOT/dist-windows" "$ROOT/build-windows"
wine "$WROOT/python.exe" -m PyInstaller --clean --noconfirm --onefile --name krypt --distpath "$ROOT/dist-windows" --workpath "$ROOT/build-windows" --specpath "$ROOT" --paths "$ROOT" --hidden-import tkinter --hidden-import _tkinter kryptc.py
file "$ROOT/dist-windows/krypt.exe"
ls -lh "$ROOT/dist-windows/krypt.exe"
