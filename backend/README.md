# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7+** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.
- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database.
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb -h localhost -U postgres trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder run:

```bash
psql -h localhost -U postgres trivia < trivia.psql
```

### Run the Server

From within the `backend` directory, ensure you are working using your created virtual environment, then run:

```bash
export FLASK_APP=flaskr
flask run --debug
```

The `--debug` flag enables auto-reload on file changes and the interactive debugger.

## Testing

To run the tests, first create the test database:

```bash
createdb -h localhost -U postgres trivia_test
```

Then from the `backend` directory run:

```bash
python -m unittest test_flaskr
```

## API Reference

### Base URL

`http://localhost:5000`

### Error Handling

Errors are returned as JSON objects in the following format:

```json
{
  "success": false,
  "error": 404,
  "message": "Not Found"
}
```

The API will return the following error types:

- `400` Bad Request
- `404` Not Found
- `422` Unprocessable Entity
- `500` Internal Server Error

---

### Endpoints

#### `GET /categories`

Fetches all available categories.

- **Request Parameters:** None
- **Response:**

```json
{
  "success": true,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

---

#### `GET /questions`

Fetches a paginated list of questions along with all categories.

- **Request Parameters:**
  - `page` (integer, optional) - Page number, defaults to 1. 10 questions per page.
- **Response:**

```json
{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What is the capital of France?",
      "answer": "Paris",
      "category": "3",
      "difficulty": 1
    }
  ],
  "total_questions": 19,
  "categories": {
    "1": "Science",
    "2": "Art"
  },
  "current_category": null
}
```

- **Errors:** Returns `404` if the page is out of range.

---

#### `DELETE /questions/{question_id}`

Deletes a question by ID.

- **Request Parameters:** None
- **Response:**

```json
{
  "success": true,
  "deleted": 1
}
```

- **Errors:** Returns `404` if the question does not exist.

---

#### `POST /questions`

Creates a new question or searches for questions by search term. The behavior depends on the request body.

**Create a question** — omit `searchTerm`:

- **Request Body:**

```json
{
  "question": "What is the capital of France?",
  "answer": "Paris",
  "category": "3",
  "difficulty": 1
}
```

- **Response:**

```json
{
  "success": true,
  "created": 24
}
```

- **Errors:** Returns `400` if any required fields are missing.

**Search for questions** — include `searchTerm`:

- **Request Body:**

```json
{
  "searchTerm": "capital"
}
```

- **Response:**

```json
{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What is the capital of France?",
      "answer": "Paris",
      "category": "3",
      "difficulty": 1
    }
  ],
  "total_questions": 1,
  "current_category": null
}
```

---

#### `GET /categories/{category_id}/questions`

Fetches all questions for a given category.

- **Request Parameters:** None
- **Response:**

```json
{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What is the capital of France?",
      "answer": "Paris",
      "category": "3",
      "difficulty": 1
    }
  ],
  "total_questions": 1,
  "current_category": 3
}
```

- **Errors:** Returns `404` if the category does not exist.

---

#### `POST /quizzes`

Returns a random question for the quiz that has not been previously asked.

- **Request Body:**

```json
{
  "previous_questions": [1, 2, 3],
  "quiz_category": {
    "id": 1,
    "type": "Science"
  }
}
```

Set `quiz_category.id` to `0` to get questions from all categories.

- **Response:**

```json
{
  "success": true,
  "question": {
    "id": 4,
    "question": "What is the speed of light?",
    "answer": "299,792,458 m/s",
    "category": "1",
    "difficulty": 3
  }
}
```

Returns `question: null` when all questions in the category have been asked.

- **Errors:** Returns `400` if `quiz_category` is missing from the request body.
