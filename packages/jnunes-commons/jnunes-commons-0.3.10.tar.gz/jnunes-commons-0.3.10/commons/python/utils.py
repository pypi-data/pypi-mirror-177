import locale
from datetime import date, datetime


class Format:
    @staticmethod
    def decimal(val, decimal_places):
        """
        Format decimal values
        :param val: number
        :param decimal_places: number of decimal places
        :return: number
        """
        if isinstance(val, (int, float)):
            return round(val, decimal_places)
        return 0

    @staticmethod
    def price(val):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        return locale.currency(val, grouping=True, symbol=True)

    @staticmethod
    def date(date_value: date):
        return date_value.strftime('%d/%m/%Y')

    @staticmethod
    def date_time(date_time: datetime):
        return date_time.strftime('%d/%m/%Y %H:%M')

    @staticmethod
    def date_time_integer(date_time: datetime):
        return date_time.strftime('%Y%m%d%H%M%S')


class Help:
    @staticmethod
    def is_ajax(request) -> bool:
        try:
            return request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        except Exception as e:
            raise RuntimeError(e)

    @staticmethod
    def is_delete_method(request) -> bool:
        try:
            return request.method == 'DELETE'
        except Exception as e:
            raise RuntimeError(e)

    @staticmethod
    def is_post_method(request) -> bool:
        try:
            return request.method == 'POST'
        except Exception:
            raise RuntimeError

    @staticmethod
    def to_date(day, month, year):
        try:
            return date(day=int(day), month=int(month), year=int(year))
        except Exception as error:
            raise RuntimeError(error)


class Utils:
    @staticmethod
    def datetime_now_integer():
        return Format.date_time_integer(datetime.now())
