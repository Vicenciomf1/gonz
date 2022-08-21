from flask_app import app
from flask import render_template, request, redirect, flash
from flask_app.models.usuario import Usuario


@app.route('/')
def inicio():
    return redirect('/friendships')


@app.route('/friendships')
def amistades():
    contexto = {
        'usuarios': Usuario.usuarios_con_amistades(),
        'solitos': Usuario.traer_todos(),
        #'solitos': Usuario.solitos()  #Mete este si quieres hacer que sólo los forever alone puedan hacer nuevos amigos, pues los demás ya están conformes
    }
    return render_template('amistades.html', **contexto)


# DML INSERT sin relaciones
@app.route('/registrador-de-usuarios', methods=['POST'])
def registro_procesador():
    data = {
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
    }
    Usuario.anadir_usuario(data)
    return redirect('/friendships')


@app.route('/ser_amigos', methods=['POST'])
def crear_favorito_desde_autor():
    usuario = request.form['user_id']
    amigo = request.form['friend_id']
    data = {
        'id_usuario': usuario,
        'id_amigo': amigo
    }
    amistades = Usuario.verificar_amistad({'id_usuario': usuario})
    if not amistades: #Quizá este es un buen ejemplo para mostrar que se empieza desde premisas falsas hasta la verdaera? Cómo lo distribuyo?
        Usuario.nueva_relacion(data)
    elif int(amigo) in amistades:  # Puedo hacer también que un friend no se haga amigo de un user por ya serlo
        flash("No puedes crear amistades repetidas")  # Flashearlo
    elif usuario == amigo:
        flash("Una persona no puede ser amiga de sí misma, ¿o no? jaja") # Flashearlo
    else:
        Usuario.nueva_relacion(data)

    return redirect('/friendships')


