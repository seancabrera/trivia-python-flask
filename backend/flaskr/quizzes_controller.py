from flask import Blueprint, request, abort, jsonify
import random
from models import Question

quizzes_bp = Blueprint('quizzes', __name__)


@quizzes_bp.route('/quizzes', methods=['POST'])
def play_quiz():
    request_body = request.get_json()
    previous_questions = request_body.get('previous_questions', [])
    quiz_category = request_body.get('quiz_category')

    if quiz_category is None:
        abort(400)

    category_id = quiz_category.get('id')

    if category_id == 0:
        questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
    else:
        questions = Question.query.filter(
            Question.category == str(category_id),
            Question.id.notin_(previous_questions)
        ).all()

    if questions:
        random_question = random.choice(questions)
        return jsonify({
            'success': True,
            'question': random_question.format()
        })
    else:
        return jsonify({
            'success': True,
            'question': None
        })
