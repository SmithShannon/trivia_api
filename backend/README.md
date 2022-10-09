# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

`GET '/questions'`

- Fetches a json object with a list of questions at the specified page / set of indexes for the selected category
- Request Arguments:
- - `page` - the page segment requested.  Defaults to 1
- - `current_category` - the category to filter by.  Defaults to null/None.  If null assumes all categories
- Returns a json with as keys:
- - `questions` - the list of questions from the page segment, ordered by question id
- - `total_questions` - the total number of questions in the selected category
- - `categories` - all the categories available (as returned by `GET '/categories`)
- - `current_category` - the selected category
- Throws error 404 if there are no questions within the selected page segment or if the category is invalid.

Sample Request

`/questions?page=1&current_category=2`

Sample Response

```json
{
  "categories": {
    "1":"Science",
    "2":"Art",
    "3":"Geography",
    "4":"History",
    "5":"Entertainment",
    "6":"Sports"
  },
  "current_category":"2",
  "questions":[
    {
      "answer":"Escher",
      "category":"2",
      "difficulty":"1",
      "id": "16",
      "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
    },
    {
      "answer":"Mona Lisa",
      "category": "2",
      "difficulty": "3",
      "id": "17",
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": "2",
      "difficulty": "4",
      "id": "18",
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category":"2",
      "difficulty": "2",
      "id":"19",
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
      "total_questions":"4"
}
```

`DELETE '/questions/{$question_id}'`

- Deletes from the database the question of the given ID
- Request Argument: question_id - the id of the question being deleted
- Returns a message saying it has been done
- Throws error 422 if given an ID that does not exist

Sample Request

`/questions/14`

Sample Response

```json
{
  "message": "Deleted"
}
```

`POST '/questions/create'`

- Creates a new question
- Request Arguments:
- - `question` - the text of the question
- - `answer` - the text of the question's answer
- - `difficulty` - the question's difficulty
- - `category` - the id of the category
- Returns None
- Throws error 422 if given empty fields

Sample Request Body:

```json
{
  "question": "Who was the first host of Jeopardy?",
  "answer":"Alex Trebak",
  "difficulty": "2",
  "category": "5"
}
```

`POST '/questions/search'`

- Searches for question containing a keyword. Search is case insensitive.
- Request Argument: `searchTerm` - the keyword being searched on
- Returns: list of questions

Sample Request Body:

```json
{
  "searchTerm": "How"
}
```

Sample Response:

```json
{
  "current_category": null, 
  "questions": [
    {
      "answer": "One",
      "category": "2",
      "difficulty": "4", 
      "id": "18", 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "six", 
      "category": "5", 
      "difficulty": "4", 
      "id": "29", 
      "question": "How mant sages are in Legend of Zelda Ocarina of Time?"
    }
    ], 
      "total_questions": "2"
}
```

`POST '/quizzes'`

- Called to play the game.  One question is returned on every call.  Previous questions are passed to avoid repeats
- Request Arguments:
- - `previous_questions` - an array containing the ids of previously asked questions
- - `quiz_category` - the category that is being filtered for
- Returns `question`, with a json of a question, or False if there are no more questions

Sample Request Body:

```json
{
  "previous_questions": [],
  "quiz_category": 4
}
```
Sample Return:

```json
{
  "question": {
    "answer": "Scarab",
    "category": "4", 
    "difficulty": "4", 
    "id": "23", 
    "question": "Which dung beetle was worshipped by the ancient Egyptians?"}
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
