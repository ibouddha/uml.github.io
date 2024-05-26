import mysql.connector

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="tache"
    )

def authenticate(username, password):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM users WHERE usename = %s AND password = %s and status = %s", (username, password,'online'))
    account = cursor.fetchone()
    if account:
        return account
    else:
        return False
    
def register(username,password,name):
    cursor = mydb.cursor()
    cursor.ecxecute("insert into users values (%s,%s,%s,%s)",(name,username,password,'offline'))
    cursor.commit()

def authentified(username):
    cursor = mydb.cursor()
    cursor.execute("UPDATE users set status = 'online' where username = %s",(username))
    cursor.commit()
    
def logout(usename):
    cursor = mydb.cursor()
    cursor.execute("UPDATE users set status = 'offline' where username = %s",(username))
    cursor.commit()

def getAllTask():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM task where state != 'archived'")
    results = mycursor.fetchall()
    return results

def getTaskById(id):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM task where id = %s", (id,))
    result = mycursor.fetchone()
    if result :
        return result
    else:
        return "id incorrect"
    
def addTask(idtask,title,descript,etat):
    mycursor = mydb.cursor()
    mycursor.execute("INSERT INTO task (idtask,titre,description,state) VALUES (%s,%s,%s,%s)", (idtask,title,descript,etat))
    mydb.commit()
    
def deleteTask(task_id):
    cur = mydb.cursor()
    cur.execute("update task set state = 'archived' where idtask = %s", task_id)
    mydb.commit()
    
def markdone(task_id):
    cur = mydb.cursor()
    cur.execute("UPDATE task SET state = 'completed' WHERE idtask = %s", task_id)
    mydb.commit()