# Interactive GIS Maps

Utilizamos Python para generar un mapa web interactivo a partir de archivos CSV (que tamibén podemos subir a tablas en MySQL) que contienen geometrías en formato WKT. El proyecto utiliza Pandas, Shapely y Folium para representar automáticamente puntos, líneas y polígonos como capas independientes, con soporte para marcadores personalizados, ventanas emergentes y control de visibilidad. Su objetivo es facilitar la exploración y comunicación de datos geoespaciales sin depender de software SIG de escritorio, mediante una arquitectura sencilla y reutilizable para proyectos de análisis territorial, visualización de datos y cartografía digital.

### Antes de empezar:
- Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
- pip install virtualenv
- python -m venv ./ambiente
- ambiente/Scripts/activate
- pip install -r requirements.txt
- python application.py

### El resultado del proyecto se puede visualizar en:
https://leetmaster.pythonanywhere.com
