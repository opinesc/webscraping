#  Para instalar automáticamente chromedriver
from webdriver_manager.chrome import ChromeDriverManager
# driver de selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# para modificar las opciones de webdriver en Chrome
from selenium.webdriver.chrome.options import Options
# para definir el tipo de busqueda del elemento
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # para esperar por elementos
from selenium.webdriver.support import expected_conditions as ec # para condiciones
from selenium.common.exceptions import TimeoutException # excepciones de timeout en selenium
# importamos la credenciales de Comunio
from env import *
import time
import sys
import os

def iniciar_chrome():
    """ inicia Chrome con los parámetros indicados y devuelve el driver """

    #Instalamos la versión correspondiente. Nos devuelve la ruta
    ruta = ChromeDriverManager(path='./chromedriver').install()

    # Opciones: https://peter.sh/experiments/chromium-command-line-switches
    options = Options()
    user_agent ="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    # options.add_argument("--headless") # Ejecuta Chrome sin abrir la ventana
    options.add_argument(f'user-agent={user_agent}') # define el user agent
    # options.add_argument("--window-size=1000,1000")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-web-security") #deshabilita la politica del mismo origen
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--ignore-certificate-errors") # Para ignorar su conexión no es segura
    options.add_argument("--no-sandbox") #deshabilita el modo sandbox
    options.add_argument("--log-level=3")
    options.add_argument("allow-running-insecure-context") # desactiva aviso "contenido no seguro"
    options.add_argument("--no-default-browser-check")
    options.add_argument("--no-first-run") # Evita la ejecución de ciertas tareas
    options.add_argument("--no-proxy-server")
    options.add_argument("--disable-blink-feactures=AutomaticControlled")
    #Parametros a omitir en en inicio

    exp_opt=[
        "ignore-certificate-errors",
        "enable-automation",
        "enable-logging"
    ]
    options.add_experimental_option('excludeSwitches', exp_opt)

    # Parametros de preferencias de chromedriver

    prefs = {
        'profile.default_content_setting_values.notifications':2, # notificaciones 0=preguntar, 1=permitir | 2=no permitir
        'intl.accept_languages': ['es-ES','es'],
        'credentials_enable_service': False # evitar chrome pregunte si guardar contraseña
    }
    options.add_experimental_option('prefs', prefs)

    # instanciamos el servicio de chromedriver

    s = Service(ruta)

    # instanciamos Webdriver 

    driver = webdriver.Chrome(service=s,options=options)

    # devolvemos el driver
    
    return driver

def login_comunio():
    """ Realizamos login por cookies y sino desde cero """
    print("Login Comunio sin cookies")
    driver.get('https://www.comunio.es')
    # 
    driver.find_element(By.XPATH,"//button/span[contains(text(),'ACEPTO')]").click()
    # Pulsamos para login
    elemento = wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@id='above-the-fold-container']/div[2]/div[1]/div[2]/a[1]")))
    elemento.click()
    # Rellenamos los campos
    try:
        elemento = wait.until(ec.visibility_of_element_located((By.ID, "input-login")))
        elemento.send_keys(USER_COMUNIO)
    except TimeoutException:
        print('Error: Elemento no disponible')
        return "ERROR"
    elemento = wait.until(ec.visibility_of_element_located((By.ID, "input-pass")))
    elemento.send_keys(PASS_COMUNIO)
    elemento = wait.until(ec.element_to_be_clickable((By.ID, "login-btn-modal")))
    elemento.click()
    
def getPlantilla_comunio():
    try:
        elemento= wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "a[title='Alineación']")))
        elemento.click()
    except TimeoutException:
        print("Error: No se puede acceder a 'Alineación'")
        return "Alineación: Error"

def modo_de_uso():
    mensaje  = f'Modo de uso:\n'
    mensaje += f'    {os.path.basename(sys.executable)} {sys.argv[0]} [opciones]\n\n'
    mensaje += f'    opciones:\n'
    mensaje += f'       -p obtener plantilla\n'
    mensaje += f'       -p obtener plantilla\n'
    mensaje += f'       -p obtener plantilla\n\n'
    mensaje += f'    Ejemplos:\n'
    mensaje += f'       {os.path.basename(sys.executable)} {sys.argv[0]} -p \n'
    # mensaje += f'       {os.path.basename(sys.executable)} {sys.argv[0]} -c'

    return mensaje

# MAIN ################################
if __name__ == '__main__':
    # control de parametros
    if len(sys.argv) > 3:
        print(modo_de_uso())
        sys.exit(1)
    
    # inicioamos selenium
    driver = iniciar_chrome()
    # Configuramos el tiempo de espera para cargar elementos
    wait = WebDriverWait(driver,10) # Tiempo de espera hasta que este disponible

    # nos logeamos en Comunio
    res = login_comunio()
    if res=="ERROR":
        input("Pulsa ENTER para salir....") # pulsamos para estudiar el error
        driver.quit() # Cerramos chrome
        sys.exit(1) # Salimos del programa con error
    # Obtener la plantilla
    res = getPlantilla_comunio()
    input("Pulsa ENTER para Salir")
    driver.quit()
