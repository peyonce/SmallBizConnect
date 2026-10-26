import csv
import json
import os
from datetime import datetime, date, timedelta

DATA_FILE = os.path.join(os.path.dirname(__file__), "business_data.json")
CSV_FILE  = os.path.join(os.path.dirname(__file__), "transactions.csv")

class BusinessData:
    def __init__(self):
        self.transactions = []
        self.load()

    def add_sale(self, amount):
        if amount <= 0: raise ValueError("Sale amount must be greater than zero.")
        self._add_transaction("sale", amount)

    def add_expense(self, amount):
        if amount <= 0: raise ValueError("Expense amount must be greater than zero.")
        self._add_transaction("expense", amount)

    def delete_transaction(self, transaction_id):
        original_count = len(self.transactions)
        self.transactions = [t for t in self.transactions if t.get("id") != transaction_id]
        if len(self.transactions) < original_count:
            self.save()
            return True
        return False

    def reset_day(self):
        self.transactions = []
        self.save()

    def export_to_csv(self, path=None):
        if path is None: path = CSV_FILE
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "date", "time", "type", "amount"])
            for t in sorted(self.transactions, key=lambda t: (t.get("date", ""), t.get("time", ""), t.get("id", 0))):
                writer.writerow([t.get("id", ""), t.get("date", ""), t.get("time", ""), t.get("type", ""), t.get("amount", "")])
        return path

    @property
    def today_sales(self):
        today = date.today().isoformat()
        return sum(t["amount"] for t in self.transactions if t["type"] == "sale" and t.get("date") == today)

    @property
    def today_expenses(self):
        today = date.today().isoformat()
        return sum(t["amount"] for t in self.transactions if t["type"] == "expense" and t.get("date") == today)

    @property
    def profit(self):
        return self.today_sales - self.today_expenses

    def get_grouped_by_date(self):
        buckets = {}
        for t in self.transactions:
            d = t.get("date", "unknown")
            buckets.setdefault(d, []).append(t)

        sorted_dates = sorted(buckets.keys(), reverse=True)
        today_str = date.today().isoformat()
        yesterday_str = (date.today() - timedelta(days=1)).isoformat()

        result = []
        for d in sorted_dates:
            if d == today_str: label = "Today"
            elif d == yesterday_str: label = "Yesterday"
            else: label = d

            records = sorted(buckets[d], key=lambda t: (t.get("time", ""), t.get("id", 0)), reverse=True)
            result.append((label, records))
        return result

    def _add_transaction(self, kind, amount):
        now = datetime.now()
        next_id = max((t.get("id", 0) for t in self.transactions), default=0) + 1
        record = {
            "id": next_id, "type": kind, "amount": amount,
            "date": now.strftime("%Y-%m-%d"), "time": now.strftime("%H:%M:%S"),
        }
        self.transactions.append(record)
        self.save()

    def save(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.transactions, f, indent=2)

    def load(self):
        if not os.path.exists(DATA_FILE): return
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
            if isinstance(data, list): self.transactions = data
        except (json.JSONDecodeError, ValueError, OSError):
            self.transactions = []
