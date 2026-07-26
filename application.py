from flask import Flask, render_template, request, send_file
from sqlalchemy import create_engine
from pathlib import Path
from funciones import crear_capa, obtener_datos, unir_capas, crear_tabla
import folium
import pandas as pd

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

THIS_FOLDER = Path(__file__).parent.resolve()

@app.route("/", methods=["GET", "POST"])
def index():
    # Configuración de la Base de Datos
    database = {'db_name': '{nombre_de_base}', 'user': '{nombre_de usuario}', 'password': '{password}', 'host': '{direccion_de_la_base}'}

    if request.method == 'POST':
        
        database['table_name'] = request.form['capa']

        df = pd.read_csv(f'{THIS_FOLDER}/datos/{request.form["capa"]}.csv')
        df = obtener_datos(database)
        
        # Crea la capa a descargar como CSV
        df.to_csv(THIS_FOLDER / 'datos/capa_descargada.csv', index=False)
        return send_file(THIS_FOLDER / 'datos/capa_descargada.csv', download_name=f"{request.form['capa']}.csv", as_attachment=True)

    # Poner el nombre de las tablas y aparte el nombre real de la capa
    tablas = {'puntos': 'Cafeterías', 'poligonos': 'Barrios','lineas': 'Light Link Rail'}

    # Inicializar el mapa
    m = folium.Map(location=[47.608715, -122.3397979])

    # Crear Capas (database, tabla, tipo (Punto, Poligono, Linea), nombre_capa, mostrar = False)
    """
    Habilitar estas 3 líneas para ejecutar de manera local
    ======================================================
    """
    capa_puntos= crear_capa(THIS_FOLDER / 'datos/puntos.csv', '',  'Capa de puntos de cafeterías', mostrar = True)
    capa_lineas = crear_capa(THIS_FOLDER / 'datos/lineas.csv', '',  'Capa de línea del tren', mostrar=False)
    capa_poligono = crear_capa(THIS_FOLDER / 'datos/poligonos.csv', '', 'Capa de polígonos de barrios', mostrar=False)
    

    """
    Habilitar estas 3 líneas para ejecutar de de manera remota
    ==========================================================
    
    capa_puntos= crear_capa(database, 'puntos', 'Punto', 'Capa de puntos de cafeterías', mostrar = True)
    capa_lineas = crear_capa(database, 'lineas', 'Linea', 'Capa de línea del tren', mostrar=False)
    capa_poligono = crear_capa(database, 'poligonos', 'Poligono', 'Capa de polígonos de barrios', mostrar=False)
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
    """
    Servicio para escribir los datos en la base
    ===========================================
    """
    database = {'db_name': '{nombre_de_base}', 'user': '{nombre_de usuario}', 'password': '{password}', 'host': '{direccion_de_la_base}'}
    
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
