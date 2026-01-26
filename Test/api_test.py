import pytest
from pathlib import Path
from Backend.api import app
from Backend.Database.db import create_db_instance, connect_db

# set config for database location
app.config["DATABASE"] = "../Backend/Database/database.db"

def test_flask_api():
    # start flask test client
    client = app.test_client()

    # send get request and recieve response
    response = client.get("/api/check")

    # test response
    assert response.status_code == 200
    assert response.json == {"status": "ok"}

def test_insert_contact_api():
    # test parameters
    first_name = 'Jacob'
    last_name = 'Roy'

    # create database instance, connection, and cursor
    create_db_instance('../Backend/Database/schema.sql', '../Backend/Database/database.db')
    conn = connect_db('../Backend/Database/database.db')
    cur = conn.cursor()

    # start flask test client
    client = app.test_client()

    # create and send request
    request = {'first_name': first_name,
               'last_name': last_name}
    response = client.post("/api/add/contact", json=request)

    # test response
    assert response.status_code == 201
    assert response.json['message'] == "New Contact Added Successfully"

    # retrieve contents of database table contacts
    cur.execute("SELECT first_name, last_name FROM contacts")
    row = cur.fetchone()

    # test if contact inserted
    assert (row[0], row[1]) == (first_name, last_name)

    # close connection remove database
    cur.close()
    conn.close()
    Path.unlink('../Backend/Database/database.db', missing_ok=True)