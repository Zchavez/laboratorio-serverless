# Laboratorio: Servicio Serverless (FaaS) con OpenFaaS, Docker y Kubernetes

**Asignatura:** Introducción al Cómputo en la Nube  
**Tema:** Computación Serverless y modelo Functions as a Service (FaaS)  

---

## 📌 Descripción del Proyecto

Este laboratorio consiste en la implementación de una arquitectura **Serverless** local utilizando **OpenFaaS** sobre **Kubernetes** y **Docker Desktop**. 

La aplicación despliega un servicio en **Python** (`registro-serverless`) que realiza dos tareas principales:
1. **GET Request:** Retorna un formulario web responsivo donde el usuario ingresa su Nombre, Apellido y Correo Electrónico institucional.
2. **POST Request:** Procesa la información enviada, recolecta métricas del entorno de ejecución de la función (contenedor Linux, arquitectura, versión de Python), asigna un identificador único global (`UUIDv4`), firma digitalmente el registro con un hash `SHA-256` y retorna un archivo `.json` descargable de forma directa.

---

## 🛠️ Requisitos Previos y Herramientas

* **Sistema Operativo:** Windows 10/11 (64-bit) con **WSL 2** activado.
* **Docker Desktop:** Con el motor de Kubernetes habilitado.
* **CLI Tools:** `kubectl`, `helm`, `faas-cli`.
* **Editor:** Visual Studio Code.

---

## 🚀 Guía Paso a Paso para la Ejecución

### Parte 1: Verificación del Entorno e Infraestructura
1. Verificar que WSL 2 y Docker Desktop estén en ejecución con el clúster de Kubernetes habilitado.
2. Comprobar la conexión del nodo en PowerShell:
   ```powershell
   kubectl get nodes
   ```
3. Iniciar el reenvío de puertos para el Gateway de OpenFaaS:
   ```powershell
   kubectl port-forward -n openfaas svc/gateway 8080:8080
   ```

### Parte 2: Construcción y Despliegue de la Función
1. Configurar OpenFaaS para utilizar imágenes locales sin intentar descargarlas del registro remoto:
   ```powershell
   helm upgrade openfaas openfaas/openfaas --namespace openfaas --reuse-values --set functions.imagePullPolicy=Never
   ```
2. Descargar la plantilla de Python HTTP y crear la función:
   ```powershell
   faas-cli template store pull python3-http
   faas-cli new --lang python3-http registro-serverless
   ```
3. Copiar el código del manejador (`handler.py`) y configurar el archivo `stack.yaml`.
4. Preparar la carpeta de build y construir la imagen Docker:
   ```powershell
   New-Item -ItemType Directory -Force -Path "build\registro-serverless\function" | Out-Null
   Copy-Item "template\python3-http\Dockerfile" "build\registro-serverless\"
   Copy-Item "template\python3-http\index.py" "build\registro-serverless\"
   Copy-Item "template\python3-http\requirements.txt" "build\registro-serverless\"
   Copy-Item "registro-serverless\*" "build\registro-serverless\function\" -Recurse -Force

   docker build -t registro-serverless:v1 ./build/registro-serverless
   ```
5. Ejecutar la función para habilitar el servicio web:
   ```powershell
   docker run --rm -p 8080:8080 registro-serverless:v1
   ```

### Parte 3: Generación de la Evidencia JSON
1. Abrir el navegador e ingresar a `http://localhost:8080`.
2. Completar los campos requeridos con tus datos de estudiante.
3. Hacer clic en **Generar archivo JSON**.
4. Mover el archivo descargado (`registro_<UUID>.json`) a la raíz del repositorio local antes de realizar el `git commit`.

---

## 📂 Estructura del Repositorio

```text
laboratorio-serverless/
├── .gitignore
├── README.md
├── stack.yaml
├── registro_f449bcaf-fdf4-4d97-9390-db4c40db6cef.json (Evidencia generada)
└── registro-serverless/
    ├── handler.py
    └── requirements.txt
```

---

## 📄 Licencia y Entregables
Proyecto desarrollado para fines académicos correspondientes a la unidad de Competencias Fundamentales en la Nube.