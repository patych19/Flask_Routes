from datetime import datetime
from extensions import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'usuario'
    id        = db.Column(db.Integer, primary_key=True)
    nombre    = db.Column(db.String(50), nullable=False)
    correo    = db.Column(db.String(100), unique=True, nullable=False)
    contrasena= db.Column(db.String(255), nullable=False)
    rol       = db.Column(db.Enum('admin','usuario', name='rol'), nullable=False, default='usuario')
    consultas = db.relationship('HistorialConsulta', backref='usuario', lazy=True)

class Provincia(db.Model):
    __tablename__ = 'provincia'
    id       = db.Column(db.Integer, primary_key=True)
    nombre   = db.Column(db.String(100), unique=True, nullable=False)
    es_costera = db.Column(db.Boolean, default=False)
    origenes = db.relationship('Conexion', foreign_keys='Conexion.origen_id', backref='origen', lazy=True)
    destinos = db.relationship('Conexion', foreign_keys='Conexion.destino_id', backref='destino', lazy=True)

class Conexion(db.Model):
    __tablename__= 'conexion'
    id        = db.Column(db.Integer, primary_key=True)
    origen_id = db.Column(db.Integer, db.ForeignKey('provincia.id'), nullable=False)
    destino_id= db.Column(db.Integer, db.ForeignKey('provincia.id'), nullable=False)
    costo     = db.Column(db.Float, nullable=False)

class HistorialConsulta(db.Model):
    __tablename__     = 'historial_consulta'
    id                = db.Column(db.Integer, primary_key=True)
    usuario_id        = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    origen_id         = db.Column(db.Integer, db.ForeignKey('provincia.id'), nullable=False)
    destino_id        = db.Column(db.Integer, db.ForeignKey('provincia.id'), nullable=False)
    pasar_por_costera = db.Column(db.Boolean, default=False)
    camino            = db.Column(db.Text, nullable=False)
    costo_total       = db.Column(db.Float, nullable=False)
    fecha_consulta    = db.Column(db.DateTime, default=datetime.utcnow)
