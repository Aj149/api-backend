from flask import Flask,  jsonify, request
from psycopg2 import connect, extras
from flask_cors import CORS, cross_origin

app = Flask(__name__)

# conexión base de datos
host = 'localhost'
port = 5432
dbname = 'la trattoria'
user = 'postgres'
password = 'adrian'

CORS(app,resources={r"/app/*":{"origins": "*"}})

# función para conectar a la base de datos
def get_connection():
    conn = connect(host=host, port=port, dbname=dbname, user=user, password=password)
    return conn

CORS(app)
# @app.route('/')
# def holamundo():
#     return 'primera pagina'
# Insertar pago
@cross_origin
@app.route('/app/insertar/pagos', methods=['POST'])
def crear_pago():
    try:
        nuevo_pago = request.get_json()
        new_correo = nuevo_pago["correo"]
        new_numero_telefono = nuevo_pago["numero_telefono"]
        new_nombre = nuevo_pago["nombre"]
        new_fecha_Expiracion = nuevo_pago["fecha_Expiracion"]
        new_cedula = nuevo_pago["cedula"]
        new_dia=nuevo_pago["dia"]
        new_mes=nuevo_pago["mes"]
        new_anio=nuevo_pago["anio"]

        with get_connection() as conn, conn.cursor(cursor_factory=extras.RealDictCursor) as cursor:
            cursor.execute("INSERT INTO pagos_tarjeta (correo, numero_telefono, nombre, fecha_Expiracion, cedula, dia, mes, anio) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING *",
                           (new_correo, new_numero_telefono, new_nombre, new_fecha_Expiracion, new_cedula, new_dia, new_mes, new_anio))
            selectPagos = cursor.fetchall()

        return jsonify({"mensaje": "creado", "data": selectPagos})

    except KeyError as e:
        return jsonify({"error": f"Falta la clave en el JSON: {str(e)}"}), 400
    except Exception as e:
        return handle_error(e)

# Función para manejar errores
@app.errorhandler(Exception)
def handle_error(e):
    # Loguear el error podría ser útil para la depuración
    print(f"Error: {str(e)}")
    response = jsonify(error=str(e))
    response.status_code = 500
    return response


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
