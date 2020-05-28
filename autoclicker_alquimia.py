from autoclicker import Clicker
import json
import random

if __name__ == '__main__':
    # loads config file
    with open("./config/config_alquimia.json", "r") as file:
        configuration = json.loads(file.read())
    
    clicker = Clicker(configuration["max_error_margin"], configuration['loop_delay'])
    clicker.load_click_list(configuration["click_list_file"])
    clicker.loop(configuration["number_of_loops"])