from dataclasses import dataclass
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, PickleType
from datetime import datetime
from sqlalchemy.orm import relationship
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'my_secret_key'

db = SQLAlchemy(app)

@dataclass
class Users(db.Model):
    __tablename__ = 'user'
    id: int
    email: str
    password: str

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable = False)
    password = db.Column(db.String(255), nullable = False)
    
    def __repr__(self):
        return f'<User {self.id}>'    

@dataclass
class Trainer(db.Model):
    __tablename__ = 'trainer'
    id: int
    email: str
    password: str
    calificacion: PickleType

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable = False)
    password = db.Column(db.String(255), nullable = False)
    calificacion = db.Column(db.PickleType, nullable = False)
    
    def __repr__(self):
        return f'<Trainer {self.id}>'   

@dataclass
class Sesion(db.Model):
    __tablename__ = 'sesion'
    id: int
    entrenador_id: int
    usuario_id: int
    fecha: datetime
    precio: int

    id = db.Column(db.Integer, primary_key=True)
    entrenador_id = db.Column(db.Integer,ForeignKey("trainer.id")  ,primary_key=True)
    usuario_id = db.Column(db.Integer,ForeignKey("user.id") ,primary_key=True)
    fecha = db.Column(db.DateTime, nullable = False)
    precio = db.Column(db.Integer, nullable = False)

    entrenador = relationship("Trainer")
    usuario = relationship("Users")


    def __repr__(self):
        return f'<Sesion {self.id}>'
    

@dataclass
class Solicitudes(db.Model):
    id: int
    usuario_id: int
    entrenador_id: int
    fecha: datetime
    precio: int

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, primary_key=True)
    entrenador_id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable = False)
    precio = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f'<Solicitudes {self.id}>'
    

with app.app_context():
    db.create_all()


@app.route('/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
def route_users():
    if request.method == 'GET':
        users = Users.query.all()
        return jsonify(users)
    elif request.method == 'POST':
        user_form = request.get_json()
        if Users.query.filter_by(email=user_form['email']).first() is not None:
            return jsonify('USEREXISTS')
        users = Users(email=user_form['email'], password=user_form['password'])
        db.session.add(users)
        db.session.commit()
        return 'SUCCESS'
    elif request.method == 'PUT':
        user = Users.query.get(request.get_json()['id'])
        user.email = request.get_json()['email']
        user.password = request.get_json()['password']
        db.session.commit()
        return 'SUCCESS'
    elif request.method == 'DELETE':
        user = Users.query.get(request.get_json()['id'])
        db.session.delete(user)
        db.session.commit()
        return 'SUCCESS'

@app.route('/users/<id>', methods=['GET'])
def route_user(id):
    if request.method == 'GET':
        user = Users.query.get(id)
        return jsonify(user)

    
@app.route('/trainer', methods=['GET', 'POST', 'PUT', 'DELETE'])
def route_trainers():
    if request.method == 'GET':
        trainers = Trainer.query.all()
        return jsonify(trainers)
    elif request.method == 'POST':
        trainer = Trainer(email=request.get_json()['email'], password=request.get_json()['password'])
        db.session.add(trainer)
        db.session.commit()
        return 'SUCCESS'
    elif request.method == 'PUT':
        trainer = Trainer.query.get(request.get_json()['id'])
        trainer.email = request.get_json()['email']
        trainer.password = request.get_json()['password']
        db.session.commit()
        return 'SUCCESS'
    elif request.method == 'DELETE':
        trainer = Trainer.query.get(request.get_json()['id'])
        db.session.delete(trainer)
        db.session.commit()
        return 'SUCCESS'
    
@app.route('/sesion', methods=['GET', 'POST', 'PUT', 'DELETE'])
def route_sesion():
    if request.method == 'GET':
        sesion = Sesion.query.all()
        return jsonify(sesion)
    elif request.method == 'POST':
        sesion = Sesion(id=request.form['id'], entrenador_id=request.form['entrenador_id'], usuario_id=request.form['usuario_id'], fecha=request.form['fecha'], hora=request.form['hora'], precio=request.form['precio'])
        db.session.add(sesion)
        db.session.commit()
        return 'SUCCESS'
    elif request.method == 'PUT':
        sesion = Sesion.query.get(request.form['id'])
        sesion.entrenador_id = request.form['entrenador_id']
        sesion.usuario_id = request.form['usuario_id']
        sesion.fecha = request.form['fecha']
        sesion.hora = request.form['hora']
        sesion.precio = request.form['precio']
        db.session.commit()
        return 'SUCCESS'
    elif request.method == 'DELETE':
        sesion = Sesion.query.get(request.form['id'])
        db.session.delete(sesion)
        db.session.commit()
        return 'SUCCESS'

@app.route('/solicitudes', methods=['GET', 'POST', 'PUT', 'DELETE'])
def route_solicitudes():
    if request.method == 'GET':
        solicitudes = Solicitudes.query.all()
        return jsonify(solicitudes)
    elif request.method == 'POST':
        solicitudes = Solicitudes(id=request.form['id'], usuario_id=request.form['usuario_id'], entrenador_id=request.form['entrenador_id'], fecha=request.form['fecha'], precio=request.form['precio'])
        db.session.add(solicitudes)
        db.session.commit()
        return 'SUCCESS'
    elif request.method == 'PUT':
        solicitudes = Solicitudes.query.get(request.form['id'])
        solicitudes.usuario_id = request.form['usuario_id']
        solicitudes.entrenador_id = request.form['entrenador_id']
        solicitudes.fecha = request.form['fecha']
        solicitudes.precio = request.form['precio']
        db.session.commit()
        return 'SUCCESS'
    elif request.method == 'DELETE':
        solicitudes = Solicitudes.query.get(request.form['id'])
        db.session.delete(solicitudes)
        db.session.commit()
        return 'SUCCESS'
    



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
