from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# --- MongoDB Database Configuration ---
# Replace with your MongoDB URI if using MongoDB Atlas
client = MongoClient('mongodb://localhost:27017/')
db = client['flask_todo_db']       # Database name
todos_collection = db['todos']     # Collection name

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    # Accept itemName and itemDescription via POST request
    item_name = request.form.get('itemName')
    item_description = request.form.get('itemDescription')

    if item_name and item_description:
        # Store details in MongoDB
        todo_data = {
            "itemName": item_name,
            "itemDescription": item_description
        }
        todos_collection.insert_one(todo_data)
        return jsonify({"status": "success", "message": "Item stored successfully in MongoDB!"}), 201
    
    return jsonify({"status": "error", "message": "Missing fields!"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
