from pynput.keyboard import Listener
from threading import Thread

class KeyboardController:
    def __init__(self):
        self.listener = Thread(target=self.listen)
        self.listener.start()
        self.key = ''

    def listen(self):
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def on_press(self, key):
        self.key = key.name

    def on_release(self, key):
        pass

    def disconnect(self):
        self.listener.join()

    def get_key_pressed(self):
        key = self.key
        self.key = ''
        return key