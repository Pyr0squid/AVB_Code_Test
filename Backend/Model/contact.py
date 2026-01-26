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
    
    # convert contact to dict to make JSON serializable
    def to_dict(self) -> dict:
        return {"id": self.id,
                "first_name": self.first_name,
                "middle_name_init": self.middle_name_init,
                "last_name": self.last_name,
                "birthday": self.birthday,
                "e_addresses": sorted(self.e_addresses)} # convert set -> list
    
# ORM: Maps Contact object to relational records in database
class Repository:

    def __init__(self, database: str):
        self.conn = connect_db(database)

    # Insert a contact into database with tables contact and e_addresses, and returns the id of the contact
    def insert_contact(self, contact: Contact) -> int:
        
        cur = self.conn.cursor()

        try:
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

        except:
            self.conn.rollback()
            
            raise Exception("Failed to Insert Contact")

        finally:
            cur.close()

    # insert address to e_address table
    def insert_address(self, id: int, address: str) -> bool:

        cur = self.conn.cursor()

        try:
            cur.execute("""
                INSERT INTO e_address (
                    id, address
                )
                VALUES (?, ?)
                """, (
                    id, address
            ))

            self.conn.commit()

            return cur.rowcount > 0
        
        except:
            self.conn.rollback()

            raise Exception("Failed to Insert Address")
        
        finally:
            cur.close()
    
    # search for a contact by ID
    def get_by_id(self, id: int) -> Contact | None:

        cur = self.conn.cursor()

        # retrieve info from contacts table
        try:
            cur.execute("SELECT * FROM contacts WHERE id = ?", (id,))
            row = cur.fetchone()
        
        except:
            row = False

        # if id exist, convert info into contact
        if row:

            contact = Contact(id = row[0], first_name = row[1], middle_name_init = row[2], 
                              last_name = row[3], birthday = row[4])
                
            # retrieve info from e_address table
            try:
                cur.execute("SELECT address FROM e_address WHERE id = ?", (id,))
                rows = cur.fetchall()

            except:
                rows = None

            # if id exist, add addresses to contact
            for row in rows:

                contact.e_addresses.add(row[0])

            cur.close()

            return contact
            
        cur.close()

        return None

    # retrieve all contacts names in database as list of tuples (id, first_name, last_name)
    def get_all_names(self) -> list[tuple] | None:

        cur = self.conn.cursor()

        # retrieve info from contacts table
        try:
            cur.execute("SELECT id, first_name, last_name FROM contacts")
            rows = cur.fetchall()

            # if table not empty, convert records into list of contacts
            if rows:
                return [(row[0], row[1], row[2]) for row in rows]
            
            return None

        except Exception:
            raise

        finally:
            cur.close()
    
    # update arbitrary number of contact's details by id and return True if successful; fields must be one of first_name, 
    # middle_name_init, last_name, birthday
    def update(self, id: int, **fields: str) -> bool:

        # check if arguments exist
        if not fields:
            return 0
        
        # check if fields satisfy requirement
        for field in fields:
            if field not in ('first_name', 'middle_name_init', 'last_name', 'birthday'):
                raise ValueError(f'Invalid Field: {field}')

        cur = self.conn.cursor()

        # construct sql query from fields kwarg
        sql_clause = ', '.join(f'{field} = ?' for field, value in fields.items() if value is not None)
        values = list(x for x in fields.values() if x is not None)
        values.append(id)
        sql = f"UPDATE contacts SET {sql_clause} WHERE id = ?"

        # execute sql query
        try:
            cur.execute(sql, values)

            self.conn.commit()
            
            return cur.rowcount > 0

        except:
            self.conn.rollback()
            
            raise Exception('Failed to Update Contact')

        finally:
            cur.close()
    
    # deletes a contact from the database; returns true if successful
    def delete_contact(self, id: int) -> bool:

        cur = self.conn.cursor()

        try:
            cur.execute("DELETE FROM contacts WHERE id=?", (id,))
            
            self.conn.commit()

            return cur.rowcount > 0
        
        except:
            self.conn.rollback()
            
            raise Exception('Failed to Delete Contact')
        
        finally:
            cur.close()

    # deletes an email address from database; returns true if successful
    def delete_address(self, id: int, address: str) -> bool:

        cur = self.conn.cursor()

        try:
            cur.execute("DELETE FROM e_address WHERE id=? AND address=?", (id, address,))
            
            self.conn.commit()

            return cur.rowcount > 0
        
        except:
            self.conn.rollback()

            raise Exception('Failed to Delete Address')
        
        finally:
            cur.close()
    
    # close db connection
    def close(self):

        self.conn.close()