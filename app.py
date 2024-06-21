from flask import Flask, session, render_template, request, redirect, jsonify
import models
from random import randrange
 
# from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = "IamBouddh@"



@app.route('/')
def index():
    if('username' in session):
        return redirect('/list')
    else:
        return render_template('login.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if('username' in session):
        return redirect('/list')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        if(not models.isconnected(username) and ('username' not in session)):
            models.authentified(username)
            account = models.authenticate(username,password)
            # print(account)
            if account:
                # print(account)
                session['username'] = username
                session['userId'] = account[0]
                # print(session['userId'])
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
    if('username' in session):
        results = models.getAllTasks()
        if('userId' in session):
            return render_template('index.html', tasks=results)
        else:
            return redirect('/')
    else:
        return redirect('/logout')
    
@app.route('/all')
def getAll():
    results = models.getAllDoneTask()
    if('userId' in session):
        return render_template('index.html', tasks=results)
    else:
        return redirect('/')

@app.route('/add-task',methods=['GET','POST'])
def add():
    userId = session['userId']
    if request.method == 'POST':
        title = request.form.get('titre')
        descript = request.form.get('description')
        etat = request.form.get('state')
        models.addTask(title,descript,etat,userId)
        return redirect('/list')
    else:
        return redirect('/')
    
@app.route("/process", methods=['POST'])
def treatment():
    data = request.get_json()
    donnée = []
    json_data = data['data']
    number = len(models.getAllDoneTask())
    print(data['size'])
    if(data['size']>number):
        size = data['size']-number
        for index in range(0,size):
            # print(datum,end='\n')
            while(models.addjsonTask(json_data[index]) != 'done'):
                index+=1
                size+=1
    else:
        print(number)
        for index in range(0,number):
            models.addjsonTask(json_data[index])
            donnée.append(json_data[index])
    return donnée
            
    

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
