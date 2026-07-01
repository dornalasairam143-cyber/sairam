import os
import shutil
import subprocess
import time
import tkinter as tk
from tkinter import filedialog

# Hide tkinter window
root = tk.Tk()
root.withdraw()

print("Select the Excel or PDF file from the server.")

SERVER_FILE = filedialog.askopenfilename(
    title="Select Server File",
    filetypes=[
        ("Excel Files", "*.xls *.xlsx *.xlsm"),
        ("PDF Files", "*.pdf"),
        ("All Files", "*.*")
    ]
)

if SERVER_FILE == "":
    print("No file selected.")
    input("Press Enter to exit...")
    raise SystemExit

LOCAL_FOLDER = os.path.join(os.environ["USERPROFILE"], "Documents", "LauncherFiles")
os.makedirs(LOCAL_FOLDER, exist_ok=True)

LOCAL_FILE = os.path.join(
    LOCAL_FOLDER,
    os.path.basename(SERVER_FILE)
)

print("Copying file to local PC...")
shutil.copy2(SERVER_FILE, LOCAL_FILE)

print("Opening file...")

os.startfile(LOCAL_FILE)

print("Waiting for you to close the file...")

while True:
    try:
        os.rename(LOCAL_FILE, LOCAL_FILE)
        break
    except PermissionError:
        time.sleep(2)

print("Uploading file back to server...")

shutil.copy2(LOCAL_FILE, SERVER_FILE)

print("Done!")

input("Press Enter to exit...")
