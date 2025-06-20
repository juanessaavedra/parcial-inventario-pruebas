
from locust import HttpUser, task, between
import json
import random
import time # Importar time para nombres únicos

class InventarioUser(HttpUser):
    """
    Simula un usuario que interactúa con la API de gestión de inventario.
    """
    wait_time = between(1, 3)
    
    host = "http://127.0.0.1:5000"

    def on_start(self):
        
        self.categoria_id = None
        self.producto_id = None
        
        # Intentar crear una categoría y un producto al inicio para que las operaciones de PUT/GET tengan datos
        self.crear_categoria_inicial()
        self.crear_producto_inicial()

    def crear_categoria_inicial(self):
        """Crea una categoría si no existe para usar en la creación de productos."""
        if not self.categoria_id:
            nombre = f"Cat Inicial {int(time.time() * 1000)}"
            descripcion = "Categoría para pruebas de carga iniciales"
            response = self.client.post("/categorias", 
                                      json={"nombre": nombre, "descripcion": descripcion},
                                      name="Setup: Crear Categoria Inicial")
            if response.status_code == 201:
                self.categoria_id = response.json()['id']
                print(f"DEBUG: Categoria inicial creada con ID: {self.categoria_id}")
            else:
                print(f"ERROR: No se pudo crear la categoria inicial: {response.status_code} - {response.text}")

    def crear_producto_inicial(self):
        """Crea un producto si no existe para usar en actualizaciones de stock."""
        if not self.producto_id and self.categoria_id:
            nombre = f"Producto Inicial {int(time.time() * 1000)}"
            response = self.client.post("/productos", 
                                      json={
                                          "nombre": nombre,
                                          "categoria_id": self.categoria_id,
                                          "precio": 99.99,
                                          "stock": 50
                                      },
                                      name="Setup: Crear Producto Inicial")
            if response.status_code == 201:
                self.producto_id = response.json()['id']
                print(f"DEBUG: Producto inicial creado con ID: {self.producto_id}")
            else:
                print(f"ERROR: No se pudo crear el producto inicial: {response.status_code} - {response.text}")
        elif not self.categoria_id:
            print("INFO: No se pudo crear producto inicial porque no hay categoria inicial.")

    @task(3)  
    def verificar_salud(self):
        """Prueba el endpoint de salud de la API."""
        self.client.get("/health", name="GET /health")

    @task(2)  
    def listar_categorias(self):
        """Obtiene la lista de todas las categorías."""
        self.client.get("/categorias", name="GET /categorias")

    @task(2)
    def listar_productos(self):
        """Obtiene la lista de todos los productos."""
        self.client.get("/productos", name="GET /productos")

    @task(1) 
    def obtener_productos_stock_bajo(self):
        """Obtiene la lista de productos con stock bajo."""
        self.client.get("/productos/stock", name="GET /productos/stock")

    @task(1)
    def crear_nueva_categoria(self):
        """Crea una nueva categoría aleatoria."""
        nombre = f"Nueva Cat {random.randint(10000, 99999)}"
        descripcion = f"Descripción de la categoría {nombre}"
        self.client.post("/categorias", 
                        json={"nombre": nombre, "descripcion": descripcion},
                        name="POST /categorias")

    @task(1)
    def crear_nuevo_producto(self):
        """
        Crea un nuevo producto aleatorio.
        Requiere que haya al menos una categoría existente.
        """
        if self.categoria_id: # Solo intentar crear producto si hay una categoría disponible
            nombre = f"Nuevo Prod {random.randint(100000, 999999)}"
            response = self.client.post("/productos", 
                                        json={
                                            "nombre": nombre,
                                            "categoria_id": self.categoria_id,
                                            "precio": round(random.uniform(5.0, 500.0), 2),
                                            "stock": random.randint(1, 100)
                                        },
                                        name="POST /productos")
            if response.status_code != 201:
                print(f"WARN: Error al crear nuevo producto: {response.status_code} - {response.text}")
        else:
            print("INFO: No se puede crear producto, no hay categoria disponible.")

    @task(1)
    def actualizar_stock_producto(self):
        """
        Actualiza el stock de un producto existente (el producto inicial).
        """
        if self.producto_id:
            nuevo_stock = random.randint(1, 100)
            self.client.put(f"/productos/{self.producto_id}",
                            json={"stock": nuevo_stock},
                            name="PUT /productos/{id} (Actualizar Stock)")
        else:
            print("INFO: No se puede actualizar stock, no hay producto inicial disponible.")

    @task(0) 
    def obtener_producto_por_categoria(self):
        """
        Obtiene productos de una categoría específica.
        Esta tarea es útil si quieres probar el filtro por categoría, pero
        para pruebas básicas, las tareas de listar son suficientes.
        """
        if self.categoria_id:
            self.client.get(f"/productos/categoria/{self.categoria_id}",
                            name="GET /productos/categoria/{id}")
        else:
            print("INFO: No se puede obtener productos por categoria, no hay categoria inicial.")

