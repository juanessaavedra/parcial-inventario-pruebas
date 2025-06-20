# tests/test_inventario_crud.py
import json
import pytest
from app.models import Categoria, Producto, db # Importa los modelos y db para operaciones directas en los tests

#

class TestCRUDCategorias:
    """Tests unitarios del CRUD de categorías."""
    
    def test_crear_categoria(self, client):
        """Test 1: Crear una nueva categoría."""
        data = {
            "nombre": "Electrónica",
            "descripcion": "Dispositivos electrónicos y gadgets"
        }
        response = client.post('/categorias',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert response_data['nombre'] == "Electrónica"
        assert response_data['descripcion'] == "Dispositivos electrónicos y gadgets"
        assert 'id' in response_data

    


class TestCRUDProductos:
    """Tests unitarios del CRUD de productos."""

    def test_crear_producto(self, client, sample_categoria):
        """Test 6: Crear un nuevo producto."""
        data = {
            "nombre": "Laptop Gamer",
            "categoria_id": sample_categoria.id,
            "precio": 1500.00,
            "stock": 10
        }
        response = client.post('/productos',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert response_data['nombre'] == "Laptop Gamer"
        assert response_data['categoria_id'] == sample_categoria.id
        assert response_data['precio'] == 1500.00
        assert response_data['stock'] == 10
        assert 'id' in response_data

    def test_obtener_productos(self, client, sample_producto):
        """Test 7: Obtener la lista de productos."""
        response = client.get('/productos')
        
        assert response.status_code == 200
        productos = json.loads(response.data)
        assert len(productos) >= 1
        assert any(p['nombre'] == sample_producto.nombre for p in productos)

    

class TestBusinessLogicSpecific:
    """Tests para lógica de negocio adicional de inventario."""

    def test_obtener_productos_stock_bajo(self, client, sample_categoria):
        """
        Test 11: Prueba que el endpoint /productos/stock devuelve solo productos con stock < 10.
        """
        with client.application.app_context():
            producto1 = Producto(nombre='Laptop', categoria_id=sample_categoria.id, precio=1200.0, stock=5) # Stock bajo
            producto2 = Producto(nombre='Monitor', categoria_id=sample_categoria.id, precio=300.0, stock=15) # Stock normal
            producto3 = Producto(nombre='Teclado', categoria_id=sample_categoria.id, precio=75.0, stock=8) # Stock bajo
            db.session.add_all([producto1, producto2, producto3])
            db.session.commit()

        response = client.get('/productos/stock')
        assert response.status_code == 200
        data = response.get_json()
        
        assert len(data) == 2
        nombres_productos_stock_bajo = {p['nombre'] for p in data}
        assert 'Laptop' in nombres_productos_stock_bajo
        assert 'Teclado' in nombres_productos_stock_bajo
        assert 'Monitor' not in nombres_productos_stock_bajo


    

class TestDataValidations:
    """Tests para las validaciones de entrada de datos."""

    def test_crear_categoria_validacion_requeridos(self, client):
        """Test 13: Prueba validaciones para crear categoría sin campos requeridos."""
        # Sin nombre
        response_no_name = client.post('/categorias', json={'descripcion': 'Una descripción'})
        assert response_no_name.status_code == 400
        assert 'Nombre y descripcion son requeridos' in response_no_name.get_json()['error']

        # Sin descripción
        response_no_desc = client.post('/categorias', json={'nombre': 'Test Cat'})
        assert response_no_desc.status_code == 400
        assert 'Nombre y descripcion son requeridos' in response_no_desc.get_json()['error']
        
        # Sin ningún dato
        response_empty = client.post('/categorias', json={})
        assert response_empty.status_code == 400
        assert 'Nombre y descripcion son requeridos' in response_empty.get_json()['error']

    