## GET /api/get_column_distinct
Get all the distinct values of a column from the dataset.

```
Query param: column_name = 'title' | 'genre' | 'network' | 'city'
Param type: string [REQUIRED]

Return type: list
Returns:
  Response Syntax:
  ['string', 'string', ...]

```

## POST /api/analyze_data
Get a dataset of selected metrics, matching a provided group and filter.

```
Body: {
  'metrics': 'total_viewers' | 'average_viewers',
  'group_by': 'genre' | 'network',
  'filter': {
    'city': ['string', 'string', ...]
  }
}
Parameters:
  metrics = string [REQUIRED]
  group_by = string [REQUIRED]
  filter = dict [REQUIRED]

Return type: dict
Returns:
  Response Example:
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
```
