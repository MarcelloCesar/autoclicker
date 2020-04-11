from pynput.mouse import Controller, Button
import time
import random

class Clicker:

    def __init__(self):
        self.click_list = []
        self.mouse = Controller()


    def load_click_list(self, path="clicklist.json"):
        import json
        with open(path, "r") as file:
            clicklist = json.loads(file.read())
            self.click_list = clicklist


    def loop(self, times=1):
        round = 0
        while round < times:
            print("Starting loop: ", round)
            # clicks
            for x, y, time_to_wait in self.click_list:

                self.wait(time_to_wait)
                posx, posy = self.prepare_position(x, y)
                print("Position: ", posx, posy)
                self.click()
                # after click, sends mouse to another random position
                self.confunde()


            #Time after endloop
            self.wait(7, 1)
            round += 1

    def wait(self, wait_time, max_extra_time=3):
        # add some random extra time to the click so it looks less automatic
        time.sleep(wait_time + random.uniform(0, max_extra_time))


    def prepare_position(self, initial_x, initial_y, max_error_margin=30):

        final_x = random.randrange(initial_x-max_error_margin, initial_x+max_error_margin)
        final_y = random.randrange(initial_y-max_error_margin, initial_y+max_error_margin)

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


    def click(self):
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)


if __name__ == '__main__':
    import sys
    try:
        number_loops, file_to_load = int(sys.argv[1]), sys.argv[2]
        clicker = Clicker()
        clicker.load_click_list(file_to_load)

    except IndexError:
        print("Command utilization: python autoclicker.py NUMBER_OF_LOOPS FILE_WITH_CLICKLIST_CONFIGURATION_RECORDERED")

    except ValueError:
        print("NUMBER_OF_LOOPS must be integer")

    except FileNotFoundError as exc:
        print("Unable to find FILE_WITH_CLICKLIST_CONFIGURATION_RECORDERED. ", exc)

    else:
        clicker.loop(number_loops)

