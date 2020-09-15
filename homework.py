import datetime as dt

DATE_FORMAT = '%d.%m.%Y'


class Calculator:
    def __init__(self, limit):
        self.records = []
        self.limit = limit

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        records_list = list(filter(lambda r: r.date == dt.date.today(), self.records))
        return sum(r.amount for r in records_list)

    def get_week_stats(self):
        date_week_start = dt.date.today() - dt.timedelta(days=7)
        records_list = list(
            filter(lambda r: date_week_start <= r.date <= dt.date.today(), self.records))
        return sum(r.amount for r in records_list)


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        self.date = dt.date.today()

        if date is not None:
            try:
                self.date = dt.datetime.strptime(date, DATE_FORMAT).date()
            except ValueError:
                print("Incorrect Format date")
                exit()


class CashCalculator(Calculator):
    USD_RATE = 74.86
    EURO_RATE = 89.08
    RUB_RATE = 1

    def get_today_cash_remained(self, currency):
        cash_remained = self.limit - self.get_today_stats()
        result = 'Денег нет, держись'

        currencies = {
            'eur': ('Euro', self.EURO_RATE),
            'usd': ('USD', self.USD_RATE),
            'rub': ('руб', self.RUB_RATE),
        }

        if currency not in currencies:
            try:
                raise ValueError("Currency not found")
            except ValueError as e:
                print(e)
                exit()

        currency_name, currency_rate = currencies[currency]

        if currency_rate == 1:
            result_cache = abs(cash_remained)
        else:
            result_cache = round(abs(cash_remained) / currency_rate, 2)

        if cash_remained > 0:
            result = f'На сегодня осталось {result_cache} {currency_name}'
        elif cash_remained < 0:
            result += f': твой долг - {result_cache} {currency_name}'

        return result


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        calories_remained = self.limit - self.get_today_stats()

        if calories_remained > 0:
            result = f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {calories_remained} кКал'
        else:
            result = 'Хватит есть!'

        return result
