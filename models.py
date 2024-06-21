import mysql.connector
from flask import session
from faker import Faker

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
    
def getId():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM users")
    ids = len(cursor.fetchall())
    return ids
    
def register(name,username,password):
    cursor = mydb.cursor()
    idtask = getId()+1
    cursor.execute("insert into users values (%s,%s,%s,%s,%s)",(idtask,name,username,password,'offline'))
    mydb.commit()

def titleExist(title):
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM task where titre = %s",(title,))
        titles = cursor.fetchone()
        return titles is not None
    except Exception as e:
        print(f"error from checking existence {e}")
        return False

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

def logout(userId):
    cursor = mydb.cursor()
    cursor.execute("UPDATE users set status = %s where userId = %s",('offline',userId))
    mydb.commit()

def getAllTasks():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM task where state != %s and userId = %s",('archived',session['userId']))
    results = mycursor.fetchall()
    return results

def getAllDoneTask():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM task where userId = %s",(session['userId'],))
    results = mycursor.fetchall()
    return results

def getTaskByTitle(title):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM task where id = %s and userId = %s", (title,session['userId']))
    result = mycursor.fetchall()
    if result :
        return result
    else:
        return "id incorrect"
    
def addTask(title,descript,etat,userId):
    mycursor = mydb.cursor()
    mycursor.execute("INSERT INTO task (titre,description,state,userId) VALUES (%s,%s,%s,%s)", (title,descript,etat,userId))
    mydb.commit()
    
def deleteTask(task_id):
    cur = mydb.cursor()
    cur.execute("update task set state = 'archived' where idtask = %s", task_id)
    mydb.commit()
    
def markdone(task_id):
    cur = mydb.cursor()
    cur.execute("UPDATE task SET state = 'completed' WHERE idtask = %s",task_id)
    mydb.commit()
    
def checkId(id,userId):
    cur = mydb.cursor()
    cur.execute("SELECT * FROM task WHERE idtask = %s and userId = %s",(id,userId))
    result = cur.fetchone()
    if result:
        return True
    else:
        return False
    
def addjsonTask(data):
    faker = Faker()
    userId      =   data['userId']
    idtask      =   data['id']
    title       =   data['title']
    description =   faker.text()
    if(data['completed']):
        state = 'completed'
    else:
        state = 'todo'
    mycursor = mydb.cursor()
    print(title)
    if(titleExist(title)):
        print("title already exist")
        return 'blocked'
    else:
        # print(title)
        if(not checkId(idtask,userId)):
            mycursor.execute("INSERT INTO task (titre,description,state,userId) VALUES (%s,%s,%s,%s)",(title,description,state,userId))
        else:
            idtask = len(getAllDoneTask())+1
            print(idtask)
            mycursor.execute("INSERT INTO task (titre,description,state,userId) VALUES (%s,%s,%s,%s)",(title,description,state,userId))
        mydb.commit()
        return 'done'
    
        
    # print(title)