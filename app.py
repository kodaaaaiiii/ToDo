from flask import Flask, render_template, request, redirect, session
import os
import json

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ファイルパス
data_file = "todos.json"

# ToDoリストのデータを読み込む関数
def load_todos():
    todos = []
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            todos = json.load(file)
    return todos

# ToDoリストのデータを保存する関数
def save_todos(todos):
    with open(data_file, "w") as file:
        json.dump(todos, file)

def view_todos(user_id):
    todos = load_todos()
    user_todos = [todo for todo in todos if todo['user_id'] == user_id]
    return user_todos

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    user_id = request.form.get('user_id')
    if not user_id:
        return redirect('/')
    session['user_id'] = user_id
    user_todos = view_todos(user_id)
    return render_template('view.html', user_id=user_id, todos=user_todos)

@app.route('/input')
def input():
    return render_template('input.html')

@app.route('/view', methods=['GET', 'POST'])
def view():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/')
    user_todos = view_todos(user_id)
    # sortパラメータの取得
    sort = request.args.get('sort', default='entry')
    
    # ソート処理
    if sort == 'date':
        user_todos = sorted(user_todos, key=lambda x: x['date'])
    else:
        user_todos = sorted(user_todos, key=lambda x: x['id'])
    return render_template('view.html', todos=user_todos, user_id=user_id)

@app.route('/add', methods=['POST'])
def add():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/')
    task = request.form.get('task')  # フォームからタスクの値を取得
    date = request.form.get('date')  # フォームから日付の値を取得

    # 入力された日付を文字列のままリストに追加
    todos = load_todos()
    todos.append({'user_id': user_id,'id': len(todos)+1, 'task': task, 'date': date})
    save_todos(todos)

    return redirect('/view')

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete(todo_id):
    todos = load_todos()
    if 0 < todo_id <= len(todos):
        todos.pop(todo_id - 1)  # 指定したIDのToDoリスト項目を削除
        i = 1
        for todo in todos:
            todo['id'] = i
            i += 1 
        save_todos(todos)
    return redirect('/view')

@app.route('/sort_date', methods=['POST'])
def sort_date():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/')
    user_todos = view_todos(user_id)
    # sortパラメータの取得
    sort = request.args.get('sort', default='entry')

    user_todos = sorted(user_todos, key=lambda x: x['date'])

    return render_template('view.html', todos=user_todos, user_id=user_id)

@app.route('/sort_id', methods=['POST'])
def sort_id():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/')
    user_todos = view_todos(user_id)
    # sortパラメータの取得
    sort = request.args.get('sort', default='entry')
    
    user_todos = sorted(user_todos, key=lambda x: x['id'])

    return render_template('view.html', todos=user_todos, user_id=user_id)

if __name__ == '__main__':
    app.run()
