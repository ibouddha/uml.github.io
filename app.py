from flask import Flask, session, render_template, request, redirect
import models
from random import randrange
 
# from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = "IamBouddh@"



@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login',methods=['GET','POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if(not models.isconnected(username) and ('username' not in session)):
        models.authentified(username)
        account = models.authenticate(username,password)
        print(account)
        if account:
            session['username'] = username
            return redirect('/list')
    else:
        return redirect('/')
    
@app.route('/logout',methods=('POST','GET'))
def logout():
    if('username' in session):
        models.logout(session['username'])
        session.pop('username',None)
    return redirect('/')
    

@app.route('/register',methods=['GET','POST'])
def register():
    name = request.form.get('nom')
    username = request.form.get('username')
    password = request.form.get('password')
    models.register(name,username,password)
    return redirect('/')

    
@app.route('/list')
def display():
    results = models.getAllTasks()
    if('username' in session):
        return render_template('index.html', tasks=results)
    else:
        return redirect('/')
    
@app.route('/all')
def getAll():
    results = models.getAllDoneTask()
    if('username' in session):
        return render_template('index.html', tasks=results)
    else:
        return redirect('/')

@app.route('/add-task',methods=['GET','POST'])
def add():
    idtask = 0
    username = session['username']
    if request.method == 'POST':
        idtask = randrange(10000000)
        title = request.form.get('titre')
        descript = request.form.get('description')
        etat = request.form.get('state')
        models.addTask(idtask,title,descript,etat,username)
        return redirect('/list')
    else:
        return redirect('/')
    

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
