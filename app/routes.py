from flask import Blueprint, request, jsonify # Jsonify convierte respuestas a JSON
# Tambien importo request para manejar peticiones HTTP
from app.models import db, Categoria, Producto
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__) #Crea un blueprint llamado 'main' para agrupar las rutas de la aplicación

# @main_bp viene del import de routes.py, que es donde se define el blueprint

# ============= ENDPOINT DE SALUD =============

@main_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK', 'message': 'API funcionando correctamente'})

# ============= CRUD CATEGORIAS =============

@main_bp.route('/categorias', methods=['GET'])
def obtener_categorias():
    categorias = Categoria.query.all() #Lista de categorias
    return jsonify([categoria.to_dict() for categoria in categorias])#Lista comprehension para convertir cada categoria a un diccionario

@main_bp.route('/categorias', methods=['POST'])
def crear_categoria():
    data = request.get_json()
    
    if not data.get('nombre') or not data.get('descripcion'): #If not es para hacer algo si el campo no existe o es None
        return jsonify({'error': 'Nombre y descripcion son requeridos'}), 400

    categoria = Categoria(nombre=data['nombre'], descripcion=data['descripcion']) # Puede recibir cualquier campo que hayas definido en el modelo, excepto los que tienen valores automáticos.
    db.session.add(categoria) #Carrito de compras que guarda los cambios en la base de datos
    db.session.commit() # Guarda los cambios en la base de datos
    return jsonify(categoria.to_dict()), 201

@main_bp.route('/categorias/<int:id>', methods=['DELETE'])
def eliminar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    return jsonify({'message': 'Categoria eliminada'})

@main_bp.route('/categorias/<int:id>', methods=['PUT'])
def actualizar_categoria(id):
    data = request.get_json()
    categoria = Categoria.query.get_or_404(id)
    
    if 'nombre' in data:
        categoria.nombre = data['nombre']
    if 'descripcion' in data:
        categoria.descripcion = data['descripcion']
    
    db.session.commit()
    return jsonify(categoria.to_dict()), 200

# ============= CRUD DE PRODUCTOS =============

@main_bp.route('/productos', methods=['GET'])
def obtener_productos():  # ✅ CORREGIDO: nombre de función correcto
    productos = Producto.query.all()
    return jsonify([producto.to_dict() for producto in productos])

@main_bp.route('/productos', methods=['POST'])
def crear_producto():  # ✅ CORREGIDO: nombre de función correcto
    data = request.get_json()
    
    # ✅ AGREGADO: Validación del nombre del producto
    if not data.get('nombre'):
        return jsonify({'error': 'Nombre del producto es requerido'}), 400
    
    categoria_id = data.get('categoria_id')
    
    if not categoria_id:
        return jsonify({'error': 'Categoria_id es requerido'}), 400
    
    # Verificar que la categoria existe
    categoria = Categoria.query.get(categoria_id)

    if not categoria:
        return jsonify({'error': 'Categoria no encontrada'}), 404
    
    # Crear producto
    producto = Producto(
        nombre=data.get('nombre'),
        categoria_id=categoria_id,
        precio=data.get('precio', 0.0),
        stock=data.get('stock', 0)
    )
    db.session.add(producto)
    db.session.commit()
    
    return jsonify(producto.to_dict()), 201

@main_bp.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return jsonify({'message': 'Producto eliminado'})

@main_bp.route('/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    data = request.get_json()
    producto = Producto.query.get_or_404(id)
    
    if 'nombre' in data:
        producto.nombre = data['nombre']
    if 'categoria_id' in data:
        # ✅ AGREGADO: Validar que la nueva categoría existe
        categoria = Categoria.query.get(data['categoria_id'])
        if not categoria:
            return jsonify({'error': 'Categoria no encontrada'}), 404
        producto.categoria_id = data['categoria_id']
    if 'precio' in data:
        producto.precio = data['precio']
    if 'stock' in data:
        producto.stock = data['stock']
    
    db.session.commit()
    return jsonify(producto.to_dict()), 200

# ============= Endpoint para productos con stock bajo (< 10 unidades) =============
@main_bp.route('/productos/stock', methods=['GET'])
def obtener_productos_stock_bajo():
    productos = Producto.query.filter(Producto.stock < 10).all()
    return jsonify([producto.to_dict() for producto in productos])

# ✅ AGREGADO: Endpoint para obtener productos por categoría
@main_bp.route('/productos/categoria/<int:categoria_id>', methods=['GET'])
def obtener_productos_por_categoria(categoria_id):
    # Verificar que la categoria existe
    categoria = Categoria.query.get_or_404(categoria_id)
    
    productos = Producto.query.filter_by(categoria_id=categoria_id).all()
    return jsonify([producto.to_dict() for producto in productos])

# ✅ AGREGADO: Endpoint para obtener un producto específico
@main_bp.route('/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = Producto.query.get_or_404(id)
    return jsonify(producto.to_dict())

# ✅ AGREGADO: Endpoint para obtener una categoría específica
@main_bp.route('/categorias/<int:id>', methods=['GET'])
def obtener_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    return jsonify(categoria.to_dict())