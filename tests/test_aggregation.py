import pytest

from utils.salary_aggregation.exeptions import ValidationException
from utils.salary_aggregation.salary_aggregation import MongoAggregator


@pytest.mark.parametrize(
    'input_data',
    [
        {
            'dt_from': '2019-01-30T00:00:00',
            'dt_upto': '2024-01-30T00:00:00',
            'group_type': 'days'
        },
        {
            'dt_from': '2019-01-30 00:00:00',
            'dt_upto': '2024--01-30T00:00:00',
            'group_type': 'week'
        },
        {
            'dt_from': '2019-01-30   00:00:00',
            'dt_upto': '2024-01-30 00:00:00',
            'group_type': 'week'
        },
    ]
)
@pytest.mark.asyncio
async def test_wrong_input(input_data, client):
    aggregator = MongoAggregator(await client)
    with pytest.raises(ValidationException):
        await aggregator.get_salary(
            dt_from=input_data['dt_from'],
            group_type=input_data['group_type'],
            dt_upto=input_data['dt_upto'])


@pytest.mark.asyncio
async def test_input_week(client):
    res = {'dataset': [0, 0, 0, 1029, 26097, 0],
           'labels': ['2022-11-28T00:00:00',
                      '2022-12-05T00:00:00',
                      '2022-12-12T00:00:00',
                      '2022-12-19T00:00:00',
                      '2022-12-26T00:00:00',
                      '2023-01-02T00:00:00']}
    dt_from = '2022-11-30T00:00:00'
    dt_upto = '2023-01-05T00:00:00'
    group_type = 'week'
    aggregator = MongoAggregator(await client)
    result = await aggregator.get_salary(
        dt_from=dt_from,
        group_type=group_type,
        dt_upto=dt_upto)
    assert result == res


@pytest.mark.asyncio
async def test_input_hour(client):
    res = {'dataset': [1435, 2086, 626],
           'labels': ['2023-01-01T01:00:00',
                      '2023-01-01T02:00:00',
                      '2023-01-01T03:00:00']}
    dt_from = '2023-01-01T01:39:00.000Z'
    dt_upto = '2023-01-01T04:13:00.000Z'
    group_type = 'hour'
    aggregator = MongoAggregator(await client)
    result = await aggregator.get_salary(
        dt_from=dt_from,
        group_type=group_type,
        dt_upto=dt_upto)
    assert res == result
