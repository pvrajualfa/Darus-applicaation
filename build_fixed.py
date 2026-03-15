# Fixed build script for School Management System EXE
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
    
    # Build command with hidden imports
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=SchoolManagement",
        "--hidden-import=sqlite3",
        "--hidden-import=PySide6.QtWidgets",
        "--hidden-import=PySide6.QtCore",
        "--hidden-import=PySide6.QtGui",
        "--collect-all=PySide6",
        "Darus_complete_single.py"
    ]
    
    print("Building EXE file with all dependencies...")
    print("Command: " + " ".join(cmd))
    
    # Run PyInstaller
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("EXE built successfully!")
        print("Location: dist/SchoolManagement.exe")
        print("Size: " + str(os.path.getsize("dist/SchoolManagement.exe")) + " bytes")
    else:
        print("Build failed:")
        print(result.stderr)
    
    return result.returncode == 0

if __name__ == "__main__":
    build_exe()
