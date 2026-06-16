from flask import Blueprint, request, abort, jsonify
from models import Question, Category

questions_bp = Blueprint('questions', __name__)

QUESTIONS_PER_PAGE = 10


@questions_bp.route('/questions', methods=['GET'])
def get_questions():
    page = request.args.get('page', 1, type=int)
    questions = Question.query.paginate(page=page, per_page=QUESTIONS_PER_PAGE).items
    categories = {category.id: category.type for category in Category.query.all()}
    return jsonify({
        'success': True,
        'questions': [question.format() for question in questions],
        'total_questions': Question.query.count(),
        'categories': categories,
        'current_category': None
    })


@questions_bp.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    question = Question.query.get(question_id)
    if question is None:
        abort(404)
    question.delete()
    return jsonify({
        'success': True,
        'deleted': question_id
    })


@questions_bp.route('/questions', methods=['POST'])
def create_or_search_questions():
    request_body = request.get_json()
    if request_body is None:
        abort(400)
    search_term = request_body.get('searchTerm')

    if search_term is not None:
        return _search_questions(request_body)
    else:
        return _create_question(request_body)


def _create_question(request_body):
    question = request_body.get('question')
    answer = request_body.get('answer')
    category = request_body.get('category')
    difficulty = request_body.get('difficulty')

    if not question or not answer or not category or difficulty is None:
        abort(400)

    new_question = Question(
        question=question,
        answer=answer,
        category=category,
        difficulty=difficulty
    )
    new_question.insert()
    return jsonify({
        'success': True,
        'created': new_question.id
    }), 201


def _search_questions(request_body):
    search_term = request_body.get('searchTerm', '')
    questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
    return jsonify({
        'success': True,
        'questions': [question.format() for question in questions],
        'total_questions': len(questions),
        'current_category': None
    })
