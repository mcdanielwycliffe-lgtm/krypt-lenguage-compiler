@echo off
setlocal EnableExtensions

REM ================================================================
REM Build oficial do compilador/runtime Krypt para Windows
REM Saida: dist\krypt.exe
REM ================================================================

cd /d "%~dp0"
set "PYTHON=python"

where python >nul 2>nul
if errorlevel 1 (
    echo [ERRO] Python nao foi encontrado no PATH.
    echo Instale Python 3.10+ em https://www.python.org/downloads/windows/
    exit /b 1
)

%PYTHON% --version
if errorlevel 1 exit /b 1

echo.
echo [1/4] Instalando/atualizando PyInstaller...
%PYTHON% -m pip install --upgrade pyinstaller
if errorlevel 1 (
    echo [ERRO] Nao foi possivel instalar o PyInstaller.
    exit /b 1
)

echo.
echo [2/4] Limpando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist krypt.spec del /q krypt.spec

 echo.
echo [3/4] Gerando dist\krypt.exe...
%PYTHON% -m PyInstaller ^
  --clean ^
  --noconfirm ^
  --onefile ^
  --name krypt ^
  --paths "%~dp0" ^
  --hidden-import tkinter ^
  --hidden-import _tkinter ^
  kryptc.py
if errorlevel 1 (
    echo [ERRO] O PyInstaller falhou.
    exit /b 1
)

if not exist dist\krypt.exe (
    echo [ERRO] O arquivo dist\krypt.exe nao foi criado.
    exit /b 1
)

echo.
echo [4/4] Testando o executavel...
dist\krypt.exe --version
if errorlevel 1 (
    echo [ERRO] krypt.exe nao conseguiu executar --version.
    exit /b 1
)

dist\krypt.exe --help >nul
if errorlevel 1 (
    echo [ERRO] krypt.exe nao conseguiu executar --help.
    exit /b 1
)

if exist examples\hello.krypt (
    dist\krypt.exe check examples\hello.krypt
    if errorlevel 1 exit /b 1
)

echo.
echo ================================================================
echo SUCESSO: dist\krypt.exe foi criado e testado.
echo Uso:
echo   dist\krypt.exe --version
echo   dist\krypt.exe --help
echo   dist\krypt.exe -File "arquivo.krypt"
echo ================================================================
exit /b 0
