from flask_app.config.mysqlconnection import connectToMySQL
from string import Template


# Tan solo hacemos esto mismo, pero desde el otro lado también
class Usuario:
    def __init__(self, diccionario):
        self.id = diccionario['id_usuario']
        self.nombre = diccionario['nombre_usuario']
        self.amistades = []


    @classmethod
    def traer_todos(cls):
        query = "SELECT id as id_usuario, CONCAT(first_name,' ',last_name) AS nombre_usuario FROM users"
        respuesta = connectToMySQL().query_db(query)
        usuarios = []
        for usuario in respuesta:
            usuarios.append(cls(usuario))
        return usuarios

    @classmethod
    def verificar_amistad(cls, data):
        query = Template('SELECT friend_id FROM friendships WHERE user_id = $id_usuario;').substitute(**data)
        respuesta = connectToMySQL().query_db(query)
        amigos_id = []
        if respuesta:
            for fila in respuesta:
                amigos_id.append(fila['friend_id'])
            print(amigos_id)
            return amigos_id
        else:
            return False


    @classmethod #Lo hice de esta manera para que queden todos con todos
    def usuarios_con_amistades(cls):
        query = "SELECT t1.id as id_usuario, CONCAT(t1.first_name,' ',t1.last_name) AS nombre_usuario, CONCAT(t3.first_name,' ',t3.last_name) AS nombre_amistad, t3.id as id_amistad FROM users as t1 INNER JOIN friendships as t2 ON t1.id = t2.user_id INNER JOIN users as t3 ON t2.friend_id = t3.id ORDER BY nombre_usuario;"
        respuesta = connectToMySQL().query_db(query)
        usuarios = []
        for fila in respuesta:
            usuario = cls(fila)
            diccionario = {
                'id_usuario': fila['id_amistad'],
                'nombre_usuario': fila['nombre_amistad']
            }
            usuario.amistades.append(cls(diccionario))
            usuarios.append(usuario)
        return usuarios

    # Añadir usuario sin relación
    @classmethod
    def anadir_usuario(cls, data):
        query = Template(
            'INSERT INTO users (first_name, last_name, created_at, updated_at) VALUES ("$nombre", "$apellido", NOW(), NOW());').substitute(
            **data)
        return connectToMySQL().query_db(query, data)


    # Relaciones
    @classmethod  # En realidad podría reutilizar el mismo que usan en el modelo de autor, en el controlador de libros
    def nueva_relacion(cls, data):
        query = Template('INSERT INTO friendships (user_id, friend_id) VALUES ($id_usuario, $id_amigo);').substitute(**data)
        return connectToMySQL().query_db(query, data)

    # Este es especial, otra funcionalidad nueva que se me ocurrió
    @classmethod
    def solitos(cls):
        query = "SELECT t1.id as id_usuario, CONCAT(t1.first_name,' ',t1.last_name) AS nombre_usuario, CONCAT(t3.first_name,' ',t3.last_name) AS nombre_amistad, t3.id as id_amistad FROM users as t1 LEFT JOIN friendships as t2 ON t1.id = t2.user_id LEFT JOIN users as t3 ON t2.friend_id = t3.id WHERE t2.user_id IS NULL;"
        respuesta = connectToMySQL().query_db(query)
        usuarios = []
        for usuario in respuesta:
            usuarios.append(cls(usuario))
        return usuarios


