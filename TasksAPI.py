from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from firebase import firebase
import pprint

app = FlaskAPI(__name__)
firebase = firebase.FirebaseApplication('https://proyecto-final-arquitectura.firebaseio.com')

@app.route("/tasks", methods=['GET'])
def get_tasks():
    if request.method == 'GET':
        print('about to fetch to firebase')
    	tasks = firebase.get('/tasks', None)
        if tasks === None:
            return status.HTTP_204_NO_CONTENT
        return tasks, status.HTTP_200_OK

@app.route("/tasks", methods=['POST', 'DELETE'])
def post_tasks():
    title =  request.data.get('title','')
    description = request.data.get('description','')
    dueDate = request.data.get('dueDate','')
    reminder = request.data.get('reminder','')

    if request.method == 'POST':
        new_task = firebase.post('/tasks', {
                                            'title': title,
                                            'description': description,
                                            'dueDate': dueDate,
                                            'reminder': reminder
                                           })
        return firebase.get('/tasks',1), status.HTTP_201_CREATED

@app.route("/tasks", methods=['DELETE'])
def delete_task():
    if request.method == 'DELETE': 
        new_task = firebase.delete('/tasks', {'PyTEST':'Works'})
        return '', status.HTTP_204_NO_CONTENT

@app.route("/tasks/myTasks", methods=['GET'])
def get_my_tasks():
    if request.method == 'GET':
    	tasks = firebase.get('/tasks/myTasks', None)
        return tasks, status.HTTP_200_OK

@app.route("/tasks/<int:key>/", methods=['GET'])
def task_detail(key):
    if request.method == 'GET':
        tasks = firebase.get('/tasks', None)
        return tasks, status.HTTP_200_OK

@app.route("/tasks/myTasks/<int:key>/", methods=['GET'])
def my_task_detail(key):
    if request.method == 'GET':
        tasks = firebase.get('/tasks', None)
        return tasks, status.HTTP_200_OK

if __name__ == "__main__":
    app.run(debug=True)