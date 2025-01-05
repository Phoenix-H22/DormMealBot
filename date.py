from datetime import datetime, timedelta

class TomorrowDate:
    def __init__(self):
        self.tomorrow = datetime.now() + timedelta(days=1)
        self.formatted_date = f"{self.tomorrow.day}/{self.tomorrow.month}/{self.tomorrow.year}"
    def get_tomorrow_date(self):
        return self.formatted_date
