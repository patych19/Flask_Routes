# routes/graph_routes.py

from flask import Blueprint, render_template, request, send_file
from flask_login import login_required
from utils.helpers import roles_required
from controllers.graph_controller import procesar_consulta, listar_ciudades
from utils.graph_utils import generar_imagen

graph_bp = Blueprint('graph_bp', __name__, url_prefix='/rutas')

@graph_bp.route('/grafo')
@login_required
@roles_required('usuario')
def mostrar_grafo():
    """
    Devuelve la imagen PNG del grafo, resaltando la ruta
    si se pasa en la query string (?camino=A,B,C).
    """
    camino_str = request.args.get('camino', '')
    destacar = camino_str.split(',') if camino_str else None
    buf = generar_imagen(destacar)
    return send_file(buf, mimetype='image/png')

@graph_bp.route('/consulta', methods=['GET', 'POST'])
@login_required
@roles_required('usuario')
def consulta():
    """
    Muestra el formulario y, tras el POST, calcula la ruta,
    guarda el historial y renderiza el resultado.
    """
    ciudades = listar_ciudades()
    resultado = None

    if request.method == 'POST':
        origen  = request.form.get('origen')
        destino = request.form.get('destino')
        resultado = procesar_consulta(origen, destino)

    return render_template(
        'user/consulta.html',
        ciudades=ciudades,
        resultado=resultado
    )
