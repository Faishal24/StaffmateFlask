import os
from flask import Flask, flash, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    role = db.Column(db.String(20), nullable=False)
    group = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'<User {self.nama}>'
    
@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/<int:user_id>/')
def user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user.html', user=user)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        nama = request.form['nama']
        age = int(request.form['age'])
        role = request.form['role']
        group = request.form['group']
        user = User(nama=nama,
                          age=age,
                          role=role,
                          group=group)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<int:user_id>/edit/', methods=('GET', 'POST'))
def edit(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        nama = request.form['nama']
        age = int(request.form['age'])
        role = request.form['role']
        group = request.form['group']

        user.nama = nama
        user.role = role
        user.age = age
        user.group = group

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit.html', user=user)

@app.post('/<int:user_id>/delete/')
def delete(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/login/')
def login():
    return render_template('login.html')