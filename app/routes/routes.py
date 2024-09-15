from flask import request,jsonify
from app import app
from app.models.models import User
#AAdded routing for the user table
@app.route('/')
def index():
    return "status:connected"

@app.route('/users',methods=['GET'])
def get_users():
    user_model = User()
    users = user_model.get_all_users()
    user_model.close()
    return jsonify(users)

@app.route('/addUser',methods=['POST'])
def add_user():
    data=request.json
    user_model = User()
    user_id=user_model.create_user(first_name=data['firstName'],
                                   last_name=data['lastName'],
                                   email=data['email'],
                                   password=data['password'],
                                   role_id=data['roleId'],
                                   phone_number=data['phoneNumber'],
                                   dob=data['DOB'],
                                   street_address=data['streetAdd'],
                                   city=data['city'],
                                   pincode=data['pincode'],
                                   country=data['country'],
                                   created_by=data['createdBy'])
    user_model.close()
    return jsonify({"message": "User added", "userID": user_id})

@app.route('/updateuser/<int:userId>',method=['PUT'])
def update_user(userId):
    data=request.json
    user_model = User()
    updatedCount=user_model.update_user(user_id=userId,**data)
    user_model.close()
    return jsonify({"message": f"Updated {updatedCount} user(s)"})

@app.route('/delete_user/<int:user_id>',method=['DELETE'])
def delete_user(user_id):
    user_model = User()
    user_model.delete_user(user_id)
    user_model.close()
    return f"Deleted user {user_id}"

@app.route('/search_user/<int:user_id>', methods=['GET'])
def search_user(user_id):
    user_model = User()
    user = user_model.get_user_by_id(user_id)
    user_model.close()
    return jsonify(user) if user else ("User not found", 404)