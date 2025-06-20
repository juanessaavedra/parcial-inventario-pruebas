
FROM python:3.9-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requisitos al directorio de trabajo
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


COPY .env .

COPY . .

# Expone el puerto en el que se ejecutará la aplicación Flask
EXPOSE 5000


CMD ["sh", "-c", "export FLASK_APP=app && flask db upgrade && gunicorn -b 0.0.0.0:5000 app:create_app()"]
