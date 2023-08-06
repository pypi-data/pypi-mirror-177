import calendar
import pandas as pd
from datetime import datetime, timezone


def truncate_datetime(date, timeframe):
    kwargs = {
        'year': date.year
    }
    if timeframe.endswith(('M', 'd', 'h', 'm')):
        kwargs['month'] = date.month

    if timeframe.endswith(('d', 'h', 'm')):
        kwargs['day'] = date.day

    if timeframe.endswith(('h', 'm')):
        kwargs['hour'] = date.hour

    if timeframe.endswith('m'):
        kwargs['minute'] = date.minute

    return datetime(
        tzinfo=timezone.utc,
        **kwargs
    )


def get_unix_time(date, timeframe):
    return float(calendar.timegm(truncate_datetime(date, timeframe).timetuple()))


def get_timestamp_range(start, end, timeframe):
    date_objects = pd.date_range(
        start=truncate_datetime(start, timeframe),
        end=truncate_datetime(end, timeframe),
        freq=timeframe,
        tz=timezone.utc
    ).to_pydatetime().tolist()
    return [get_unix_time(date_object, timeframe) for date_object in date_objects]


def convert_timeframe_to_seconds(timeframe):
    seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
    return int(timeframe[:-1]) * seconds_per_unit[timeframe[-1]]
