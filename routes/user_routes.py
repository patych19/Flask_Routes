# routes/user_routes.py

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from controllers.user_controller import listar_ciudades, procesar_consulta
from models.models import HistorialConsulta, Provincia

user_bp = Blueprint('user_bp', __name__, url_prefix='/usuario')

@user_bp.route('/consulta', methods=['GET', 'POST'])
@login_required
def consulta():
    ciudades = listar_ciudades()
    resultado = None
    if request.method == 'POST':
        resultado = procesar_consulta(
            request.form['origen'],
            request.form['destino']
        )
    return render_template('user/consulta.html', ciudades=ciudades, resultado=resultado)

@user_bp.route('/historial')
@login_required
def historial():
    registros = HistorialConsulta.query.filter_by(usuario_id=current_user.id).all()
    datos = []
    for r in registros:
        origen = Provincia.query.get(r.origen_id).nombre
        destino = Provincia.query.get(r.destino_id).nombre
        datos.append({
            'origen': origen,
            'destino': destino,
            'costo': r.costo_total,
            'fecha': r.fecha_consulta
        })
    return render_template('user/historial.html', datos=datos)
