import pytest
import sqlite3
from project import User, connect_sql

def test_user_init():
    """Tests the initialization of the User class."""
    user = User("Alice")
    assert user.name == "Alice"

def test_user_get_infos(monkeypatch):
    """Tests the get_infos method, ensuring it capitalizes the input."""
    # Simulate user typing "bob"
    monkeypatch.setattr('builtins.input', lambda _: "bob")
    user = User(None)
    user.get_infos()
    assert user.name == "Bob"

def test_connect_sql():
    """Tests if the database connection returns correct types."""
    db, cursor = connect_sql()
    assert isinstance(db, sqlite3.Connection)
    assert isinstance(cursor, sqlite3.Cursor)
    db.close()
