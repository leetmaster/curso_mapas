import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from pathlib import Path
import re
import random
import folium

THIS_FOLDER = Path(__file__).parent.resolve()

def transformar_coordenadas(df):

    final_coords = []
    for wkt in list(df['WKT']):
        coords = re.sub(r'[a-zA-Z()]', '', wkt).strip().split(',')
        final_coords.append(list(map(lambda x: (float(x.split(' ')[1]), float(x.split(' ')[0])), coords)))

    return final_coords


def capa(df, coordenadas, tipo, nombre_capa, mostrar=False):
    feature_group = folium.FeatureGroup(name=nombre_capa, show=mostrar)  # overlay=False

    for index, coords in enumerate(coordenadas):

        if tipo == 'Punto':
            color = random.choices(
                ['gray', 'darkpurple', 'beige', 'lightgreen', 'lightblue', 'red', 'green', 'purple', 'darkred', 'black',
                 'cadetblue', 'blue', 'orange', 'pink', 'lightgray', 'darkgreen', 'darkblue', 'lightred'])[0]
            folium.Marker(
                location=[coords[0][0], coords[0][1]],
                popup=folium.Popup(popup(df.loc[index,:].to_dict())), #min_width=850, max_width=850
                icon=folium.Icon(color=color, icon='building', prefix='fa'), ).add_to(feature_group)
        if tipo == 'Poligono':
            folium.Polygon(coords,
                           weight=2,
                           color="red",
                           fill_color="yellow",
                           fill_opacity=0.3,
                           popup=f'Manzana {index}').add_to(feature_group)  # folium.Popup(popup(df.loc[index,:].to_dict()))).add_to(feature_group)
        if tipo == 'Linea':
            folium.PolyLine(coords,
                            weight=2,
                            color="red",
                            fill_color="yellow",
                            fill_opacity=0.3,
                            popup=folium.Popup(popup(df.loc[index,:].to_dict()))).add_to(feature_group)

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

def crear_capa(database, tabla, tipo, nombre_capa, mostrar = False):

    if isinstance(database, dict):
        database['table_name'] = tabla
        df = obtener_datos(database)
    else:
        df = pd.read_csv(database)

    coordenadas = transformar_coordenadas(df)
    return capa(df, coordenadas, tipo, nombre_capa, mostrar)


def obtener_datos(database):
    engine = create_engine(f"mysql+pymysql://{database['user']}:{database['password']}@{database['host']}/{database['db_name']}")

    return pd.read_sql_query(f'SELECT * FROM {database["table_name"]}', engine)


def AddDatosTabla(data, database):
    #engine = create_engine(f"mysql+pymysql://{database['user']}:{database['password']}@{database['host']}/{database['db_name']}")

    data.to_sql(database['table_name'], engine, if_exists= 'append', index=False)

