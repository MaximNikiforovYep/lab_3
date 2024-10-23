from customexceptions import InvalidInputException
from datetime import datetime

# класс для записи сна
class SleepEntry:
    def __init__(self, date, start_time, end_time, comment=""):
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.comment = comment
        self.duration = self.calculate_duration()

    def calculate_duration(self):
        fmt = '%H:%M'
        try:
            tdelta = datetime.strptime(self.end_time, fmt) - datetime.strptime(self.start_time, fmt)
            return tdelta.seconds / 3600  # в часах
        except ValueError:
            raise InvalidInputException("Некорректный формат времени")

