import datetime
import calendar


class Month():
    def __init__(self, month, year):
        self.month = month
        self.year = year

    def number_of_weeks(self) -> int:
        return calendar.monthrange(self.year, self.month)[1]
