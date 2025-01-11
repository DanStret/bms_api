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




@commands_bp.route('/sistemas/<int:id_sistema>', methods=['GET'])
def get_comandos_sistema(id_sistema):
    try: 

        query = """
            SELECT 
                s.id_sistema, 
                s.nombre AS sistema_nombre, 
                t.nombre AS comando_nombre, 
                t.descripcion AS comando_descripcion, 
                t.codigo_comando, t.id_tipo_comando
            FROM 
                sistemas s
            JOIN 
                sistemas_comandos sc ON s.id_sistema = sc.id_sistema
            JOIN 
                tipos_comandos t ON sc.id_tipo_comando = t.id_tipo_comando
            WHERE 
                s.id_sistema = :id_sistema;
        """
        result = db.session.execute(text(query), {"id_sistema": id_sistema}).fetchall()

        comandos = [{
            "id_sistema": row.id_sistema,
            "id_tipo_comando": row.id_tipo_comando,
            "sistema_nombre": row.sistema_nombre,
            "comando_nombre": row.comando_nombre,
            "comando_descripcion": row.comando_descripcion,
            "codigo_comando": row.codigo_comando
        } for row in result]

        return jsonify({"status": "success", "comandos": comandos}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error al obtener comandos: {str(e)}"}), 500

@commands_bp.route('/insert', methods=['POST'])
def insertar_comando():
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Verificar campos requeridos
        if not all(field in data for field in ["id_sistema", "id_tipo_comando", "descripcion"]):
            return jsonify({
                "status": "error", 
                "message": "Faltan campos requeridos"
            }), 400

        # Insertar comando ejecutado en la tabla comandos_ejecutados
        insert_comando_query = """
            INSERT INTO comandos_ejecutados (id_sistema, id_usuario, id_tipo_comando, parametros, descripcion)
            VALUES (:id_sistema, :id_usuario, :id_tipo_comando, :parametros, :descripcion)
        """
        db.session.execute(text(insert_comando_query), {
            "id_sistema": data["id_sistema"],
            "id_usuario": data.get("id_usuario", 1),  # Usuario predeterminado si no se especifica
            "id_tipo_comando": data["id_tipo_comando"],
            "parametros": data.get("parametros", "{}"),  # Parámetros predeterminados si no se especifican
            "descripcion": data["descripcion"]
        })
        db.session.commit()

        return jsonify({"status": "success", "message": "Comando ejecutado correctamente"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": f"Error al ejecutar el comando: {str(e)}"}), 500

