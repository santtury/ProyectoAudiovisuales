from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_mysqldb import MySQL,MySQLdb
from flask import Flask
import time


app = Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='audiovisuales'


mysql = MySQL(app)

app.secret_key = 'mysecretkey'

    #  if para comparar la fecha      if   fecha>=(data+3):


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM profesores')
    data = cur.fetchall()
    return render_template('registrar.html', profesores = data)


@app.route("/getTime", methods=['GET'])
def getTime():
    data=time.strftime('%Y')
    print("AÑO:  ", data)
    print("server time : ", time.strftime('%A %B, %d %Y %H:%M:%S'));
    return render_template('registrar.html')

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM profesores WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()

        if len(user) > 0:
            if (password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("index.html")
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
    else:
        return render_template("login.html")


    return render_template('layoutAdmin.html')

@app.route('/add_profesor',  methods=['POST'])
def add_profesor():
    if  request.method == 'POST':
        nombre = request.form['Nombre']
        apellido = request.form['Apellido']
        cedula = request.form['Cedula']
        email = request.form['Email']
        programa = request.form['Programa']
        contraseña = request.form['Contraseña']
        data=time.strftime('%d')
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO profesores (Nombre,Apellido,Cedula,Email,Programa,Contraseña) VALUES (%s, %s, %s,%s, %s, %s)',
         (nombre,apellido,cedula,email,programa,contraseña))
        mysql.connection.commit()
        flash('Profesor Agregado')

        return redirect(url_for('index'))



@app.route('/edit/<cedula>')
def get_contact(cedula):
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM profesores WHERE cedula = %s',{cedula})
    data=cur.fetchall()
    print(data)
    return render_template('editar_profesor.html', profesor = data[0])

@app.route('/update/<string:cedula>', methods = ['POST'])
def update_profesor(cedula):
    if request.method == 'POST':
         nombre = request.form['nombre']
         apellido = request.form['apellido']
         email = request.form['email']
         programa = request.form['programa']
         contraseña = request.form['contraseña']
         cur = mysql.connection.cursor()
         cur.execute("""
            UPDATE profesores
            SET nombre = %s,
                apellido = %s,
                email = %s,
                programa = %s,
                contraseña = %s

            WHERE cedula = %s
          """,(nombre, apellido,cedula,email,programa,contraseña))
         cur.connection.commit()
         flash('actualizado')
         return redirect(url_for('index'))

@app.route('/delete/<string:cedula>')
def delete_profesor(cedula):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM profesores WHERE cedula=  %(Cedula)s', {'Cedula':cedula})
    mysql.connection.commit()
    return redirect(url_for('index'))

@app.route('/Busqueda')
def Busqueda():
   
    return render_template('buscarprofesor.html')


@app.route('/Buscar', methods = ['POST'])
def Buscar():
    if request.method == 'POST':
        busqueda = request.form['busqueda']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM profesores WHERE cedula = %(cedula)s", {'cedula':busqueda})
        data = cur.fetchall()
        print(data)
        return render_template('buscarprofesor.html', profesores = data)



if __name__== "__main__":
    app.run(port =3000, debug = True)