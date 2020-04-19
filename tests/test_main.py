import pytest
import yaml

from main import add_urls

@pytest.mark.parametrize(
    'yml,expected', [
        ('url: {"pattern": "p", "interval": 1}',  ('url', 'p', 1)),
        ('url: ["p", 1]',                         ('url', 'p', 1)),
        ('url: "p"',                              ('url', 'p', 0)),
        ('url: 1',                                ('url', ' ', 1)),
        ('url: 1.0',                              ('url', ' ', 1.0)),
        ('url:',                                  ('url', ' ', 0)),
        ('url: {}',                               ('url', ' ', 0)),
        ('url: []',                               ('url', ' ', 0)),
    ]
)
def test_add_urls(yml, expected):
    class Checker:
        def add(self, url, pattern=' ', interval=0):
            supplied = (url, pattern, interval)
            for i in range(len(supplied)):
                assert supplied[i] == expected[i]
                assert isinstance(supplied[i], type(expected[i]))

    checker = Checker()
    args = yaml.safe_load(yml)
    add_urls(checker, args)


