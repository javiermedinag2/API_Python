# Proyecto Flask que lee un archivo JSON y muestra su contenido en una página web 

from flask import Flask, request # Importa Flask que es el framework web
from pymongo import MongoClient # Importa MongoClient para interactuar con MongoDB

app = Flask(__name__) # Crea una instancia de la aplicación Flask
wsgi_app = app.wsgi_app # Exponer la aplicación WSGI para servidores compatibles con WSGI
Cliente = MongoClient('mongodb://root:root@localhost:27050') # Conecta al servidor MongoDB en localhost y puerto 27017
db = Cliente.Escuela # Selecciona la base de datos 'Escuela'
Libros = db.Libros # Selecciona la colección 'Libros'

@app.route('/') # Define la ruta para la URL raíz
def hello(): # Define la función que se ejecuta cuando se accede a la ruta

    salida = "<h1>Libros de Python 5P</h1>"
    salida += "<ul>"
    
    items=list(Libros.find())
    for libro in items: # Itera sobre cada libro en la lista de libros
        salida += "".join(f"<li>{libro['id']} - {libro['title']} - {libro['author']}</li>")
        # Agrega cada libro a la salida en formato HTML
    salida += "</ul>" # Cierra la lista HTML0
    return salida # Devuelve la salida como respuesta HTTP
@app.route('/libro',methods=["GET"]) 
def api_libro():
    salida=""
    if "id" in request.args:
        id = int(request.args["id"])
    else:
        return "No se ha proporcionado un identificador de libro"
    items=list(Libros.find({"id":id}))
    for libro in items:  # Itera sobre cada libro en la lista de libros
   #     if libro["id"]== id:
            salida += "".join(f"<li>{libro['id']} - {libro['isbn']} - {libro['title']} - {libro['author']}</li>")
            continue   
    return salida #falta validar si no encuentra el libro
####------------------------------------
@app.route('/libro/ingresa',methods=["POST"]) 
def obtener_libro():
    salida=""
    if "id" in request.form:    
        id = request.form["id"]
    else:
        return "No se ha proporcionado un identificador de libro"
    if "nombre" in request.form:
        nombre = request.form["nombre"]
    else:
        return "No se ha proporcionado nombre del libro"
    ISBN= request.form["ISBN"]
    genero= request.form["genero"]
    descripcion=request.form["descripcion"]
    publicacion=request.form["publicacion"]
    libro = {"id":int(id) ,"author": nombre, "isbn":ISBN, "genre":genero, "description":descripcion, "publishedYear":publicacion} # Crea un diccionario con los datos del libro
    print(libro)
    print("Libro recibido:", libro) # Imprime el libro recibido en la consola
    Libros.insert_one(libro)
    return f"Libro con id {id} y nombre {nombre} ingresado correctamente"
if __name__ == '__main__': # Si el script se ejecuta directamente, inicia el servidor de desarrollo
    import os # Importa el módulo os para acceder a variables de entorno
    HOST = os.environ.get('SERVER_HOST', 'localhost') # Obtiene el host del entorno o usa 'localhost' por defecto
    try:
        PORT = int(os.environ.get('SERVER_PORT', '1300')) # Obtiene el puerto del entorno o usa 5000 por defecto
    except ValueError:
        PORT = 1300 # Si la conversión falla, usa 5000 por defecto
    app.run(HOST, PORT) # Inicia el servidor de desarrollo en el host y puerto especificados
