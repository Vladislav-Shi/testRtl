from enum import StrEnum


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
