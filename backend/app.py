from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb+srv://shanmukhi_kairuppala:123@cluster0.8umjfel.mongodb.net/notes?retryWrites=true&w=majority&appName=Cluster0"

try:
    mongo = PyMongo(app)
    notes_collection = mongo.db.NoteMaking
    print("MongoDB connected successfully.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")



@app.route('/')
def home():
    return "Welcome to the Notes API! Use /notes to interact with notes.", 200

@app.route('/notes',methods=['POST'])
def add_note():
    data = request.json
    title = data.get('title')
    content = data.get('content')
    if title and content:
        note_id = notes_collection.insert_one({'title':title, 'content':content}).inserted_id
        new_note = notes_collection.find_one({'_id': ObjectId(note_id)})
        return jsonify({'_id': str(new_note['_id']), 'title': new_note['title'], 'content': new_note['content']}), 201
    else:
        return jsonify({'error': 'Missing title or content'}), 400


@app.route('/notes', methods=['GET'])
def get_notes():
    notes = notes_collection.find()
    result = [{'_id': str(note['_id']), 'title': note['title'], 'content': note['content']} for note in notes]
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
