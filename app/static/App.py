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

#  if para comparar la fecha      if   fecha>=(data+3):


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


@app.route("/seguimiento")
def seguimiento():
    """
    Método que permite ingresar a la página del seguimiento del profesor
    """

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM seguimiento")
    data = cur.fetchall()
    return render_template("seguimientoProfesor.html", seguimientos=data)


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

                        return render_template("nuevoLayout.html")


                    else:

                        return render_template("layoutProfesor.html")

                                       
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
        
    else:
        return render_template("login.html")



@app.route("/add_seguimiento", methods=["POST"])
def add_seguimiento():
    """
    Método que permite agregar un seguimiento del profesor
    """

    if request.method == "POST":
        idseguimiento = request.form["Idseguimiento"]
        profesor = request.form["Profesor"]
        prestamo = request.form["Prestamo"]
        calificacion = request.form["Calificacion"]

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO seguimiento (Idseguimiento,Profesor,Prestamo,Calificacion) VALUES (%s, %s, %s,%s)",
            (idseguimiento, profesor, prestamo, calificacion),
        )
        mysql.connection.commit()
        flash("Seguimeitno Agregado")

        return redirect(url_for("index"))


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
        rol= request.form["Rol"]

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO personas (Nombre,Apellido,Cedula,Email,Programa,Contraseña,Rol) VALUES (%s, %s, %s,%s, %s, %s, %s)",
            (nombre, apellido, cedula, email, programa, contraseña,rol),
        )
        mysql.connection.commit()
        flash("Profesor Agregado")

        return redirect(url_for("index"))


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
        rol= request.form["rol"]
        cur = mysql.connection.cursor()
        cur.execute(
            """
            UPDATE personas
            SET nombre = %s,
                apellido = %s,
                email = %s,
                programa = %s,
                contraseña = %s

            WHERE cedula = %s
          """,
            (nombre, apellido,  email, programa, contraseña, cedula)
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
    return redirect(url_for("index"))


@app.route("/Busqueda")
def Busqueda():
    """
    Método que permite ingresar a la página de buscar profesores
    """
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM personas")
    data = cur.fetchall()
    return render_template("buscarpersona.html", persona=data)


@app.route("/Buscar", methods=["POST"])
def Buscar():
    if request.method == "POST":
        busqueda = request.form["busqueda"]
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM personas WHERE cedula = %(cedula)s", {"cedula": busqueda}
        )
        data = cur.fetchall()
        print(data)
        return render_template("buscarpersona.html", personas=data)


# --------------------------------END Profesores--------------------------------

# --------------------------------START Equipos--------------------------------


@app.route("/BuscarEquipo", methods=["POST"])
def BuscarEquipo():
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


@app.route("/inicioEquipos")
def inicioEquipos():
    """
    Método que permite ingresar a la página de registrar equipos
    """
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM equipos")
    data = cur.fetchall()
    return render_template("registrarEquipo.html", equipos=data)


@app.route("/buscarEquipos")
def buscarEquipos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM equipos")
    data = cur.fetchall()
    return render_template("buscarEquipo.html", equipo=data)


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
            (nombre, facultad, estadoActual,disponibilidad),
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
    return redirect(url_for("inicioEquipos"))


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
            (nombre, facultad, estadoActual, disponibilidad, id)
        )
        mysql.connection.commit()
        flash("equipo actualizado satisfactoriamente")
        return redirect(url_for("inicioEquipos"))


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
        #disponibilidad = request.form["disponibilidad"]
        #estado = request.form['estado']
        fechaS = time.strftime("%A %B, %d %Y %H:%M:%S")
        fechaSolicitud = str(fechaS)

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO prestamos (idEquipo,cedulaProfesor,salon,horario,fecha,fechaSolicitud) VALUES (%s, %s, %s, %s, %s, %s)",
            (
                idEquipo,
                cedulaProfesor,
                salon,
                horario,
                fecha,
                #estado,
                fechaSolicitud,
            ),
        )
        mysql.connection.commit()
        flash("Prestamo agregadisimo")

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
            (
                idEquipo,
                cedulaProfesor,
                salon,
                horario,
                fecha,
                estado,
                idPrestamo,
            ),
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
            "SELECT * FROM prestamos WHERE idPrestamo = %(idPrestamo)s",
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

if __name__ == "__main__":
    app.run(port=3000, debug=True)

