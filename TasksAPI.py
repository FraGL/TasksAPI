from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from firebase import firebase

app = FlaskAPI(__name__)
firebase = firebase.FirebaseApplication('https://proyecto-final-arquitectura.firebaseio.com')

'''def note_repr(key):
    return {
        'url': request.host_url.rstrip('/') + url_for('notes_detail', key=key),
        'text': notes[key]
    }
'''

@app.route("/tasks", methods=['POST'])
def tasks():
    if request.method == 'POST':
    	new_task = firebase.post('/tasks', {'PyTEST':'Works'})
        return new_task(idx), status.HTTP_201_CREATED
        pass


@app.route("/<int:key>/", methods=['GET', 'PUT', 'DELETE'])
def notes_detail(key):
    """
    Retrieve, update or delete note instances.
    """
    if request.method == 'PUT':
        note = str(request.data.get('text', ''))
        notes[key] = note
        return note_repr(key)

    elif request.method == 'DELETE':
        notes.pop(key, None)
        return '', status.HTTP_204_NO_CONTENT

    # request.method == 'GET'
    if key not in notes:
        raise exceptions.NotFound()
    return note_repr(key)


if __name__ == "__main__":
    app.run(debug=True)