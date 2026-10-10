@app.route('/todo')
def todo_page():
    return render_template('todo.html')
