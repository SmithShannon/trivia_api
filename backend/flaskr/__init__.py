import os
import sys

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_cors import CORS
import random
import json

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
CURRENT_CATEGORY = None

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app,resource={'/*':{'origins':'*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers','Content-Type,true')
        response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories',methods=['GET'])
    def get_categories():
        cats = Category.query.all()
        json = {}
        for cat in cats:
            json[str(cat.id)] = cat.type
        return jsonify({'categories': json})

    @app.route('/questions',methods=['GET'])
    def get_questions():
        #Combined getQuestions with get Questions by Category
        try:
            page = int(request.args.get('page',1))
            start = QUESTIONS_PER_PAGE*(page-1)
            end = QUESTIONS_PER_PAGE*page

            current_category = None if request.args.get('current_category',None) in ['null','undefined'] else request.args.get('current_category',None)
            print(current_category)

            questions = Question.query.order_by(Question.id.asc())
            if current_category is None:
                questions = questions.all()
            else:
                questions = questions.filter_by(category=current_category).all()

            qlist = []
            for q in questions[start:end]:
                qlist.append(q.format())
            cats = {}
            for c in Category.query.all():
                cats[c.id] = c.type
            return jsonify({
                'questions':qlist,
                'total_questions':len(questions),
                'categories':cats,
                'current_category':current_category
            })
        except:
            print(sys.exc_info())

    @app.route('/questions/<question_id>',methods=['DELETE'])
    def delete_question(question_id):
        try:
            Question.query.filter_by(id=question_id).first().delete()
            return get_questions()
        except:
            print(sys.exc_info())


    @app.route('/questions/create',methods=['POST'])
    def create_question():
        try:
            form = json.loads(request.data)
            question = Question(question=form['question'],answer=form['answer'],difficulty=form['difficulty'],category=int(form['category']))
            question.insert()
            return get_questions()
        except:
            print(sys.exc_info())

    @app.route('/questions/search',methods=['POST'])
    def get_questions_based_on_search():
        try:
            keyword = json.loads(request.data)
            questions = Question.query.filter(func.lower(Question.question).contains(keyword['searchTerm'].lower())).all()
            data = []
            for q in questions:
                data.append(q.format())
            return jsonify({
                'questions':data,
                'total_questions':len(questions),
                'current_category':CURRENT_CATEGORY
            })

        except:
            print(sys.exc_info())

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quizzes',methods=['POST'])
    def play():
        pass

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

