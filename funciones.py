import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from pathlib import Path
import re
import random
import folium

from shapely import wkt
from shapely.geometry import mapping
from shapely.geometry import Point, LineString

THIS_FOLDER = Path(__file__).parent.resolve()

def capa(df, nombre_capa, mostrar=False):

    feature_group = folium.FeatureGroup(name=nombre_capa, show=mostrar)

    colores = [
        'gray','darkpurple','beige','lightgreen','lightblue','red',
        'green','purple','darkred','black','cadetblue','blue',
        'orange','pink','lightgray','darkgreen','darkblue','lightred'
    ]
    print(nombre_capa)
    for _, row in df.iterrows():

        geom = wkt.loads(row["WKT"])
        popup_html = folium.Popup(popup(row))
        
        if isinstance(geom, Point):

            folium.Marker(
                location=(geom.y, geom.x),
                popup=popup_html,
                icon=folium.Icon(
                    color=random.choice(colores),
                    icon="coffee",
                    prefix="fa"
                ),
            ).add_to(feature_group)

        elif isinstance(geom, (LineString)):
            folium.GeoJson(
                    mapping(geom),
                    popup=popup_html,
                    style_function=lambda _: {
                        "color": "green",
                        "weight": 2,
                        "fillColor": "green",
                        "fillOpacity": 0.2,
                    },
                ).add_to(feature_group)

        else:
            folium.GeoJson(
                mapping(geom),
                popup=popup_html,
                style_function=lambda _: {
                    "color": "blue",
                    "weight": 1,
                    "fillColor": "gray",
                    "fillOpacity": 0.2,
                },
            ).add_to(feature_group)

    return feature_group

def unir_capas(m, capas):
    for capa in capas:
        capa.add_to(m)
    folium.LayerControl().add_to(m)
    m.save(THIS_FOLDER / 'templates/mapa_generado.html')
    return m

def popup(row):

        cad = ''
        for col, value in row.items():
            cad += f'<b>{col.upper()}:</b> {value.upper() if type(value) == str else str(value)}<br>\n'
        return cad

def crear_capa(database, tabla, nombre_capa, mostrar=False):

    if isinstance(database, dict):
        database["table_name"] = tabla
        df = obtener_datos(database)
    else:
        df = pd.read_csv(database)

    return capa(df, nombre_capa, mostrar)


def obtener_datos(database):
    engine = create_engine(f"mysql+pymysql://{database['user']}:{database['password']}@{database['host']}/{database['db_name']}")

    return pd.read_sql_query(f'SELECT * FROM {database["table_name"]}', engine)


def crear_tabla(data, database):
    engine = create_engine(f"mysql+pymysql://{database['user']}:{database['password']}@{database['host']}/{database['db_name']}")

    data.to_sql(database['table_name'], engine, if_exists= 'append', index=False)
