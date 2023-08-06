import datetime as dt
import calendar


def str_to_date(date_str: str, _format='%Y%m%d'):
    return dt.datetime.strptime(date_str, _format)


def date_to_str(date: dt.date, _format='%Y%m%d'):
    return date.strftime(_format)


def date_move(date_str: str, num: int):
    return date_to_str(str_to_date(date_str) + dt.timedelta(days=num))


def year_first(year: 'str|int'):
    return str(year) + '0101'


def year_end(year: 'str|int'):
    return str(year) + '1231'


def month_first(year: 'str|int', month: 'str|int'):
    return str(year) + str(month).zfill(2) + '01'


def month_end(year: 'str|int', month: 'str|int'):
    end = calendar.monthrange(int(year), int(month))[1]
    return str(year) + str(month) + str(end)
