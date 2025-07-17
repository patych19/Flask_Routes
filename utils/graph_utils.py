# utils/graph_utils.py

import matplotlib
# 1) Forzar backend no interactivo (evita Tkinter)
matplotlib.use('Agg')

import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
from models.models import Provincia, Conexion

def cargar_grafo():
    G = nx.Graph()
    for p in Provincia.query.all():
        G.add_node(p.nombre, costera=p.es_costera)
    for c in Conexion.query.all():
        ori = Provincia.query.get(c.origen_id).nombre
        des = Provincia.query.get(c.destino_id).nombre
        G.add_edge(ori, des, weight=c.costo)
    return G

def calcular_ruta(origen, destino):
    G = cargar_grafo()
    camino = nx.dijkstra_path(G, source=origen, target=destino, weight='weight')
    costo  = nx.dijkstra_path_length(G, source=origen, target=destino, weight='weight')
    costeras = {n for n,d in G.nodes(data=True) if d.get('costera')}
    pasa_costera = any(ciudad in camino for ciudad in costeras)
    return camino, costo, pasa_costera

def generar_imagen(destacar_camino=None):
    """
    Dibuja el grafo y resalta 'destacar_camino' (lista de nodos) en rojo.
    Devuelve un BytesIO con la imagen PNG.
    """
    G = cargar_grafo()
    pos = nx.spring_layout(G, seed=42)

    # 2) Crear figura y ejes explícitamente
    fig, ax = plt.subplots(figsize=(10, 8))

    # Dibuja todos los nodos y aristas
    nx.draw(
        G, pos,
        with_labels=True,
        node_color='lightblue',
        node_size=1500,
        font_size=10,
        font_weight='bold',
        edge_color='gray',
        ax=ax
    )

    # Etiquetas de peso
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8, ax=ax)

    # Resaltar camino en rojo grueso
    if destacar_camino and len(destacar_camino) > 1:
        path_edges = list(zip(destacar_camino, destacar_camino[1:]))
        nx.draw_networkx_edges(
            G, pos,
            edgelist=path_edges,
            edge_color='red',
            width=3,
            ax=ax
        )

    ax.axis('off')

    # 3) Guardar la figura en el buffer
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)  # cierra solo esta figura
    buf.seek(0)
    return buf
