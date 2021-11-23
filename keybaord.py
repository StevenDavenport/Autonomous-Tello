from pynput.keyboard import Listener
from threading import Thread

class KeyboardController:
    '''
    Class creates Listeners for keyboard input on
    a separate thread.
    '''
    def __init__(self):
        self.listener = Thread(target=self.listen) # Create a new thread
        self.listener.start()                      # Start the thread
        self.key = ''                              # Initialize key to empty string

    def listen(self):
        '''
        Target of the listener thread.
        listens for keyboard input. (event listeber)
        '''
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def on_press(self, key):
        '''
        Sets the key variable to the key pressed.
        '''
        self.key = key.name

    def on_release(self, key):
        pass

    def disconnect(self):
        ''' 
        Stops the listener thread.
        '''
        self.listener.join()

    def get_key_pressed(self):
        ''' 
        Returns the last Pressed key.
        '''
        key = self.key
        self.key = ''
        return key