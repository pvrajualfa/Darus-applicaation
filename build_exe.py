#!/usr/bin/env python3
"""
Build script for creating executable from the Darus application
"""

import os
import sys
import subprocess
import shutil

def clean_build_dirs():
    """Clean previous build directories"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name}...")
            shutil.rmtree(dir_name)

def build_executable():
    """Build the executable using PyInstaller"""
    
    # PyInstaller command with all necessary options
    cmd = [
        'pyinstaller',
        '--name=Darus',
        '--windowed',  # Hide console window
        '--onefile',    # Create single executable
        '--add-data=icons;icons',  # Include icons folder
        '--add-data=data;data',    # Include data folder
        '--add-data=fonts;fonts',  # Include fonts folder
        '--add-data=assets;assets', # Include assets folder
        '--add-data=ui2;ui2',  # Include ui2 folder
        '--hidden-import=ui2.mainwindow',
        '--hidden-import=ui2.student_registration',
        '--hidden-import=ui2.student_list',
        '--hidden-import=ui2.reports',
        '--hidden-import=PySide6.QtCore',
        '--hidden-import=PySide6.QtGui', 
        '--hidden-import=PySide6.QtWidgets',
        '--hidden-import=sqlite3',
        '--hidden-import=reportlab',
        '--hidden-import=PyPDF2',
        'main.py'  # Entry point
    ]
    
    print("Building executable...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build successful!")
        print(result.stdout)
        
        # Check if executable was created
        exe_path = os.path.join('dist', 'Darus.exe')
        if os.path.exists(exe_path):
            print(f"Executable created: {os.path.abspath(exe_path)}")
            print(f"Size: {os.path.getsize(exe_path) / (1024*1024):.1f} MB")
        else:
            print("Executable not found!")
            
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False
    
    return True

def main():
    """Main build function"""
    print("Building Darus Application Executable")
    print("=" * 50)
    
    # Check if main.py exists
    if not os.path.exists('main.py'):
        print("main.py not found!")
        return
    
    # Clean previous builds
    clean_build_dirs()
    
    # Build executable
    if build_executable():
        print("\nBuild completed successfully!")
        print(f"Executable location: {os.path.abspath('dist/Darus.exe')}")
        print("\nYou can now run the executable from the dist folder.")
    else:
        print("\nBuild failed!")

if __name__ == "__main__":
    main()
