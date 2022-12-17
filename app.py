from flask import Flask, jsonify, Response, request, redirect
from http import HTTPStatus
import json

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
    return jsonify(peliculas)

@app.route("/home/<id>")
def mostrar(): #ACA SE MUESTRA LA INFO DE UNA PELICULA
    a=a
    return a


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

@app.route("/home/agregar", methods=["POST"]) #Agrega peliculas
def agregarPelis(): #Falta que compruebe si el usuario es anonimo o no

    if request.method == "POST":
        id = 20 #Ver alguna forma de q el numero suba solo, sin determinar esta variable
        id += 1 #O hacer un aleatoreo y una lista con los numeros ya utilizados

        #with open("pruebaArch.json") as listaDeP:
        #    archivo = json.load(listaDeP)

        #archivoEscritura = open("pruebaArch.json", "a")
        #archivoEscritura.write(archivo["peliculas"].append()

        datos_cliente = request.get_json()

        if "nombre" in datos_cliente: 
            peliculas.append({
                "id": id,
                "nombre" : datos_cliente["nombre"],
                "director" : datos_cliente["director"],
                "genero" : datos_cliente["genero"],
                "cartelera" : datos_cliente["cartelera"]}
            )

        return jsonify(peliculas)


    else:
        return Response("{}", status=HTTPStatus.BAD_GATEWAY)


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


@app.route("/directores", methods=["GET"])
def directores():
    b=b
    return b

@app.route("/generos", methods=["GET"])
def generos():
    a=a
    return a

@app.route("/directores/<director>", methods=["GET"]) #Aca tiene q devolver las pelicualas q dirigio
def direccion():
    a=a
    return a

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