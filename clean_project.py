# Clean Project Structure Organizer
import os
import shutil

def clean_project():
    print("Cleaning up project structure...")
    
    # Define clean structure
    clean_structure = {
        "D:/Newapp_Clean/": {
            "src/": {
                "ui2/": "Keep only essential files",
                "main.py": "Main entry point",
                "run_in_pycharm.py": "PyCharm runner"
            },
            "dist/": "Built executables",
            "docs/": {
                "DEPLOYMENT_GUIDE.txt": "Deployment instructions",
                "EXE_INSTRUCTIONS.txt": "EXE running guide"
            },
            "backup/": "Backup old files",
            "assets/": "Images, fonts, icons",
            "data/": "Database and data files"
        }
    }
    
    # Create clean directory
    if os.path.exists("D:/Newapp_Clean"):
        shutil.rmtree("D:/Newapp_Clean")
    
    os.makedirs("D:/Newapp_Clean", exist_ok=True)
    
    # Copy essential files
    essential_files = [
        "ui2/__init__.py",
        "ui2/header.py", 
        "ui2/database.py",
        "ui2/common_form.py",
        "ui2/common_table.py",
        "ui2/mainwindow.py",
        "ui2/vouchers.py",
        "ui2/student_list.py", 
        "ui2/student_registration.py",
        "ui2/reports.py",
        "ui2/heads.py",
        "ui2/data/",
        "ui2/assets/",
        "ui2/fonts/",
        "ui2/icons/",
        "main.py",
        "run_in_pycharm.py",
        "DEPLOYMENT_GUIDE.txt",
        "EXE_INSTRUCTIONS.txt"
    ]
    
    # Create directories
    os.makedirs("D:/Newapp_Clean/src/ui2", exist_ok=True)
    os.makedirs("D:/Newapp_Clean/dist", exist_ok=True)
    os.makedirs("D:/Newapp_Clean/docs", exist_ok=True)
    os.makedirs("D:/Newapp_Clean/backup", exist_ok=True)
    os.makedirs("D:/Newapp_Clean/assets", exist_ok=True)
    os.makedirs("D:/Newapp_Clean/data", exist_ok=True)
    
    # Copy essential files
    for file_path in essential_files:
        src = f"D:/Newapp/{file_path}"
        dst = f"D:/Newapp_Clean/src/{file_path}"
        
        if os.path.isfile(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            print(f"Copied: {file_path}")
        elif os.path.isdir(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"Copied folder: {file_path}")
    
    # Copy best EXE files
    exe_files = [
        "dist/SchoolManagement_WithSidebar.exe",
        "dist/SchoolManagement_FinalWorking.exe"
    ]
    
    for exe in exe_files:
        if os.path.exists(f"D:/Newapp/{exe}"):
            shutil.copy2(f"D:/Newapp/{exe}", f"D:/Newapp_Clean/dist/{os.path.basename(exe)}")
            print(f"Copied EXE: {os.path.basename(exe)}")
    
    # Copy documentation
    docs = ["DEPLOYMENT_GUIDE.txt", "EXE_INSTRUCTIONS.txt"]
    for doc in docs:
        if os.path.exists(f"D:/Newapp/{doc}"):
            shutil.copy2(f"D:/Newapp/{doc}", f"D:/Newapp_Clean/docs/{doc}")
            print(f"Copied doc: {doc}")
    
    print("\nClean project created at: D:/Newapp_Clean")
    print("\nNew Structure:")
    print("D:/Newapp_Clean/")
    print("├── src/")
    print("│   ├── ui2/           # All UI modules")
    print("│   ├── main.py         # Entry point")
    print("│   └── run_in_pycharm.py # PyCharm runner")
    print("├── dist/              # Executables")
    print("├── docs/              # Documentation")
    print("├── backup/            # Old files backup")
    print("├── assets/            # Images, fonts")
    print("└── data/              # Database files")

if __name__ == "__main__":
    clean_project()
