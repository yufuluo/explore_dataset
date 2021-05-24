import logging
from .db import get_db_connection
from .method import sum, avg

TABLE_NAME = 'viewers'

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

map_param_to_column = {
    'title': 'Program Title',
    'genre': 'Program Genre',
    'network': 'Program Network',
    'city': 'Viewer Hometown',
    'viewer': 'Number of Viewers'
}

def _get_data_with_criteria(col_name, criteria, limit, offset):
    """Internal function to get a list of data that mataches the criteria.

    Get at most x rows from the n-th result matching the search criteria,
    and retrieve a list of data for the target column.


    Args:
        col_name: Name of the target column. For example: 'Number of Viewers'.
        criteria: A dictionary for the query filter. For example:
        {
            'Program Genre': 'Science Fiction',
            'Viewer Hometown': 'Pittsburgh'
        }
        limit: A SELECT statement may return one million rows, so that cannot be fit in RAM.
        We use a reasonable integer to constrain the number of rows returned by the query.
        For example: 1000.
        offset: A integer. Specifies the number of rows to skip before starting to return
        rows from the query.

    Returns:
        A list of data from the target column. For example, the 'Number of Viewers' for criteria
        {
            'Program Genre': 'Science Fiction',
            'Viewer Hometown': 'Pittsburgh'
        }
        with limit=1000, offset=0 is:
        [200, 175, 100]
    """
    result = []
    conn = get_db_connection()
    sql_str = 'SELECT \"%s\" FROM %s WHERE' % (col_name, TABLE_NAME)
    for key, value in criteria.items():
        sql_str += ' \"%s\" = \"%s\" AND' % (key, value)
    sql_str = sql_str.rsplit(' ', 1)[0]
    sql_str += ' LIMIT %s OFFSET %s;' % (limit, offset)
    try:
        data = conn.execute(sql_str)
    except Exception as e:
        logging.error('Error', exc_info=True)
    for item in data:
        result.append(item[col_name])
    return result

def get_col_distinct(col_name):
    """Public function to get a list of distinct items in a column.

    Args:
        col_name: Name of the target column. For example: 'Program Genre'.

    Returns:
        A list of sting. For example:
        ['Sports', 'Science Fiction', 'Mystery']
    """
    distinct_list = []
    conn = get_db_connection()
    try:
        distinct_items = conn.execute('SELECT DISTINCT \"%s\" FROM %s' % (col_name, TABLE_NAME))
    except Exception as e:
        logging.error('Error', exc_info=True)
        distinct_items = []
    for item in distinct_items:
        if col_name in item.keys():
            distinct_list.append(item[col_name])
        else:
            logging.error('Error: column name \"%s\" not found in table %s' % (col_name, TABLE_NAME))
    return distinct_list

def analyze_data(method, col_name, group_by, filter, chunck_size):
    """Public function to analyze data.

    Args:
        method: The method for processing data. Currently supports sum and average of the data
        set. Valid values are: 'sum' | 'avg'
        col_name: Name of the target column. For example: 'Number of Viewers'.
        group_by: Name of the column that use to group the data. For example: 'Program Genre'.
        filter: A dictionary for the query filter. Only have one key-vaule pair. For example:
        {
            'Viewer Hometown': ['Pittsburgh', 'New York', 'Boston']
        }
        chunck_size: A SELECT statement may return one million rows, so that cannot be fit in RAM.
        We devide the result into muleiple chuncks, and use a reasonable integer to constrain the
        number of rows returned by the query each time.
        For example: 1000.

    Returns:
        A list of data from the target column. For example the total viewers group by genre
        in the selected cities:
        {
           "Sports":{
              "Pittsburgh":1007,
              "New York":300,
              "Boston":130
           },
           "Science Fiction":{
              "Pittsburgh":475,
              "New York":1950,
              "Boston":1100
           },
           "Mystery":{
              "Pittsburgh":1550,
              "New York":2250,
              "Boston":2100
           }
        }
    """
    result = {}
    filter_key = list(filter)[0]
    filter_list = list(filter.values())[0]
    group_by_list = get_col_distinct(group_by)
    for item in group_by_list:
        for filter_item in filter_list:
            criteria = {
                group_by: item,
                filter_key: filter_item
            }
            offset = 0
            num = 0
            data = _get_data_with_criteria(col_name, criteria, chunck_size, offset)
            while data:
                if method == 'sum':
                    num = sum(num, data)
                elif method == 'avg':
                    num = avg(num, data, offset)
                offset += chunck_size
                data = _get_data_with_criteria(col_name, criteria, chunck_size, offset)
            if item not in result:
                result[item] = {}
            result[item][filter_item] = num
    return result
