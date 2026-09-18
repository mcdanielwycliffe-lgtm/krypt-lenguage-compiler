$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

Write-Host '[1/4] Instalando/atualizando PyInstaller...'
python -m pip install --upgrade pyinstaller

Write-Host '[2/4] Limpando builds anteriores...'
if (Test-Path build) { Remove-Item build -Recurse -Force }
if (Test-Path dist) { Remove-Item dist -Recurse -Force }
if (Test-Path krypt.spec) { Remove-Item krypt.spec -Force }

Write-Host '[3/4] Gerando dist\krypt.exe...'
python -m PyInstaller --clean --noconfirm --onefile --name krypt --paths $PSScriptRoot --hidden-import tkinter --hidden-import _tkinter kryptc.py

if (-not (Test-Path 'dist\krypt.exe')) { throw 'dist\krypt.exe não foi criado.' }

Write-Host '[4/4] Testando o executável...'
& 'dist\krypt.exe' --version
& 'dist\krypt.exe' --help | Out-Null
if (Test-Path 'examples\hello.krypt') { & 'dist\krypt.exe' check 'examples\hello.krypt' }

Write-Host ''
Write-Host 'SUCESSO: dist\krypt.exe foi criado e testado.' -ForegroundColor Green
Write-Host 'Uso: dist\krypt.exe -File "arquivo.krypt"'
