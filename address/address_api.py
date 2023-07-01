import sqlite3

from flask import request, jsonify, Blueprint
from address.address_model import Address
from db.db_controller import get_db

address_bp = Blueprint("address", __name__)


@address_bp.route('/address', methods=['GET', 'POST', 'DELETE'])
def all_addresses():
    if request.method == 'GET':
        db = get_db()
        cursor = db.cursor()
        address_raw = cursor.execute('SELECT * FROM Address').fetchall()
        cursor.close()

        addresses = list()
        for a in address_raw:
            address = Address(*a)
            addresses.append(address.__dict__)

        return jsonify(addresses)

    if request.method == 'POST':
        data = request.json

        country = data['Country']
        city = data['City']
        street = data['Street']
        postal_code = data['PostalCode']

        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute('INSERT INTO Address (Country, City, Street, PostalCode) VALUES (?, ?, ?, ?)'
                           , (country, city, street, postal_code))

            db.commit()
            cursor.close()
            return jsonify({"message": "You successfully added new address in DB"})

        except sqlite3.IntegrityError:
            return jsonify({"message": "You cannot add address with the same Street Name, it should be unique!"})

    if request.method == 'DELETE':
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM Address')
        deleted_rows = cursor.rowcount
        db.commit()
        cursor.close()
        if deleted_rows > 0:
            return jsonify({"message": f"You successfully deleted all addresses from DB"})
        else:
            return jsonify({"message": f"You failed to delete all addresses from DB"})


@address_bp.route('/address/<int:address_id>', methods=['GET', 'DELETE', 'PATCH'])
def specific_address(address_id):
    if request.method == 'GET':
        db = get_db()
        cursor = db.cursor()
        data = cursor.execute('SELECT * FROM address WHERE address.Id = ?', (address_id, )).fetchone()
        cursor.close()
        if data:
            address = Address(*data)
            return jsonify(address.__dict__)
        else:
            return jsonify({"message": f"There is no address with id '{address_id}' in DB"})

    if request.method == 'DELETE':
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM address WHERE address.Id = ?', (address_id,))
        deleted_rows = cursor.rowcount
        db.commit()
        cursor.close()
        if deleted_rows > 0:
            return jsonify({"message": f"You successfully deleted address with id '{address_id}' from DB"})
        else:
            return jsonify({"message": f"There is no address with id '{address_id}' in DB"})

    if request.method == 'PATCH':
        data = request.json

        set_keys = ", ".join(f"{key} = ?" for key in data.keys())
        set_values = tuple(data.values())

        db = get_db()
        cursor = db.cursor()
        try:
            data = cursor.execute(f"UPDATE address SET {set_keys} WHERE id = ?", (*set_values, address_id))
            db.commit()
            cursor.close()
            if data.rowcount > 0:
                return jsonify({"message": f"You successfully updated address with id {address_id}"})
            else:
                return jsonify({"message": f"You failed to update address with id {address_id}"})

        except sqlite3.IntegrityError:
            return jsonify({"message": "You cannot update address to have the same street name as other address, "
                                       "it should be unique!"})
