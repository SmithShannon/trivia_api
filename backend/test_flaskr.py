import os
import unittest
import json
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgresql://{}@{}/{}".format('postgres:abc','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass


    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(len(data['categories']),len(Category.query.all()))


    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(len(data['questions']),10)


    def test_get_questions_with_categories(self):
        res = self.client().get('/questions?current_category=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(len(data['questions']),4)


    def test_create_question(self):
        res = self.client().post('questions/create',json={
            'question':'How many tribes make up the Iroquis nation?',
            'answer':'6',
            'category':4,
            'difficulty':2
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)

    def test_fail_create_question(self):
        res = self.client().post('/questions/create',json={})
        self.assertEqual(res.status_code,422)

    def test_delete_question(self):
        id = Question.query.order_by(Question.id.asc()).all()
        res = self.client().delete('/questions/'+str(id[len(id)-1].id))

        self.assertEqual(res.status_code,200)

    def test_failed_delete_question(self):
        res = self.client().delete('/questions/11')

        self.assertEqual(res.status_code,422)

    def test_get_questions_based_on_search(self):
        res = self.client().post('/questions/search',json={'searchTerm':'how'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(len(data['questions']),2)

    def test_fail_get_questions_based_on_search(self):
        res = self.client().post('/questions/search',json={})
        self.assertEqual(res.status_code,404)

    def test_play(self):
        playing = True
        previous_questions = []
        count = 0
        while playing:
            res = self.client().post('/quizzes',json={'previous_questions':previous_questions,'quiz_category':4})
            data = json.loads(res.data)
            playing = True if data['question'] else False
            self.assertEqual(res.status_code,200)
            if playing:
                self.assertTrue(data['question']['id'] not in previous_questions)
                self.assertEqual(data['question']['category'],4)
                count += 1
                previous_questions.append(data['question']['id'])
        self.assertEqual(count,2)
    def test_404error(self):
        res = self.client().get('/questions?page=10')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['message'],'Not found')

    def test_422error(self):
        res = self.client().delete('/questions/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,422)
        self.assertEqual(data['message'],'Unable to process')




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()