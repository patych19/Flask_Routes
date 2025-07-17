# controllers/graph_controller.py

from flask_login import current_user
from utils.graph_utils import cargar_grafo, calcular_ruta, generar_imagen
from models.models import HistorialConsulta, Provincia
from extensions import db

def listar_ciudades():
    G = cargar_grafo()
    return list(G.nodes())

def procesar_consulta(origen_nombre, destino_nombre):
    # 1) Calcular ruta
    camino, costo, costera = calcular_ruta(origen_nombre, destino_nombre)

    # 2) Guardar en historial si hay usuario autenticado
    if current_user.is_authenticated:
        origen_obj = Provincia.query.filter_by(nombre=origen_nombre).first()
        destino_obj = Provincia.query.filter_by(nombre=destino_nombre).first()
        if origen_obj and destino_obj:
            registro = HistorialConsulta(
                usuario_id      = current_user.id,
                origen_id       = origen_obj.id,
                destino_id      = destino_obj.id,
                pasar_por_costera = costera,
                camino          = " → ".join(camino),
                costo_total     = costo
            )
            db.session.add(registro)
            db.session.commit()

    # 3) Devolver resultado
    return {
        'camino':  camino,
        'costo':   costo,
        'costera': costera
    }

def obtener_imagen_grafo():
    return generar_imagen()
