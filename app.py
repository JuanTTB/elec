from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import config

app = Flask(__name__)

# Conexión a MongoDB Atlas
client = MongoClient(config.MONGO_URI)
db = client.task_manager  # Nombre de la base de datos
collection = db.tasks  # Nombre de la colección

# Endpoints

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = list(collection.find())
    for task in tasks:
        task['_id'] = str(task['_id'])
    return jsonify(tasks)

@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    task = collection.find_one({'_id': ObjectId(task_id)})
    if task:
        task['_id'] = str(task['_id'])
        return jsonify(task)
    else:
        return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    result = collection.insert_one(data)
    new_task = collection.find_one({'_id': result.inserted_id})
    new_task['_id'] = str(new_task['_id'])
    return jsonify(new_task), 201

@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    result = collection.update_one({'_id': ObjectId(task_id)}, {'$set': data})
    if result.matched_count:
        updated_task = collection.find_one({'_id': ObjectId(task_id)})
        updated_task['_id'] = str(updated_task['_id'])
        return jsonify(updated_task)
    else:
        return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    result = collection.delete_one({'_id': ObjectId(task_id)})
    if result.deleted_count:
        return jsonify({'message': 'Task deleted'})
    else:
        return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
