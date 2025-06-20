
import pytest
import uuid
from app import create_app
from app.models import db, Categoria, Producto # Importa los modelos correctos
from config import TestConfig # Importa la configuración de pruebas

@pytest.fixture(scope='session') # Se ejecuta una vez por toda la sesión de pruebas
def app():
   
    app = create_app(TestConfig) # Crea la aplicación Flask con la configuración de pruebas
    
    with app.app_context():
        db.create_all() 
        yield app 
        db.drop_all() 

@pytest.fixture # Sin scope, se ejecuta para cada test individual
def client(app): # Recibe la app creada por el fixture app
    """
    Fixture para crear un cliente de prueba HTTP para hacer peticiones a la aplicación.
    """
    return app.test_client() # Crea un cliente HTTP falso para hacer peticiones a la aplicación durante las pruebas

@pytest.fixture(autouse=True) # Se ejecuta antes y después de cada test automáticamente
def clean_db(app):
    """
    Fixture para limpiar la base de datos antes de cada test.
    Esto asegura que cada test se ejecute con un estado de base de datos limpio.
    """
    with app.app_context():
        # Elimina los datos de las tablas en un orden que respete las dependencias (foreign keys)
        db.session.query(Producto).delete()
        db.session.query(Categoria).delete()
        db.session.commit()
        yield # Pausa, deja que el test se ejecute con BD limpia
        db.session.rollback()  # Deshace cambios no confirmados (red de seguridad para errores en tests)

@pytest.fixture
def sample_categoria(app):
    """
    Fixture para crear una categoría de prueba en la base de datos.
    """
    with app.app_context():
        categoria = Categoria(nombre=f'Categoría Test {uuid.uuid4().hex[:4]}', descripcion='Descripción de test')
        db.session.add(categoria)
        db.session.commit()
        db.session.refresh(categoria) # Refresca el objeto para obtener el ID asignado por la BD
        return categoria

@pytest.fixture
def sample_producto(app, sample_categoria):
    """
    Fixture para crear un producto de prueba asociado a una categoría.
    Depende del fixture `sample_categoria` para asegurar que haya una categoría.
    """
    with app.app_context():
        producto = Producto(
            nombre=f'Producto Test {uuid.uuid4().hex[:4]}',
            categoria_id=sample_categoria.id,
            precio=10.99,
            stock=15
        )
        db.session.add(producto)
        db.session.commit()
        db.session.refresh(producto) # Refresca el objeto para obtener el ID asignado por la BD
        return producto
