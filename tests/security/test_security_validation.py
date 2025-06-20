# tests/security/test_security_validation.py
import pytest
import json
from app import create_app
from app.models import db, Categoria, Producto # Importa los modelos correctos
from config import TestConfig # Importa la configuración de pruebas

@pytest.fixture(scope="module")
def app():
    """
    Fixture para crear y configurar la aplicación Flask para pruebas.
    Usa una base de datos en memoria que se crea y se elimina una vez por sesión de pruebas.
    """
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """
    Fixture para crear un cliente de prueba HTTP para hacer peticiones a la aplicación.
    """
    return app.test_client()

@pytest.fixture(autouse=True) # Se ejecuta antes y después de cada test automáticamente
def clean_db(app):
    """
    Fixture para limpiar la base de datos antes de cada test.
    Esto asegura que cada test se ejecute con un estado de base de datos limpio.
    """
    with app.app_context():
        db.session.query(Producto).delete()
        db.session.query(Categoria).delete()
        db.session.commit()
        yield
        db.session.rollback()

@pytest.fixture
def sample_categoria(app):
    """
    Fixture para crear una categoría de prueba.
    """
    with app.app_context():
        categoria = Categoria(nombre='Sample Cat', descripcion='Sample Description')
        db.session.add(categoria)
        db.session.commit()
        db.session.refresh(categoria)
        return categoria

# ===============================================
# PRUEBAS DE VALIDACIÓN DE ENTRADA DE DATOS
# ===============================================

class TestCategoriaValidations:
    """Pruebas de validación para los endpoints de Categorías."""

    def test_crear_categoria_campos_requeridos(self, client):
        """
        Test: La creación de categoría debe fallar si faltan campos requeridos (nombre, descripción) o están vacíos.
        """
        # Caso 1: Sin nombre
        data_no_name = {"descripcion": "Descripción sin nombre"}
        response = client.post('/categorias', data=json.dumps(data_no_name), content_type='application/json')
        assert response.status_code == 400
        assert 'Nombre y descripcion son requeridos' in response.get_json()['error']

        # Caso 2: Nombre vacío
        data_empty_name = {"nombre": "", "descripcion": "Descripción con nombre vacío"}
        response = client.post('/categorias', data=json.dumps(data_empty_name), content_type='application/json')
        assert response.status_code == 400
        assert 'Nombre y descripcion son requeridos' in response.get_json()['error']

        # Caso 3: Sin descripción
        data_no_desc = {"nombre": "Nombre sin descripción"}
        response = client.post('/categorias', data=json.dumps(data_no_desc), content_type='application/json')
        assert response.status_code == 400
        assert 'Nombre y descripcion son requeridos' in response.get_json()['error']

        # Caso 4: Descripción vacía
        data_empty_desc = {"nombre": "Nombre con descripción vacía", "descripcion": ""}
        response = client.post('/categorias', data=json.dumps(data_empty_desc), content_type='application/json')
        assert response.status_code == 400
        assert 'Nombre y descripcion son requeridos' in response.get_json()['error']

        # Caso 5: JSON vacío
        response_empty_json = client.post('/categorias', data=json.dumps({}), content_type='application/json')
        assert response_empty_json.status_code == 400
        assert 'Nombre y descripcion son requeridos' in response_empty_json.get_json()['error']

    def test_actualizar_categoria_json_vacio_o_invalido(self, client, sample_categoria):
        """
        Test: La actualización de categoría debe manejar JSON vacío o sin campos válidos.
        """
        # Caso 1: JSON vacío
        response = client.put(f'/categorias/{sample_categoria.id}', data=json.dumps({}), content_type='application/json')
        assert response.status_code == 200 # Flask debería aceptarlo y no hacer cambios

        # Caso 2: JSON con campos no válidos
        data_invalid_field = {"campo_extra": "valor", "otro_campo": 123}
        response = client.put(f'/categorias/{sample_categoria.id}', data=json.dumps(data_invalid_field), content_type='application/json')
        assert response.status_code == 200 # Flask ignora campos no reconocidos

        # Verificar que la categoría no cambió el nombre
        response_get = client.get(f'/categorias/{sample_categoria.id}')
        assert response_get.status_code == 200
        assert response_get.get_json()['nombre'] == sample_categoria.nombre


