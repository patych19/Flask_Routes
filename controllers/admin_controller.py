from extensions import db
from models.models import Provincia, Conexion
from flask import flash, redirect, render_template, request, url_for
from models.models import Provincia
from extensions import db

def listar_provincias():
    return Provincia.query.order_by(Provincia.nombre).all()

def agregar_provincia():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip().title()
        es_costera = True if request.form.get('es_costera') == 'on' else False

        # Verificar duplicado
        existente = Provincia.query.filter_by(nombre=nombre).first()
        if existente:
            flash('La provincia ya existe. No se puede duplicar.', 'danger')
        else:
            nueva = Provincia(nombre=nombre, es_costera=es_costera)
            db.session.add(nueva)
            db.session.commit()
            flash('Provincia agregada exitosamente.', 'success')

    return redirect(url_for('admin_bp.provincias'))

def editar_provincia(id, nombre, es_costera):
    p = Provincia.query.get(id)
    p.nombre = nombre
    p.es_costera = es_costera
    db.session.commit()

def eliminar_provincia(id):
    db.session.delete(Provincia.query.get(id))
    db.session.commit()

def listar_conexiones():
    return Conexion.query.all()

def agregar_conexion(origen_id, destino_id, costo):
    c = Conexion(origen_id=origen_id, destino_id=destino_id, costo=costo)
    db.session.add(c)
    db.session.commit()

def eliminar_conexion(id):
    db.session.delete(Conexion.query.get(id))
    db.session.commit()
