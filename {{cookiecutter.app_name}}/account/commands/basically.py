import os
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent.parent


def get_active_directories():
    app_dirs = []
    dirs = os.popen(f"ls -d */").read()
    dirs = [dir.replace("/", "") for dir in dirs.split("\n") if dir]
    for dir in dirs:
        files = os.popen(f"ls {PROJECT_DIR}/{dir}").read()
        files = [file for file in files.split("\n") if files]
        if 'models.py' in files:
            app_dirs.append(dir)
    return app_dirs


def get_files(dir):
    dirs = os.popen(f"ls {dir}").read()
    dirs = [dir.replace("/", "") for dir in dirs.split("\n") if dir]
    return dirs
