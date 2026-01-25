from flask import Flask, jsonify, request
from flask_cors import CORS
from Backend.Model.contact import Contact, Repository 

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/api/contacts", methods=["GET"])
def get_by_id():
    """fetch contact"""
    # retrieve GET request
    data = request.get_json()

    # open database repository
    repository = Repository()

    try:
        # retrieve contact by id
        contact = repository.get_by_id(int(data['id']))

        # send contact data to caller
        return jsonify(contact.__dict__)

    except:
        return jsonify({"error": "Failed to Retrieve Contact"}), 400

    finally:
        # close database connection
        repository.close()


@app.route("/api/contacts", methods=["GET"])
def get_all_names():
    """fetch_all_contacts_names"""
    # open database repository
    repository = Repository()

    try:
        # retrieve list of contacts names
        contacts = repository.get_all_names()

        # send data to caller
        return jsonify([contact.__dict__ for contact in contacts])
    
    except:
        return jsonify({"error": "Failed to Retrieve Contact Names"}), 400

    finally:
        # close database connection
        repository.close()

@app.route("/api/contacts", methods=["POST"])
def add_contact():
    """insert_contact"""

    # retrieve POST request
    data = request.get_json()

    # validate data for required fields
    required_fields = ["first_name", "last_name"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields: first_name, last_name"}), 400

    # process data by replacing empty string values with None
    clean_data = {k: (v if v != "" else None) for k, v in data.items()}

    # validate email address and birthday formatting

    # create Contact instance using submitted data
    contact = Contact(
        first_name=clean_data.get("first_name"),
        middle_name_init=clean_data.get("middle_name_init"),
        last_name=clean_data.get("last_name"),
        birthday=clean_data.get("birthday"),
        e_addresses=clean_data.get("e_addresses")
    )

    try:
        # create repository and insert new contact
        repository = Repository()
        contact_id=repository.insert_contact(contact)

        # get contact instance from repository
        new_contact = repository.get_by_id(contact_id)

        # return contact instance to caller
        return jsonify(new_contact.__dict__), 201
    
    except:

        return jsonify({"error": "Failed to Insert Contact in Database"}), 400

    finally:
        # close database connection
        repository.close()



@app.route("/api/check", methods=["GET"])
def quick_check():
    """check if working"""
    return jsonify({"status":"ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)