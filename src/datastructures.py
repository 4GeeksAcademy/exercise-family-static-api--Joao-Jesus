from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize the FamilyStructure class with the three specified members
class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1
        self._members = []
        self._initialize_members()

    def _initialize_members(self):
        family_members_data = [
            {"first_name": "John", "age": 33, "lucky_numbers": [7, 13, 22]},
            {"first_name": "Jane", "age": 35, "lucky_numbers": [10, 14, 3]},
            {"first_name": "Jimmy", "age": 5, "lucky_numbers": [1]}
        ]
        for member_data in family_members_data:
            self.add_member(member_data)

    def _generate_id(self):
        return self._next_id

    def add_member(self, member):
        new_id = self._generate_id()
        member_data = {
            'id': new_id,
            'first_name': member['first_name'],
            'last_name': self.last_name,
            'age': member['age'],
            'lucky_numbers': member['lucky_numbers']
        }
        self._members.append(member_data)
        self._next_id += 1

    def delete_member(self, id):
        for index, member in enumerate(self._members):
            if member['id'] == id:
                del self._members[index]
                break

    def get_member(self, id):
        for member in self._members:
            if member['id'] == id:
                return member
        return None

    def get_all_members(self):
        return self._members
