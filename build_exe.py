"""
Script to build standalone LeafTimer.exe executable using PyInstaller.
"""

import os
import subprocess
import sys
import customtkinter

def build():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_dir, "assets")
    ico_path = os.path.join(assets_dir, "app_icon.ico")
    
    # CustomTkinter assets directory
    ctk_dir = os.path.dirname(customtkinter.__file__)

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onefile",
        "--name", "LeafTimer",
        f"--icon={ico_path}",
        f"--add-data={assets_dir};assets",
        f"--add-data={ctk_dir};customtkinter",
        "--clean",
        os.path.join(base_dir, "main.py")
    ]

    print("Building standalone executable...")
    print("Running command:", " ".join(cmd))
    res = subprocess.run(cmd, cwd=base_dir)
    if res.returncode == 0:
        exe_path = os.path.join(base_dir, "dist", "LeafTimer.exe")
        print("\n=======================================================")
        print(f" Build Successful!")
        print(f" Standalone Executable created at:\n {exe_path}")
        print("=======================================================\n")
    else:
        print(f"Build failed with exit code {res.returncode}")

if __name__ == "__main__":
    build()
