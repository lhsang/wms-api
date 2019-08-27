import requests
import json
import pytest
from . import host

url = host + '/api/books/'
headers = {'content-type': 'application/json'}


@pytest.mark.get_book_success
@pytest.mark.parametrize(('path',), [
    (f'{url}',),
    (f'{url}?title=&isbn=',),
    (f'{url}?title=toi',),
    (f'{url}?title=toi&isbn=a98787',)
])
def test_get_book(path):
    res = requests.get(path)
    assert res.status_code == 200
    result = json.loads(res.text)
    assert result['success'] == True


@pytest.mark.post_success
def test_post_book_success():
    book = {
        "title": "Toi tai gioi ban cung the",
        "year": 2009,
        "isbn": "9828778787878",
        "authorID": 1
    }

    res = requests.post(url, json.dumps(book), headers=headers)
    assert res.status_code == 200

    result = json.loads(res.text)
    assert result['success'] == True
    assert len(result['data']) > 0


@pytest.mark.post_fail
@pytest.mark.parametrize(('payload', 'status_code'), [
    ('{"year": 2020, "isbn": "9828778787878","authorID": 1}', 400),
    ('{"title": "Toi tai gioi ban cung the", "year": 2020, "authorID": 1}', 400),

    ('{"title": "Toi tai gioi ban cung the", "year": 2020, "isbn": "9828778787878","authorID": 1}', 400),
    ('{"title": "Toi tai gioi ban cung the", "year": -199, "isbn": "9828778787878","authorID": 1}', 400),
    ('{"title": "Toi tai gioi ban cung the", "year": 20aaa20, "isbn": "9828778787878","authorID": 1}', 400),
    ('{"title": "Toi tai gioi ban cung the", "year": "2020", "isbn": "9828778787878","authorID": 1}', 400),

    ('{"title": "Toi tai gioi ban cung the", "year": 2020, "isbn": "9828778787878","authorID": -1998}', 400),
    ('{"title": "Toi tai gioi ban cung the", "year": 2020, "isbn": "9828778787878"}', 400),

    ('{"title": "Toi tai gioi ban cung the", "year": 2020, "isbn": "9828778787878","authorID": 1}', 400),

])
def test_post_book_fail(payload, status_code):
    res = requests.post(url, payload, headers=headers)
    print(res.text)
    assert res.status_code == status_code


@pytest.mark.get_a_book
@pytest.mark.parametrize(('id', 'status_code'), [
    (-1999, 404),
    (0, 400),
    (2, 200)
])
def test_get_a_book(id, status_code):
    res = requests.get(url + str(id))
    assert res.status_code == status_code


@pytest.mark.delete_book
@pytest.mark.parametrize(('id', 'status_code'), [
    (-1999, 404),
    (0, 400),
    (4, 200)
])
def test_delete_book(id, status_code):
    res = requests.delete(url + str(id))
    assert res.status_code == status_code


@pytest.mark.put_book
@pytest.mark.parametrize(('payload', 'status_code'), [
    ('{}', 200),
    ('{"title": "Toi tai", "year": 2011, "isbn": "9828778787878","authorID": 1}', 200),
    ('{"year": 2011}', 200),
    ('{"isbn": "9828778787878"}', 200),
    ('{"title": "Toi tai gioi ban cung the", "year": 2011, "isbn": "9828778787878","authorID": 2}', 200),

    ('{"year": 2020}', 400),
    ('{"authorID": 0}', 400),
    ('{"title":,}', 400),
])
def test_put_book(payload, status_code):
    bookID = 7
    res = requests.put(url + str(bookID), payload, headers= headers)
    assert res.status_code == status_code

