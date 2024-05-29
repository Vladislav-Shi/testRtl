import abc
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from utils.salary_aggregation.exeptions import ValidationException
from utils.salary_aggregation.models import GROUP_ISO_MAPPING, GROUP_ISO_STEP_MAPPING


class BaseAggregator:
    @abc.abstractmethod
    async def get_salary(self, dt_from, dt_upto, group_type, **kwargs):
        raise NotImplementedError


class MongoAggregator(BaseAggregator):

    def __init__(self, client: AsyncIOMotorClient):
        self._client = client

    def is_iso_date(self, date: str) -> bool:
        try:
            datetime.fromisoformat(date)
            return True
        except Exception:
            return False

    def _get_collection(self) -> AsyncIOMotorCollection:
        return self._client["sampleDB"]["sample_collection"]

    def _date_formatting(self, date_string: str, group_type: str) -> str:
        if group_type == 'week':
            new_data = datetime.strptime(f'{date_string}-1', '%G-%V-%u')
            return new_data.strftime('%Y-%m-%dT00:00:00')
        else:
            return date_string

    def _set_empty_result(self, dt_from: str, dt_upto: str, group_type: str) -> list[str]:
        """Т.к. если значенйи в бд нет, то должно быть 0, инициируем значения"""
        dates = []
        step = GROUP_ISO_STEP_MAPPING[group_type]
        cur = datetime.fromisoformat(dt_from)
        end = datetime.fromisoformat(dt_upto)
        while cur <= end:
            dates.append(cur.isoformat())
            cur += step
        return dates

    def _formatting_result(self, raw_result: dict, dates: list[str]) -> dict:
        result: dict = {
            'dataset': [],
            'labels': []
        }
        for date in dates:
            value = raw_result[date] if date in raw_result else 0
            result['dataset'].append(value)
            result['labels'].append(date)
        return result

    def _get_aggregate_dict(self, dt_from: str, dt_upto: str, group_type: str) -> list[dict]:
        return [
            {
                '$match':
                    {
                        "dt": {'$gte': datetime.fromisoformat(dt_from),
                               '$lte': datetime.fromisoformat(dt_upto),
                               }
                    },
            },
            {
                '$group': {
                    '_id': {'$dateToString': {
                        'format': GROUP_ISO_MAPPING[group_type],
                        'date': '$dt'
                    }},
                    'value': {'$sum': '$value'}
                }
            },
            {
                '$sort': {
                    '_id': 1
                }
            }
        ]

    async def _aggregate(self, query: list[dict], group_type: str) -> dict[str, int]:
        """Возвращает Dict в формате date: number"""
        collection = self._get_collection()
        response = await collection.aggregate(query).to_list(None)
        return {self._date_formatting(row['_id'], group_type): row['value'] for row in response}

    async def get_salary(
            self,
            dt_from: str,
            dt_upto: str,
            group_type: str,
            **kwargs
    ):
        errors = {}
        if not self.is_iso_date(dt_from):
            errors['dt_from'] = f'dt_from is incorrect {dt_from}'
        if not self.is_iso_date(dt_upto):
            errors['dt_upto'] = f'dt_upto is incorrect {dt_upto}'
        if group_type not in GROUP_ISO_MAPPING:
            errors['group_type'] = f'group_type is incorrect {group_type}'
        if len(errors) > 0:
            raise ValidationException(message='Validation error in', details=errors)
        query = self._get_aggregate_dict(dt_from, dt_upto, group_type)
        raw_result = await self._aggregate(query=query, group_type=group_type)
        dates = self._set_empty_result(dt_from=dt_from, dt_upto=dt_upto, group_type=group_type)
        result = self._formatting_result(raw_result=raw_result, dates=dates)
        return result
