from src.gql_query_utils.utils import query_to_dict


def test_query_simple_fields():
    result = query_to_dict("""
        {
            a
            b
        }
    """)
    assert result == {'query': {'a': True, 'b': True}}


def test_query_field_sets():
    result = query_to_dict("""
        {
            a
            b {
                c
            }
        }
    """)
    assert result == {'query': {'a': True, 'b': {'c': True}}}


def test_query_field_arguments():
    result = query_to_dict("""
        query {
            a
            b (id: 50) {
                c
            }
        }
    """)
    assert result == {'query': {'a': True, 'b': {'c': True, '__args': {'id': '50'}}}}
