# Clean build script to avoid conflicts
import os
import sys
import subprocess
import shutil

def clean_and_build():
    # Clean dist directory
    if os.path.exists("dist"):
        shutil.rmtree("dist")
        print("Cleaned dist directory")
    
    # Clean build directory
    if os.path.exists("build"):
        shutil.rmtree("build")
        print("Cleaned build directory")
    
    # Install PyInstaller if not installed
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Build command with clean environment
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name=SchoolManagement_Final",
        "--hidden-import=sqlite3",
        "--clean",
        "Darus_complete_single.py"
    ]
    
    print("Building clean EXE with embedded files...")
    print("Command: " + " ".join(cmd))
    
    # Run PyInstaller
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("EXE built successfully!")
        exe_path = "dist/SchoolManagement_Final.exe"
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
    clean_and_build()
