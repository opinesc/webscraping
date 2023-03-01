# para instalar automáticamente chromedrive
# pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager
# Driver de Selenium
# pip install selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# Para modificar las opciones de webdriver
from selenium.webdriver.chrome.options import Options
# Para definir el tipo de busqueda del elemento
from selenium.webdriver.common.by import By
# importamos la credenciales de Comunio
from env import *

def iniciar_chrome():
    """ Instalamos la versión del Chromedriver correspondiente """
    ruta = ChromeDriverManager(path='./chromedriver').install()
    
    #  Opciones de Chrome
    
    options = Options()  # instanciamos las opciones de chrome
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

# MAIN

if __name__ == '__main__':
    driver = iniciar_chrome()
    url="https://www.comunio.es"
    driver.get(url)
    # quitamos mensaje inicial "Su privacidad.."
    # xpath //button/span[contains(text(),'ACEPTO')]
    driver.find_element(By.XPATH,"//button/span[contains(text(),'ACEPTO')]").click()
    input("Pulsar ENTER para Salir")
    driver.quit()