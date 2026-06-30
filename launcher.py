import os
import shutil
import subprocess
import time

SERVER_FILE = r"Z:\Projects\Dashboard.xlsm"
LOCAL_FOLDER = os.path.join(os.environ["USERPROFILE"], "Documents", "Dashboard")
LOCAL_FILE = os.path.join(LOCAL_FOLDER, "Dashboard.xlsm")

os.makedirs(LOCAL_FOLDER, exist_ok=True)

print("Copying file...")

shutil.copy2(SERVER_FILE, LOCAL_FILE)

print("Opening Excel...")

process = subprocess.Popen(["start", "", LOCAL_FILE], shell=True)

input("After closing Excel, press Enter to continue...")

print("Uploading file back to server...")

shutil.copy2(LOCAL_FILE, SERVER_FILE)

print("Done!")
