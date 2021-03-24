import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10
picked_questions = []
def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions
def search_picked_questions(picked_questions, previous_questions):
    search = False
    for question in picked_questions:
        for prev_question in previous_questions:
            if question == prev_question:
                search = True
                return search
    return search
def empty_full_list(picked_questions):
    MAX_LENGTH = 5
    if len(picked_questions) >= MAX_LENGTH:
        picked_questions.clear()
    return picked_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # '''
    # `/categories/${id}/questions`
    # @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    # '''
    CORS(app)

    '''
    after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'ContentType, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, PUT, DELETE, OPTIONS')
        return response

#--------Endpoints--------------------------------------------------------------

    '''
    Endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.

    '''
    '''
    POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''

    @app.route('/questions', methods = ['GET', 'POST'])
    def questions():
        categories = Category.query.all()
        if request.method == 'GET':
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)
            if len(current_questions) == 0:
                abort(404)
            elif len(current_questions) > 0:
                return jsonify({
                    'success': True,
                    'questions' : current_questions,
                    'total_questions' : len(current_questions),
                    'categories' : {category.id:category.type for category in categories},
                    'current_Category': None
                })
        if request.method == 'POST':
            if request.is_json:
                search_term=request.get_json()['searchTerm']
                search_term = "%{}%".format(search_term)
                question = Question.query.filter(Question.question.ilike(search_term)).all()
                current_questions = paginate_questions(request, question)
                print(current_questions)
                if question == 0:
                    abort(404)
                else:
                    return jsonify({
                        'success': True,
                        'questions' : current_questions,
                        'total_questions' : len(question),
                        'categories' : {category.id:category.type for category in categories},
                        'current_Category': None
                    })
            else:
                abort(400)

    '''
    Endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories', methods = ['GET'])
    def get_categories():
        selection = Category.query.all()
        categories = {category.id:category.type for category in selection}
        if len(categories) == 0:
            abort(404)
        return jsonify({
        'success': True,
        'categories': categories
        })

    '''
    GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/categories/<int:id>/questions', methods = ['GET'])
    def get_questions_per_category(id):
        print(id)
        category = Category.query.get(id)
        questions = Question.query.filter(Question.category == id).all()
        paginated_questions = paginate_questions(request, questions)
        if len(questions) == 0:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'questions': paginated_questions,
                'total_questions': len(questions),
                'current_category': category.type
            })


    '''
    Endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    '''
    @app.route('/questions/create', methods = ['POST'])
    def create_question():
        body = request.get_json()
        question = body.get('question')
        answer = body.get('answer')
        difficulty = body.get('difficulty')
        category = body.get('category')

        try:
            new_question = Question(
            question = question,
            answer = answer,
            difficulty = difficulty,
            category = category)

            new_question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
            'success' : True,
            'question' : current_questions,
            'total_questions': len(Question.query.all())
            })

        except:
            abort(422)
            db.session.rollback()
        finally:
            db.session.close()



    @app.route('/questions/<int:id>', methods = ['DELETE'])
    def delete_question(id):
        question = Question.query.filter(Question.id==id)
        if question is None:
            abort(404)
        else:
            try:
                question.delete()
            except:
                db.session.rollback()
                abort(404)
            finally:
                db.session.close()
            return jsonify({
                'success': True,
                'message': 'The following question {} \nhas been deleted'.format(question)
            })

        '''
        POST endpoint to get questions to play the quiz.
        This endpoint should take category and previous question parameters
        and return a random questions within the given category,
        if provided, and that is not one of the previous questions.

        TEST: In the "Play" tab, after a user selects "All" or a category,
        one question at a time is displayed, the user is allowed to answer
        and shown whether they were correct or not.
        '''

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()
        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', None)
        empty_full_list(picked_questions)
        check = search_picked_questions(picked_questions, previous_questions)
        if check == False:
            if quiz_category['id'] == 0:
                questions = Question.query.all()
                question = random.choice(questions)
            elif quiz_category['id'] != 0:
                questions = Question.query.filter(Question.category == quiz_category['id']).all()
                if questions == []:
                    abort(404)
                else:
                    question = random.choice(questions)
                formatted_question = question.format()
                picked_questions.append(formatted_question['id'])
                return jsonify({
                    'success': True,
                    'question': formatted_question
                })

        else:
            questions = Question.query.filter(~Question.id.in_(question for question in previous_questions))
            if quiz_category['id'] == 0:
                questions = questions.all()
                question = random.choice(questions)
            elif quiz_category['id'] != 0:
                questions = questions.filter(Question.category == quiz_category['id']).all()
                if questions == []:
                    abort(404)
                elif questions:
                    question = random.choice(questions)
                formatted_question = question.format()
                picked_questions.append(formatted_question['id'])
                return jsonify({
                    'success': True,
                    'question': formatted_question
                })

#-----------Error Handlers------------------------------------------------------
    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
        'success': False,
        'error': 400,
        'message': "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
        'success': False,
        'error': 404,
        'message': "resource not found"
        }), 404
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        'success': False,
        'error': 422,
        'message': "unprocessable entity"
        }), 422
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
        'success': False,
        'error': 400,
        'message': "bad request"
        }), 400

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
        'success': False,
        'error': 405,
        'message': "method not allowed"
        }), 405
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
        'success': False,
        'error': 500,
        'message': "internal server error"
        }), 500

    return app
