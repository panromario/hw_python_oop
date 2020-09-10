import datetime as dt

dateFormat = '%d.%m.%Y'


class Calculator:
    def __init__(self, limit):
        self.records = []
        self.limit = limit

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        records_list = list(filter(lambda r: r.date == dt.datetime.now().date(), self.records))
        return sum(r.amount for r in records_list)

    def get_week_stats(self):
        date_week_start = dt.date.today() - dt.timedelta(days=7)
        records_list = list(
            filter(lambda r: date_week_start <= r.date <= dt.date.today(), self.records))
        return sum(r.amount for r in records_list)


class Record:
    def __init__(self, amount, comment='', date=''):
        self.amount = amount
        self.comment = comment
        self.date = dt.datetime.now().date()

        if date != '':
            try:
                self.date = dt.datetime.strptime(date, dateFormat).date()
            except ValueError:
                print("Incorrect Format date")
                exit()


class CashCalculator(Calculator):
    USD_RATE = 74.86
    EURO_RATE = 89.08

    def get_today_cash_remained(self, currency):
        cash_remained = self.limit - self.get_today_stats()
        result = 'Денег нет, держись'

        if currency == 'usd':
            cash = round(abs(cash_remained) / self.USD_RATE, 2)
            print_cache = f'{cash} USD'
        elif currency == 'eur':
            cash = round(abs(cash_remained) / self.EURO_RATE, 2)
            print_cache = f'{cash} Euro'
        else:
            cash = abs(cash_remained)
            print_cache = f'{cash} руб'

        if cash_remained > 0:
            result = f'На сегодня осталось {print_cache}'
        elif cash_remained < 0:
            result += f': твой долг - {print_cache}'

        return result

    def get_week_stats(self):
        cash = super().get_week_stats()
        return f'За последние 7 дней потрачено {cash} руб'


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        calories_remained = self.limit - self.get_today_stats()

        if calories_remained > 0:
            result = f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {calories_remained} кКал'
        else:
            result = 'Хватит есть!'

        return result

    def get_week_stats(self):
        calories = super().get_week_stats()
        return f'За последние 7 дней получено {calories} калорий'
