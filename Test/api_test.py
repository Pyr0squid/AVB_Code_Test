import pytest
from pathlib import Path
from Backend.api import app
from Backend.Database.db import create_db_instance, connect_db
from Backend.Model.contact import Contact, Repository

# set config for database location
DB_PATH = "../Backend/Database/database.db"
app.config["DATABASE"] = DB_PATH


def test_flask_api():
    # start flask test client
    client = app.test_client()

    # send get request and recieve response
    response = client.get("/api/check")

    # test response
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


# test functionality of add_contact api function
def test_add_contact_api():
    # test parameters
    first_name = "Jacob"
    last_name = "Roy"

    # create database instance, connection, and cursor
    create_db_instance("../Backend/Database/schema.sql", DB_PATH)
    conn = connect_db(DB_PATH)
    cur = conn.cursor()

    # start flask test client
    client = app.test_client()

    # create and send request
    request = {"first_name": first_name, "last_name": last_name}
    response = client.post("/api/add/contact", json=request)

    # test response
    assert response.status_code == 201
    assert response.json["message"] == "New Contact Added Successfully"

    # retrieve contents of database table contacts
    cur.execute("SELECT first_name, last_name FROM contacts")
    row = cur.fetchone()

    # test if contact inserted
    assert (row[0], row[1]) == (first_name, last_name)

    # close connection remove database
    cur.close()
    conn.close()
    Path.unlink("../Backend/Database/database.db", missing_ok=True)


# test functionality of add_address api function
def test_add_address_api():
    # test parameters
    id = 1
    first_name = "Jacob"
    last_name = "Roy"
    e_address = "jacobaustin1@hotmail.com"

    # create database instance, connection, and cursor
    create_db_instance("../Backend/Database/schema.sql", DB_PATH)
    conn = connect_db(DB_PATH)
    cur = conn.cursor()

    # create repository and insert contact
    repo = Repository(DB_PATH)
    repo.insert_contact(Contact(first_name=first_name, last_name=last_name))

    # start flask test client
    client = app.test_client()

    # create and send request
    request = {"id": id, "address": e_address}
    response = client.post("/api/add/address", json=request)

    # test response
    assert response.status_code == 201
    assert response.json["message"] == "New Email Address Added Successfully"

    # retrieve contents of database table address
    cur.execute("SELECT address FROM e_address")
    row = cur.fetchone()

    # test if contact inserted
    assert row[0] == e_address

    # close connection remove database
    repo.close()
    cur.close()
    conn.close()
    Path.unlink("../Backend/Database/database.db", missing_ok=True)


# test functionality of get_by_id api function
def test_get_by_id_api():
    # test parameters
    id = 1
    first_name = "Jacob"
    last_name = "Roy"
    e_addresses = {"jacobaustin1@hotmail.com", "jacob0roy99@gmail.com"}

    # create database instance, connection, and cursor
    create_db_instance("../Backend/Database/schema.sql", DB_PATH)

    # create repository and insert contact
    repo = Repository(DB_PATH)
    repo.insert_contact(
        Contact(first_name=first_name, last_name=last_name, e_addresses=e_addresses)
    )

    # start flask test client
    client = app.test_client()

    # create and send request
    response = client.get(f"/api/retrieve/{id}")

    # unpackage response
    contact = response.get_json()
    print(contact)

    # test response
    assert response.status_code == 200
    assert contact["id"] == id
    assert contact["first_name"] == first_name
    assert contact["last_name"] == last_name
    assert contact["e_addresses"] == sorted(e_addresses)

    # close connection remove database
    repo.close()
    Path.unlink("../Backend/Database/database.db", missing_ok=True)


# test functionality of get_all_names api function
def test_get_all_names_api():
    # test parameters
    id1 = 1
    first_name1 = "Jacob"
    last_name1 = "Roy"
    id2 = 2
    first_name2 = "Felix"
    last_name2 = "Lyne"

    # create database instance, connection, and cursor
    create_db_instance("../Backend/Database/schema.sql", DB_PATH)

    # create repository and insert contacts
    repo = Repository(DB_PATH)
    repo.insert_contact(Contact(first_name=first_name1, last_name=last_name1))
    repo.insert_contact(Contact(first_name=first_name2, last_name=last_name2))

    # start flask test client
    client = app.test_client()

    # create and send request
    response = client.get(f"/api/names")

    # unpackage response
    contact = response.get_json()
    print(contact)

    # test response
    assert response.status_code == 200
    assert contact[0]["id"] == id1
    assert contact[0]["first_name"] == first_name1
    assert contact[0]["last_name"] == last_name1
    assert contact[1]["id"] == id2
    assert contact[1]["first_name"] == first_name2
    assert contact[1]["last_name"] == last_name2

    # close connection remove database
    repo.close()
    Path.unlink("../Backend/Database/database.db", missing_ok=True)


# test functionality of update contact api function
def test_update_contact_api():
    # test parameters
    id = 1
    first_name = "Jacob"
    last_name = "Roy"
    middle_name_init = "A"
    birthday = "1999-11-22"

    # create database instance, connection, and cursor
    create_db_instance("../Backend/Database/schema.sql", DB_PATH)
    conn = connect_db(DB_PATH)
    cur = conn.cursor()

    # create repository and insert contact
    repo = Repository(DB_PATH)
    repo.insert_contact(Contact(first_name=first_name, last_name=last_name))

    # start flask test client
    client = app.test_client()

    # create and send request
    request = {"id": id, "middle_name_init": middle_name_init, "birthday": birthday}
    response = client.post("/api/update", json=request)

    # test response
    assert response.status_code == 200
    assert response.get_json()["message"] == "Contact Updated Successfully"

    # retrieve contents of database table contacts
    cur.execute("SELECT * FROM contacts")
    row = cur.fetchone()

    # test if contact updated
    assert (row[1], row[2], row[3], row[4]) == (
        first_name,
        middle_name_init,
        last_name,
        birthday,
    )

    # close connection remove database
    repo.close()
    cur.close()
    conn.close()
    Path.unlink("../Backend/Database/database.db", missing_ok=True)


# test functionality of delete contact api function
def test_delete_contact_api():
    # test parameters
    id = 1
    first_name = "Jacob"
    last_name = "Roy"
    e_addresses = {"jacobaustin1@hotmail.com", "jacob0roy99@gmail.com"}

    # create database instance, connection, and cursor
    create_db_instance("../Backend/Database/schema.sql", DB_PATH)
    conn = connect_db(DB_PATH)
    cur = conn.cursor()

    # create repository and insert contact
    repo = Repository(DB_PATH)
    repo.insert_contact(
        Contact(first_name=first_name, last_name=last_name, e_addresses=e_addresses)
    )

    # start flask test client
    client = app.test_client()

    # create and send request
    request = {"id": id}
    response = client.post("/api/delete/contact", json=request)

    # test response
    assert response.status_code == 200
    assert response.get_json()["message"] == "Contact Successfully Deleted"

    # retrieve contents of database table contacts
    cur.execute("SELECT * FROM contacts")
    row = cur.fetchone()

    # test if contact was deleted
    assert row is None

    # retrieve contents of database table e_address
    cur.execute("SELECT * FROM e_address")
    row = cur.fetchone()

    # test if e_address was deleted
    assert row is None

    # close connection remove database
    repo.close()
    cur.close()
    conn.close()
    Path.unlink("../Backend/Database/database.db", missing_ok=True)


# test functionality of delete address api function
def test_delete_address_api():
    # test parameters
    id = 1
    first_name = "Jacob"
    last_name = "Roy"
    e_addresses = {"jacobaustin1@hotmail.com", "jacob0roy99@gmail.com"}

    # create database instance, connection, and cursor
    create_db_instance("../Backend/Database/schema.sql", DB_PATH)
    conn = connect_db(DB_PATH)
    cur = conn.cursor()

    # create repository and insert contact
    repo = Repository(DB_PATH)
    repo.insert_contact(
        Contact(first_name=first_name, last_name=last_name, e_addresses=e_addresses)
    )

    # start flask test client
    client = app.test_client()

    # create and send request
    request = {"id": id, "address": e_addresses.pop()}
    response = client.post("/api/delete/address", json=request)

    # test response
    assert response.status_code == 200
    assert response.get_json()["message"] == "Email Address Successfully Deleted"

    # retrieve contents of database table e_address
    cur.execute("SELECT * FROM e_address")
    row = cur.fetchone()

    # test if e_address was deleted
    assert row[1] == e_addresses.pop()

    # close connection remove database
    repo.close()
    cur.close()
    conn.close()
    Path.unlink("../Backend/Database/database.db", missing_ok=True)
