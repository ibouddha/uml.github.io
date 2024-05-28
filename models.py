import mysql.connector
from flask import session

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="tache"
    )

def authenticate(username, password):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s and status = %s", (username, password,'online'))
    account = cursor.fetchone()
    if account:
        return account
    else:
        return False
    
def register(name,username,password):
    cursor = mydb.cursor()
    cursor.execute("insert into users values (%s,%s,%s,%s)",(name,username,password,'offline'))
    mydb.commit()

def authentified(username):
    cursor = mydb.cursor()
    cursor.execute("UPDATE users set status = %s where username = %s",('online',username))
    mydb.commit()
    
def isconnected(username):
    cursor = mydb.cursor()
    cursor.execute("select status from users where username = %s",(username,))
    status = cursor.fetchone()
    if(status == 'online'):
        return True
    else:
        return False

def logout(username):
    cursor = mydb.cursor()
    cursor.execute("UPDATE users set status = %s where username = %s",('offline',username))
    mydb.commit()

def getAllTasks():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM task where state != %s and username = %s",('archived',session['username']))
    results = mycursor.fetchall()
    return results

def getAllDoneTask():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM task where username = %s",(session['username'],))
    results = mycursor.fetchall()
    return results

def getTaskByTitle(title):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM task where id = %s and username = %s", (title,session['username']))
    result = mycursor.fetchall()
    if result :
        return result
    else:
        return "id incorrect"
    
def addTask(idtask,title,descript,etat,username):
    mycursor = mydb.cursor()
    mycursor.execute("INSERT INTO task (idtask,titre,description,state,username) VALUES (%s,%s,%s,%s,%s)", (idtask,title,descript,etat,username))
    mydb.commit()
    
def deleteTask(task_id):
    cur = mydb.cursor()
    cur.execute("update task set state = 'archived' where idtask = %s", task_id)
    mydb.commit()
    
def markdone(task_id):
    cur = mydb.cursor()
    cur.execute("UPDATE task SET state = 'completed' WHERE idtask = %s",task_id)
    mydb.commit()