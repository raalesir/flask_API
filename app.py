#! /usr/bin/env python3

from flask import Flask, jsonify, abort
from flask import make_response, request, url_for

app = Flask(__name__)


tasks = [
        {
            "id":1,
            "title":u"Buy groceries",
            "description": u"milk, cheese, pizza, fruit",
            "done": False
        },
        {
            "id": 2,
            "title": u"learn python",
            "description": u"working on APIs",
            "done": False
        }

        ]

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def index():
    for task in tasks:
        task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
    return jsonify({
        "tasks": tasks
        }
        )


@app.route("/todo/api/v1.0/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = [task for task in tasks if task['id']== task_id]
    if len(task)==0:
        abort(404)
    return jsonify({'task': task[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': "Not found"}), 404)



@app.route("/todo/api/v1.0/tasks", methods=["POST"])
def  create_task():
    if not request.json or 'title' not in request.json:
        abort(400)
    task = {
            'id': tasks[-1]['id']+1,
            'title': request.json['title'],
            'description': request.json.get('description',''),
            'done': False
            }
    tasks.append(task)
    return jsonify({"task": task}), 201


@app.route("/todo/api/v1.0/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id][0]
    print(task)
    task['title'] = request.json.get('title', task['title'])
    task['description'] = request.json.get('description', task['description'])
    task ['done'] = request.json.get('done', task['done'])
    print(task)
    return jsonify({'task': task}) 

if __name__ == "__main__":
    app.run(debug=True)
