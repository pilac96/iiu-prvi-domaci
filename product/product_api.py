import sqlite3

from flask import request, jsonify, Blueprint
from product.product_model import Product
from db.db_controller import get_db

product_bp = Blueprint("product", __name__)


@product_bp.route('/products', methods=['GET', 'POST', 'DELETE'])
def all_products():
    if request.method == 'GET':
        db = get_db()
        cursor = db.cursor()
        products_raw = cursor.execute('SELECT * FROM Product').fetchall()
        cursor.close()

        products = list()
        for p in products_raw:
            product = Product(*p)
            products.append(product.__dict__)

        return jsonify(products)

    if request.method == 'POST':
        data = request.json

        name = data['Name']
        description = data['Description']
        price = data['Price']
        quantity = data['Quantity']

        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute('INSERT INTO Product (Name, Description, Price, Quantity) VALUES (?, ?, ?, ?)'
                           , (name, description, price, quantity))
            db.commit()
            cursor.close()
            return jsonify({"message": "You successfully added new product in DB"})

        except sqlite3.IntegrityError:
            return jsonify({"message": "You cannot add product with the same name, it should be unique!"})

    if request.method == 'DELETE':
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM Product')
        deleted_rows = cursor.rowcount
        db.commit()
        cursor.close()
        if deleted_rows > 0:
            return jsonify({"message": f"You successfully deleted all products from DB"})
        else:
            return jsonify({"message": f"You failed to delete all products from DB"})


@product_bp.route('/products/<int:product_id>', methods=['GET', 'DELETE', 'PATCH'])
def specific_product(product_id):
    if request.method == 'GET':
        db = get_db()
        cursor = db.cursor()
        data = cursor.execute('SELECT * FROM product WHERE product.Id = ?', (product_id, )).fetchone()
        cursor.close()
        if data:
            product = Product(*data)
            return jsonify(product.__dict__)
        else:
            return jsonify({"message": f"There is no product with id '{product_id}' in DB"})

    if request.method == 'DELETE':
        db = get_db()
        cursor = db.cursor()
        data = cursor.execute('DELETE FROM product WHERE product.Id = ?', (product_id,))
        db.commit()
        cursor.close()
        if data.connection.total_changes > 0:
            return jsonify({"message": f"You successfully deleted product with id '{product_id}' from DB"})
        else:
            return jsonify({"message": f"There is no product with id '{product_id}' in DB"})

    if request.method == 'PATCH':
        data = request.json

        set_keys = ", ".join(f"{key} = ?" for key in data.keys())
        set_values = tuple(data.values())

        db = get_db()
        cursor = db.cursor()
        try:
            data = cursor.execute(f"UPDATE product SET {set_keys} WHERE id = ?", (*set_values, product_id))
            db.commit()
            cursor.close()
            if data.rowcount > 0:
                return jsonify({"message": f"You successfully updated product with id {product_id}"})
            else:
                return jsonify({"message": f"You failed to update product with id {product_id}"})
        except sqlite3.IntegrityError:
            return jsonify({"message": "You cannot update product to have the same name as other product, it should "
                                       "be unique!"})
