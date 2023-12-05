from flask import Flask,  jsonify, request
from psycopg2 import connect, extras
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(__name__) 
CORS(app, resources={r"/*": {"origins": "*"}})
# app.config['CORS_HEADERS'] = 'Content-Type'

# conexión base de datos
host = 'localhost'
port = 5432
dbname = 'la trattoria'
user = 'postgres'
password = 'adrian'

# función para conectar a la base de datos
def get_connection():
    conn = connect(host=host, port=port, dbname=dbname, user=user, password=password)
    return conn


# @app.route('/')
# def holamundo():
#     return 'primera pagina'

# insertar pago
@app.post("/app/insertar/pagos")
def crear_pago():
    nuevo_pago = request.get_json()
    new_correo = nuevo_pago["correo"]
    new_numero_telefono = nuevo_pago["numero_telefono"]
    new_nombre = nuevo_pago["nombre"]
    new_fecha_expiracion = nuevo_pago["fecha_expiracion"]
    new_cedula = nuevo_pago["cedula"]
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    cursor.execute("INSERT INTO pagos_tarjeta (correo, numero_telefono, nombre, fecha_expiracion, cedula) VALUES (%s, %s, %s, %s, %s) RETURNING *",
    (new_correo, new_numero_telefono, new_nombre,  new_fecha_expiracion, new_cedula))
    selectPagos = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close
    print(selectPagos)
    return jsonify({"mensaje":"creado", "data": selectPagos})

# leer datos
@app.get("/app/ver/pagos")
def seleccionar_pago():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    cursor.execute("SELECT * FROM pagos_tarjeta")
    selectPagos = cursor.fetchall()
    print(selectPagos)
    return selectPagos

# leer un dato específico
@app.get("/app/especifico/pagos/<id>")
def seleccionar_pago2(id):
    conn = get_connection()
    cursor=conn.cursor(cursor_factory=extras.RealDictCursor)
    cursor.execute("SELECT * FROM pagos_tarjeta where id=%s", (id,))
    selectPagos = cursor.fetchone()
    print(selectPagos)
    if selectPagos is None:
        return jsonify({"mensaje ":"el pago no existe"}), 404
    return selectPagos

# actualizar datos
@app.put("/app/actualizar/pagos/<id>")
def update_person(id):
    return 'actualizando  id: ' + id

# borrar datos
@app.delete("/app/eliminar/pagos/<id>")
def borrando_pago(id):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
    cursor.execute("DELETE FROM pagos_tarjeta where id=%s RETURNING *", (id,))
    selectPagos = cursor.fetchone()
    print(selectPagos)
    if selectPagos is None:
        return jsonify({"mensaje ":"el pago ya a sido borrado"}), 404
    else:
        conn.commit()
        cursor.close()
        conn.close()
    return jsonify(selectPagos)

if __name__ == '__main__':
    app.run(debug=True)
