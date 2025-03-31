Pasos para conectar el microservicio a AWS:

1. crear un usuario IAM en AWS
2. crear una clave de acceso a ese usuario y agregarla al archivo `.env` junto la region de esta manera
   * `"AWS_ACCESS_KEY_ID="..."`
   * `AWS_SECRET_ACCESS_KEY="..."`
   * `AWS_REGION=us-east-1`
3. crear una identidad tipo correo en el servicio de SES, esta identidad se debe agregar al archivo .env como
   * `"AWS_CREATED_IDENTITY=<ejemplo@email.com>"`
4. configurar AWS CLI en la comsola con aws configure y las credenciales de la clave de acceso
5. ejecutar el siguiente comando para crear la plantilla de `template.json`en AWS SES:
   * `aws ses create-template --region us-east-1 --cli-input-json file://template.json`