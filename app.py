from flask import Flask, jsonify, Response, request
from http import HTTPStatus

app = Flask(__name__)


#====================================
#ES EL LUGAR DONDE SE MUESTRAN LAS PELICULAS
#====================================


@app.route("/home")
def home():
    a=a
    return a

@app.route("/home/<pelicula>", methods=["GET"])
def mostrar(): #ACA SE MUESTRA LA INFO DE UNA PELICULA
    a=a
    return a


#====================================
#LOGIN
#====================================



@app.route("/login", methods=["GET","POST"])
#Si se encuentra el usuario, q siga, sino q large un erro
#Si entra como anonimo, el usuario es anonimo, se le da el valor de "anonimo"
def login() :
    if (request.method==["GET"]):
        a=a
        #Aca tiene q mostrar los datos

    elif (request.method==["POST"]): #aca se le manda la info para verificar
        if (usuario == True): #si ingresa como usuario
            usuario=usuario
            #Aca tendria q mostrar que ingreso con usuario y todos los permisos q se le da")
            #Despues los manda al home


        elif (usuario == False): #ingresa como anonimo
            #Aca lo manda directo a ver el home
            a=a

        else:
            a=a
            return Response("{}", status=HTTPStatus.NOT_FOUND)

    else:
        return Response("{}", status=HTTPStatus.NOT_FOUND)






#====================================
#ACA VA LA PARTE DE LO QUE PUEDE HACER EL USUARIO
#====================================
@app.route("/home/<pelicula>/comentarios", methods=["GET","PUT"])
def comentarios():
    #Es para mostrar los comentarios y agregar comentarios
    #Con el GET los muestra, con el PUT los agrega
    #Siempre chequear que el usuario este registrado
    a=a
    return a


@app.route("/home/<pelicula>", methods=["DELETE"])
def borrar():
    #Es para borrar una peli, verificar q no tenga comentarios
    #Siempre chequear que el usuario este registrado
    a=a
    return a


@app.route("/home/<pelicula>", methods=["PUT"])
def editar():
    #Editar solo los datos de la peli, no los comentarios
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

@app.route("/ABM", methods=["GET"]) #Devuelve la puntuacion de cada pelicula
def ABM():
    a=a
    return a


#====================================
#FUNCIONALIDAD ADICIONAL
#====================================

@app.route("/buscar") #Es un buscador q devuelve peliculas, directores, generos, etc
def buscar():
    a=a
    return a
