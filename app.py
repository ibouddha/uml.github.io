from flask import Flask, render_template, request, redirect
import mysql.connector



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="tache"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM tache")

    results = mycursor.fetchall()

    return render_template('index.html', tasks=results)

@app.route('/delete/<int:task_id>', methods=['GET'])
def delete_task(task_id):
    conn = mysql.connect
    cur = conn.cursor()
    cur.execute("DELETE FROM tache WHERE id = %s", [task_id])
    conn.commit()
    cur.close()

    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>', methods=['GET'])
def complete_task(task_id):
    conn = mysql.connect
    cur = conn.cursor()
    cur.execute("UPDATE tache SET completed = NOT completed WHERE id = %s", [task_id])
    conn.commit()
    cur.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
