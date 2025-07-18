# routes/user_routes.py

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from controllers.user_controller import listar_ciudades, procesar_consulta
from models.models import HistorialConsulta, Provincia

user_bp = Blueprint('user_bp', __name__, url_prefix='/usuario')

@user_bp.route('/consulta', methods=['GET', 'POST'])
@login_required  # Solo usuario autenticado
def consulta():
    ciudades = listar_ciudades()
    resultado = None
    
    # Obtener parámetros de URL para prellenar formulario
    origen_param = request.args.get('origen', '')
    destino_param = request.args.get('destino', '')
    
    if request.method == 'POST':
        resultado = procesar_consulta(
            request.form['origen'],
            request.form['destino']
        )
    
    return render_template('user/consulta.html', 
                         ciudades=ciudades, 
                         resultado=resultado,
                         origen_prellenado=origen_param,
                         destino_prellenado=destino_param)

@user_bp.route('/historial')
@login_required  # Solo usuario autenticado
def historial():
    # Obtener registros ordenados por fecha más reciente
    registros = HistorialConsulta.query.filter_by(usuario_id=current_user.id)\
                                      .order_by(HistorialConsulta.fecha_consulta.desc())\
                                      .all()
    datos = []
    for r in registros:
        origen = Provincia.query.get(r.origen_id).nombre
        destino = Provincia.query.get(r.destino_id).nombre
        datos.append({
            'origen': origen,
            'destino': destino,
            'costo': r.costo_total,
            'fecha': r.fecha_consulta,
            'camino': r.camino.split(',') if r.camino else []
        })
    return render_template('user/historial.html', datos=datos)
