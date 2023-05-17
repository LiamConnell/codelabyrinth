from coder.db import Database


def test_pg_connection():
    db = Database()

    db_version = db.fetch_query("SELECT version();")[0]
    assert db_version is not None
    print(f"PostgreSQL version : {db_version}")


def test_vector_operations():
    db = Database()

    db.execute_query("CREATE SCHEMA IF NOT EXISTS tests;")
    db.execute_query("SET search_path TO tests, public;")
    db.execute_query("CREATE TABLE IF NOT EXISTS items (id bigserial PRIMARY KEY, embedding vector(3));")
    db.execute_query("INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]');")
    results = db.fetch_query("SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5;")
    assert results is not None

    db.execute_query("DROP TABLE IF EXISTS items;")