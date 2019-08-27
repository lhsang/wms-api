import requests
import json
import pytest
from . import host

url = host + '/api/authors/'
headers = {'content-type': 'application/json'}


def test_get_author():
    res = requests.get(url)
    assert res.status_code == 200
    result = json.loads(res.text)
    assert result['success'] == True


@pytest.mark.post_success
def test_post_author():
    author1 = {
        "first_name": "le",
        "last_name": "tester",
        "email": "lghsang@gmail.com",
        "phone": "0987654321"
    }
    res = requests.post(url, json.dumps(author1), headers=headers)
    assert res.status_code == 200

    result = json.loads(res.text)
    assert result['success'] == True
    assert len(result['data']) > 0


@pytest.mark.parametrize(('payload',),[
        (' {}',),
        (' {"first_name": "le", "email": "lghsang@gmail.com", "phone": "0987654321"}',),
        (' {"last_name": "le", "email": "lghsang@gmail.com", "phone": "0987654321"}',),

        (' {"first_name": "le", "last_name": "sang", "email": "lghsang@gmail", "phone": "0987654321"}',),
        (' {"first_name": "le", "last_name": "sang", "email": "@gmail", "phone": "0987654321"}',),
        (' {"first_name": "le", "last_name": "sang", "email": "lhsang", "phone": "0987654321"}',),
        (' {"first_name": "le", "last_name": "sang", "email": "lg+/hsang@gmail", "phone": "0987654321"}',),

        (' {"first_name": "le", "last_name": "sang", "email": "lhsang@gmail", "phone": "+0987654321"}',),
        (' {"first_name": "le", "last_name": "sang", "email": "lghsang@gmail", "phone": "987654321"}',),
        (' {"first_name": "le", "last_name": "sang", "email": "lghsang@gmail", "phone": "09876543211111"}',),
        (' {"first_name": "le", "last_name": "sang", "email": "lghsang@gmail", "phone": "0987654325555555555555551"}',),
        (' {"first_name": "le", "last_name": "sang", "email": "lghsang@gmail", "phone": "22"}',),
        (' {"first_name": "le", "last_name": "sang", "email": "lghsang@gmail", "phone": "0e4554545"}',),
])
@pytest.mark.post_fail
def test_post_author_fail(payload):
    res = requests.post(url, payload, headers=headers)
    assert res.status_code == 400