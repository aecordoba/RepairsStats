#!/usr/bin/python3
# main.py
""" Derqui repairs statistics app. """
from datetime import datetime
from subscribersmanager import SubscribersManager
from processor import time_stats, repairs_stats, recurrence, claims_per_subscriber


menu_options = {
    1: ('Repair times statistics', time_stats),
    2: ('Repairs quantity statistics', repairs_stats),
    3: ('Recurrence of claims', recurrence),
    4: ('Claims per subscribers', claims_per_subscriber),
    0: ('Exit', None)
}


def main():
    menu_option = get_menu_option()
    while menu_option[1] is not None:
        start_date = get_date('Start date')
        end_date = get_date('End date')
        subscribers_manager = SubscribersManager(start_date, end_date)
        subscribers = subscribers_manager.subscribers
        menu_option[1](subscribers)

        menu_option = get_menu_option()


def get_menu_option():
    option = -1
    while option not in menu_options.keys():
        print('\n====== MENU OPTIONS ======\n')
        for index, value in menu_options.items():
            print(f'{index}- {value[0]}')
        try:
            option = int(input('\nYour option: '))
        except ValueError:
            print('Invalid option! (Integer number must be entered.)')
        else:
            if option not in menu_options.keys():
                print('Invalid option! (Menu item number must be entered.)')
    return menu_options[option]


def get_date(message):
    date = '-'
    while date == '-':
        try:
            date = datetime.strptime(input(f'{message} (YYYY-mm-dd): '), '%Y-%m-%d')
        except ValueError:
            print('Invalid date format!')
    return date


if __name__ == '__main__':
    main()
