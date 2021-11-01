from flask import Blueprint, render_template, redirect, url_for, request
from bson.objectid import ObjectId
from flask import Flask
from werkzeug.utils import secure_filename

from flask_pymongo import PyMongo

mongo = PyMongo()

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://m001-student:m001-mongodb-basics@sandbox.akvcd.mongodb.net/My_Database?retryWrites=true&w=majority'
mongo.init_app(app)


@app.route('/')
def index():
    todos_collection = mongo.db.Todo_List
    todos = todos_collection.find()
    return render_template('index.html', todos = todos)

@app.route('/add_todo', methods = ['POST'])
def add_todo():
    todos_collection = mongo.db.Todo_List
    todo_item = request.form.get('add-todo')
    todos_collection.insert_one({"task":todo_item, "complete":False})
    return redirect(url_for('index'))

@app.route('/complete_todo/<oid>')
def complete_todo(oid):
    todos_collection = mongo.db.Todo_List
    todo_item = todos_collection.find_one({'_id':ObjectId(oid)})
    todo_item['complete'] = True
    todos_collection.save(todo_item)
    return redirect(url_for('index'))

@app.route('/delete_completed')
def delete_completed():
    todos_collection = mongo.db.Todo_List
    todos_collection.delete_many({'complete':True})
    return redirect(url_for('index'))

@app.route('/delete_all')
def delete_all():
    todos_collection = mongo.db.Todo_List
    todos_collection.delete_many({})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug = True)

