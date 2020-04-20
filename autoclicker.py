from pynput.mouse import Controller, Button
import time
import random
import json

class Clicker:

    def __init__(self, max_error_margin=30, loop_delay=7):
        self.click_list = []
        self.mouse = Controller()
        self.max_error_margin = max_error_margin
        self.loop_delay = loop_delay


    def load_click_list(self, path="clicklist.json"):
        with open(path, "r") as file:
            clicklist = json.loads(file.read())
            self.click_list = clicklist


    def loop(self, times=1):
        round = 0
        while round < times:
            print("Starting loop: ", round)
            # clicks
            for click in self.click_list:

                self.wait(click["time_to_wait"])
                posx, posy = self.prepare_position(click["x"], click["y"])
                print("Position: ", posx, posy)
                self.click(click["type"])
                # after click, sends mouse to another random position
                self.confunde()


            #Time after endloop
            self.wait(self.loop_delay, 1)
            round += 1

    def wait(self, wait_time, max_extra_time=3):
        # add some random extra time to the click so it looks less automatic
        time.sleep(wait_time + random.uniform(0, max_extra_time))


    def prepare_position(self, initial_x, initial_y):
        final_x = random.randrange(initial_x-self.max_error_margin, initial_x+self.max_error_margin)
        final_y = random.randrange(initial_y-self.max_error_margin, initial_y+self.max_error_margin)

        self.smooth_moviment(final_x, final_y)

        # move the mouse
        self.mouse.position = (final_x, final_y)

        return final_x, final_y


    def smooth_moviment(self, final_x, final_y):
        #get current position of mouse
        actual_x = self.mouse.position[0]
        actual_y = self.mouse.position[1]

        # calculates a route to move the mouse
        path_x = list(range(actual_x, final_x, 1 if actual_x < final_x else -1))
        path_y = list(range(actual_y, final_y, 1 if actual_y < final_y else -1))

        # get the minimum route
        min_route = max(len(path_x), len(path_y))

        # makes path x and y have the same lengh
        path_x = [actual_x for i in range(min_route-len(path_x))] + path_x
        path_y = [actual_y for i in range(min_route-len(path_y))] + path_y

        # moves the mouse smothly
        for position in range(min_route):

            self.mouse.position = (path_x[position], path_y[position])
            self.confunde(8)


    def confunde(self, deep=1000):
        for i in range(deep):
            self.mouse.move(random.randrange(-1, 2), random.randrange(-1, 2))


    def click(self, left_click=True):
        button = Button.left if left_click else Button.right
        self.mouse.press(button)
        self.mouse.release(button)


if __name__ == '__main__':

    # loads config file
    with open("config.json", "r") as file:
        configuration = json.loads(file.read())

    clicker = Clicker(configuration["max_error_margin"], configuration['loop_delay'])
    clicker.load_click_list(configuration["click_list_file"])
    clicker.loop(configuration["number_of_loops"])

