import json
import logging
from jsonschema import validate
import lib.util as util

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

schema = {
    'type': 'object',
    'properties': {
        'column_name': {
            'enum': [
                'title',
                'genre',
                'network',
                'city'
            ]
        }
    },
    'required': ['column_name']
}

def get_column_distinct(query_param):
    try:
        validate(instance=query_param, schema=schema)
    except Exception as e:
        logging.error('Error', exc_info=True)

    column_name = util.map_param_to_column.get(query_param['column_name'])
    col_list = util.get_col_distinct(column_name)
    return json.dumps(col_list)
