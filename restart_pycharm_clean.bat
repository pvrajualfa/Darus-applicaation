@echo off
echo Restarting PyCharm with Cascade fix...

REM Step 1: Close PyCharm gracefully
echo Closing PyCharm...
taskkill /F /IM pycharm64.exe 2>NUL
timeout /T 3 /NOBREAK >NUL

REM Step 2: Clear plugin cache
echo Clearing plugin cache...
rd /S /Q "%APPDATA%\JetBrains\PyCharm2024.1\plugins" 2>NUL
rd /S /Q "%APPDATA%\JetBrains\PyCharm2024.1\caches" 2>NUL

REM Step 3: Wait for cleanup
echo Waiting for cleanup to complete...
timeout /T 5 /NOBREAK >NUL

REM Step 4: Start PyCharm
echo Starting PyCharm...
start "" "C:\Program Files\JetBrains\PyCharm 2024.1\bin\pycharm64.exe"

echo PyCharm restarted. Cascade should now load properly.
echo If issue persists, run fix_pycharm_cascade.bat for complete cleanup.
pause
