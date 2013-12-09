import csv
import datetime

class Fund(object):

    def __init__(self, id_, name):
        self.id = id_
        self.name = name


class Department(object):

    def __init__(self, id_, name):
        self.id = id_
        self.name = name

class CSVData(object):
    DEPT_ID_KEY = "Department ID"
    DEPT_NAME_KEY = "Department Name"
    FUND_NAME_KEY = "Fund Name"
    FUND_ID_KEY = "Fund ID"
    MONTH_KEY = "Month"
    YEAR_KEY = "Year"
    AMOUNT_KEY = "Amount"
    TRANSACTION_NAME_KEY = "Object Name"

    def __init__(self, dict_list):
        self.list = dict_list

    def get_transactions(self):
        return [self.get_transaction(e) for e in self.list]

    def is_entry_empty(self, entry):
        empty = True
        for prop in entry:
            if prop != '':
                empty = False
        return empty


    def get_transaction(self, entry):
        fund = Fund(id_=(entry.get(self.FUND_ID_KEY)), name=entry.get(self.FUND_NAME_KEY))
        dept = Department(id_=entry.get(self.DEPT_ID_KEY), name=entry.get(self.DEPT_NAME_KEY))
        month = entry.get(self.MONTH_KEY)
        if not month:
            month = 0
        else:
            month = int(month)
        year = entry.get(self.YEAR_KEY)
        if not year:
            return None
        else:
            year = int(year)
        date = datetime.date(year=year, month=month, day=1)
        transaction = Transaction(
            name=entry.get(self.TRANSACTION_NAME_KEY),
            date=date,
            amount=float(entry.get(self.AMOUNT_KEY)),
            fund=fund,
            dept=dept
        )
        return transaction


class Transaction(object):
    def __init__(self, name, fund, dept, date, amount):
        self.name = name
        self.fund = fund
        self.dept = dept
        self.date = date
        self.amount = amount

    @classmethod
    def from_csv_file(cls, file):
        r = csv.DictReader(file.read().splitlines())
        return CSVData(r).get_transactions()

    @classmethod
    def transaction_report(cls, ts):
        rows_parsed = [t.flatten() for t in ts if t is not None]
        aggregations = cls.get_aggregations(ts)
        return {
            'rows_parsed': rows_parsed,
            'aggregations': aggregations
        }

    @classmethod
    def get_aggregations(cls, ts):
        years = {}
        for t in ts:
            if t is None:
                continue
            if t.amount > 0:
                amount_type = "revenues"
            else:
                amount_type = "expenses"
            cls.add_to_aggregation(years, [t.date.year, amount_type, "funds", t.fund.name], t.amount)
            cls.add_to_aggregation(years, [t.date.year, amount_type, "departments", t.dept.name], t.amount)
            cls.add_to_aggregation(years, [t.date.year, amount_type, "total"], t.amount)
        return years


    @classmethod
    def add_to_aggregation(cls, d, props, value):
        prop = props.pop(0)
        intermediate = d.get(prop, 0)
        if not props:
            d[prop] = intermediate+value
            return
        if not intermediate:
            d[prop] = {}
        return cls.add_to_aggregation(d[prop], props, value)

    def flatten(self):
        return [
            self.date.year,
            self.date.month,
            self.fund.id,
            self.dept.id,
            self.fund.name,
            self.dept.name,
            self.name,
            self.amount
        ]



