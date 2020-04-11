import win32api, keyboard
from pynput import mouse
import time


class Recorder:

    def __init__(self):
        self.click_list = []
        self.last_time_registered = time.time()


    def listen(self):
        listener = mouse.Listener(
           # on_move=self.mouse_move,
            on_click=self.mouse_click,
            #on_scroll=self.mouse_scroll
        )
        listener.start()

        while keyboard.read_key() != 'f4':
            pass


    def mouse_move(self, x, y):
        print("Andou para: ", x , y)


    def mouse_click(self, x, y, button, pressed):
        if pressed:
            previous_time = self.last_time_registered
            self.last_time_registered = time.time()
            time_passed = (self.last_time_registered - previous_time)

            print("click at: ", x, y)
            self.click_list.append([x, y, time_passed])


    def save_click_list(self):
        import json
        with open("clicklist.json", "w") as file:
            file.write(json.dumps(self.click_list))


if __name__ == '__main__':
    recorder = Recorder()
    recorder.listen()
    recorder.save_click_list()