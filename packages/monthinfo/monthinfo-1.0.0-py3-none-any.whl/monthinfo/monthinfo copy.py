import datetime
import calendar

WEEK_DAYS = {0: "Monday",
             1: "Tuesday",
             2: "Wednesday",
             3: "Thursday",
             4: "Friday",
             5: "Saturday",
             6: "Sunday"}


class _Saturday():
    def is_saturday(self, day) -> bool:
        return datetime.date(self.year, self.month, day).weekday() == 5

    def is_first_saturday(self, day) -> bool:
        return self.is_first_weekend(day) and self.is_saturday(day)

    def list_of_saturdays(self) -> list:
        return [day for day in self.list_of_days() if self.is_saturday(day)]

    def number_of_saturdays(self) -> int:
        return len(self.list_of_saturdays())


class _Sunday():
    def is_sunday(self, day) -> bool:
        return datetime.date(self.year, self.month, day).weekday() == 6

    def is_first_sunday(self, day) -> bool:
        return self.is_first_weekend(day) and self.is_sunday(day)

    def list_of_sundays(self) -> list:
        return [day for day in self.list_of_days() if self.is_sunday(day)]

    def number_of_sundays(self) -> int:
        return len(self.list_of_sundays())


class _Weekends(_Saturday, _Sunday):
    def is_weekend(self, day) -> bool:
        return datetime.date(self.year, self.month, day).weekday() >= 5

    def is_first_weekend(self, day) -> bool:
        return self.is_weekend(day) and day < 8

    def number_of_weekends(self) -> int:
        if self.number_of_saturdays() >= self.number_of_sundays():
            return self.number_of_saturdays()

        return self.number_of_sundays()


class _Monday():
    def is_monday(self, day) -> bool:
        return datetime.date(self.year, self.month, day).weekday() == 0

    def is_first_monday(self, day) -> bool:
        return self.is_monday(day) and day < 8

    def list_of_mondays(self) -> list:
        return [day for day in self.list_of_days() if self.is_monday(day)]

    def number_of_mondays(self) -> int:
        return len(self.list_of_mondays())


class _Tuesday():
    def is_tuesday(self, day) -> bool:
        return datetime.date(self.year, self.month, day).weekday() == 1

    def is_first_tuesday(self, day) -> bool:
        return self.is_tuesday(day) and day < 8

    def list_of_tuesdays(self) -> list:
        return [day for day in self.list_of_days() if self.is_tuesday(day)]

    def number_of_tuesdays(self) -> int:
        return len(self.list_of_tuesdays())


class _Wednesday():

    def is_wednesday(self, day) -> bool:
        return datetime.date(self.year, self.month, day).weekday() == 2

    def is_first_wednesday(self, day) -> bool:
        return self.is_wednesday(day) and day < 8

    def list_of_wednesdays(self) -> list:
        return [day for day in self.list_of_days() if self.is_wednesday(day)]

    def number_of_wednesdays(self) -> int:
        return len(self.list_of_wednesdays())


class _Thursday():
    def is_thursday(self, day) -> bool:
        return datetime.date(self.year, self.month, day).weekday() == 3

    def is_first_thursday(self, day) -> bool:
        return self.is_thursday(day) and day < 8

    def list_of_thursdays(self) -> list:
        return [day for day in self.list_of_days() if self.is_thursday(day)]

    def number_of_thursdays(self) -> int:
        return len(self.list_of_thursdays())


class _Friday():
    def is_friday(self, day) -> bool:
        return datetime.date(self.year, self.month, day).weekday() == 4

    def is_first_friday(self, day) -> bool:
        return self.is_friday(day) and day < 8

    def list_of_fridays(self) -> list:
        return [day for day in self.list_of_days() if self.is_friday(day)]


class WeekDays(_Monday, _Tuesday, _Wednesday, _Thursday, _Friday):

    def number_of_fridays(self) -> int:
        return len(self.list_of_fridays())

    def number_of_weekdays(self) -> int:
        return self.number_of_days() - (self.number_of_saturdays() + self.number_of_sundays())


class CurrentMonth(_Weekends, WeekDays):

    def __init__(self, month, year, first_week_day=0):
        self.month = month
        self.year = year
        calendar.setfirstweekday(first_week_day)

    def calendar(self):
        return calendar.monthcalendar(self.year, self.month)

    def first_week_day(self) -> str:
        return WEEK_DAYS[datetime.date(self.year, self.month, 1).weekday()]

    def list_of_days(self) -> list:
        return list(range(1, calendar.monthrange(self.year, self.month)[1]+1))

    def list_of_weeks(self) -> list:
        return list(calendar.monthcalendar(self.year, self.month))

    def number_of_weeks(self) -> int:
        return len(calendar.monthcalendar(self.year, self.month))

    def number_of_days(self) -> int:
        return calendar.monthrange(self.year, self.month)[1]

    def get_calendar_indexes_for_this_day(self, day):
        for i, week in enumerate(self.calendar()):
            for j, d in enumerate(week):
                if d == day:
                    return i, j
