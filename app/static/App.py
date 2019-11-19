from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL, MySQLdb
from flask import Flask
from datetime import datetime, date, time, timedelta
import calendar
import time
import os


app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "audiovisuales"


mysql = MySQL(app)

app.secret_key = "mysecretkey"

#Comaster's

@app.route("/")
def index():
    """
    Método que permite ingresar a la página de inicio de la plataforma
    """

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM profesores")
    fecha = "14/10/2019"
    day = fecha[0] + fecha[1]
    dos = int(float(day))
    uno = time.strftime("%d")
    cast = str(uno)
    dia = int(float(uno))
    dias = dia + 3
    if dos >= dias:
        print("GUARDAR", cast)
        print("DIAS HABILES:  ", dias)
        print("FECHA SOLICITUD:  ", dos)
    data = cur.fetchall()
    return render_template("login.html", personas=data)


@app.route("/inicio")
def inicio():
    """
    Método que permite ingresar a la página de registrar profesores
    """

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM personas")
    data = cur.fetchall()
    return render_template("registrarPersonas.html", personas=data)


@app.route("/getTime", methods=["GET"])
def getTime():
    """
    Método que permite capturar el tiempo y la fecha del servidor
    """

    dia = time.strftime("%Y")
    print("DIAAAAA:  ", dia)
    print("server time : ", time.strftime("%A %B, %d %Y %H:%M:%S"))
    return render_template("registrar.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Método que permite ingresar al login de la plataforma
    """

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM personas WHERE email=%s", (email,))
        user = curl.fetchone()
        print(str(password))

        curl.close()
        if len(user) > 0:
            if str(user["contraseña"]) == str(password):

                if user["rol"] == "administrador":

                    return render_template("layoutAdmin.html")

                else:

                    return render_template("layoutProfesor.html")

            else:
                return "Error password and email not match"
        else:
            return "Error user not found"

    else:
        return render_template("login.html")


# --------------------------------START Profesores--------------------------------


@app.route("/add_profesor", methods=["POST"])
def add_profesor():
    """
    Método que permite registrar un profesor en la plataforma
    """
    if request.method == "POST":
        nombre = request.form["Nombre"]
        apellido = request.form["Apellido"]
        cedula = request.form["Cedula"]
        email = request.form["Email"]
        programa = request.form["Programa"]
        contraseña = request.form["Contraseña"]
        rol = request.form["Rol"]

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO personas (Nombre,Apellido,Cedula,Email,Programa,Contraseña,Rol) VALUES (%s, %s, %s,%s, %s, %s, %s)",
            (nombre, apellido, cedula, email, programa, contraseña, rol),
        )
        mysql.connection.commit()
        flash("Profesor Agregado")

        return redirect(url_for("inicio"))


@app.route("/edit/<cedula>")
def get_contact(cedula):

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM personas WHERE cedula = {0}".format(cedula))
    data = cur.fetchall()
    print(data)
    return render_template("editar_persona.html", persona=data[0])


@app.route("/update/<string:cedula>", methods=["POST"])
def update_profesor(cedula):
    """
    Método que permite editar a un profesor en la plataforma
    """
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        email = request.form["email"]
        programa = request.form["programa"]
        contraseña = request.form["contraseña"]
        rol = request.form["rol"]
        cur = mysql.connection.cursor()
        cur.execute(
            """
            UPDATE personas
            SET nombre = %s,
                apellido = %s,
                email = %s,
                programa = %s,
                contraseña = %s,
                rol= %s
                WHERE cedula = %s
                """,
            (nombre, apellido, email, programa, rol, contraseña, cedula),
        )
        cur.connection.commit()
        flash("actualizado")
        return redirect(url_for("inicio"))


@app.route("/delete/<string:cedula>")
def delete_profesor(cedula):
    """
    Método que permite eliminar un profesor de la plataforma
    """
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM personas WHERE cedula=  %(Cedula)s", {"Cedula": cedula})
    mysql.connection.commit()
    return redirect(url_for("inicio"))


@app.route("/Busqueda")
def Busqueda():
    """
    Método que permite ingresar a la página de buscar profesores
    """
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM personas")
    data = cur.fetchall()
    return render_template("buscarpersona.html", personas=data)


@app.route("/Buscar", methods=["POST"])
def Buscar():
    if request.method == "POST":
        busqueda = request.form["busqueda"]
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM personas WHERE cedula = %(busca)s OR rol=%(busca)s",
            {"busca": busqueda},
        )
        data = cur.fetchall()
        print(data)
        return render_template("buscarpersona.html", personas=data)


# --------------------------------END Profesores--------------------------------
# --------------------------------START Inventario--------------------------------


@app.route("/BuscarInventario", methods=["POST"])
def BuscarInventario():
    """
    Método que permite hacer el inventari de los equipos por parte del administrador
    """
    if request.method == "POST":
        busquedaEquipo = request.form["busquedaEquipo"]
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM equipos WHERE id = %(busca)s OR facultad = %(busca)s",
            {"busca": busquedaEquipo},
        )
        data = cur.fetchall()
        print(data)
        return render_template("inventarioEquipo.html", inventarios=data)


@app.route("/buscarInventarios")
def buscarInventarios():
    """
    Método que permite ingresar a la pagina para que el administrador puedan ver el inventario de equipos
    """
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM equipos")
    data = cur.fetchall()
    return render_template("inventarioEquipo.html", inventarios=data)


# --------------------------------END Inventario--------------------------------

# --------------------------------START Equipos--------------------------------


@app.route("/listarEquipos", methods=["POST"])
def listarEquipos():
    """
    Método que permite listar los equipos para los profesores
    """
    if request.method == "POST":
        busquedaEquipo = request.form["busquedaEquipo"]
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM equipos WHERE id = %(busca)s OR facultad = %(busca)s",
            {"busca": busquedaEquipo},
        )
        data = cur.fetchall()
        print(data)
        return render_template("listarEquipos.html", equipos=data)


@app.route("/listadoEquipos")
def listadoEquipos():
    """
    Método que permite ingresar a la pagina para que los profesores puedan ver los equipos
    """
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM equipos")
    data = cur.fetchall()
    return render_template("listarEquipos.html", equipos=data)


@app.route("/BuscarEquipo", methods=["POST"])
def BuscarEquipo():
    """
    Método que permite hacer el inventari de los equipos por parte del administrador
    """
    if request.method == "POST":
        busquedaEquipo = request.form["busquedaEquipo"]
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM equipos WHERE id = %(busca)s OR facultad = %(busca)s",
            {"busca": busquedaEquipo},
        )
        data = cur.fetchall()
        print(data)
        return render_template("buscarEquipo.html", equipos=data)


@app.route("/buscarEquipos")
def buscarEquipos():
    """
    Método que permite ingresar a la pagina para que el administrador puedan ver el inventario de equipos
    """
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM equipos")
    data = cur.fetchall()
    return render_template("buscarEquipo.html", equipos=data)


@app.route("/inicioEquipos")
def inicioEquipos():
    """
    Método que permite ingresar a la página de registrar equipos
    """
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM equipos")
    data = cur.fetchall()
    return render_template("registrarEquipo.html", equipos=data)


@app.route("/add_equipo", methods=["POST"])
def add_equipo():
    """
    Método que permite añadir un equipo a la plataforma
    """

    if request.method == "POST":
        nombre = request.form["nombre"]
        facultad = request.form["facultad"]
        estadoActual = request.form["estadoActual"]
        disponibilidad = request.form["disponibilidad"]
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO equipos (nombre,facultad,estadoActual,disponibilidad) VALUES (%s,%s,%s,%s)",
            (nombre, facultad, estadoActual, disponibilidad),
        )
        mysql.connection.commit()
        flash("Equipo Agregado")

        return redirect(url_for("inicioEquipos"))


@app.route("/deleteEquipo/<string:id>")
def delete_equipo(id):
    """
    Método que permite eliminar un equipo de la plataforma
    """
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM equipos WHERE id= {0}".format(id))
    mysql.connection.commit()
    flash("Equipo eliminado")
    return redirect(url_for("buscarEquipos"))


@app.route("/editarEquipo/<id>")
def editar_equipo(id):
    """
    Método que permite ingresar a la página de editar equipos
    """
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM equipos WHERE id= %s", (id))
    data = cur.fetchall()
    return render_template("editarEquipo.html", equipo=data[0])


@app.route("/updateEquipo/<id>", methods=["POST"])
def updateEquipo(id):
    if request.method == "POST":
        nombre = request.form["nombre"]
        facultad = request.form["facultad"]
        estadoActual = request.form["estadoActual"]
        disponibilidad = request.form["disponibilidad"]
        cur = mysql.connection.cursor()
        cur.execute(
            """
        UPDATE equipos
        SET nombre = %s,
          facultad = %s,
          estadoActual = %s,
          disponibilidad=%s
          WHERE id = %s
      """,
            (nombre, facultad, estadoActual, disponibilidad, id),
        )
        mysql.connection.commit()
        flash("equipo actualizado satisfactoriamente")
        return redirect(url_for("buscarEquipos"))


# --------------------------------END Equipos--------------------------------

# --------------------------------START Prestamos--------------------------------


@app.route("/prestamos")
def prestamos():
    """
    Método que permite ingresar a la página de registrar Prestamos
    """

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM prestamos")
    data = cur.fetchall()
    return render_template("registrarPrestamo.html", prestamos=data)


@app.route("/listarPrestamos")
def listarPrestamos():
    """
    Método que permite listar las solicitudes de prestamos realizadas
    """

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM prestamos")
    data = cur.fetchall()
    return render_template("listarSolicitudes.html", prestamos=data)


@app.route("/add_prestamo", methods=["POST"])
def add_prestamo():
    """
    Método que permite registrar un prestamos en la plataforma
    """

    if request.method == "POST":

        # idPrestamo = request.form['idPrestamo']
        idEquipo = request.form["idEquipo"]
        cedulaProfesor = request.form["cedulaProfesor"]
        salon = request.form["salon"]
        horario = request.form["horario"]
        fecha = request.form["fecha"]
        # disponibilidad = request.form["disponibilidad"]
        # estado = request.form['estado']
        fechaS = time.strftime("%A %B, %d %Y %H:%M:%S")
        fechaSolicitud = str(fechaS)
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM personas WHERE cedula=%s", (cedulaProfesor,))
        user = curl.fetchone()
        uq = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        uq.execute("SELECT * FROM equipos WHERE id=%s", (idEquipo,))
        eq = uq.fetchone()

        if (not user is None) and (not eq is None):

            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO prestamos (idEquipo,cedulaProfesor,salon,horario,fecha,fechaSolicitud) VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    idEquipo,
                    cedulaProfesor,
                    salon,
                    horario,
                    fecha,
                    # estado,
                    fechaSolicitud,
                ),
            )
            mysql.connection.commit()
            flash("Prestamo Agregado")

            return redirect(url_for("prestamos"))
        else:

            flash("Prestamo No Agregado verifique que la informacion sea valida")

            return redirect(url_for("prestamos"))


@app.route("/deletePrestamo/<string:idPrestamo>")
def delete_prestamo(idPrestamo):
    """
    Método que permite eliminar un prestamo de la plataforma
    """
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM prestamos WHERE idPrestamo= {0}".format(idPrestamo))
    mysql.connection.commit()
    flash("Prestamo eliminado :.v")
    return redirect(url_for("prestamos"))


@app.route("/editarPrestamo/<idPrestamo>")
def editar_prestamo(idPrestamo):
    """
    Método que permite ingresar a la página de editar prestamos
    """
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM prestamos WHERE idPrestamo=%(idp)s", {"idp": idPrestamo})
    data = cur.fetchall()
    return render_template("editarPrestamo.html", prestamo=data[0])


@app.route("/updatePrestamo/<string:idPrestamo>", methods=["POST"])
def update_prestamo(idPrestamo):
    if request.method == "POST":
        idEquipo = request.form["idEquipo"]
        cedulaProfesor = request.form["cedulaProfesor"]
        salon = request.form["salon"]
        horario = request.form["horario"]
        fecha = request.form["fecha"]
        estado = request.form["estado"]
        cur = mysql.connection.cursor()
        cur.execute(
            """
            UPDATE prestamos
            SET idEquipo = %s,
                cedulaProfesor = %s,
                salon = %s,
                horario = %s,
                fecha = %s,
                estado = %s

            WHERE idPrestamo = %s
          """,
            (idEquipo, cedulaProfesor, salon, horario, fecha, estado, idPrestamo),
        )
        cur.connection.commit()
        flash("Prestamo actualizado :d")
        return redirect(url_for("prestamos"))


@app.route("/buscarPrestamos")
def buscarPrestamo():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM prestamos")
    data = cur.fetchall()
    return render_template("buscarPrestamo.html", prestamo=data)


@app.route("/BuscarPrestamo", methods=["POST"])
def BuscarPrestamo():
    if request.method == "POST":
        busquedaPrestamo = request.form["busquedaPrestamo"]
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM prestamos WHERE idPrestamo = %(idPrestamo)s OR cedulaProfesor = %(idPrestamo)s",
            {"idPrestamo": busquedaPrestamo},
        )
        data = cur.fetchall()
        print(data)
        return render_template("buscarPrestamo.html", prestamos=data)


# --------------------------------END Prestamos--------------------------------


# --------------------------------START Peticiones--------------------------------


@app.route("/peticiones")
def peticiones():
    """
    Método que permite ingresar a la página de hacer peticiones
    """

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM peticiones")
    data = cur.fetchall()
    return render_template("registrarPeticion.html", peticiones=data)


@app.route("/listarPeticiones")
def listarPeticiones():
    """
    Método que permite listar las peticiones enviadas
    """

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM peticiones")
    data = cur.fetchall()
    return render_template("listarPeticiones.html", peticiones=data)


@app.route("/add_peticion", methods=["POST"])
def add_peticion():
    """
    Método que permite enviar una petición en la plataforma
    """

    if request.method == "POST":

        # idPeticion = request.form["idPeticion"]
        idPrestamo = request.form["idPrestamo"]
        cedulaProfesor = request.form["cedulaProfesor"]
        solicitud = request.form["solicitud"]
        comentario = request.form["comentario"]
        estado = "En proceso"
        fechaP = time.strftime("%A %B, %d %Y %H:%M:%S")
        fechaPeticion = str(fechaP)
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM personas WHERE cedula=%s", (cedulaProfesor,))
        user = curl.fetchone()
        uq = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        uq.execute("SELECT * FROM prestamos WHERE idPrestamo=%s", (idPrestamo,))
        eq = uq.fetchone()

        if (not user is None) and (not eq is None):
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO peticiones (idPrestamo,cedulaProfesor,solicitud,comentario,estado,fechaPeticion) VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    idPrestamo,
                    cedulaProfesor,
                    solicitud,
                    comentario,
                    estado,
                    fechaPeticion,
                ),
            )
            mysql.connection.commit()
            flash("Petición enviada")

            return redirect(url_for("peticiones"))
        else:

            flash("Peticion No Agregado verifique que la informacion sea valida")

            return redirect(url_for("peticiones"))


@app.route("/deletePeticion/<string:idPeticion>")
def delete_peticion(idPeticion):
    """
    Método que permite eliminar una peticion de la plataforma
    """
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM peticiones WHERE idPeticion= {0}".format(idPeticion))
    mysql.connection.commit()
    flash("Peticion eliminada")
    return redirect(url_for("listarPeticiones"))


@app.route("/editarPeticion/<idPeticion>")
def editar_peticion(idPeticion):
    """
    Método que permite ingresar a la página de editar peticiones
    """
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM peticiones WHERE idPeticion=%(idp)s", {"idp": idPeticion}
    )
    data = cur.fetchall()
    return render_template("editarPeticion.html", peticion=data[0])


@app.route("/updatePeticion/<string:idPeticion>", methods=["POST"])
def update_peticion(idPeticion):
    if request.method == "POST":
        idPrestamo = request.form["idPrestamo"]
        cedulaProfesor = request.form["cedulaProfesor"]
        solicitud = request.form["solicitud"]
        comentario = request.form["comentario"]
        estado = request.form["estado"]
        cur = mysql.connection.cursor()
        cur.execute(
            """
            UPDATE peticiones
            SET idPrestamo = %s,
                cedulaProfesor = %s,
                solicitud = %s,
                
                comentario = %s,
                estado = %s

            WHERE idPeticion = %s
          """,
            (idPrestamo, cedulaProfesor, solicitud, comentario, estado, idPeticion),
        )
        cur.connection.commit()
        flash("Petición actualizada")
        return redirect(url_for("listarPeticiones"))


@app.route("/buscarPeticiones")
def buscarPeticiones():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM peticiones")
    data = cur.fetchall()
    return render_template("buscarPeticion.html", peticion=data)


@app.route("/BuscarPeticion", methods=["POST"])
def BuscarPeticion():
    if request.method == "POST":
        busquedaPeticion = request.form["busquedaPeticion"]
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM peticiones WHERE idPeticion = %(idPeticion)s OR cedulaProfesor = %(idPeticion)s",
            {"idPeticion": busquedaPeticion},
        )
        data = cur.fetchall()
        print(data)
        return render_template("buscarPeticion.html", peticiones=data)

        
# --------------------------------END Peticiones--------------------------------

# --------------------------------START Calificacion--------------------------------


@app.route("/calificaciones")
def calificaciones():
    """
    Método que permite ingresar a la página de calificar el servicio
    """

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM calificaciones")
    data = cur.fetchall()
    return render_template("registrarCalificacion.html", calificaciones=data)


@app.route("/listarCalificaciones")
def listarCalificaciones():
    """
    Método que permite listar las calificaciones de los servicios
    """

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM calificaciones")
    data = cur.fetchall()
    return render_template("listarCalificaciones.html", calificaciones=data)


@app.route("/add_calificacion", methods=["POST"])
def add_calificacion():
    """
    Método que permite calificar un servicio en la plataforma
    """

    if request.method == "POST":

        # idCalificacion = request.form["idCalificacion"]
        idPrestamo = request.form["idPrestamo"]
        calificacion = request.form["calificacion"]

        uq = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        uq.execute("SELECT * FROM prestamos WHERE idPrestamo=%s", (idPrestamo,))
        eq = uq.fetchone()

        if not eq is None:

            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO calificaciones (idPrestamo,calificacion) VALUES (%s, %s)",
                (idPrestamo, calificacion),
            )
            mysql.connection.commit()
            flash("Servicio calificado")

            return redirect(url_for("calificaciones"))
        else:
            flash("Calificacion No Agregada verifique que la informacion sea valida")

            return redirect(url_for("calificaciones"))


# --------------------------------END Calificacion--------------------------------


# --------------------------------START Seguimiento--------------------------------


@app.route("/seguimientos")
def seguimientos():
    """
    Método que permite ingresar a la página de calificar el servicio
    """

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM seguimientos")
    data = cur.fetchall()
    return render_template("registrarSeguimiento.html", seguimientos=data)


@app.route("/listarSeguimientos")
def listarSeguimientos():
    """
    Método que permite listar las calificaciones de los servicioss
    """

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM seguimientos")
    data = cur.fetchall()
    return render_template("listarSeguimientos.html", seguimientos=data)


@app.route("/add_seguimientos", methods=["POST"])
def add_seguimientos():
    """
    Método que permite calificar un servicio en la plataforma
    """

    if request.method == "POST":

        # idCalificacion = request.form["idCalificacion"]
        idPrestamo = request.form["idPrestamo"]
        cedulaProfesor = request.form["cedulaProfesor"]
        calificacion = request.form["calificacion"]

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM personas WHERE cedula=%s", (cedulaProfesor,))
        user = curl.fetchone()
        uq = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        uq.execute("SELECT * FROM prestamos WHERE idPrestamo=%s", (idPrestamo,))
        eq = uq.fetchone()

        if (not user is None) and (not eq is None):

            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO seguimientos (idPrestamo,cedulaProfesor,calificacion) VALUES (%s, %s, %s)",
                (idPrestamo, cedulaProfesor, calificacion),
            )
            mysql.connection.commit()
            flash("Profesor calificado")

            return redirect(url_for("listarSeguimientos"))
        else:
            flash("Seguimiento NO agregado, verifique que la información sea válida")

            return redirect(url_for("seguimientos"))


# --------------------------------END Seguimiento--------------------------------

if __name__ == "__main__":
    app.run(port=3000, debug=True)

