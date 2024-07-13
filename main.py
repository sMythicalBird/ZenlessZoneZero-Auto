from threading import Thread
from pynput.keyboard import Key, Listener
from utils.task import task
from handle import *


def key_event():
    def on_press(key):
        if key == Key.f12:
            task.stop()
            return False
        if key == Key.f11:
            task.pause()
        if key == Key.f10:
            task.restart()
        return None

    with Listener(on_press=on_press) as listener:
        listener.join()


key_thread = Thread(target=key_event)
key_thread.start()


if __name__ == "__main__":
    task.run()
