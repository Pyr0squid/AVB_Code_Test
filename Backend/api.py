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
        repository.insert_contact(contact)

        # return contact instance to caller
        return jsonify({"message": "New Contact Added Successfully"}), 201
    
    except:

        return jsonify({"error": "Failed to Insert Contact in Database"}), 400

    finally:
        # close database connection
        repository.close()

@app.route("/api/contacts", methods=["POST"])
def add_address():
    """insert_address"""

    # retrieve POST request
    data = request.get_json()

    # validate data for required fields
    required_fields = ["id", "address"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields: id, address"}), 400

    # process data by replacing empty string values with None
    clean_data = {k: (v if v != "" else None) for k, v in data.items()}

    # validate email address formatting

    try:
        # create repository and insert new address
        repository = Repository()
        repository.insert_address(clean_data['id'], clean_data['address'])

        # return contact instance to caller
        return jsonify({"message": "New Email Address Added Successfully"}), 201
    
    except:

        return jsonify({"error": "Failed to Insert Email Address in Database"}), 400

    finally:
        # close database connection
        repository.close()

@app.route("/api/contacts", methods=["POST"])
def update_contact():
    """update_contact"""

    # retrieve POST request
    data = request.get_json()

    # validate data for required fields
    required_fields = ["id"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields: id"}), 400

    # process data by replacing empty string values with None
    clean_data = {k: (v if v != "" else None) for k, v in data.items()}

    # validate email address and birthday formatting

    try:
        # create repository and update contact
        repository = Repository()
        repository.update(id=clean_data['id'], first_name=clean_data['first_name'], 
                                     middle_name_init=clean_data['middle_name_init'],
                                     last_name=clean_data['last_name'], birthday=clean_data['birthday'])

        # get contact instance from repository
        new_contact = repository.get_by_id(clean_data['id'])

        # return contact instance to caller
        return jsonify({new_contact.__dict__}), 200
    
    except:

        return jsonify({"error": "Failed to Insert Contact in Database"}), 400

    finally:
        # close database connection
        repository.close()

@app.route("/api/contacts", methods=["POST"])
def delete_contact():
    """delete_contact"""

    # retrieve POST request
    data = request.get_json()

    # validate data for required fields
    required_fields = ["id"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields: id"}), 400

    # process data by replacing empty string values with None
    clean_data = {k: (v if v != "" else None) for k, v in data.items()}

    try:
        # create repository and delete contact
        repository = Repository()
        repository.delete_contact(id=clean_data['id'])

        # send data to caller
        return jsonify({"message": "Contact Successfully Deleted"}), 200
    
    except:

        return jsonify({"error": "Failed to Insert Contact in Database"}), 400

    finally:
        # close database connection
        repository.close()

@app.route("/api/contacts", methods=["POST"])
def delete_address():
    """delete_address"""

    # retrieve POST request
    data = request.get_json()

    # validate data for required fields
    required_fields = ["id", "address"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields: id, address"}), 400

    # process data by replacing empty string values with None
    clean_data = {k: (v if v != "" else None) for k, v in data.items()}

    try:
        # create repository and delete contact
        repository = Repository()
        repository.delete_address(id=clean_data['id'], address=clean_data['address'])

        # send data to caller
        return jsonify({"message": "Email Address Successfully Deleted"}), 200
    
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