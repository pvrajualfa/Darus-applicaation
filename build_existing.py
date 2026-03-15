# Build EXE using existing ui2 directory
import subprocess
import os

# Build command that uses existing ui2 directory
cmd = [
    "pyinstaller",
    "--onefile",
    "--name=SchoolManagement_Existing",
    "--hidden-import=sqlite3",
    "--add-data=ui2;ui2",
    "Darus_complete_single.py"
]

print("Building EXE using existing ui2 directory...")
result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    print("EXE built successfully!")
    exe_path = "dist/SchoolManagement_Existing.exe"
    if os.path.exists(exe_path):
        print("Location:", exe_path)
        print("Size:", os.path.getsize(exe_path), "bytes")
        print("\nThis EXE uses your existing working ui2 directory")
else:
    print("Build failed:")
    print(result.stderr)
