# Trivia_API
This project is a RESTful API that serves as a practice module for API Development and Documentation. By completing this project,</br>
I've shown the application of my API development and documentation skills. Structuring and implementing well formatted API endpoints</br> 
that leverage knowledge of HTTP and API development best practices.

The endpoints provide CRUD operations on psql database, and gameplay functionality to clients

### **Getting Started** </br>
* Base URL: At present this app can only be run locally and is not hosted as a base URL</br>The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration
* Authentication: This version of the application does not require authentication or API keys.

### Error Handlers
Errors are returned as JSON objects in the following format:
```javascript
  {
    "error": 400,
    "message": "bad request",
    "success": false
  }
```
The API will return three error types when requests fail:

* 400: Bad Request
* 404: Resource Not Found
* 405: Method Not Allowed
* 422: Not Processable
* 500: Internal Server Error

## Endpoint Library
### GET /questions
* General: </br>
  Returns a list of question objects, success value, categories, and total number of questions </br>
  Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.</br>
* Sample:
```
   curl http://127.0.0.1:5000/questions
```
```javascript
  {
  "categories":{
    "1":"Science",
    "2":"Art",
    "3":"Geography",
    "4":"History",
    "5":"Entertainment",
    "6":"Sports"
    },
  "current_Category":null,
  "questions":[{
    "answer":"Apollo 13",
    "category":5,
    "difficulty":4,
    "id":2,
    "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },{
    "answer":"Tom Cruise",
    "category":5,
    "difficulty":4,
    "id":4,
    "question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },{
    "answer":"Maya Angelou",
    "category":4,
    "difficulty":2,
    "id":5,
    "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },{
    "answer":"Edward Scissorhands",
    "category":5,
    "difficulty":3,
    "id":6,
    "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },{
    "answer":"Muhammad Ali",
    "category":4,
    "difficulty":1,"id":9,
    "question":"What boxer's original name is Cassius Clay?"
    },{
    "answer":"Brazil",
    "category":6,
    "difficulty":3,
    "id":10,
    "question":"Which is the only team to play in every soccer World Cup tournament?"
    },{
    "answer":"Uruguay",
    "category":6,
    "difficulty":4,
    "id":11,
    "question":"Which country won the first ever soccer World Cup in 1930?"
    },{
    "answer":"George Washington Carver",
    "category":4,
    "difficulty":2,
    "id":12,
    "question":"Who invented Peanut Butter?"
    }],
   "success":true,
   "total_questions":10
   }
```

### GET /categories
* General: </br>
  Returns a list of category objects, and success value </br>
* Sample:
```
   curl http://127.0.0.1:5000/categories
```
``` javascript
  {
  "categories":{
    "1":"Science",
    "2":"Art",
    "3":"Geography",
    "4":"History",
    "5":"Entertainment",
    "6":"Sports"
    },
   "success":true
  }
```

### GET /categories/<int:id>/questions
* General: </br>
  Returns a list of questions based on category, and success value </br>
  Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.</br>
* Sample:
``` 
curl http://127.0.0.1:5000/categories/2/questions
```
```javascript
  {
  "current_category":"Art",
  "questions":[{
    "answer":"Escher",
    "category":2,
    "difficulty":1,
    "id":16,
    "question":"Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },{
    "answer":"Mona Lisa",
    "category":2,
    "difficulty":3,
    "id":17,
    "question":"La Giaconda is better known as what?"
    },{
    "answer":"One",
    "category":2,
    "difficulty":4,
    "id":18,
    "question":"How many paintings did Van Gogh sell in his lifetime?"
    },{
    "answer":"Jackson Pollock",
    "category":2,
    "difficulty":2,
    "id":19,
    "question":"Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }],
    "success":true,
    "total_questions":4
   }
```

### POST /questions/create
* General: </br>
  Creates a new question using the submitted question, answer, category, and difficulty. </br>
  Returns all questions including the newly created question, success value, and number of total questions. </br>
* Sample:
``` 
curl http://127.0.0.1:5000/questions/create?page=3 -X POST -H "Content-Type: application/json" -d '{"question":"Whos is the current president of the United States?", "answer":"Joe Biden", "difficulty":"1", "category":"2"}'
```
```javascript
  {
  "categories":{
    "1":"Science",
    "2":"Art",
    "3":"Geography",
    "4":"History",
    "5":"Entertainment",
    "6":"Sports"
    },
  "current_Category":null,
  "questions":[{
    "answer":"Apollo 13",
    "category":5,
    "difficulty":4,
    "id":2,
    "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },{
    "answer":"Tom Cruise",
    "category":5,
    "difficulty":4,
    "id":4,
    "question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    ...
    {
    "answer":"Joe Biden",
    "category":2,
    "difficulty":1,
    "id":25,
    "question":"Whos is the current president of the United States?"
    }],
   "success":true,
   "total_questions":10
   }
```

### DELETE //questions/<int:id>'
* General: </br>
  Deletes a question using the question id if the question exist. </br>
  Returns success value, and a message which states that the specified question has been deleted
* Sample:
``` 
curl -X DELETE http://127.0.0.1:5000/questions/28
```
``` javascript
  {
  "message":"The question  with ID: 28 has been deleted",
  "success":true
  }

```

### POST /quizzes
* General: </br>
  This endpoint should take category and previous question parameter and </br>
  Returns a random question within the given category, if provided, and that is not one of the previous questions </br>
* Sample:
``` 
curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[2], "quiz_category": {"type":"history", "id":"1"}}'
```
```javascript
{
"question":{
  "answer":"Alexander Fleming",
  "category":1,
  "difficulty":3,
  "id":21,
  "question":"Who discovered penicillin?"
  },
 "success":true
}
```
*P.S: All backend code follows PEP8 style guidelines*
