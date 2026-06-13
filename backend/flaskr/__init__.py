from flask import Flask, jsonify
from flask_cors import CORS

from models import setup_db, db
from .categories_controller import categories_bp
from .questions_controller import questions_bp
from .quizzes_controller import quizzes_bp


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    CORS(app, origins='*')

    with app.app_context():
        db.create_all()

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    app.register_blueprint(categories_bp)
    app.register_blueprint(questions_bp)
    app.register_blueprint(quizzes_bp)

    @app.errorhandler(400)
    @app.errorhandler(404)
    @app.errorhandler(422)
    @app.errorhandler(500)
    def handle_error(error):
        return jsonify({'success': False, 'error': error.code, 'message': error.description}), error.code

    return app
