import json
import pytest
from app.models import db, Categoria, Producto 



def test_endpoint_health_check(client):
    response = client.get('/health')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'OK'
    assert data['message'] == 'API funcionando correctamente'

def test_endpoint_productos_stock_bajo(client, sample_categoria):
    with client.application.app_context():
       
        
        producto_bajo_1 = Producto(nombre='Auriculares', categoria_id=sample_categoria.id, precio=50.0, stock=5)
        producto_normal_1 = Producto(nombre='Monitor', categoria_id=sample_categoria.id, precio=300.0, stock=12)
        producto_bajo_2 = Producto(nombre='Teclado', categoria_id=sample_categoria.id, precio=75.0, stock=8)
        db.session.add_all([producto_bajo_1, producto_normal_1, producto_bajo_2])
        db.session.commit()

    response = client.get('/productos/stock')
    
    assert response.status_code == 200
    productos_en_stock_bajo = json.loads(response.data)
    
    assert len(productos_en_stock_bajo) == 2
    nombres_productos_bajo_stock = {p['nombre'] for p in productos_en_stock_bajo}
    assert 'Auriculares' in nombres_productos_bajo_stock
    assert 'Teclado' in nombres_productos_bajo_stock
    assert 'Monitor' not in nombres_productos_bajo_stock # Este no debería estar



def test_integracion_crear_producto_con_categoria_y_verificar_relacion(client):
    
    with client.application.app_context():
        new_categoria = Categoria(nombre='Electrodomésticos', descripcion='Grandes y pequeños electrodomésticos')
        db.session.add(new_categoria)
        db.session.commit()
        db.session.refresh(new_categoria) # Obtener el ID de la categoría recién creada
        categoria_id = new_categoria.id
        categoria_nombre = new_categoria.nombre

    producto_data = {
        "nombre": "Refrigerador Inteligente",
        "categoria_id": categoria_id,
        "precio": 1200.00,
        "stock": 3
    }
    response_post_producto = client.post('/productos',
                                         data=json.dumps(producto_data),
                                         content_type='application/json')
    
    assert response_post_producto.status_code == 201
    producto_creado = json.loads(response_post_producto.data)
    assert producto_creado['nombre'] == "Refrigerador Inteligente"
    assert producto_creado['categoria_id'] == categoria_id
    assert 'id' in producto_creado
    
    assert producto_creado['categoria']['nombre'] == categoria_nombre
    assert producto_creado['categoria']['id'] == categoria_id

    with client.application.app_context():
        producto_recuperado = Producto.query.get(producto_creado['id'])
        
        assert producto_recuperado is not None
        assert producto_recuperado.nombre == "Refrigerador Inteligente"
        assert producto_recuperado.categoria_id == categoria_id
        
        assert producto_recuperado.categoria is not None
        assert producto_recuperado.categoria.nombre == categoria_nombre
        assert producto_recuperado.categoria.id == categoria_id
