from Backend.Database.db import connect_db, create_db_instance
from Backend.Model.contact import Contact, Repository
from pathlib import Path
import pytest

def test_db_initialization():

    create_db_instance('../Backend/Database/schema.sql', '../Backend/Database/database.db')

    assert Path.exists('../Backend/Database/database.db') == True

    Path.unlink('../Backend/Database/database.db', missing_ok=True)

# test == operator in Contact class
def test_contact_equality():

    # define test parameters
    first_name = 'Jacob'
    middle_init = 'A'
    last_name = 'Roy'
    birthday = '1999-11-22'
    e_addresses = set(['jacobaustin1@hotmail.com', 'jacob0roy99@gmail.com'])

    # test with same ids
    contact1 = Contact(id=1, first_name=first_name, middle_name_init=middle_init,
                        last_name=last_name, birthday=birthday, e_addresses=e_addresses)
    
    assert contact1 == contact1

    # test with None ids
    contact2 = Contact(first_name=first_name, middle_name_init=middle_init,
                        last_name=last_name, birthday=birthday, e_addresses=e_addresses)
    
    assert contact1 == contact2
    assert contact2 == contact2

    # test with wrong fields
    contact3 = Contact(id=1, first_name=first_name, last_name=last_name, 
                       birthday=birthday, e_addresses=e_addresses)
    
    assert contact1 != contact3
    assert contact2 != contact3

    # test with wrong object
    assert contact1 != 3

# test insert_contact method in Repository class
def test_insert_contact_basic():

    # define test parameters
    first_name = 'Jacob'
    middle_init = 'A'
    last_name = 'Roy'
    birthday = '1999-11-22'
    e_addresses = set(['jacobaustin1@hotmail.com', 'jacob0roy99@gmail.com'])

    # initialize database
    create_db_instance('../Backend/Database/schema.sql', '../Backend/Database/database.db')

    # get connection and cursor to database
    conn = connect_db('../Backend/Database/database.db')
    cur = conn.cursor()

    # create instance of Repository and Contact for test
    repo = Repository('../Backend/Database/database.db')
    contact = Contact(first_name=first_name, middle_name_init=middle_init,
                       last_name=last_name, birthday=birthday, e_addresses=e_addresses)

    # insert contact into database through repository
    repo.insert_contact(contact=contact)

    # use cursor to fetch records from table contacts
    cur.execute('SELECT * FROM contacts')
    row = cur.fetchone()

    # test data
    assert (row[1], row[2], row[3], row[4]) == (first_name, middle_init, last_name, birthday)

    # use cursor to fetch records from table e_address
    cur.execute('SELECT * FROM e_address')
    rows = cur.fetchall()

    # test data
    for i in range(len(rows)):
        assert rows[i][1] in e_addresses

    # close connection remove database
    cur.close()
    conn.close()
    repo.close()
    Path.unlink('../Backend/Database/database.db', missing_ok=True)

# test insert_address method in Repository class
def test_insert_address_basic():

    # define test parameters
    id = 1
    first_name = 'Jacob'
    last_name = 'Roy'
    e_address = 'jacobaustin1@hotmail.com'

    # initialize database
    create_db_instance('../Backend/Database/schema.sql', '../Backend/Database/database.db')

    # get connection and cursor to database
    conn = connect_db('../Backend/Database/database.db')
    cur = conn.cursor()

    # create instance of Repository and Contact for test
    repo = Repository('../Backend/Database/database.db')
    contact = Contact(first_name=first_name, last_name=last_name)

    # insert contact into database
    repo.insert_contact(contact)

    # insert address into database through repository
    repo.insert_address(id=id, address=e_address)

    # use cursor to fetch records from table contacts
    cur.execute('SELECT * FROM e_address')
    row = cur.fetchone()

    # test data
    assert (row[0], row[1]) == (id, e_address)

    # close connection remove database
    cur.close()
    conn.close()
    repo.close()
    Path.unlink('../Backend/Database/database.db', missing_ok=True)

# test get_by_id method in Repository class
def test_get_by_id_basic():

    # define test parameters
    first_name = 'Jacob'
    middle_init = 'A'
    last_name = 'Roy'
    birthday = '1999-11-22'
    e_addresses = set(['jacobaustin1@hotmail.com', 'jacob0roy99@gmail.com'])

    # initialize database
    create_db_instance('../Backend/Database/schema.sql', '../Backend/Database/database.db')

    # create instance of Repository and Contact for test
    repo = Repository('../Backend/Database/database.db')
    contact = Contact(first_name=first_name, middle_name_init=middle_init, 
                      last_name=last_name, birthday=birthday, e_addresses=e_addresses)

    # insert contact into database through repository
    id = repo.insert_contact(contact=contact)

    # test get_by_id method when id exist
    assert repo.get_by_id(id) == contact

    # test get_by_id method when id doesnt exist
    assert repo.get_by_id(0) == None

    # close connection remove database
    repo.close()
    Path.unlink('../Backend/Database/database.db', missing_ok=True)

# test get_all_names method in Repository class
def test_get_all_names_basic():

    # define test parameters
    first_name = 'Jacob'
    middle_init = 'A'
    last_name = 'Roy'

    # initialize database
    create_db_instance('../Backend/Database/schema.sql', '../Backend/Database/database.db')

    # create instance of Repository and Contact for test
    repo = Repository('../Backend/Database/database.db')
    contact = Contact(first_name=first_name, middle_name_init=middle_init, last_name=last_name)

    # test get_all method when database empty
    assert repo.get_all_names() == None

    # insert contact into database through repository
    id = repo.insert_contact(contact=contact)

    # test get_all method when records in database
    names = repo.get_all_names()
    assert names[0]['id'] == id
    assert names[0]['first_name'] == first_name
    assert names[0]['last_name'] == last_name

    # close connection remove database
    repo.close()
    Path.unlink('../Backend/Database/database.db', missing_ok=True)

# test update method in Repository class
def test_update_basic():

    # define test parameters
    first_name = 'Jacob'
    middle_init = 'A'
    last_name = 'Roy'
    birthday = '1999-11-22'
    
    # initialize database
    create_db_instance('../Backend/Database/schema.sql', '../Backend/Database/database.db')

    # create instance of Repository and Contact for test
    repo = Repository('../Backend/Database/database.db')
    contact = Contact(first_name=first_name, last_name=last_name)

    # insert contact into database through repository
    id = repo.insert_contact(contact=contact)

    # update database
    repo.update(id, middle_name_init = middle_init, birthday = birthday)

    # test if contact updated
    assert repo.get_by_id(id) == Contact(first_name=first_name, middle_name_init=middle_init, 
                                         last_name=last_name, birthday=birthday)
    
    # close connection remove database
    repo.close()
    Path.unlink('../Backend/Database/database.db', missing_ok=True)

# test delete_contact method in Repository class
def test_delete_contact_basic():

    # define test parameters
    first_name = 'Jacob'
    middle_init = 'A'
    last_name = 'Roy'
    birthday = '1999-11-22'
    e_addresses = set(['jacobaustin1@hotmail.com', 'jacob0roy99@gmail.com'])
    
    # initialize database
    create_db_instance('../Backend/Database/schema.sql', '../Backend/Database/database.db')

    # get connection and cursor to database
    conn = connect_db('../Backend/Database/database.db')
    cur = conn.cursor()

    # create instance of Repository and Contact for test
    repo = Repository('../Backend/Database/database.db')
    contact = Contact(first_name=first_name, middle_name_init=middle_init, 
                      last_name=last_name, birthday=birthday, e_addresses=e_addresses)

    # insert contact into database through repository
    id = repo.insert_contact(contact=contact)

    # delete contact database
    repo.delete_contact(id)

    # test if contact deleted
    cur.execute("SELECT * FROM contacts")
    assert cur.fetchall() == []
    
    # close connection remove database
    cur.close()
    conn.close()
    repo.close()
    Path.unlink('../Backend/Database/database.db', missing_ok=True)

# test delete_address method in Repository class
def test_delete_address_basic():

    # define test parameters
    first_name = 'Jacob'
    last_name = 'Roy'
    e_addresses = set(['jacobaustin1@hotmail.com', 'jacob0roy99@gmail.com'])
    
    # initialize database
    create_db_instance('../Backend/Database/schema.sql', '../Backend/Database/database.db')

    # get connection and cursor to database
    conn = connect_db('../Backend/Database/database.db')
    cur = conn.cursor()

    # create instance of Repository and Contact for test
    repo = Repository('../Backend/Database/database.db')
    contact = Contact(first_name=first_name, last_name=last_name, e_addresses=e_addresses)

    # insert contact into database through repository
    id = repo.insert_contact(contact=contact)

    # delete address from database
    repo.delete_address(id, e_addresses.pop())

    # test if contact deleted
    cur.execute("SELECT address FROM e_address")
    assert cur.fetchone()[0] == e_addresses.pop()
    
    # close connection remove database
    cur.close()
    conn.close()
    repo.close()
    Path.unlink('../Backend/Database/database.db', missing_ok=True)