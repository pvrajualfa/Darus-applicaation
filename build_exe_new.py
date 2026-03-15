# Build script for School Management System EXE
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
    
    # Build command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Create single EXE
        "--windowed",                   # No console window
        "--name=SchoolManagement",     # EXE name
        "--icon=NONE",                  # No icon (you can add icon file path)
        "--add-data=ui2;ui2",           # Include ui2 directory (will be created)
        "Darus_complete_single.py"      # Main script
    ]
    
    print("Building EXE file...")
    print(f"Command: {' '.join(cmd)}")
    
    # Run PyInstaller
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ EXE built successfully!")
        print("📁 Location: dist/SchoolManagement.exe")
    else:
        print("❌ Build failed:")
        print(result.stderr)
    
    return result.returncode == 0

if __name__ == "__main__":
    build_exe()
