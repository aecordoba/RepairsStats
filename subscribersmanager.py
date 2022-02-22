# subscribersmanager.py
from databasemanager import DatabaseManager


class SubscribersManager:
    """ Subscribers manager. """

    def __init__(self, start_date, end_date):
        self._subscribers = []
        self._database_manager = DatabaseManager()
        self._query = f'SELECT orden_de_servicio, numero_de_abonado, fecha_de_solicitud, fecha_de_cumplido FROM ' \
                      f'ord_servicio WHERE fecha_de_solicitud >= "{start_date}" AND fecha_de_solicitud <= ' \
                      f'"{end_date}" ORDER BY numero_de_abonado, orden_de_servicio; '
        dataset = self._database_manager.get_dataset(self._query)
        for row in dataset:
            subs = self._get_subscriber(row[1])
            if subs is None:
                subs = Subscriber(row[1])
                self._subscribers.append(subs)
            subs.add_repair(Repair(row[0], row[2], row[3]))

    def _get_subscriber(self, number):
        for subscriber in self._subscribers:
            if subscriber.number == number:
                return subscriber

    @property
    def subscribers(self):
        return self._subscribers


class Subscriber:
    """ Hold subscriber data. """

    def __init__(self, number):
        self._number = number
        self._repairs = []

    @property
    def number(self):
        return self._number

    @property
    def repairs(self):
        return self._repairs

    @number.setter
    def number(self, number):
        self._number = number

    def __repr__(self):
        return f'Number: {self._number} \trepairs: {len(self._repairs)}'

    def __str__(self):
        return f'Number: {self._number} \trepairs: {len(self._repairs)}'

    def add_repair(self, repair):
        self._repairs.append(repair)


class Repair:
    """ Hold repair data."""

    def __init__(self, number, open_date, close_date):
        self._number = number
        self._open_date = open_date
        self._close_date = close_date

    @property
    def number(self):
        return self._number

    @property
    def open_date(self):
        return self._open_date

    @property
    def close_date(self):
        return self._close_date

    def __repr__(self):
        return f'Repair number: {self._number} \tOpen: {self._open_date} \tClosed: {self._close_date}'

    def __str__(self):
        return f'Repair number: {self._number} \tOpen: {self._open_date} \tClosed: {self._close_date}'

    def get_complete_time(self):
        complete_time = None
        if self._close_date is not None:
            complete_time = (self._close_date - self._open_date).days
        return complete_time
