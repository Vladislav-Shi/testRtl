import abc
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from utils.salary_aggregation.exeptions import ValidationException
from utils.salary_aggregation.models import GROUP_ISO_MAPPING


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

    def _formatting_result(self, raw_result: list[dict], group_type: str) -> dict:
        result: dict = {
            'dataset': [],
            'labels': []
        }
        for data in raw_result:
            result['dataset'].append(data['value'])
            result['labels'].append(self._date_formatting(data['_id'], group_type))
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
        collection = self._get_collection()
        query = self._get_aggregate_dict(dt_from, dt_upto, group_type)
        raw_result = await collection.aggregate(query).to_list(None)
        result = self._formatting_result(raw_result=raw_result, group_type=group_type)
        return result
