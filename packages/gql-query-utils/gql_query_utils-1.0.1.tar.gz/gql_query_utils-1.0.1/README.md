# gql-query-utils
Python package with graphql queries utilities. 

## Install
Install with `pip`:
```commandline
pip install gql-query-utils
```

## Utilities

### Convert graphql query string into dictionary 
```python
from gql_query_utils.utils import query_to_dict 

query_dict = query_to_dict("""
query GetThisStuff {
    viewer {
        personal(criteria: {
            name: "PETER",
            lastName: "SCHMIDT"
        }) {
            name
            address
        }
    }
}""")

print(query_dict)
```
Output:
```json
{
  "query": {
    "viewer": {
      "personal": {
        "__args": {
          "criteria": {
            "name": "PETER",
            "lastName": "SCHMIDT"
          }
        },
        "name": true,
        "address": true
      }
    }
  }
}
```

## Usage

```python
from gql_query_utils.utils import query_to_dict 

query_to_dict(""" ${GQL_QUERY} """)
```
## License
[MIT](./LICENSE)