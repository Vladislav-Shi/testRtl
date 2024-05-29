from datetime import timedelta
from enum import StrEnum

from dateutil.relativedelta import relativedelta  # type: ignore


class GroupTypeEnum(StrEnum):
    DAY = 'day'
    MONTH = 'month'
    HOUR = 'hour'
    WEEK = 'week'
    YEAR = 'year'


GROUP_ISO_MAPPING = {
    'hour': '%Y-%m-%dT%H:00:00',
    'day': '%Y-%m-%dT00:00:00',
    'month': '%Y-%m-01T00:00:00',
    'week': '%G-%V',
    'year': '%Y-01-01T00:00:00',
}

GROUP_ISO_STEP_MAPPING = {
    'hour': timedelta(hours=1),
    'day': timedelta(days=1),
    'month': relativedelta(months=1),
    'week': timedelta(weeks=1),
    'year': relativedelta(year=1),
}
