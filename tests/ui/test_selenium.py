import pytest
import time
import subprocess
import sys
import os 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="module")
def flask_server():
    
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    
    server_script_content = f"""
import sys
import os
# Asegúrate de que el directorio raíz del proyecto esté en el sys.path
sys.path.insert(0, '{project_root}')

from app import create_app
from app.models import db
from config import TestConfig # Usar TestConfig para el entorno de pruebas

app = create_app(TestConfig)
with app.app_context():
    db.create_all()
    print("✅ Base de datos inicializada para UI testing en Flask server.")

print("🚀 Servidor de API iniciando en http://127.0.0.1:5000 (para UI tests)")
app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False) # use_reloader=False es importante para subprocess
"""
    # Guardar el script en un archivo temporal
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".py") as f:
        f.write(server_script_content)
        script_path = f.name
    
    
    process = subprocess.Popen([sys.executable, script_path])
    
    # Dar tiempo al servidor para iniciar
    time.sleep(5)
    
    yield "http://127.0.0.1:5000" # URL base de la API
    
    process.terminate()
    process.wait()
    os.remove(script_path)

@pytest.fixture
def driver():
    
    chrome_options = Options()
  
    
    try:
        # Cambiado de webdriver.Safari a webdriver.Chrome
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(1200, 800) # Ajusta el tamaño de la ventana para visualización
        yield driver
        driver.quit() # Cierra el navegador después de cada test
    except Exception as e:
        # Mensaje de error actualizado
        pytest.skip(f"Chrome WebDriver no disponible o error al iniciarlo: {e}")


def test_crear_categoria_desde_ui(driver, flask_server):
   
  
    frontend_html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend/index.html'))
    driver.get(f"file://{frontend_html_path}")
    
    wait = WebDriverWait(driver, 10) # Esperar hasta 10 segundos
    
    wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1")))
    assert "Gestión de Inventario" in driver.title or "Gestión de Inventario" in driver.page_source

    nombre_categoria = f"Nueva Categoría UI {time.time()}" # Nombre único para evitar colisiones
    descripcion_categoria = "Descripción para prueba UI"

    nombre_input = wait.until(EC.presence_of_element_located((By.ID, "nombreCategoria")))
    descripcion_input = driver.find_element(By.ID, "categoriaDescripcion")
    submit_button = driver.find_element(By.CSS_SELECTOR, "#formCategoria button[type='submit']")

    nombre_input.clear()
    nombre_input.send_keys(nombre_categoria)
    descripcion_input.clear()
    descripcion_input.send_keys(descripcion_categoria)

    submit_button.click()

    
    wait.until(EC.text_to_be_present_in_element((By.ID, "mensajeCategoria"), "Categoría creada exitosamente"))
    mensaje_categoria_div = driver.find_element(By.ID, "mensajeCategoria") # Re-obtener el elemento si es necesario, o simplemente ya lo tenemos de la línea anterior
    assert "Categoría creada exitosamente" in mensaje_categoria_div.text

    
    refresh_categorias_button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[onclick='cargarCategorias()']")
    ))
    refresh_categorias_button.click()
    
    categorias_lista_div = wait.until(EC.presence_of_element_located((By.ID, "categoriasLista")))
    # Esperar hasta que el texto de la nueva categoría esté visible en la lista
    wait.until(EC.text_to_be_present_in_element((By.ID, "categoriasLista"), nombre_categoria))
    assert nombre_categoria in categorias_lista_div.text
    assert descripcion_categoria in categorias_lista_div.text

    print(f"Categoría '{nombre_categoria}' creada y verificada exitosamente en la UI.")
