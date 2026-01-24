from Backend.Database.db import connect_db

# Defines contact 
class Contact:

    def __init__(self, id: int = None, first_name: str = None, middle_name_init: str = None, 
                 last_name: str = None, birthday: str = None, e_addresses: set[str] | None = None):
        self.id = id
        self.first_name = first_name
        self.middle_name_init = middle_name_init
        self.last_name = last_name
        self.birthday = birthday
        self.e_addresses = e_addresses or set()

    def __eq__(self, other: object) -> bool:

        if not isinstance(other, Contact):
            return NotImplemented

        return (
            (self.id is None or other.id is None or self.id == other.id)
            and self.first_name == other.first_name
            and self.middle_name_init == other.middle_name_init
            and self.last_name == other.last_name
            and self.birthday == other.birthday
            and self.e_addresses == other.e_addresses
        )
    
    def to_dict(self):
        return {"ID": self.id,
                "FirstName": self.first_name,
                "MiddleNameInit": self.middle_name_init,
                "LastName": self.last_name,
                "Birthday": self.birthday,
                "E_Addresses": self.e_addresses}
    
# ORM: Maps Contact object to relational records in database
class Repository:

    def __init__(self, database: str):
        self.conn = connect_db(database)

    # Insert a contact into database with tables contact and e_addresses, and returns the id of the contact
    def insert_contact(self, contact: Contact) -> int:
        
        cur = self.conn.cursor()

        cur.execute("""
            INSERT INTO contacts (
                first_name, middle_name_init, last_name, birthday
            )
            VALUES (?, ?, ?, ?)
        """, (
            contact.first_name, contact.middle_name_init, contact.last_name, contact.birthday
        ))

        id = cur.lastrowid

        for address in contact.e_addresses:

            cur.execute("""
                INSERT INTO e_address (
                    id, address
                )
                VALUES (?, ?)
                """, (
                    id, address
            ))

        self.conn.commit()

        return id
    
    # search for a contact by ID
    def get_by_id(self, id: int) -> Contact | None:

        cur = self.conn.cursor()

        # retrieve info from contacts table
        cur.execute("SELECT * FROM contacts WHERE id = ?", (id,))
        row = cur.fetchone()

        # if id exist, convert info into contact
        if row:

            contact = Contact(id = row[0], first_name = row[1], middle_name_init = row[2], 
                              last_name = row[3], birthday = row[4])
                
            # retrieve info from e_address table
            cur.execute("SELECT address FROM e_address WHERE id = ?", (id,))
            rows = cur.fetchall()

            # if id exist, add addresses to contact
            for row in rows:

                contact.e_addresses.add(row[0])

            return contact
            
        return None

    # retrieve all contacts names in database as tuple (id, first_name, last_name)
    def get_all_names(self) -> list[tuple] | None:

        cur = self.conn.cursor()

        # retrieve info from contacts table
        cur.execute("SELECT id, first_name, last_name FROM contacts")
        rows = cur.fetchall()

        # if table not empty, convert records into list of contacts
        if rows:

            return [(row[0], row[1], row[2]) for row in rows]

        return None
    
    # update 

    # close db connection
    def close(self):

        self.conn.close()