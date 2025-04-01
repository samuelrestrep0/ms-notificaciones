# Microservicio de Notificaciones por Correo Electrónico

Este proyecto es un microservicio desarrollado en Python con Flask para enviar notificaciones automáticas vía correo electrónico, utilizando el servicio AWS SES (Simple Email Service). La configuración se gestiona a través de un archivo `.env` y se apoya en archivos complementarios como `.gitignore`, `template.json` y `requirements.txt`.

## Archivos del Proyecto

- **main.py**: Código principal de la API, que contiene la lógica para enviar correos utilizando plantillas de SES.
- **.gitignore**: Lista de archivos y carpetas que se excluyen del control de versiones.
- **template.json**: Archivo que define la plantilla para los correos en AWS SES.
- **requirements.txt**: Dependencias necesarias para el funcionamiento del proyecto.

## Configuración en AWS

Sigue estos pasos para conectar el microservicio a AWS:

1. **Crear un usuario IAM en AWS**  
   Accede a la consola de AWS y crea un usuario con permisos para utilizar SES.

2. **Generar claves de acceso**  
   Crea una clave de acceso para el usuario y agrega los siguientes datos al archivo `.env`:
   ```env
   AWS_ACCESS_KEY_ID="..."
   AWS_SECRET_ACCESS_KEY="..."
   AWS_REGION=us-east-1
    ```
   
3. **Verificar una identidad de correo**

   En el servicio de SES, crea y verifica una identidad (dirección de correo). Añade la dirección verificada al archivo `.env`:

```env
AWS_CREATED_IDENTITY=ejemplo@email.com
```

4. **Configurar AWS CLI**

   Abre la consola y ejecuta:


```env
aws configure
Ingresa las credenciales correspondientes.
```
5. **Crear la plantilla de correo en AWS SES**

   Ejecuta el siguiente comando para crear la plantilla definida en template.json:
```env
aws ses create-template --region us-east-1 --cli-input-json file://template.json
```

## Funcionamiento del Microservicio
#### El microservicio expone varios endpoints:
### `GET /`
Verifica el funcionamiento de la API y devuelve un mensaje de confirmación.

### `POST /email-confirmacion`
Envía un correo de confirmación. El cuerpo de la solicitud debe ser un JSON con:

- `destination`: Dirección de correo del destinatario (obligatorio)
- `subject`: Asunto del correo (opcional, por defecto `"Confirmación de Solicitud de Servicio"`)
- `message`: Mensaje del correo (opcional, por defecto `"Su solicitud de servicio ha sido confirmada."`)

### `POST /email-actualizacion`
Envía un correo de actualización. Requiere un JSON similar al endpoint anterior, con:

- `destination`: Dirección de correo del destinatario (obligatorio)
- `subject`: Asunto del correo (opcional, por defecto `"Actualización de Servicio"`)
- `message`: Mensaje del correo (opcional, por defecto `"Se han actualizado los detalles de su servicio."`)


## Instalación y Ejecución
### Instalación de Dependencias
Instala las dependencias necesarias ejecutando:

```sh
pip install -r requirements.txt
```

### Ejecución de la Aplicación
Inicia la API con:
```sh
python main.py
```
La API se ejecutará en el puerto `5000` en modo `debug`.

## Notas de Seguridad y Buenas Prácticas


### Archivo `.env`:
- No subas este archivo al repositorio, ya que contiene información sensible (credenciales de AWS).
- Asegúrate de incluirlo en el `.gitignore`.

### Plantillas en AWS SES:
- Verifica que la plantilla definida en `template.json` se haya creado correctamente en AWS SES para evitar errores al enviar correos.

### Variables de Entorno:
- Utiliza métodos seguros para gestionar credenciales, como AWS Secrets Manager o variables de entorno en el servidor, en lugar de incluirlas directamente en el código.



