# processor.py
from datetime import timedelta
import csv
import pandas as pd


def time_stats(subscribers):
    complete_times = []
    for subscriber in subscribers:
        for repair in subscriber.repairs:
            complete_times.append(repair.get_complete_time())
    times = pd.Series(data=complete_times)
    print_stats(times.describe())


def recurrence(subscribers):
    stats = {}
    count = 0
    recurrence_period = get_integer('Maximum period between claims')
    for subscriber in subscribers:
        repairs = []
        if len(subscriber.repairs) > 1:
            for index in range(len(subscriber.repairs) - 1):
                current_repair = subscriber.repairs[index]
                current_close_date = current_repair.close_date
                next_repair = subscriber.repairs[index + 1]
                next_open_date = next_repair.open_date
                if current_close_date and (current_close_date + timedelta(days=recurrence_period)) > next_open_date:
                    repairs.append((current_repair, next_repair))
                    count += 1
        if len(repairs) > 0:
            stats[subscriber] = repairs
    write_recurrence_file(stats)
    print_recurrence(count)


def get_integer(message):
    integer = ''
    while not isinstance(integer, int):
        try:
            integer = int(input(f'{message}: '))
        except ValueError:
            print('Integer number must be entered.')
    return integer


def write_recurrence_file(stats):
    with open('recurrence.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Number', 'Repair', 'Open', 'Close'])
        for subscriber, repairs in stats.items():
            writer.writerow([subscriber.number])
            for repair in repairs:
                writer.writerow([None, repair[0].number, repair[0].open_date, repair[0].close_date])
                writer.writerow([None, repair[1].number, repair[1].open_date, repair[1].close_date])


def print_stats(message):
    print('\n', '-' * 35, sep='')
    print('===== REPAIR TIMES STATISTICS =====')
    print(message)
    print('-' * 35)


def print_recurrence(count):
    print('\n', '-' * 32, sep='')
    print('===== RECURRENCE OF CLAIMS =====')
    print(f'It were fond {count} recurrence of clains.')
    print('(recurrence.csv file was saved.)')
    print('-' * 32)
