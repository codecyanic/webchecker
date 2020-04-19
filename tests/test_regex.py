import pytest
from regex import safe_search

@pytest.mark.parametrize(
    'text,result', [
        ('cab', True),
        ('bac', False),
        ('a' * 100000 + 'c', None),
    ]
)
def test_safe_search(text, result):
    pattern = '(.*a)b'
    found = None
    try:
        found = safe_search(pattern, text, .1)
    except TimeoutError:
        pass

    assert result == found
