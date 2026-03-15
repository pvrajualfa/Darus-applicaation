# Create a working single file manually
import shutil

# Copy the original file
shutil.copy("Darus_complete_single.py", "Darus_working_single.py")

# Read the file
with open("Darus_working_single.py", "r") as f:
    lines = f.readlines()

# Find the database.py string and fix it
fixed_lines = []
inside_database = False
database_start = None
database_end = None

for i, line in enumerate(lines):
    if '"database.py": ''' in line:
        inside_database = True
        database_start = i
        fixed_lines.append(line)
    elif inside_database and line.strip() == "''',":
        database_end = i
        fixed_lines.append(line)
        inside_database = False
    elif inside_database:
        fixed_lines.append(line)
    else:
        fixed_lines.append(line)

# Write the fixed file
with open("Darus_working_single_fixed.py", "w") as f:
    f.writelines(fixed_lines)

print("Created working single file")

# Now build the EXE
import subprocess
import os

cmd = [
    "pyinstaller",
    "--onefile",
    "--name=SchoolManagement_Final",
    "--hidden-import=sqlite3",
    "--clean",
    "Darus_working_single_fixed.py"
]

print("Building final EXE...")
result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    print("EXE built successfully!")
    print("Location: dist/SchoolManagement_Final.exe")
    if os.path.exists("dist/SchoolManagement_Final.exe"):
        print("Size:", os.path.getsize("dist/SchoolManagement_Final.exe"), "bytes")
else:
    print("Build failed:")
    print(result.stderr)
