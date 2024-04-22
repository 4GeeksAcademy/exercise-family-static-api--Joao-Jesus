import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Add the initial family members
jackson_family.add_member({
    'first_name': 'John',
    'age': 33,
    'lucky_numbers': [7, 13, 22]
})

jackson_family.add_member({
    'first_name': 'Jane',
    'age': 35,
    'lucky_numbers': [10, 14, 3]
})

jackson_family.add_member({
    'first_name': 'Jimmy',
    'age': 5,
    'lucky_numbers': [1]
})

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200


@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if member is None:
        return jsonify({"error" : "Member not found"}), 404
    else:
        return jsonify(member), 200


@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = jackson_family.delete_member(id)
    if member is None:
        return jsonify({"error" : "Memeber not found"}), 404
    else:
        return jsonify(member), 200


@app.route('/member', methods=['POST'])
def add_new_member():
    data = request.json  

    # Check if all required fields are present in the request
    required_fields = ['first_name', 'age', 'lucky_numbers']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
        
    # Check if 'id' is provided in the request
    if 'id' in data:
        new_member_id = data['id']
    else:
        # Generate a new random ID
        new_member_id = jackson_family._generateId()

    # Call the add_member method to add the new member
    data['id'] = new_member_id  # Assign the ID to the data
    new_member = jackson_family.add_member(data)
    if new_member is None:
        return jsonify({"error": "Failed to add member"}), 500  # Server error
    else:
        return jsonify({"done" : True, "id": new_member_id}), 200  # Successfully added, return the new member with status code 201


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)