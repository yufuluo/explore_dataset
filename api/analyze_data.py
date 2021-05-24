import json
import logging
from jsonschema import validate
import lib.util as util

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

chunck_size = 1000

schema = {
    'type': 'object',
    'properties': {
        'metrics': {
            'enum': [
                'total_viewers',
                'average_viewers'
            ]
        },
        'group_by': {
            'enum': [
                'genre',
                'network'
            ]
        },
        'filter': {
            'type': 'object',
            'minProperties': 1,
            'maxProperties': 1,
            'properties': {
                'city': {
                    'type': 'array',
                    'items' : {
                        'type' : 'string'
                    }
                }
            }
        }
    },
    'required': [
        'metrics',
        'group_by',
        'filter'
    ]
}


def analyze_data(query_param):
    try:
        validate(instance=query_param, schema=schema)
    except Exception as e:
        logging.error('Error', exc_info=True)

    group_by = util.map_param_to_column.get(query_param['group_by'])
    filter_key = util.map_param_to_column.get(list(query_param['filter'])[0])
    filter_value = list(query_param['filter'].values())[0]
    filter = {filter_key: filter_value}
    if query_param['metrics'] == 'total_viewers':
        method = 'sum'
        col_name = util.map_param_to_column.get('viewer')
    elif query_param['metrics'] == 'average_viewers':
        method = 'avg'
        col_name = util.map_param_to_column.get('viewer')
    data = util.analyze_data(method, col_name, group_by, filter, chunck_size)
    return json.dumps(data)

# print(analyze_data({'metrics': 'total_viewers', 'group_by': 'genre', 'filter': {'city': ['Pittsburgh', 'New York']}}))
