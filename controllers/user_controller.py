from extensions import db
from models.models import Provincia, HistorialConsulta
from flask_login import current_user
from utils.graph_utils import calcular_ruta

def listar_ciudades():
    return [p.nombre for p in Provincia.query.all()]

def procesar_consulta(origen, destino):
    camino, costo, costera = calcular_ruta(origen, destino)
    if current_user.is_authenticated:
        o = Provincia.query.filter_by(nombre=origen).first()
        d = Provincia.query.filter_by(nombre=destino).first()
        h = HistorialConsulta(
            usuario_id=current_user.id,
            origen_id=o.id,
            destino_id=d.id,
            pasar_por_costera=costera,
            camino=','.join(camino),
            costo_total=costo
        )
        db.session.add(h)
        db.session.commit()
    return {'camino': camino, 'costo': costo, 'costera': costera}
