from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from firebase import firebase

app = FlaskAPI(__name__)
firebase = firebase.FirebaseApplication('https://proyecto-final-arquitectura.firebaseio.com')


@app.route("/tasks", methods=['GET'])
def get_tasks():
    if request.method == 'GET':
    	tasks = firebase.get('/tasks', None)
        return tasks, status.HTTP_200_OK

@app.route("/tasks/myTasks", methods=['GET'])
def get_my_tasks():
    if request.method == 'GET':
    	tasks = firebase.get('/tasks/myTasks', None)
        return tasks, status.HTTP_200_OK

@app.route("tasks/<int:key>/", methods=['GET'])
def task_detail(key):
    if request.method == 'GET':
        tasks = firebase.get('/tasks', None)
        return tasks, status.HTTP_200_OK

@app.route("tasks/myTasks/<int:key>/", methods=['GET'])
def my_task_detail(key):
    if request.method == 'GET':
        tasks = firebase.get('/tasks', None)
        return tasks, status.HTTP_200_OK

@app.route("/tasks", methods=['POST'])
def post_tasks():
    if request.method == 'POST':
    	new_task = firebase.post('/tasks', {'PyTEST':'Works'})
        return '', status.HTTP_201_CREATED

@app.route("/tasks", methods=['DELETE'])
def delete_task():
    if request.method == 'POST':
    	new_task = firebase.delete('/tasks', {'PyTEST':'Works'})
        return '', status.HTTP_204_NO_CONTENT

if __name__ == "__main__":
    app.run(debug=True)