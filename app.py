from datetime import datetime
from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "Python & Flask - Web Development"

# defining the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks_db.db'
db = SQLAlchemy(app)

# designing the table task model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    responsible = db.Column(db.String(18), nullable=False)
    content = db.Column(db.String(40), nullable=False)
    due_date = db.Column(db.String(15), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created_date = db.Column(db.DateTime, default= datetime.now)
    task_status = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Task %r>' % self.id

# creating all database with all tables
with app.app_context():
    db.create_all() 

# defiing add new task method
@app.route('/', methods=['POST', 'GET'])
def index():
    status = False

    if request.method == 'POST':
        #getting the values from the form
        task_content = request.form['content']
        responsible = request.form['responsible']
        due_date = request.form['due_date']

        if due_date >= datetime.now().strftime("%m/%d/%Y"):
            status = True

        new_task = Todo(content = task_content, responsible = responsible, due_date = due_date, task_status = status)

        #save the data into DB
        try:
            db.session.add(new_task)
            db.session.commit()

            flash('Task "' + task_content + '" added successfully', 'success')
            return redirect('/')
        except:
            return flash('Could not save the Task! Try again.', 'fail')
    else:
        try:
            # defining the pagination
            page = request.args.get('page', 1, type=int)

            pagination = Todo.query.order_by(Todo.created_date).paginate(
                page=page, per_page=4)

            return render_template('index.html', pagination=pagination)
        except:
            return render_template('error.html')


# defining update task method
@app.route('/update_task/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    update_task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        #getting the values from the form
        update_task.responsible = request.form['up_responsible']
        update_task.content = request.form['up_content']
        update_task.due_date = request.form['up_due_date']

        if update_task.due_date >= datetime.now().strftime("%m/%d/%Y"):
            update_task.task_status = True
        else:
            update_task.task_status = False

        #update the data into DB
        try:
            db.session.commit()
            flash('Task "' + update_task.content + '" updated successfully', 'success')
            return redirect('/')
        except:
            return flash('Could not update the task. Try again.', 'fail')
    else:
        return render_template('/', task = update_task)


# defining delete task method
@app.route('/delete/<int:id>')
def delete(id):
    delete_task = Todo.query.get_or_404(id)

    try:
        db.session.delete(delete_task)
        db.session.commit()
        flash('Task deleted successfully', 'success')
        return redirect('/')
    except:
        return flash('Could not delete the Task ' + id, 'fail')


# method to run the application
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')