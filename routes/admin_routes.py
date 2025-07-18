# routes/admin_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from utils.helpers import roles_required
from controllers.admin_controller import (
    listar_provincias,
    agregar_provincia,
    editar_provincia,
    eliminar_provincia,
    listar_conexiones,
    agregar_conexion,
    eliminar_conexion
)
from models.models import Provincia, Conexion, HistorialConsulta, User

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')


@admin_bp.route('/panel')
@login_required
@roles_required('admin')
def panel():
    provincias_count   = Provincia.query.count()
    conexiones_count   = Conexion.query.count()
    consultas_count    = HistorialConsulta.query.count()
    usuarios_count     = User.query.count()
    return render_template(
        'admin/panel.html',
        provincias_count=provincias_count,
        conexiones_count=conexiones_count,
        consultas_count=consultas_count,
        usuarios_count=usuarios_count
    )


@admin_bp.route('/provincias', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def provincias():
    # Maneja POST para añadir provincia o GET para mostrar
    if request.method == 'POST':
        nombre = request.form['nombre'].strip().title()
        es_costera = 'es_costera' in request.form
        
        # Llamar la función del controlador (ya maneja los flash messages)
        agregar_provincia(nombre, es_costera)
        return redirect(url_for('admin_bp.provincias'))

    provincias = listar_provincias()
    return render_template('admin/gestionar_provincias.html', provincias=provincias)


@admin_bp.route('/provincias/edit/<int:id>', methods=['POST'])
@login_required
@roles_required('admin')
def edit_provincia(id):
    nuevo_nombre = request.form['nombre'].strip().title()
    es_costera = 'es_costera' in request.form
    editar_provincia(id, nuevo_nombre, es_costera)
    flash('Provincia actualizada.', 'info')
    return redirect(url_for('admin_bp.provincias'))


@admin_bp.route('/provincias/delete/<int:id>')
@login_required
@roles_required('admin')
def delete_provincia(id):
    eliminar_provincia(id)
    flash('Provincia eliminada.', 'warning')
    return redirect(url_for('admin_bp.provincias'))


@admin_bp.route('/conexiones', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def conexiones():
    if request.method == 'POST':
        origen_id = int(request.form['origen_id'])
        destino_id = int(request.form['destino_id'])
        costo = float(request.form['costo'])
        agregar_conexion(origen_id, destino_id, costo)
        flash('Conexión agregada con éxito.', 'success')
        return redirect(url_for('admin_bp.conexiones'))

    conexiones = listar_conexiones()
    provincias = listar_provincias()
    return render_template(
        'admin/gestionar_conexiones.html',
        conexiones=conexiones,
        provincias=provincias
    )


@admin_bp.route('/conexiones/delete/<int:id>')
@login_required
@roles_required('admin')
def delete_conexion(id):
    eliminar_conexion(id)
    flash('Conexión eliminada.', 'warning')
    return redirect(url_for('admin_bp.conexiones'))


@admin_bp.route('/ver_grafo')
@login_required
@roles_required('admin')
def ver_grafo():
    return render_template('admin/ver_grafo.html')


@admin_bp.route('/usuarios')
@login_required
@roles_required('admin')
def usuarios():
    # Lista todos los usuarios para el panel de administración
    usuarios_list = User.query.all()
    return render_template('admin/usuarios.html', usuarios=usuarios_list)
