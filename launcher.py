import os
import sys
import time
import shutil
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox

# -------------------------------------------------
# SINGLE INSTANCE
# -------------------------------------------------

LOCK_FILE = os.path.join(tempfile.gettempdir(), "DashboardLauncher.lock")

if os.path.exists(LOCK_FILE):
    messagebox.showwarning(
        "Launcher",
        "Launcher is already running."
    )
    sys.exit()

open(LOCK_FILE, "w").close()

try:

    # -------------------------------------------------
    # ROOT
    # -------------------------------------------------

    root = tk.Tk()
    root.withdraw()

    # -------------------------------------------------
    # FILE PICKER
    # -------------------------------------------------

    SERVER_FILE = filedialog.askopenfilename(
        title="Select Server Excel / PDF File",
        filetypes=[
            ("Excel Files", "*.xls *.xlsx *.xlsm"),
            ("PDF Files", "*.pdf"),
            ("All Files", "*.*")
        ]
    )

    if not SERVER_FILE:
        sys.exit()

    # -------------------------------------------------
    # LOCAL FOLDER
    # -------------------------------------------------

    LOCAL_FOLDER = os.path.join(
        os.environ["USERPROFILE"],
        "Documents",
        "LauncherFiles"
    )

    os.makedirs(
        LOCAL_FOLDER,
        exist_ok=True
    )

    LOCAL_FILE = os.path.join(
        LOCAL_FOLDER,
        os.path.basename(SERVER_FILE)
    )

    # -------------------------------------------------
    # COPY TO LOCAL
    # -------------------------------------------------

    try:

        shutil.copy2(
            SERVER_FILE,
            LOCAL_FILE
        )

    except Exception as e:

        messagebox.showerror(
            "Copy Failed",
            str(e)
        )

        sys.exit()

    # -------------------------------------------------
    # OPEN FILE
    # -------------------------------------------------

    os.startfile(LOCAL_FILE)

    # -------------------------------------------------
    # WAIT UNTIL USER CLOSES FILE
    # -------------------------------------------------

    while True:

        try:

            with open(LOCAL_FILE, "a"):
                pass

            break

        except PermissionError:

            time.sleep(2)

    # -------------------------------------------------
    # UPLOAD BACK
    # -------------------------------------------------

    RETRY = 30

    for i in range(RETRY):

        try:

            shutil.copy2(
                LOCAL_FILE,
                SERVER_FILE
            )

            messagebox.showinfo(
                "Success",
                "Server file updated successfully."
            )

            break

        except PermissionError:

            time.sleep(2)

        except Exception:

            time.sleep(2)

            if i == RETRY - 1:

                messagebox.showerror(
                    "Upload Failed",
                    "Unable to update the server file."
                )

finally:

    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)
