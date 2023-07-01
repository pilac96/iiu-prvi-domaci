from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


def create_app():
    from address.address_api import address_bp
    from product.product_api import product_bp
    from user.user_api import user_bp
    app.register_blueprint(address_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(user_bp)
    return app


if __name__ == '__main__':
    create_app().run(port=8000, debug=True)

