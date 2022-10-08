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