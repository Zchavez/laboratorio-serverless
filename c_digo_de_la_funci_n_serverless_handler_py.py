import json
import uuid
import hashlib
import platform
import socket
from datetime import datetime, timezone
from urllib.parse import parse_qs
from html import escape

def handle(event, context):
    """
    Función Serverless para OpenFaaS (python3-http)
    Maneja solicitudes GET (Formulario HTML) y POST (Procesamiento de datos y descarga JSON).
    """
    if event.method == "GET":
        formulario = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registro Serverless</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f6f9;
            padding: 50px 20px;
            display: flex;
            justify-content: center;
        }
        .contenedor {
            max-width: 450px;
            width: 100%;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        h2 {
            margin-top: 0;
            color: #111;
        }
        p {
            color: #666;
            font-size: 14px;
        }
        label {
            display: block;
            margin-top: 15px;
            font-weight: bold;
            color: #333;
        }
        input {
            width: 100%;
            padding: 10px;
            margin-top: 5px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 12px;
            margin-top: 20px;
            background-color: #1d72b8;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover {
            background-color: #155a92;
        }
    </style>
</head>
<body>
    <div class="contenedor">
        <h2>Registro de Ejecución Serverless</h2>
        <p>Introducción al Cómputo en la Nube</p>
        <form method="POST">
            <label for="nombre">Nombre</label>
            <input type="text" id="nombre" name="nombre" required>
            
            <label for="apellido">Apellido</label>
            <input type="text" id="apellido" name="apellido" required>
            
            <label for="email">Correo del aula virtual</label>
            <input type="email" id="email" name="email" required>
            
            <button type="submit">Generar archivo JSON</button>
        </form>
    </div>
</body>
</html>"""
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html; charset=utf-8"},
            "body": formulario
        }

    elif event.method == "POST":
        # Parsear los datos del formulario enviado
        body_str = event.body.decode('utf-8') if isinstance(event.body, bytes) else str(event.body)
        datos_form = parse_qs(body_str)
        
        nombre = datos_form.get("nombre", [""])[0]
        apellido = datos_form.get("apellido", [""])[0]
        email = datos_form.get("email", [""])[0]
        
        token_id = str(uuid.uuid4())
        fecha_utc = datetime.now(timezone.utc).isoformat()
        
        so_nombre = platform.system()
        so_version = platform.version()
        arquitectura = platform.machine()
        procesador = platform.processor()
        python_ver = platform.python_version()
        hostname = socket.gethostname()
        
        # Calcular Hash SHA-256 para verificar integridad
        cadena_firma = f"{nombre}{apellido}{email}{token_id}{fecha_utc}{hostname}"
        firma_sha256 = hashlib.sha256(cadena_firma.encode('utf-8')).hexdigest()
        
        resultado = {
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "token": token_id,
            "fecha_utc": fecha_utc,
            "sistema_operativo": so_nombre,
            "version_so": so_version,
            "arquitectura": arquitectura,
            "procesador": procesador,
            "version_python": python_ver,
            "hostname_contenedor": hostname,
            "plataforma": "OpenFaaS",
            "funcion": "registro-serverless",
            "estado": "Ejecucion exitosa",
            "firma_sha256": firma_sha256
        }
        
        json_output = json.dumps(resultado, indent=4, ensure_ascii=False)
        nombre_archivo = f"registro_{token_id}.json"
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json; charset=utf-8",
                "Content-Disposition": f'attachment; filename="{nombre_archivo}"'
            },
            "body": json_output
        }

    return {
        "statusCode": 405,
        "body": "Método no permitido"
    }