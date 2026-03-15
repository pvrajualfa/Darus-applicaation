# Simple build script without console mode
import os
import sys
import subprocess

def build_exe():
    # Install PyInstaller if not installed
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Build command - console mode to avoid issues
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name=SchoolManagement_Fixed",
        "--hidden-import=sqlite3",
        "Darus_complete_single.py"
    ]
    
    print("Building EXE file with sqlite3 support...")
    print("Command: " + " ".join(cmd))
    
    # Run PyInstaller
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("EXE built successfully!")
        exe_path = "dist/SchoolManagement_Fixed.exe"
        if os.path.exists(exe_path):
            print("Location: " + exe_path)
            print("Size: " + str(os.path.getsize(exe_path)) + " bytes")
        else:
            print("EXE file not found at expected location")
    else:
        print("Build failed:")
        print(result.stderr)
    
    return result.returncode == 0

if __name__ == "__main__":
    build_exe()
