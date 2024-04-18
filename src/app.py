import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

# Add family members directly within the Flask application code




# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
def add_member():
    member_data = request.json
    jackson_family.add_member(member_data)
    return jsonify({"message": "Member added successfully"}), 201


# GET route to retrieve all members
@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify({"members": members}), 200

# GET route to retrieve a single member by ID
@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"message": "Member not found"}), 404

# DELETE route to delete a member by ID
@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    jackson_family.delete_member(id)
    return jsonify({"message": "Member deleted successfully"}), 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

