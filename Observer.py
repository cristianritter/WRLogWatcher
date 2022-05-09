from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time

class FSObserver:
    """Monitora o sistema de arquivos por modificações em quaisquer arquivos ou pastas"""

    def __init__(self, path="." ) -> None:
        patterns = ["*"]
        ignore_patterns = None
        ignore_directories = False
        case_sensitive = True
        go_recursively = True

        my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
        my_event_handler.on_created = self.on_created
        my_event_handler.on_deleted = self.on_deleted
        my_event_handler.on_modified = self.on_modified
        my_event_handler.on_moved = self.on_moved

        my_observer = Observer()
        my_observer.schedule(my_event_handler, path, recursive=go_recursively)

        my_observer.start()
        try:
            pass
        except KeyboardInterrupt:
            my_observer.stop()
            my_observer.join()
    
    def on_created(self, event):
        self.on_any_event(event)
        print(f"hey, {event.src_path} has been created!")
    
    def on_deleted(self, event):
        self.on_any_event(event)
        print(f"what the f**k! Someone deleted {event.src_path}!")
    
    def on_modified(self, event):
        self.on_any_event(event)
        print(f"hey buddy, {event.src_path} has been modified")
    
    def on_moved(self, event):
        self.on_any_event(event)
        print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")

    def on_any_event(self, event):
        print('oi')
        pass

if __name__ == "__main__":
    def on(event):
        print (event)
    teste = FSObserver()
    teste.on_any_event = on
    while True:
        time.sleep(1)




