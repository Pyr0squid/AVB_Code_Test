from Database.db import connect_db

# Defines contact 
class Contact:

    def __init__(self, id: int = None, first_name: str = None, middle_name_init: str = None, 
                 last_name: str = None, birthday: str = None, e_addresses: list[str] = []):
        self.id = id
        self.first_name = first_name
        self.middle_name_init = middle_name_init
        self.last_name = last_name
        self.birthday = birthday
        self.e_addresses = e_addresses
    
    def to_dict(self):
        return {"ID": self.id,
                "FirstName": self.first_name,
                "MiddleNameInit": self.middle_name_init,
                "LastName": self.last_name,
                "Birthday": self.birthday,
                "E_Addresses": self.e_addresses}
    
# ORM: Maps Contact object to relational records in database
class Repository:

    def __init__(self):
        self.conn = connect_db("Backend/Database/database.db")

    # Insert a contact into database with tables contact and e_addresses, and returns the id of the contact
    def insert_contact(self, contact: Contact) -> int:
        
        with self.conn.cursor() as cur:

            cur.execute("""
                INSERT INTO contacts (
                    first_name, middle_name_init, last_name, birthday
                )
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (
                contact.first_name, contact.middle_name_init, contact.last_name, contact.birthday
            ))

            id = cur.fetchone()[0]

            for address in contact.e_addresses:

                cur.execute("""
                    INSERT INTO e_address (
                        id, address
                    )
                    VALUES (%s, %s)
                    """, (
                        id, address
                ))

        self.conn.commit()

        return id
    
    # search for a contact by ID
    def get_contact_by_id(self, id: int) -> Contact | None:

        with self.conn.cursor() as cur:

            # retrieve info from contacts table
            cur.execute("SELECT * FROM contacts WHERE id = %s", (id,))
            row = cur.fetchone()

            # if id exist, convert info into contact
            if row:

                contact = Contact(id = row[0], first_name = row[1], middle_name_init = row[2], 
                                  last_name = row[3], birthday = row[4])
                
                # retrieve info from e_address table
                cur.execute("SELECT address FROM e_address WHERE id = %s", (id,))
                rows = cur.fetchall()

                # if id exist, add addresses to contact
                for row in rows:

                    contact.e_addresses.append(row[0])

                return contact
            
            return None
