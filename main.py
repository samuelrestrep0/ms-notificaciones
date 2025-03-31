from flask import Flask, request, \
    jsonify  # Importamos Flask para la API, request para manejar peticiones y jsonify para respuestas JSON
import os  # Manejo de variables de entorno
import boto3  # Cliente para interactuar con AWS SES
from dotenv import load_dotenv  # Cargar variables de entorno desde un archivo .env

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Inicializamos la aplicación Flask
app = Flask(__name__)


# Ruta raíz para verificar que la API está en funcionamiento
@app.route("/", methods=["GET"])
def home():
    return "API de Notificaciones Automáticas por Correo Electrónico"


# Función para enviar correos electrónicos con SES
def send_email(template, destination, subject, message):
    try:
        # Creación del cliente SES con credenciales de AWS
        client = boto3.client(
            "ses",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION")
        )

        # Enviar el correo utilizando una plantilla de SES
        response = client.send_templated_email(
            Destination={"ToAddresses": [destination]},  # Dirección de correo del destinatario
            Template=template,  # Nombre de la plantilla configurada en SES
            TemplateData=f'{{"subject": "{subject}", "message": "{message}"}}',
            # Datos que se inyectarán en la plantilla
            Source=os.environ.get("AWS_CREATED_IDENTITY"),  # Remitente (debe estar verificado en SES)
        )
        return jsonify({"success": True, "message_id": response["MessageId"]}), 200  # Respuesta exitosa

    # Manejo de errores específicos de SES
    except client.exceptions.MessageRejected as e:
        return jsonify({"success": False, "error": "Mensaje rechazado", "details": str(e)}), 400
    except client.exceptions.MailFromDomainNotVerifiedException as e:
        return jsonify({"success": False, "error": "Dominio no verificado en SES", "details": str(e)}), 400
    except client.exceptions.ConfigurationSetDoesNotExistException as e:
        return jsonify({"success": False, "error": "Configuración de SES no encontrada", "details": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": "Error interno", "details": str(e)}), 500


# Endpoint para enviar un correo de confirmación de servicio
@app.route("/email-confirmacion", methods=["POST"])
def email_confirmacion():
    data = request.get_json()  # Obtener datos de la solicitud
    destination = data.get("destination")  # Dirección de correo del destinatario
    subject = data.get("subject", "Confirmación de Solicitud de Servicio")  # Asunto por defecto
    message = data.get("message", "Su solicitud de servicio ha sido confirmada.")  # Mensaje por defecto

    # Validación: el campo "destination" es obligatorio
    if not destination:
        return jsonify({"success": False, "error": "El campo 'destination' es obligatorio"}), 400

    # Llamada a la función send_email para enviar el correo
    return send_email("AWS-SES-Template-Confirmacion", destination, subject, message)


# Endpoint para enviar un correo de actualización de servicio
@app.route("/email-actualizacion", methods=["POST"])
def email_actualizacion():
    data = request.get_json()  # Obtener datos de la solicitud
    destination = data.get("destination")  # Dirección de correo del destinatario
    subject = data.get("subject", "Actualización de Servicio")  # Asunto por defecto
    message = data.get("message", "Se han actualizado los detalles de su servicio.")  # Mensaje por defecto

    # Validación: el campo "destination" es obligatorio
    if not destination:
        return jsonify({"success": False, "error": "El campo 'destination' es obligatorio"}), 400

    # Llamada a la función send_email para enviar el correo
    return send_email("AWS-SES-Template-Actualizacion", destination, subject, message)


# Ejecutar la aplicación Flask en modo debug en el puerto 5000
if __name__ == "__main__":
    app.run(debug=True, port=5000)
