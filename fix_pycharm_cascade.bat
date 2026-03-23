@echo off
echo Fixing PyCharm Cascade/Windsurf loading issue...

REM Kill existing PyCharm processes
taskkill /F /IM pycharm64.exe 2>NUL
taskkill /F /IM pycharm.exe 2>NUL

REM Clear PyCharm cache
echo Clearing PyCharm cache...
rd /S /Q "%APPDATA%\JetBrains\PyCharm2024.1\caches" 2>NUL
rd /S /Q "%APPDATA%\JetBrains\PyCharm2024.1\index" 2>NUL
rd /S /Q "%LOCALAPPDATA%\JetBrains\PyCharm2024.1\log" 2>NUL

REM Clear system temp files
del /Q "%TEMP%\*pycharm*" 2>NUL

REM Set environment variables for better plugin loading
set PYCHARM_VM_OPTIONS=-Xms2g -Xmx4g -XX:ReservedCodeCacheSize=512m -XX:+UseG1GC -XX:SoftRefLRUPolicyMSPerMB=50

REM Start PyCharm with clean state
echo Starting PyCharm with optimized configuration...
start "" "C:\Program Files\JetBrains\PyCharm 2024.1\bin\pycharm64.exe"

echo PyCharm started. Cascade/Windsurf should load properly now.
pause
