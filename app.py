# Importations
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Configuration de l'application Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre_clé_secrèt  e'  # Remplacez par votre propre clé secrète
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'  # Utilisation de SQLite comme base de données
db = SQLAlchemy(app)

# Modèle de données
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# Formulaire pour ajouter une tâche
class TaskForm(FlaskForm):
    content = StringField('Tâche', validators=[DataRequired()])

# Route pour afficher la liste des tâches
@app.route('/')
def tasks():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

# Route pour ajouter une tâche
@app.route('/add_task', methods=['POST'])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(content=form.content.data)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('tasks'))

# Route pour supprimer une tâche
@app.route('/delete_task/<int:id>', methods=['POST'])
def delete_task(id):
    task_to_delete = Task.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('tasks'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
