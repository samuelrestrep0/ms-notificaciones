from flask import Flask, request
import os
import boto3
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "API de Notificaciones Automáticas por Correo Electrónico"


# Endpoint para notificaciones de confirmación de solicitud de servicio
@app.route("/email-confirmacion", methods=["POST"])
def email_confirmacion():
    data = request.get_json()
    destination = data["destination"]
    subject = data.get("subject", "Confirmación de Solicitud de Servicio")
    message = data.get("message", "Su solicitud de servicio ha sido confirmada.")

    # Crear un cliente SES
    client = boto3.client(
        "ses",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION"),
    )
    # Enviar el correo electrónico usando una plantilla predefinida en SES
    response = client.send_templated_email(
        Destination={
            "ToAddresses": [
                destination,
            ],
        },
        Template="AWS-SES-Template-Confirmacion",  # Plantilla configurada en SES para confirmaciones
        TemplateData='{"subject": "' + subject + '", "message": "' + message + '"}',
        Source="tu_correo@ejemplo.com",  # Debe ser un email verificado en SES
    )
    return response


# Endpoint para notificaciones de actualizaciones de servicio
@app.route("/email-actualizacion", methods=["POST"])
def email_actualizacion():
    data = request.get_json()
    destination = data["destination"]
    subject = data.get("subject", "Actualización de Servicio")
    message = data.get("message", "Se han actualizado los detalles de su servicio.")

    # Crear un cliente SES
    client = boto3.client(
        "ses",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION"),
    )
    # Enviar el correo electrónico usando otra plantilla predefinida en SES
    response = client.send_templated_email(
        Destination={
            "ToAddresses": [
                destination,
            ],
        },
        Template="AWS-SES-Template-Actualizacion",  # Plantilla configurada en SES para actualizaciones
        TemplateData='{"subject": "' + subject + '", "message": "' + message + '"}',
        Source="tu_correo@ejemplo.com",  # Debe ser un email verificado en SES
    )
    return response


if __name__ == "__main__":
    app.run(debug=True, port=5000)
