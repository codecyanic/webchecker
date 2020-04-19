import pytest
import json
from websitechecker import check_website, search_pattern

URL = 'https://example.com'
PATTERN = 'example'


@pytest.mark.parametrize(
    'url,pattern,missing', [
        (URL, PATTERN, 'exception'),
        ('http://localhost:100000', '', 'response'),
        (URL, '', 'search'),
        (URL, '(', 'found'),
    ]
)
def test_check_website(url, pattern, missing):
    result = check_website(url, pattern)
    if 'exception' in result:
        result['exception'] = True

    assert missing not in json.dumps(result)


def test_check_website_exception():
    with pytest.raises(TypeError):
        check_website(b'url')


def test_search_pattern():
    with pytest.raises(TypeError):
        search_pattern(b'pattern', '')
