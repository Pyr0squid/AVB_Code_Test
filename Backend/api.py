from flask import Flask, jsonify, request
from flask_cors import CORS
from Backend.Model.contact import Contact, Repository 
from pathlib import Path

app = Flask(
    __name__,
    template_folder=str("../Frontend/templates"),
    static_folder=str("../Frontend/static"),
    static_url_path="/static"
)

CORS(app, resources={r"/api/*": {"origins": "*"}})

# set database path in flask configuration files
ABS_PATH = Path(__file__).resolve().parent.parent
app.config["DATABASE"] = ABS_PATH / "Backend/Database/database.db"

@app.route("/api/retrieve/<int:contact_id>", methods=["GET"])
def get_by_id(contact_id):
    """fetch contact"""

    # open database repository
    repository = None
    repository = Repository(app.config["DATABASE"])

    try:
        # retrieve contact by id
        contact = repository.get_by_id(contact_id)

        # send contact data to caller
        return jsonify(contact.to_dict()), 200

    except Exception as e:
        app.logger.exception(e)
        return jsonify({"error": "Failed to Retrieve Contact"}), 400

    finally:
        # close database connection
        if repository is not None:
            repository.close()

@app.route("/api/names", methods=["GET"])
def get_all_names():
    """fetch_all_contacts_names"""
    # open database repository
    repository = None
    repository = Repository(app.config["DATABASE"])

    try:
        # retrieve list of contacts names
        contacts = repository.get_all_names()

        # send data to caller
        return jsonify(contacts), 200
    
    except Exception as e:
        app.logger.exception(e)
        return jsonify({"error": "Failed to Retrieve Contact Names"}), 400

    finally:
        # close database connection
        if repository is not None:
            repository.close()

@app.route("/api/add/contact", methods=["POST"])
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
        e_addresses=set(clean_data.get("e_addresses")) if clean_data.get("e_addresses") is not None else None
    )

    repository = None
    try:
        # create repository and insert new contact
        repository = Repository(app.config["DATABASE"])
        repository.insert_contact(contact)

        # return contact instance to caller
        return jsonify({"message": "New Contact Added Successfully"}), 201
    
    except Exception as e:
        app.logger.exception(e)

        return jsonify({"error": "Failed to Insert Contact in Database"}), 400

    finally:
        # close database connection
        if repository is not None:
            repository.close()

@app.route("/api/add/address", methods=["POST"])
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

    repository = None
    try:
        # create repository and insert new address
        repository = Repository(app.config["DATABASE"])
        repository.insert_address(clean_data['id'], clean_data['address'])

        # return contact instance to caller
        return jsonify({"message": "New Email Address Added Successfully"}), 201
    
    except Exception as e:
        app.logger.exception(e)

        return jsonify({"error": "Failed to Insert Email Address in Database"}), 400

    finally:
        # close database connection
        if repository is not None:
            repository.close()

@app.route("/api/update", methods=["POST"])
def update_contact():
    """update_contact"""

    # retrieve POST request
    data = request.get_json()

    # validate data for required fields
    required_fields = ["id"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields: id"}), 400

    # process data by replacing empty string values with None, add in keys that are missing from request
    clean_data = {k: (v if v != "" else None) for k, v in data.items()}
    fields = ["first_name", "middle_name_init", "last_name", "birthday"]
    for field in fields:
        if field not in clean_data.keys():
            clean_data[field] = None

    # validate email address and birthday formatting

    repository = None
    try:
        # create repository and update contact
        repository = Repository(app.config["DATABASE"])
        repository.update(id=clean_data['id'], first_name=clean_data['first_name'], 
                                     middle_name_init=clean_data['middle_name_init'],
                                     last_name=clean_data['last_name'], birthday=clean_data['birthday'])

        # return contact instance to caller
        return jsonify({"message": "Contact Updated Successfully"}), 200
    
    except Exception as e:
        app.logger.exception(e)
        return jsonify({"error": "Failed to Update Contact in Database"}), 400

    finally:
        # close database connection
        if repository is not None:
            repository.close()

@app.route("/api/delete/contact", methods=["POST"])
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

    repository = None
    try:
        # create repository and delete contact
        repository = Repository(app.config["DATABASE"])
        repository.delete_contact(id=clean_data['id'])

        # send data to caller
        return jsonify({"message": "Contact Successfully Deleted"}), 200
    
    except Exception as e:
        app.logger.exception(e)
        return jsonify({"error": "Failed to Insert Contact in Database"}), 400

    finally:
        # close database connection
        if repository is not None:
            repository.close()

@app.route("/api/delete/address", methods=["POST"])
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

    repository = None
    try:
        # create repository and delete contact
        repository = Repository(app.config["DATABASE"])
        repository.delete_address(id=clean_data['id'], address=clean_data['address'])

        # send data to caller
        return jsonify({"message": "Email Address Successfully Deleted"}), 200
    
    except Exception as e:
        app.logger.exception(e)
        return jsonify({"error": "Failed to Insert Contact in Database"}), 400

    finally:
        # close database connection
        if repository is not None:
            repository.close()

@app.route("/api/check", methods=["GET"])
def quick_check():
    """check if working"""
    return jsonify({"status":"ok"}), 200

def run():
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    run()