from flask import Flask, render_template, request, send_file
from funciones import obtener_datos, unir_capas, crear_capa
import folium
import pandas as pd

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/", methods=["GET", "POST"])
def index():
    # Configuración de la Base de Datos
    database = {'db_name': 'curso_mapas', 'user': 'postgres', 'password': 'password', 'host': 'localhost', 'port': 5432}
    
    if request.method == 'POST':
        # database['table_name'] = request.form['capa']
        # df =  obtener_datos(database)
        df = pd.read_csv(f'Datos/{request.form["capa"]}.csv')
        df.to_excel('Datos/capa_descargada.xlsx', index=False)
        return send_file('Datos/capa_descargada.xlsx', download_name=f"{request.form['capa']}.xlsx", as_attachment=True)

    # Poner el nombre de las tablas y aparte el nombre real de la capa
    tablas = {'puntos': 'Preescolar', 'poligonos': 'Manzanas','lineas': 'Calles'}

    # Inicializar el mapa
    m = folium.Map(location=[19.433289288179147, -99.14915327228645])


    # Crear Capas
    # database, tabla, tipo (Punto, Poligono, Linea), nombre_capa, mostrar = False
    capa_puntos= crear_capa('Datos/puntos.csv', '', 'Punto', 'Capa Preescolar de Puntos', mostrar = True)
    capa_lineas = crear_capa('Datos/lineas.csv', '', 'Linea', 'Capa Calles', mostrar=False)
    capa_poligono = crear_capa('Datos/poligonos.csv', '', 'Poligono', 'Capa Manzanas', mostrar=False)
    # Añadir las capas al mapa
    unir_capas(m, [capa_puntos, capa_lineas, capa_poligono])

    return render_template('index.html', tablas =tablas)

@app.route('/mapa-generado')
def mapa_generado():
    return render_template('mapa_generado.html')

# Antes de hacer deploy hay que setear el debug a False
if __name__ == '__main__':
    app.run(debug=False)