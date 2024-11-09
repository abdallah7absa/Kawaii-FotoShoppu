import sys
import time
import subprocess
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, restart_callback):
        super().__init__()
        self.restart_callback = restart_callback

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f'{event.src_path} has been modified. Restarting app...')
            self.restart_callback()

class AppReloader:
    def __init__(self):
        self.process = None

    def start_app(self):
        if self.process:
            self.process.kill()
        self.process = subprocess.Popen([sys.executable, 'splash.py'])

    def stop_app(self):
        if self.process:
            self.process.kill()

    def restart_app(self):
        print("Restarting application...")
        self.stop_app()
        self.start_app()

def main():
    reloader = AppReloader()
    reloader.start_app()

    event_handler = FileChangeHandler(reloader.restart_app)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
    reloader.stop_app()

if __name__ == '__main__':
    main()
