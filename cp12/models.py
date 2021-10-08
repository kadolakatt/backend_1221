import db 

class mensaje():
    id=0
    nombre=''
    correo=''
    mensaje=''
    respuesta=''
    estado=''

    #metodo constructor
    def __init__(self, p_id, p_nombre, p_correo, p_mensaje, p_respuesta='', p_estado ='S'):
        self.id = p_id
        self.nombre = p_nombre
        self.correo = p_correo
        self.mensaje = p_mensaje
        self.respuesta = p_respuesta
        self.estado = p_estado
    
    #Este es un metodo de clase, que sirve para "sobrecargar" constructores en python
    @classmethod
    def cargar(cls, p_id):
        sql = "SELECT * FROM mensajes WHERE id = ?;"
        obj = db.ejecutar_select(sql, [ p_id ])
        if obj:
            if len(obj)>0:
                #Llamamos al constructor de la clase para 
                #devolver una instancia de mensaje
                return cls(obj[0]["id"], obj[0]["nombre"], obj[0]["correo"], obj[0]["mensaje"], obj[0]["respuesta"], obj[0]["estado"])

        return None

    #Inserta en la base de datos un mensaje, a partir de los valores del objeto mensaje.
    def insertar(self):
        sql = "INSERT INTO mensajes (nombre, correo, mensaje, estado) VALUES (?,?,?,?);"
        afectadas = db.ejecutar_insert(sql, [ self.nombre, self.correo, self.mensaje, 'S' ])
        return (afectadas >0)

    #Borra el mensaje en la base de datos a partir del atributo id del objeto.
    def eliminar(self):
        sql = "DELETE mensajes WHERE id = ?;"
        afectadas = db.ejecutar_insert(sql, [ self.id ])
        return (afectadas >0)

    def responder(self):
        sql = "UPDATE mensajes SET respuesta = ?, estado='R' WHERE id = ?;"
        afectadas = db.ejecutar_insert(sql, [ self.respuesta, self.id ])
        return (afectadas >0)


    @staticmethod
    def listado():
        sql = "SELECT * FROM mensajes ORDER BY id;"
        return db.ejecutar_select(sql, None)