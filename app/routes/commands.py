from flask import Blueprint, jsonify, request
from sqlalchemy import text
from app import db

commands_bp = Blueprint('commands', __name__, url_prefix='/api/commands')


from flask import make_response

@commands_bp.route('/insert', methods=['OPTIONS'])
def handle_options():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")  # O especifica el origen permitido
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response

# Ruta para crear un comando
@commands_bp.route('/', methods=['POST'])
def create_comando():
    try:
        data = request.get_json()
        # Validación de campos requeridos
        if not all(k in data for k in ["id_sistema", "id_usuario", "id_tipo_comando", "codigo", "descripcion"]):
            return jsonify({"status": "error", "message": "Faltan campos requeridos"}), 400

        query = """
            INSERT INTO comandos (id_sistema, id_usuario, id_tipo_comando ,codigo, descripcion)
            VALUES (:id_sistema, :id_usuario, :id_tipo_comando, :codigo, :descripcion)
        """
        db.session.execute(text(query), {
            "id_sistema": data["id_sistema"],
            "id_usuario": data["id_usuario"],
            "id_tipo_comando": data["id_tipo_comando"],
            "codigo": data["codigo"],
            "descripcion": data["descripcion"]
        })
        db.session.commit()

        return jsonify({"status": "success", "message": "Comando creado correctamente"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": f"Error al crear el comando: {str(e)}"}), 500


@commands_bp.route('/usuario/<int:id_usuario>', methods=['GET'])
def get_comandos_usuario(id_usuario):
    try:
        query = """
            SELECT c.id, c.id_sistema, tc.nombre as tipo_comando, 
                   c.codigo, c.descripcion, c.fecha
            FROM comandos c
            JOIN tipos_comandos tc ON c.id_tipo_comando = tc.id_tipo_comando
            WHERE c.id_usuario = :id_usuario
            ORDER BY c.fecha DESC
        """
        result = db.session.execute(text(query), {"id_usuario": id_usuario}).fetchall()

        comandos = [{
            "id": row.id,
            "id_sistema": row.id_sistema,
            "tipo_comando": row.tipo_comando,
            "codigo": row.codigo,
            "descripcion": row.descripcion,
            "fecha": row.fecha.strftime('%Y-%m-%d %H:%M:%S')
        } for row in result]

        return jsonify({"status": "success", "comandos": comandos}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error al obtener comandos: {str(e)}"}), 500

@commands_bp.route('/sistema', methods=['GET'])
def get_comandos_sistema():
    try:
        id_sistema = request.args.get("id_sistema")
        if not id_sistema:
            return jsonify({"status": "error", "message": "Se requiere el parámetro 'id_sistema'"}), 400

        query = """
            SELECT c.id, tc.nombre as tipo_comando, 
                   c.codigo, c.descripcion, c.fecha
            FROM comandos c
            JOIN tipos_comandos tc ON c.id_tipo_comando = tc.id_tipo_comando
            WHERE c.id_sistema = :id_sistema
            ORDER BY c.fecha DESC
            LIMIT 10
        """
        result = db.session.execute(text(query), {"id_sistema": id_sistema}).fetchall()

        comandos = [{
            "id": row.id,
            "tipo_comando": row.tipo_comando,
            "codigo": row.codigo,
            "descripcion": row.descripcion,
            "fecha": row.fecha.strftime('%Y-%m-%d %H:%M:%S')
        } for row in result]

        return jsonify({"status": "success", "comandos": comandos}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error al obtener comandos: {str(e)}"}), 500

@commands_bp.route('/insert', methods=['POST'])
def insertar_comando():
    try:
        data = request.get_json()
        required_fields = ["id_sistema", "id_tipo_comando", "codigo", "descripcion"]
        if not all(k in data for k in required_fields):
            return jsonify({
                "status": "error", 
                "message": f"Faltan campos requeridos: {', '.join(required_fields)}"
            }), 400

        # Verificar que el tipo de comando existe
        tipo_comando_query = """
            SELECT id_tipo_comando FROM tipos_comandos 
            WHERE id_tipo_comando = :id_tipo_comando
        """
        tipo_comando = db.session.execute(text(tipo_comando_query), {
            "id_tipo_comando": data["id_tipo_comando"]
        }).fetchone()

        if not tipo_comando:
            return jsonify({
                "status": "error",
                "message": "El tipo de comando especificado no existe"
            }), 400

        query = """
            INSERT INTO comandos (id_sistema, id_usuario, id_tipo_comando, codigo, descripcion, fecha)
            VALUES (:id_sistema, :id_usuario, :id_tipo_comando, :codigo, :descripcion, NOW())
        """
        db.session.execute(text(query), {
            "id_sistema": data["id_sistema"],
            "id_usuario": data.get("id_usuario", 1),  # Usuario predeterminado si no se especifica
            "id_tipo_comando": data["id_tipo_comando"],
            "codigo": data["codigo"],
            "descripcion": data["descripcion"]
        })
        db.session.commit()

        return jsonify({"status": "success", "message": "Comando creado correctamente"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": f"Error al crear el comando: {str(e)}"}), 500