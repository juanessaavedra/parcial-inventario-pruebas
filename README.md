# 📦 Sistema de Gestión de Inventario

Un sistema completo de gestión de inventario desarrollado con Flask y PostgreSQL, que incluye una API REST robusta, interfaz web intuitiva y un pipeline de CI/CD completo con múltiples tipos de testing.



## 🛠️ Tecnologías

### Backend
- **Flask 2.3.3** - Framework web
- **Flask-SQLAlchemy 3.0.5** - ORM
- **Flask-Migrate 4.0.5** - Migraciones de BD
- **Flask-CORS 4.0.2** - Manejo de CORS
- **PostgreSQL** - Base de datos principal
- **psycopg 3.2.9** - Driver de PostgreSQL

### Frontend
- **HTML5/CSS3/JavaScript** - Interfaz web
- **Responsive Design** - Compatible con móviles

### Testing
- **pytest 7.4.2** - Framework de testing
- **Selenium 4.15.2** - Tests de UI
- **Locust 2.17.0** - Tests de carga/estrés

### DevOps
- **Docker & Docker Compose** - Containerización
- **GitHub Actions** - CI/CD
- **Bandit 1.7.7** - Análisis de seguridad estática
- **Safety 2.3.4** - Análisis de vulnerabilidades

```

## ⚙️ Configuración e Instalación

### 📋 Prerrequisitos

- **Python 3.9+**
- **PostgreSQL 13+**
- **Git**
- **Docker** (opcional)

### 🔧 Instalación Local

#### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/parcial-inventario-pruebas.git
cd parcial-inventario-pruebas
```

#### 2. Crear entorno virtual
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En macOS/Linux:
source venv/bin/activate
# En Windows:
venv\Scripts\activate
```

#### 3. Instalar dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Configurar PostgreSQL
```bash
# Crear base de datos
createdb inventario

# Para testing (opcional)
createdb inventario_test
```

#### 5. Configurar variables de entorno
Crea un archivo `.env` en la raíz del proyecto:

```env
# Flask
SECRET_KEY=tu-clave-secreta-para-desarrollo
DEBUG=False

# Base de datos - Desarrollo
DATABASE_URL=postgresql+psycopg://tu_usuario:tu_password@localhost:5432/inventario

# Base de datos - Testing
TEST_DATABASE_URL=postgresql+psycopg://postgres:admin@localhost:5432/inventario_test
```


### 🚀 Iniciar el servidor

#### Opción 1: Usando run.py (Recomendado para desarrollo)
```bash
python run.py
```

### 🌐 Acceder a la aplicación

- **API REST**: http://127.0.0.1:5000
- **Interfaz Web**: Abrir `frontend/index.html` en el navegador
- **Health Check**: http://127.0.0.1:5000/health

### 💡 Funcionalidades de la Interfaz Web

1. **📂 Gestión de Categorías**
   - Crear nuevas categorías
   - Ver lista de todas las categorías
   - Eliminar categorías existentes

2. **📦 Gestión de Productos**
   - Agregar productos con categoría, precio y stock
   - Ver todos los productos con filtros por categoría
   - Editar información de productos
   - Actualizar stock (entrada, salida, ajuste)
   - Eliminar productos

3. **⚠️ Alertas de Stock**
   - Ver productos con stock bajo (< 10 unidades)
   - Alertas visuales en la interfaz

## 🌐 API Endpoints

### 🏥 Health Check
```http
GET /health
```
**Respuesta**: Estado de la API

### 📂 Categorías

#### Listar todas las categorías
```http
GET /categorias
```

#### Crear categoría
```http
POST /categorias
Content-Type: application/json

{
  "nombre": "Electrónica",
  "descripcion": "Dispositivos electrónicos y gadgets"
}
```

#### Obtener categoría específica
```http
GET /categorias/{id}
```

#### Actualizar categoría
```http
PUT /categorias/{id}
Content-Type: application/json

{
  "nombre": "Nuevo nombre",
  "descripcion": "Nueva descripción"
}
```

#### Eliminar categoría
```http
DELETE /categorias/{id}
```

### 📦 Productos

#### Listar todos los productos
```http
GET /productos
```

#### Crear producto
```http
POST /productos
Content-Type: application/json

{
  "nombre": "Laptop Gamer",
  "categoria_id": 1,
  "precio": 1500.00,
  "stock": 10
}
```

#### Obtener producto específico
```http
GET /productos/{id}
```

#### Actualizar producto
```http
PUT /productos/{id}
Content-Type: application/json

{
  "nombre": "Laptop Gaming Pro",
  "precio": 1600.00,
  "stock": 15
}
```

#### Eliminar producto
```http
DELETE /productos/{id}
```

#### Productos con stock bajo
```http
GET /productos/stock
```

#### Productos por categoría
```http
GET /productos/categoria/{categoria_id}
```


## 🧪 Testing

### 🏃‍♂️ Ejecutar todos los tests
```bash
pytest
```

### 📝 Tests específicos

#### Tests unitarios
```bash
pytest tests/test_unit/
```

#### Tests de integración
```bash
pytest tests/integration/
```

#### Tests de interfaz (UI)
```bash
# Requiere Chrome instalado
pytest tests/ui/
```

#### Tests de seguridad
```bash
pytest tests/security/
```

### 🔥 Tests de carga/estrés con Locust
```bash
# Iniciar servidor primero
python run.py

# En otra terminal, ejecutar tests de carga
cd tests/carga-estres
locust -f tests/carga-estres/locustfile.py --headless -u 50 -r 5 -t 1m --host=http://127.0.0.1:5000
```


### 🛡️ Análisis de seguridad
```bash
# Análisis estático con Bandit
bandit -r app/

# Análisis de vulnerabilidades con Safety
safety check
```

## 🐳 Docker

### 🏗️ Construcción y ejecución

#### Con Docker Compose (Recomendado)
```bash
# Construir e iniciar todos los servicios
docker-compose up --build
```


## 🔄 CI/CD Pipeline

El proyecto incluye un pipeline completo de CI/CD con GitHub Actions que se ejecuta en cada push y pull request a la rama `main`.

### 🎯 Etapas del Pipeline

1. **🔧 Setup**
   - Configuración de Python 3.9
   - Instalación de dependencias
   - Configuración de PostgreSQL para testing

2. **🗄️ Base de Datos**
   - Verificación de disponibilidad de PostgreSQL
   - Ejecución de migraciones

3. **🧪 Testing**
   - Tests unitarios
   - Tests de integración
   - Tests de UI con Selenium (Chrome headless)

4. **🛡️ Seguridad**
   - Análisis estático con Bandit
   - Análisis de vulnerabilidades con Safety

5. **✅ Verificación**
   - Confirmación de que todo pasó correctamente

### 📋 Requisitos para el Pipeline

- Base de datos PostgreSQL configurada como servicio
- Chrome y Xvfb para tests de UI
- Variables de entorno configuradas
- Migraciones de base de datos en el repositorio


## 📖 Documentación Adicional

### 🔄 Migraciones de Base de Datos

```bash
# Crear nueva migración después de cambios en modelos
flask db migrate -m "Descripción del cambio"

# Aplicar migraciones pendientes
flask db upgrade

# Revertir última migración
flask db downgrade

# Ver historial de migraciones
flask db history
```