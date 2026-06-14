import unittest

from flaskr import create_app
from models import db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        self.database_user = "postgres"
        self.database_password = "postgres"
        self.database_host = "localhost:5432"
        self.database_path = f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}/{self.database_name}"

        # Create app with the test configuration
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })
        self.client = self.app.test_client()

        # Bind the app to the current context and create all tables
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def setup_questions(self, count=15, category='1'):
        with self.app.app_context():
            for i in range(count):
                Question(question=f'Question {i}', answer=f'Answer {i}', category=category, difficulty=1).insert()

    def test_get_questions_success(self):
        self.setup_questions()
        res = self.client.get('/questions')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 10)
        self.assertEqual(data['total_questions'], 15)

    def test_get_questions_out_of_range_page(self):
        res = self.client.get('/questions?page=1000')
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_question_success(self):
        with self.app.app_context():
            question = Question(question='Test Question', answer='Test Answer', category='1', difficulty=1)
            question.insert()
            question_id = question.id

        res = self.client.delete(f'/questions/{question_id}')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], question_id)

    def test_delete_question_not_found(self):
        res = self.client.delete('/questions/9999')
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_create_question_success(self):
        res = self.client.post('/questions', json={
            'question': 'New Question',
            'answer': 'New Answer',
            'category': '1',
            'difficulty': 1
        })
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['created'])

    def test_create_question_missing_fields(self):
        res = self.client.post('/questions', json={
            'question': 'New Question',
            'answer': 'New Answer',
            # Missing category and difficulty
        })
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_search_questions_success(self):
        with self.app.app_context():
            Question(question='Who is the GOAT in football?', answer='Tom Brady', category='1', difficulty=1).insert()
            Question(question='Who is the GOAT in soccer?', answer='Lionel Messi', category='1', difficulty=1).insert()
            Question(question='How many super bowls did Tom Brady win?', answer='7', category='1', difficulty=2).insert()

        res = self.client.post('/questions', json={'searchTerm': 'goat'})
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['total_questions'], 2)

    def test_search_questions_missing_body(self):
        res = self.client.post('/questions', content_type='application/json')
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_search_questions_no_results(self):
        res = self.client.post('/questions', json={'searchTerm': 'asdfasdf'})
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['total_questions'], 0)

    def test_get_categories_success(self):
        with self.app.app_context():
            db.session.add(Category(type='Science'))
            db.session.commit()

        res = self.client.get('/categories')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['categories']), 1)

    def test_get_questions_by_category_success(self):
        with self.app.app_context():
            category = Category(type='Science')
            db.session.add(category)
            db.session.commit()
            category_id = category.id
            Question(question='Science Q', answer='Science A', category=str(category_id), difficulty=1).insert()

        res = self.client.get(f'/categories/{category_id}/questions')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['total_questions'], 1)
        self.assertEqual(data['current_category'], category_id)

    def test_get_questions_by_category_not_found(self):
        res = self.client.get('/categories/9999/questions')
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_play_quiz_success(self):
        with self.app.app_context():
            Question(question='Q1', answer='A1', category='1', difficulty=1).insert()
            Question(question='Q2', answer='A2', category='1', difficulty=1).insert()

        res = self.client.post('/quizzes', json={
            'previous_questions': [],
            'quiz_category': {'id': 1, 'type': 'Science'}
        })
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['question'])

    def test_play_quiz_no_more_questions(self):
        with self.app.app_context():
            q = Question(question='Q1', answer='A1', category='1', difficulty=1)
            q.insert()
            question_id = q.id

        res = self.client.post('/quizzes', json={
            'previous_questions': [question_id],
            'quiz_category': {'id': 1, 'type': 'Science'}
        })
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNone(data['question'])

    def test_play_quiz_missing_category(self):
        res = self.client.post('/quizzes', json={'previous_questions': []})
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])


if __name__ == "__main__":
    unittest.main()
