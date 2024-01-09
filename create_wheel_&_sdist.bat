@ECHO off
REM Check that tucuxi-core is updated and cloned
ECHO ==============================================================================
ECHO ========================== Creating wheel and sdist ==========================
ECHO ==============================================================================
RMDIR /S /Q "dist/"
RMDIR /S /Q "_skbuild/"

pipx run build --sdist --wheel

RMDIR /S /Q "sotalya.egg-info/"
ECHO ==============================================================================
ECHO ========================== Wheel and sdist created! ==========================
ECHO ==============================================================================