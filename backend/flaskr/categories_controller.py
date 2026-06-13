from flask import Blueprint, jsonify
from models import Category, Question

categories_bp = Blueprint('categories', __name__)


@categories_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    formatted_categories = {category.id: category.type for category in categories}
    return jsonify({
        'success': True,
        'categories': formatted_categories
    })


@categories_bp.route('/categories/<int:category_id>/questions', methods=['GET'])
def get_questions_for_category(category_id):
    questions = Question.query.filter(Question.category == str(category_id)).all()
    return jsonify({
        'success': True,
        'questions': [question.format() for question in questions],
        'total_questions': len(questions),
        'current_category': category_id
    })
