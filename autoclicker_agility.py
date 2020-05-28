from autoclicker import Clicker
import json
import random

if __name__ == '__main__':
    # loads config file
    with open("./config/config_agility.json", "r") as file:
        configuration = json.loads(file.read())

    #for i in range(configuration["number_of_loops"]):
    clicker = Clicker(configuration["max_error_margin"], configuration['loop_delay'])
    clicker.load_click_list(configuration["click_list_file"])
    clicker.loop(configuration["number_of_loops"])

    #    clicker_bank = Clicker(3, 2)
    #    clicker_bank.load_click_list("./clicklists/clicklist_agility_bank.json")
    #    clicker_bank.loop(1)