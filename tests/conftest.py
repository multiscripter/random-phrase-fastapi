import pytest

from Database import Database
from db import PhraseInput


@pytest.hookimpl()
def pytest_sessionstart(session):
    """Actions before all tests."""

    db = Database()
    for a in range(1, 4):
        data = {
            'author': f'test-author-{a}',
            'text': f'test-text-{a}'
        }
        phrase = PhraseInput(**data)
        db.add(phrase)
    print('created:')
    print(list(db.items.keys()))


@pytest.hookimpl()
def pytest_sessionfinish(session, exitstatus):
    """Actions after all tests."""

    db = Database()
    for key in db.items.scan_iter(f'phrase*'):
        db.items.delete(key)
    print('deletion completed')
    print(list(db.items.keys()))
