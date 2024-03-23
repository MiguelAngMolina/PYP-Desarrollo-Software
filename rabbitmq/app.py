from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = [
    {'id': 1, 'title': 'Do homework', 'done': False},
    {'id': 2, 'title': 'Read a book', 'done': False},
]

# Ruta de bienvenida
@app.route('/')
def welcome():
    return "Welcome to the Tasks API!"

# Obtener todas las tareas
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

# Crear una nueva tarea
@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        return jsonify({'error': 'The new task must have a title.'}), 400
    new_task = {
        'id': tasks[-1]['id'] + 1 if tasks else 1,  # Para manejar cuando la lista está vacía
        'title': request.json['title'],
        'done': False
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

# Actualizar una tarea existente
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if not task:
        return jsonify({'error': 'Task not found.'}), 404
    if not request.json:
        return jsonify({'error': 'Request must be JSON.'}), 400
    task['title'] = request.json.get('title', task['title'])
    task['done'] = request.json.get('done', task['done'])
    return jsonify(task)

# Eliminar una tarea
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)
