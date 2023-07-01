from flask import request, jsonify, Blueprint
from user.user_model import User
from db.db_controller import get_db

user_bp = Blueprint("user", __name__)


@user_bp.route('/users', methods=['GET', 'POST', 'DELETE'])
def all_users():
    if request.method == 'GET':
        db = get_db()
        cursor = db.cursor()
        users_raw = cursor.execute('SELECT * FROM user').fetchall()
        cursor.close()

        users = list()
        for u in users_raw:
            user = User(*u)
            users.append(user.__dict__)

        return jsonify(users)

    if request.method == 'POST':
        data = request.json

        name = data['Name']
        email = data['Email']
        address = data['Address']
        phone_number = data['PhoneNumber']

        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO User (Name, Email, Address, PhoneNumber) VALUES (?, ?, ?, ?)'
                       , (name, email, address, phone_number))

        db.commit()
        cursor.close()
        return jsonify({"message": "You successfully added new user in DB"})

    if request.method == 'DELETE':
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM user')
        deleted_rows = cursor.rowcount
        db.commit()
        cursor.close()

        if deleted_rows > 0:
            return jsonify({"message": f"You successfully deleted all users from DB"})
        else:
            return jsonify({"message": f"You failed to delete all users from DB"})


@user_bp.route('/users/<int:user_id>', methods=['GET', 'DELETE', 'PATCH'])
def specific_user(user_id):
    if request.method == 'GET':
        db = get_db()
        cursor = db.cursor()
        data = cursor.execute('SELECT * FROM user WHERE user.Id = ?', (user_id, )).fetchone()
        cursor.close()
        if data:
            user = User(*data)
            return jsonify(user.__dict__)
        else:
            return jsonify({"message": f"There is no user with id '{user_id}' in DB"})

    if request.method == 'DELETE':
        db = get_db()
        cursor = db.cursor()
        data = cursor.execute('DELETE FROM user WHERE user.Id = ?', (user_id,))
        db.commit()
        cursor.close()
        if data.connection.total_changes > 0:
            return jsonify({"message": f"You successfully deleted user with id '{user_id}' from DB"})
        else:
            return jsonify({"message": f"There is no user with id '{user_id}' in DB"})

    if request.method == 'PATCH':
        data = request.json

        set_keys = ", ".join(f"{key} = ?" for key in data.keys())
        set_values = tuple(data.values())

        db = get_db()
        cursor = db.cursor()
        data = cursor.execute(f"UPDATE user SET {set_keys} WHERE user.id = ?", (*set_values, user_id))
        db.commit()
        cursor.close()
        if data.rowcount > 0:
            return jsonify({"message": f"You successfully updated user with id {user_id}"})
        else:
            return jsonify({"message": f"You failed to update user with id {user_id}"})
