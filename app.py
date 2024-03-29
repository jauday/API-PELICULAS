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


@app.route("/home") #Mostrar las ultimas diez peliculas de la cartelera
def listaPelis():
    with open("peliculas.json", encoding="utf8") as listaDePelis:
        archivo = json.load(listaDePelis)

        listaVacia=["Ultimas 10 peliculas agregadas:"]
        cantidadPelisEnLista = 0

        cantidadPeliculas = len(archivo["peliculas"])
        cantidadP = len(archivo["peliculas"])

        revesPeliculas = []

        while (cantidadP > 0):
            for i in archivo["peliculas"]:
                revesPeliculas.insert(0, i)
                cantidadP -= 1

        while (cantidadPeliculas > 0):

            for peli in revesPeliculas:

                if ((peli not in listaVacia) and (cantidadPelisEnLista < 10)):
                    listaVacia.append(peli)
                    cantidadPeliculas -= 1
                    cantidadPelisEnLista += 1

                else:
                    cantidadPeliculas -= 1
                    continue

        return jsonify(listaVacia)
    
@app.route("/home/<id>", methods=["GET"])
def buscarPeli(id):

    with open("peliculas.json", encoding="utf8") as archivoPelis:
        pelisJson = json.load(archivoPelis)

    id_num = int(id)

    for pelis in pelisJson["peliculas"]:
        if pelis["id"] == id_num:
            dondeID = pelisJson["peliculas"].index(pelis)
            return jsonify(pelisJson["peliculas"][dondeID])

    return Response("No se ha encontrado la pelicula", status=HTTPStatus.BAD_REQUEST)


#====================================
#LOGIN
#====================================

@app.route("/login")  #Este es con el metodo GET
def getUsuarios():
    with open("usuarios.json") as bienvenida:
        archivo = json.load(bienvenida)

        for saludo in archivo["ingreso"]:
            return jsonify(archivo["ingreso"])

@app.route("/login", methods=["GET","POST"])
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


#====================================
#ACCIONES DEL USUARIO
#====================================

#==============AGREGAR==============
@app.route("/home/agregar") #Este es con el GET
def estructurAgregar():
    estructura = [ {
        "titulo" : " ",
        "anio" : " ",
        "director" : " ",
        "genero" : " ",
        "sinopsis" : " ",
        "cartelera" : " ",
        "vacio" : "Si se desea dejar algo vacio, poner dobles comillas con un espacio (como se ve en este ejemplo)"
        }
    ]

    return jsonify(estructura)

@app.route("/home/agregar", methods=["GET","POST"])
def agregarPelis():

    if ((request.method == "POST") and (ingreso == True)):

        listaDeP = open("peliculas.json", "r+", encoding="utf8")
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
                "tieneCom": 0,
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

#==============BORRAR==============
@app.route("/home/<id>", methods=["DELETE"])
def borrar(id):
    
    if ((request.method == "DELETE") and (ingreso == True)):

        id_num = int(id)
        if ((request.method == 'DELETE') and (ingreso == True)):   
            if ((id_num) and (ingreso == True)):
                with open("peliculas.json", 'r+') as archivoPelis:
                    pelisjson = json.load(archivoPelis)
                for pelis in pelisjson["peliculas"]:
                    if ((pelis["id"] == id_num) and (pelis["tieneCom"] == 0)):
                        dondeID = pelisjson["peliculas"].index(pelis)
                        pelisjson["peliculas"].pop(dondeID)
                        with open("peliculas.json", 'w') as archivoPelis:
                            archivoPelis.seek(0) 
                            json.dump(pelisjson, archivoPelis, indent=4)
                            return Response("Pelicula eliminada", HTTPStatus.OK)
            return Response("La peliucula tiene comentarios, no se puede eliminar", HTTPStatus.OK)
            

    else:
        return Response("No tienes permisos para realizar eso!", status=HTTPStatus.BAD_GATEWAY) 

#==============EDITAR==============

@app.route("/home/<id>", methods=["PUT"])
def editar(id):

    if ((request.method == "PUT") and (ingreso == True)):

        id_num = int(id)
        datos_cliente = request.get_json()
        if ((id_num) and (ingreso == True)):
            with open("peliculas.json", 'r') as archivoPelis:
                pelisjson = json.load(archivoPelis)
            for peli in pelisjson["peliculas"]: 
                if ((id_num == peli["id"]) and (peli["tieneCom"] == 0)):
                    peli['titulo']= datos_cliente['titulo']
                    peli['anio']= datos_cliente['anio']
                    peli['director']= datos_cliente['director']
                    peli['genero']= datos_cliente['genero']
                    peli['sinopsis']= datos_cliente['sinopsis']
                    peli['cartelera']= datos_cliente['cartelera']
                    with open("peliculas.json", 'w') as archivoPelis: 
                        archivoPelis.seek(0)
                        json.dump(pelisjson, archivoPelis,  indent=4) 
                else: continue        
            return Response("Pelicula actualizada", HTTPStatus.OK)
        else: return Response('Id invalido o nulo', HTTPStatus.BAD_REQUEST)

    else:
        return Response("No tienes permisos para realizar eso!", status=HTTPStatus.BAD_GATEWAY) 

    
#==============COMENTARIOS==============

@app.route("/home/<id>/comentarios") #Este es con GET 
def estructuraComentarios(id):
    if request.method == "GET":
        id_num = int(id)

        estructuraComentarios = [
            {
                "comentario" : "Escriba aqui el comentario que desea dejar"
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

                datos_cliente = request.get_json()

                textoIngresado = datos_cliente["comentario"]

                listaDePelis = open("peliculas.json", "r+")
                archivoP = json.load(listaDePelis)
    
                for Pelis in archivoP["peliculas"]:

                    indicePeliculaID = archivoP["peliculas"][dondeID]

                    indicePeliculaID["comentarios"].append(textoIngresado)
                    indicePeliculaID["tieneCom"]= 1
                    listaDePelis.seek(0)
                    json.dump(archivoP, listaDePelis, indent = 5)

                    return jsonify(indicePeliculaID)

            #else: return Response("No se ha encontrado la pelicula", status=HTTPStatus.BAD_REQUEST)

    else:
        return Response("No tienes permisos para realizar eso!", status=HTTPStatus.BAD_GATEWAY)

#====================================
#BUSCADOR
#====================================

@app.route("/generos")
def buscarGeneros():
    if request.method == "GET":

        with open("peliculas.json", encoding="utf8") as listaDeP:
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

@app.route("/directores")
def buscarDirectores():
    if request.method == "GET":
        with open("peliculas.json", encoding="utf8") as listaDeP:
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

        with open("peliculas.json", encoding="utf8") as listaDeP:
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

@app.route("/portada")
def portada():
    if request.method == "GET":
        with open("peliculas.json", encoding="utf8") as listaDeP:
            archivo = json.load(listaDeP)
    
        conPortada = ["Con cartelera"]
        sinPortada = ["Sin cartelera"]

        cantidadPeliculas = len(archivo["peliculas"])

        while (cantidadPeliculas > 0):

            for pelis in archivo["peliculas"]:
                if (pelis["cartelera"] == " "):

                    pelicula = []

                    pelicula.append(pelis["id"])
                    pelicula.append(pelis["titulo"])
                    sinPortada.append(pelicula)

                    cantidadPeliculas -= 1

                else: 
                    pelicula = []

                    pelicula.append(pelis["id"])
                    pelicula.append(pelis["titulo"])
                    conPortada.append(pelicula)

                    cantidadPeliculas -= 1

        portadas = []
        portadas.append(conPortada)
        portadas.append(sinPortada)

        return jsonify(portadas)

    else:
        return Response("Metodo no permitido", status=HTTPStatus.BAD_GATEWAY)
