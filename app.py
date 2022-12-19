from flask import Flask, jsonify, Response, request, redirect
from http import HTTPStatus
import json
import random

app = Flask(__name__)


#====================================
#ROOT
#====================================

@app.route("/")
def home():
    return redirect("/login", code=302)

#====================================
#ES EL LUGAR DONDE SE MUESTRAN LAS PELICULAS
#====================================


@app.route("/home") #Hacer q sean solo las 10 ultimas. Hacerlo con un for/while y una variable q se el vaya sumando
def listaPelis():
    return jsonify(peliculas) #Aca falta q devuelva el json

@app.route("/home/<id>")
def buscarPeli(id):

    with open("peliculas.json") as listaDeP:
        archivo = json.load(listaDeP)

    id_num = int(id)

    for pelis in archivo["peliculas"]:
        if pelis["id"] == id_num:
            dondeID = archivo["peliculas"].index(pelis)
            return jsonify(archivo["peliculas"][dondeID])

        #aACA VA LO Q SUCEDE CUANDO NO COINCIDEN


#====================================
#LOGIN
#====================================

@app.route("/login")  #Este es con el metodo GET
def getUsuarios():
    with open("usuarios.json") as bienvenida:
        archivo = json.load(bienvenida)

        for saludo in archivo["ingreso"]:
            return jsonify(archivo["ingreso"])


@app.route("/login", methods=["GET","POST"]) #Aca se permite el get y post, xq sino te manda el Bad Getaway
def login():
    if request.method == "POST":

        with open("usuarios.json") as listaUsuarios:
            archivo = json.load(listaUsuarios)

        datos_cliente = request.get_json()

        for acceso in archivo["usuarios"]:  

            if (("nombre" in datos_cliente) and ("password" in datos_cliente)):
                
                if ( (acceso["nombre"] == datos_cliente["nombre"]) and (acceso["password"] == datos_cliente["password"]) ):
                    return Response("Bienvenido!", status=HTTPStatus.OK)

        return Response("Datos incorrectos", status=HTTPStatus.OK) #Fijarse dsps si queda el OK o el BadR

    else:
        return Response("{}", status=HTTPStatus.BAD_GATEWAY)

#Que despues te mande al home



#====================================
#ACA VA LA PARTE DE LO QUE PUEDE HACER EL USUARIO
#====================================

@app.route("/home/agregar", methods=["POST"])
def agregarPelis(): #Falta que compruebe si el usuario es anonimo o no

    if request.method == "POST":

        listaDeP = open("pruebaArch.json", "r+")
        archivo = json.load(listaDeP)
        #========================================
        id = 0

        randomID = random.sample(range(800), 1)

        while (id == 0):

            for pelis in archivo["peliculas"]:
                if pelis["id"] == randomID:
                    continue
                elif pelis["id"] != randomID:
                    id = randomID[0]
                    break
                else:
                    return Response("Ha ocurrido un error y no se puede guardar la pelicula", status=HTTPStatus.OK)

        #========================================

        datos_cliente = request.get_json()

        if "titulo" in datos_cliente: #Falta que chequee si estan los datos necesarios
            nuevaPelicula = { #Falta q solo chequee duplicados en nombre y director
                "id": id,
                "titulo" : datos_cliente["titulo"],
                "anio" : datos_cliente["anio"],
                "director" : datos_cliente["director"],
                "genero" : datos_cliente["genero"],
                "sinopsis" : datos_cliente["sinopsis"],
                "cartelera" : datos_cliente["cartelera"], #Hacer q pueda aceptar "" como none o false, y links
                "AMB" : "subida", 
                "comentarios" : [],
            }
                
            archivo["peliculas"].append(nuevaPelicula)
            listaDeP.seek(0)
            json.dump(archivo, listaDeP, indent = 4)

            return jsonify(archivo["peliculas"][-1])

    else:
        return Response("Metodo no permitido", status=HTTPStatus.BAD_GATEWAY)


@app.route("/home/<id>", methods=["DELETE"])
def borrar(id):
    #Es para borrar una peli, verificar q no tenga comentarios
    #Siempre chequear que el usuario este registrado
    a=a
    return a


@app.route("/home/<id>", methods=["PUT"])
def editar(id):
    #Editar solo los datos de la peli, no los comentarios
    #Siempre chequear que el usuario este registrado
    a=a
    return a
    

@app.route("/home/<id>/comentarios", methods=["GET","PUT"])
def comentarios(id):
    #Es para mostrar los comentarios y agregar comentarios
    #Con el GET los muestra, con el PUT los agrega
    #Siempre chequear que el usuario este registrado
    a=a
    return a


#====================================
#ACA VA LA PARTE DE LO YA CARGADO EN EL SISTEMA
#====================================

#Siempre devuelve lo q se le pide al json.
#Ej: Si es la aprte del ABM, va peli por peli y buscando todos los amd, y despues los devuelve en un jsonify


@app.route("/directores")
def buscarDirectores():
    if request.method == "GET":
        with open("pruebaArch.json") as listaDeP:
            archivo = json.load(listaDeP)
    
        director = []

        cantidadPeliculas = len(archivo["peliculas"])

        while (cantidadPeliculas > 0):

            for pelis in archivo["peliculas"]:
                if (pelis["director"] in director):
                    cantidadPeliculas -= 1
                else:
                    director.append(pelis["director"])
                    cantidadPeliculas -= 1

        return jsonify(director)

    else:
        return Response("Metodo no permitido", status=HTTPStatus.BAD_GATEWAY)

@app.route("/directores/<director>")
def direccion(director):

    if request.method == "GET":

        with open("pruebaArch.json") as listaDeP:
            archivo = json.load(listaDeP)

        direccionPeliculas = []
        directorSTR = str(director)

        cantidadPeliculas = len(archivo["peliculas"])

        while (cantidadPeliculas > 0):

            for pelis in archivo["peliculas"]:

                if pelis["director"] == directorSTR:
                    direccionPeliculas.append(pelis["titulo"])
                    cantidadPeliculas -= 1    
                else:
                    cantidadPeliculas -= 1
    
        return jsonify(direccionPeliculas)
        
    else:
        return Response("Metodo no permitido", status=HTTPStatus.BAD_GATEWAY)


@app.route("/generos")
def buscarGeneros():
    if request.method == "GET":
        
        with open("pruebaArch.json") as listaDeP:
            archivo = json.load(listaDeP)
    
        generos = []

        cantidadPeliculas = len(archivo["peliculas"])

        while (cantidadPeliculas > 0):

            for pelis in archivo["peliculas"]:
                if (pelis["genero"] in generos):
                    cantidadPeliculas -= 1
                else:
                    generos.append(pelis["genero"])
                    cantidadPeliculas -= 1

        return jsonify(generos)
    
    else:
        return Response("Metodo no permitido", status=HTTPStatus.BAD_GATEWAY)

@app.route("/portada", methods=["GET"]) #Devuelve las peliculas q tienen imagen
def portada():
    a=a
    return a

@app.route("/ABM", methods=["GET"]) #Devuelve la alta, baja, y no se q mas
def ABM():
    a=a
    return a


#====================================
#FUNCIONALIDAD ADICIONAL
#====================================

@app.route("/buscar") #Es un buscador q devuelve peliculas, directores, generos, etc
def buscar(): #Q vaya agregando tambien que fue lo ultimo buscado en otra lista
    a=a
    return a


#====================================
#LISTAS
#====================================

peliculas = [
    {
        "id" : 127,
        "nombre" : "Titanic",
        "director" : "Burton",
        "genero" : "Romance",
        "cartelera" : None
    },
    {
        "id" : 20,
        "nombre" : "28",
        "director" : "Williams",
        "genero" : "Comedia",
        "cartelera" : True
    },
    {
        "id" : 5,
        "nombre" : "Trucy",
        "director" : "Shakespeare",
        "genero" : "Drama",
        "cartelera" : False
    },
    {
        "id" : 65,
        "nombre" : "Fabrica de chocolates",
        "director" : "Burton",
        "genero" : "Infaltil",
        "cartelera" : True
    }
]