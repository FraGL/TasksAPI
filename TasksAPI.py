from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from firebase import firebase
import urllib2
import pprint
import json

app = FlaskAPI(__name__)
firebase = firebase.FirebaseApplication('https://proyecto-final-arquitectura.firebaseio.com')

@app.route("/tasks", methods=['GET']) #Shows all TASKS || UT missing || DONE
def get_tasks():
    if request.method == 'GET':
        print('about to fetch to firebase')
    	tasks = firebase.get('/tasks', None)
        if tasks == None:
            return status.HTTP_401_UNAUTHORIZED
        return tasks, status.HTTP_200_OK

@app.route("/tasks/<string:userToken>/", methods=['POST']) #Creates a new TASK || UT missing || DONE
def post_tasks(userToken):
    title =  request.data.get('title','')
    description = request.data.get('description','')
    dueDate = request.data.get('dueDate','')
    hourReminder = request.data.get('hourReminder','')
    dateReminder = request.data.get('dateReminder','')

    userData = urllib2.urlopen("https://guarded-anchorage-21945.herokuapp.com/decodeToken/"+userToken).read()
    print('what I get from Isaac is ========= '+userData)
    #userJSON = json.dumps(userData)
    #userDict = json.loads(userJSON)
    #print('userDict es ========= '+ userDict)
    #userUID = userDict.get('uid','NOT FOUND')
    print(len(userData))
    userUID_dirty = ''
    userUID_clean = ''
    for x in range(377, len(userData)): #pos: 377 es donde empieza el uid
        userUID_dirty+= userData[x]
    print('userUID esta sucio y se ve asi ===> ' + userUID_dirty)
    for x in range(0, len(userUID_dirty)):
        if(userUID_dirty[x]!='\"' and userUID_dirty[x]!='}'):
            userUID_clean += userUID_dirty[x]
    print('userUID quedo limpio y se ve asi ===> ' + userUID_clean)
    userUID = userUID_clean

    if (title == '' or description == '' or dueDate == '' or hourReminder == '' or dateReminder == ''):
        errorJSON = {
                        'error':'You are missing parameters or the ones you sent are incorrect',
                    }
        return errorJSON, status.HTTP_400_BAD_REQUEST

    if request.method == 'POST':
        new_task = firebase.post('/tasks', {
                                            'title': title,
                                            'description': description,
                                            'dueDate': dueDate,
                                            'hourReminder': hourReminder,
                                            'dateReminder': dateReminder,
                                            'owner': userUID,
                                           })
        print(new_task)
        newTaskID_dirty = str(new_task)
        newTaskID_almostClean = ''
        newTaskID_clean = ''
        for x in range(12, len(newTaskID_dirty)):
            newTaskID_almostClean+= newTaskID_dirty[x]
        print('almostClean ID of new Task is ===> ' + newTaskID_almostClean)
        for x in range(0, len(newTaskID_almostClean)):
            if (newTaskID_almostClean[x] != '\'' and newTaskID_almostClean[x] != '}'):
                newTaskID_clean += newTaskID_almostClean[x]
        print('the clean ID of new Task finally is ===> ' + newTaskID_clean)
        createdTaskData = {
                        'id': newTaskID_clean,
                        'title': title,
                        'description': description,
                        'dueDate': dueDate,
                        'hourReminder': hourReminder,
                        'dateReminder': dateReminder,
                      }
        createdTask = json.dumps(createdTaskData)
        return createdTask, status.HTTP_201_CREATED
    return status.HTTP_500_INTERNAL_SERVER_ERROR

@app.route("/tasks/<string:taskID>", methods=['DELETE']) #DELETES a Task | DONE | UT missing
def delete_task(taskID):
    if request.method == 'DELETE': 
        firebase.delete('/tasks', taskID)
        return '', status.HTTP_204_NO_CONTENT

@app.route("/tasks/<string:userToken>", methods=['GET'])
def get_my_tasks(userToken):
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