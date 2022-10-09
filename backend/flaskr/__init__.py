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
        try:
            cats = Category.query.all()
            json = {}
            for cat in cats:
                json[str(cat.id)] = cat.type
            return jsonify({'categories': json})
        except:
            print(sys.exc_info())
            abort(404)

    @app.route('/questions',methods=['GET'])
    def get_questions():
        #Combined getQuestions with get Questions by Category
        try:
            page = int(request.args.get('page',1))
            start = QUESTIONS_PER_PAGE*(page-1)
            end = QUESTIONS_PER_PAGE*page

            current_category = None if request.args.get('current_category',None) in ['null','undefined'] else request.args.get('current_category',None)

            questions = Question.query.order_by(Question.id.asc())
            if current_category is None:
                questions = questions.all()
            else:
                questions = questions.filter_by(category=current_category).all()

            qlist = []

            if len(questions[start:end]) == 0:
                abort(404)

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
            abort(404)

    @app.route('/questions/<question_id>',methods=['DELETE'])
    def delete_question(question_id):
        try:
            q = Question.query.filter_by(id=question_id).first()
            if q is None:
                abort(422)
            q.delete()
            return jsonify({'message':'Deleted'})
        except:
            print(sys.exc_info())
            abort(422)


    @app.route('/questions/create',methods=['POST'])
    def create_question():
        try:
            form = json.loads(request.data)
            question = Question(question=form['question'],answer=form['answer'],difficulty=form['difficulty'],category=int(form['category']))
            question.insert()
            return get_questions()
        except:
            print(sys.exc_info())
            abort(422)

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
                'current_category':None
            })

        except:
            print(sys.exc_info())
            abort(404)


    @app.route('/quizzes',methods=['POST'])
    def play():
        try:
            r = json.loads(request.data)
            questions = Question.query.order_by(Question.id.asc())
            if r['quiz_category'] != 0:
                questions = questions.filter_by(category=r['quiz_category']['id'])
            questions = questions.filter(Question.id.notin_(r['previous_questions'])).all()
            if len(questions) == 0:
                return jsonify({
                    "question": False
                })
            else:
                return jsonify({
                    "question":questions[random.randint(0,len(questions)-1)].format()
                })
        except:
            print(sys.exc_info())
            abort(404)



    @app.errorhandler(404)
    def error_404(error):
        return jsonify({
            'success':False,
            'error':404,
            'message':"Not found"
        }), 404

    @app.errorhandler(422)
    def error_422(error):
        return jsonify({
            'success':False,
            'error':422,
            'message':"Unable to process"
        }), 422

    return app

