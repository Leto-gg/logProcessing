from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import csv
import shutil

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Check if it's a .csv file
        if event.src_path.endswith('.csv'):
            if self.is_file_ready(event.src_path):
                # Construct the destination path using absolute paths
                filename = os.path.basename(event.src_path)
                dest_path = os.path.join('/home/major-shepard/Documents/logProcessing/logSend', filename)
                shutil.move(event.src_path, dest_path)
                print(f"Moved '{event.src_path}' to '{dest_path}'")

    def is_file_ready(self, file_path):
        try:
            with open(file_path, newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    # Check if the row has exactly 3 fields and none are empty
                    if len(row) != 3 or not all(row):
                        return False
                return True
        except Exception as e:
            print(f"Error checking file: {e}")
            return False

log_reports_path = '/home/major-shepard/Documents/logProcessing/logReports'  # Absolute path to logReports
observer = Observer()
event_handler = MyHandler()
observer.schedule(event_handler, path=log_reports_path, recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
