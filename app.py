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
                    if ((datos_cliente["nombre"] == "anonimo") and (datos_cliente["password"] == "anonimo")):
                        
                        global ingreso
                        ingreso = False
                        return Response("Has ingresado como anonimo!", status=HTTPStatus.OK)

                    else:
                        ingreso = True
                        return Response("Bienvenido!", status=HTTPStatus.OK)

        return Response("Datos incorrectos", status=HTTPStatus.OK) #Fijarse dsps si queda el OK o el BadR

    else:
        return Response("{}", status=HTTPStatus.BAD_GATEWAY)

#Que despues te mande al home



#====================================
#ACA VA LA PARTE DE LO QUE PUEDE HACER EL USUARIO
#====================================

@app.route("/home/agregar", methods=["POST"])
def agregarPelis():

    if ((request.method == "POST") and (ingreso == True)):

        listaDeP = open("peliculas.json", "r+")
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

        if (("titulo" and "anio" and "director" and "genero" and "sinopsis" and "cartelera") in datos_cliente):
            nuevaPelicula = {
                "id": id,
                "titulo" : datos_cliente["titulo"],
                "anio" : datos_cliente["anio"],
                "director" : datos_cliente["director"],
                "genero" : datos_cliente["genero"],
                "sinopsis" : datos_cliente["sinopsis"],
                "cartelera" : datos_cliente["cartelera"],
                "AMB" : "alta", 
                "comentarios" : []
            }
            
            cantidadPeliculas = len(archivo["peliculas"])

            while (cantidadPeliculas > 0):

                for pelis in archivo["peliculas"]:
                    if ((datos_cliente["titulo"] == pelis["titulo"]) and (datos_cliente["director"] == pelis["director"]) and (datos_cliente["anio"] == pelis["anio"]) and (datos_cliente["genero"] == pelis["genero"])):
                        return Response("Esta pelicula ya esta agregada!", status=HTTPStatus.OK)

                    else:
                        cantidadPeliculas -= 1


            archivo["peliculas"].append(nuevaPelicula)
            listaDeP.seek(0)
            json.dump(archivo, listaDeP, indent = 4)

            global tieneComentarios
            tieneComentarios = False

            return jsonify(archivo["peliculas"][-1])

        else:
            return Response("Te has olvidado de algo!", status=HTTPStatus.OK)
   

    else:
        return Response("No tienes permisos para realizar eso!", status=HTTPStatus.BAD_GATEWAY)


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
    
#==============COMENTARIOS==============

@app.route("/home/<id>/comentarios") #Este es con GET 
def estructuraComentarios(id):
    if request.method == "GET":
        id_num = int(id)

        estructuraComentarios = [
            {
                "cometario" : "Escriba aqui el comentario que desea dejar"
            }
        ]

        return jsonify(estructuraComentarios)

    else:
        return Response("Metodo no permitido", status=HTTPStatus.BAD_GATEWAY)


@app.route("/home/<id>/comentarios", methods=["GET","POST"]) #Este es con el POST
def comentarios(id):

    if ((request.method == "POST") and (ingreso == True)):

        with open("peliculas.json") as listaDeP:
            archivo = json.load(listaDeP)

        id_num = int(id)

        for pelis in archivo["peliculas"]:
            if pelis["id"] == id_num:
                dondeID = archivo["peliculas"].index(pelis)

                #======================================
                datos_cliente = request.get_json()

                textoIngresado = datos_cliente

                listaDePelis = open("peliculas.json", "r+")
                archivoP = json.load(listaDePelis)
    
                for Pelis in archivoP["peliculas"]:

                    indicePeliculaID = archivoP["peliculas"][dondeID]

                    indicePeliculaID["comentarios"].append(textoIngresado["comentario"])
                    listaDePelis.seek(0)
                    json.dump(archivoP, listaDePelis, indent = 5)

                    tieneComentarios = True #cambiar, poner adentro del json

                    return jsonify(indicePeliculaID)

            else:
                return Response("No se ha encontrado la pelicula", status=HTTPStatus.BAD_REQUEST)




#=================ESTO ES LO DE LAS BUSQUEDAS=================
#Falta q muestre lo del AMB y los q tienen Portada(una lista lo q tienen, otra lista los q no)

@app.route("/generos")
def buscarGeneros():
    if request.method == "GET":

        with open("peliculas.json") as listaDeP:
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


#====================================
#ACA VA LA PARTE DE LO YA CARGADO EN EL SISTEMA
#====================================

#Siempre devuelve lo q se le pide al json.
#Ej: Si es la aprte del ABM, va peli por peli y buscando todos los amd, y despues los devuelve en un jsonify


@app.route("/directores")
def buscarDirectores():
    if request.method == "GET":
        with open("peliculas.json") as listaDeP:
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

        with open("peliculas.json") as listaDeP:
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

        with open("peliculas.json") as listaDeP:
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