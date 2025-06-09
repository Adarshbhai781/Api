from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Path to the JSON file
JSON_FILE = 'quiz_data.json'

# Load existing data from JSON file if it exists
def load_quiz_data():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []  # Return empty list if file is empty or corrupted
    return []

# Save quiz data to JSON file
def save_quiz_data(data):
    with open(JSON_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Initialize quiz_data by loading from file
quiz_data = load_quiz_data()

@app.route('/api/quiz', methods=['GET'])
def get_quiz():
    return jsonify(quiz_data)

@app.route('/api/quiz', methods=['POST'])
def add_quiz():
    data = request.get_json()
    if not data or 'question' not in data or 'options' not in data or 'answer' not in data:
        return jsonify({"error": "Invalid data format"}), 400
    quiz_data.append(data)
    save_quiz_data(quiz_data)  # Save to JSON file
    return jsonify({"message": "✅ प्रश्न जोड़ा गया!"}), 201

@app.route('/api/quiz/<int:index>', methods=['DELETE'])
def delete_quiz(index):
    if 0 <= index < len(quiz_data):
        deleted = quiz_data.pop(index)
        save_quiz_data(quiz_data)  # Update JSON file after deletion
        return jsonify({"message": f"❌ '{deleted['question']}' हटाया गया!"})
    return jsonify({"error": "Invalid index"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)