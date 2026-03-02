import time
import json
import random

# This will eventually read from your Shared Folder with GNS3
LOG_FILE_PATH = "C:\\Mirage_Logs\\attacks.log" 

print("[*] NetLure bait Active. Waiting for GNS3 data...")

def tail_f(file):
    file.seek(0, 2) # Go to the end of the file
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

# For now, just a placeholder
while True:
    time.sleep(1)
    # We will add the websocket logic here later