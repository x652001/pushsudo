import time
from datetime import datetime, timedelta, timezone


class GetTime:
    # Change Time to timestamp in seconds
    @staticmethod
    def get_timestamp(date):
        timezone8 = timezone(timedelta(hours=+8))
        dt = datetime.strptime(date, '%Y-%m-%d')
        dt8 = dt.replace(tzinfo=timezone8)
        dt0 = dt8.astimezone(timezone.utc)
        timestamp = dt0.timestamp()
        return timestamp

    @staticmethod
    def get_nowtime():
        return datetime.now()

    @staticmethod
    def get_nowtime_timestamp():
        return time.time()

    @staticmethod
    def check_time(dt):
        try:
            datetime.strptime(dt, '%Y-%m-%d')
            return dt
        except ValueError:
            print("Format Error, should be YYYY-MM-DD")
            return None

