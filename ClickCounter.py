import keyboard
from pynput.mouse import Listener
import time

# Initialize a counter and a timer
counter = 0
start_time = None
end_time = None

# Define a callback function to handle mouse clicks
def on_click(x, y, button, pressed):
    global counter, start_time
    if button == button.left and pressed:
        counter += 1
        print("Clicked: {}".format(counter))
        if start_time is None:
            start_time = time.time()

# Define a function to toggle the mouse listener and timer
def toggle_listener():
    global listener, start_time, end_time, counter
    if listener is None:
        listener = Listener(on_click=on_click)
        listener.start()
        start_time = time.time()
        counter = 0
        print("Listener started")
    else:
        listener.stop()
        listener = None
        end_time = time.time()
        print("Listener stopped")

        #Write time as both minutes and seconds
        elapsed_time = end_time - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        print("Elapsed time: {:02d}:{:02d}".format(minutes, seconds))

        # Write total clicks and elapsed time to a text file
        with open("clicks.txt", "a") as file:
            file.write("Total clicks: {}\n".format(counter))
            file.write("Elapsed time: {:.2f} seconds\n".format(end_time - start_time))
            file.write("-" * 20 + "\n")

# Initialize the mouse listener to None
listener = None

# Set up a hotkey to toggle the mouse listener and timer
keyboard.add_hotkey("~", toggle_listener)

# Keep the main thread running to listen for hotkeys
keyboard.wait()
