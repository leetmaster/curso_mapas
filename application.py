from flask import Flask, render_template, request, send_file
from sqlalchemy import create_engine
from pathlib import Path
from funciones import crear_capa, obtener_datos, unir_capas
import folium
import pandas as pd

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

THIS_FOLDER = Path(__file__).parent.resolve()

@app.route("/", methods=["GET", "POST"])
def index():
    # Configuración de la Base de Datos
    database = {'db_name': '{nombre_base}', 'user': '{nombre_usuario}', 'password': '{password}', 'host': '{host_base}'}

    if request.method == 'POST':
        database['table_name'] = request.form['capa']
        #df = obtener_datos(database)
        df = pd.read_csv(f'{THIS_FOLDER}/datos/{request.form["capa"]}.csv')
        df.to_csv(THIS_FOLDER / 'datos/capa_descargada.csv', index=False)
        return send_file(THIS_FOLDER / 'datos/capa_descargada.csv', download_name=f"{request.form['capa']}.csv", as_attachment=True)

    # Poner el nombre de las tablas y aparte el nombre real de la capa
    tablas = {'puntos': 'Preescolar', 'poligonos': 'Manzanas','lineas': 'Calles'}

    # Inicializar el mapa
    m = folium.Map(location=[19.433289288179147, -99.14915327228645])

    # Crear Capas
    #database, tabla, tipo (Punto, Poligono, Linea), nombre_capa, mostrar = False
    
    capa_puntos= crear_capa(THIS_FOLDER / 'datos/puntos.csv', '', 'Punto', 'Capa Preescolar de Puntos', mostrar = True)
    capa_lineas = crear_capa(THIS_FOLDER / 'datos/lineas.csv', '', 'Linea', 'Capa Calles de Lineas', mostrar=False)
    capa_poligono = crear_capa(THIS_FOLDER / 'datos/poligonos.csv', '', 'Poligono', 'Capa Manzanas de Poligionos', mostrar=False)
    """
    capa_puntos= crear_capa(database, 'puntos', 'Punto', 'Capa Preescolar de Puntos', mostrar = True)
    capa_lineas = crear_capa(database, 'lineas', 'Linea', 'Capa Calles de Lineas', mostrar=False)
    capa_poligono = crear_capa(database, 'poligonos', 'Poligono', 'Capa Manzanas de oligionos', mostrar=False)
    """
    # Añadir las capas al mapa
    unir_capas(m, [capa_puntos, capa_lineas, capa_poligono])

    return render_template('index.html', tablas=tablas)

@app.route('/mapa-generado')
def mapa_generado():
    return render_template('mapa_generado.html')

# Ponemos una ruta para guardar el contenido de los CSV a la base de datos
@app.route('/escribir_datos')
def escribir_datos():
    database = {'db_name': '{nombre_base}', 'user': '{nombre_usuario}', 'password': '{password}', 'host': '{host_base}'}
    engine = create_engine(f"mysql+pymysql://{database['user']}:{database['password']}@{database['host']}/{database['db_name']}")

    puntos = pd.read_csv(THIS_FOLDER / 'datos/puntos.csv')
    lineas = pd.read_csv(THIS_FOLDER / 'datos/lineas.csv')
    poligonos = pd.read_csv(THIS_FOLDER / 'datos/poligonos.csv')

    engine = create_engine(f"mysql+pymysql://{database['user']}:{database['password']}@{database['host']}/{database['db_name']}")

    puntos.to_sql('puntos', engine, if_exists='replace', index=False)
    lineas.to_sql('lineas', engine, if_exists='replace', index=False)
    poligonos.to_sql('poligonos', engine, if_exists='replace', index=False)

    return render_template('success.html')

# Antes de hacer deploy hay que setear el debug a False
if __name__ == '__main__':
    app.run(debug=False)