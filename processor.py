# processor.py
from datetime import timedelta
import csv
import pandas as pd


def time_stats(subscribers):
	complete_times = []
	for subscriber in subscribers:
		for repair in subscriber.repairs:
			complete_times.append(repair.get_complete_time())
	pd.set_option('precision', 2)
	times_series = pd.Series(data=complete_times)
	print_stats('REPAIR TIMES STATISTICS (days)', times_series.describe())


def claims_stats(subscribers):
	repairs = []
	for subscriber in subscribers:
		repairs.append(len(subscriber.repairs))
	pd.set_option('precision', 2)
	repairs_series = pd.Series(data=repairs)
	print_stats('CLAIMS QUANTITY STATISTICS', repairs_series.describe())


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


def claims_per_subscriber(subscribers):
	claims = {}
	for subscriber in subscribers:
		repairs = len(subscriber.repairs)
		if repairs not in claims:
			claims[repairs] = [subscriber.number]
		else:
			claims[repairs] += [subscriber.number]
	claims_series = pd.Series(claims)
	print_claims(claims_series.apply(lambda x: len(x)))


def get_integer(message):
	integer = ''
	while not isinstance(integer, int):
		try:
			integer = int(input(f'{message}: '))
		except ValueError:
			print('Integer number must be entered.')
	return integer


def print_stats(title, content):
	print('\n', '-' * (len(title) + 12), sep='')
	print(f'===== {title} =====')
	print(content)
	print('-' * (len(title) + 12))


def print_claims(claims):
	print('\n', '-' * 34, sep='')
	print(f'===== CLAIMS PER SUBSCRIBERS =====')
	print(f'{"CLAIMS":>8}{"SUBSCRIBERS":>12}')
	for index, value in claims.items():
		print(f'{index:>8}{value:>12}')
	print('-' * 34)


def write_recurrence_file(stats):
	with open('recurrence.csv', mode='w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(['Number', 'Repair', 'Open', 'Close'])
		for subscriber, repairs in stats.items():
			writer.writerow([subscriber.number])
			for repair in repairs:
				writer.writerow([None, repair[0].number, repair[0].open_date, repair[0].close_date])
				writer.writerow([None, repair[1].number, repair[1].open_date, repair[1].close_date])


def print_recurrence(count):
	print('\n', '-' * 32, sep='')
	print('===== RECURRENCE OF CLAIMS =====')
	print(f'It were found {count} recurrence of claims.')
	print('(recurrence.csv file was saved.)')
	print('-' * 32)
