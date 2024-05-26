from flask import Flask, render_template, request, redirect
import models
from random import randrange
 
# from flask_mysqldb import MySQL

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login',methods=['GET','POST'])
def login():
    name = request.form['nom']
    username = request.form['username']
    password = request.form['password']
    account = models.authenticate(username,password)
    if account:
        models.authentified(account[1])
        return render_template('index.html',user= account)
    else:
        return redirect('/')
    

@app.route('/register',methods=['GET','POST'])
def    

    
@app.route('/list', methods=['GET', 'POST'])
def display():
    if models.authenticate(request.form['username'],request.form['password']):
        results = models.getAllTask()
        return render_template('index.html', tasks=results)
    else:
        return redirect('/')

@app.route('/add-task',methods=['GET','POST'])
def add():
    idtask = 0
    if request.method == 'POST':
        idtask = randrange(10000000)
        title = request.form.get('titre')
        descript = request.form.get('description')
        etat = request.form.get('state')
        models.addTask(idtask,title,descript,etat)
        return redirect('/list')
    

@app.route('/delete/<int:task_id>', methods=['GET'])
def delete_task(task_id):
    models.deleteTask([task_id])
    return redirect('/list')

@app.route('/complete/<int:task_id>', methods=['GET'])
def complete_task(task_id):
    models.markdone([task_id])
    return redirect('/list')

if __name__ == '__main__':
    app.run(debug=True)
