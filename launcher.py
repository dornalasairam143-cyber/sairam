import os
import shutil
import time
import tkinter as tk
from tkinter import filedialog, messagebox

# ------------------------
# Select Server File
# ------------------------

root = tk.Tk()
root.withdraw()

SERVER_FILE = filedialog.askopenfilename(
    title="Select Server Excel/PDF File",
    filetypes=[
        ("Excel Files", "*.xls *.xlsx *.xlsm"),
        ("PDF Files", "*.pdf"),
        ("All Files", "*.*")
    ]
)

if not SERVER_FILE:
    raise SystemExit

# ------------------------
# Local Folder
# ------------------------

LOCAL_FOLDER = os.path.join(
    os.environ["USERPROFILE"],
    "Documents",
    "LauncherFiles"
)

os.makedirs(LOCAL_FOLDER, exist_ok=True)

LOCAL_FILE = os.path.join(
    LOCAL_FOLDER,
    os.path.basename(SERVER_FILE)
)

# ------------------------
# Copy to Local
# ------------------------

try:
    shutil.copy2(SERVER_FILE, LOCAL_FILE)
except Exception as e:
    messagebox.showerror(
        "Copy Error",
        str(e)
    )
    raise SystemExit

# ------------------------
# Open File
# ------------------------

os.startfile(LOCAL_FILE)

messagebox.showinfo(
    "Launcher",
    "Edit the file.\n\nSave it.\n\nClose Excel.\n\nThe launcher will automatically upload it back to the server."
)

# ------------------------
# Wait until file released
# ------------------------

while True:

    try:
        with open(LOCAL_FILE, "a"):
            pass
        break

    except PermissionError:
        time.sleep(2)

# ------------------------
# Upload Back
# ------------------------

MAX_RETRY = 10

for i in range(MAX_RETRY):

    try:

        shutil.copy2(
            LOCAL_FILE,
            SERVER_FILE
        )

        messagebox.showinfo(
            "Success",
            "Server file updated successfully."
        )

        raise SystemExit

    except PermissionError:

        time.sleep(2)

    except Exception as e:

        if i == MAX_RETRY - 1:

            messagebox.showerror(
                "Upload Failed",
                str(e)
            )

            raise SystemExit

        time.sleep(2)
