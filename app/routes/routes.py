from app import app
from app.models import User
# just a template, we have to create it custom
@app.route('/users')
def get_users():
    user_model = User()
    users = user_model.get_all_users()
    user_model.close()
    return f"Users: {users}"

@app.route('/add_user/<username>/<email>')
def add_user(username, email):
    user_model = User()
    user_model.create_user(username, email)
    user_model.close()
    return f"Added user {username}"

@app.route('/update_user/<user_id>/<new_email>')
def update_user(user_id, new_email):
    user_model = User()
    user_model.update_user(user_id, new_email)
    user_model.close()
    return f"Updated user {user_id} with new email {new_email}"

@app.route('/delete_user/<user_id>')
def delete_user(user_id):
    user_model = User()
    user_model.delete_user(user_id)
    user_model.close()
    return f"Deleted user {user_id}"
