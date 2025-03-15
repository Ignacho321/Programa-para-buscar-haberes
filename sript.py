import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import re
driver_path = "C:/Users/admin/PycharmProjects/Proyecto bot para iveco/chromedriver-win64/chromedriver.exe"

# Diccionario de usuarios para autenticación
USUARIOS = {
    "usuario1": {"contraseña": "contraseña1", "rol": "admin"},
    "2": {"contraseña": "2", "rol": "normal"},
}

# Función para autenticar al usuario
def autenticar_usuario(ventana):
    def login():
        usuario = usuario_entry.get()
        contraseña = contraseña_entry.get()

        # Validación de las credenciales
        if usuario in USUARIOS and USUARIOS[usuario]["contraseña"] == contraseña:
            ventana.destroy()  # Cerrar la ventana de login
            ventana_fechas()   # Abrir la ventana de fechas
        else:
            messagebox.showerror("Error", "Credenciales incorrectas. Intenta nuevamente.")

    ventana_login = tk.Toplevel(ventana)
    ventana_login.title("Autenticación de Usuario")

    # Interfaz de ingreso de usuario y contraseña
    tk.Label(ventana_login, text="Usuario").pack(pady=5)
    usuario_entry = tk.Entry(ventana_login)
    usuario_entry.pack(pady=5)

    tk.Label(ventana_login, text="Contraseña").pack(pady=5)
    contraseña_entry = tk.Entry(ventana_login, show="*")
    contraseña_entry.pack(pady=5)

    tk.Button(ventana_login, text="Ingresar", command=login).pack(pady=10)

# Función para validar el formato de las fechas
def validar_fecha(fecha):
    if not re.match(r"^\d{2}/\d{2}/\d{4}$", fecha):
        return False
    dia, mes, año = map(int, fecha.split('/'))
    if dia < 1 or dia > 31 or mes < 1 or mes > 12 or año < 1000:
        return False
    return True

# Función para ingresar las fechas de inicio y fin
def ventana_fechas():
    def obtener_fechas():
        fecha_inicio = fecha_inicio_entry.get()
        fecha_fin = fecha_fin_entry.get()

        # Verificación de fechas
        if not fecha_inicio or not fecha_fin:
            messagebox.showerror("Error", "Por favor ingrese ambas fechas.")
            return

        if not validar_fecha(fecha_inicio):
            messagebox.showerror("Error", "Formato de fecha de inicio inválido. Use DD/MM/YYYY.")
            return
        if not validar_fecha(fecha_fin):
            messagebox.showerror("Error", "Formato de fecha de fin inválido. Use DD/MM/YYYY.")
            return

        ventana_credenciales(fecha_inicio, fecha_fin)

    ventana_fechas = tk.Toplevel()
    ventana_fechas.title("Ingreso de Fechas")

    # Interfaz de ingreso de fechas
    tk.Label(ventana_fechas, text="Fecha de inicio (DD/MM/YYYY)").pack(pady=5)
    fecha_inicio_entry = tk.Entry(ventana_fechas)
    fecha_inicio_entry.pack(pady=5)

    tk.Label(ventana_fechas, text="Fecha de fin (DD/MM/YYYY)").pack(pady=5)
    fecha_fin_entry = tk.Entry(ventana_fechas)
    fecha_fin_entry.pack(pady=5)

    tk.Button(ventana_fechas, text="Continuar", command=obtener_fechas).pack(pady=10)

# Función para ingresar las credenciales del home banking
def ventana_credenciales(fecha_inicio, fecha_fin):
    def iniciar_bot():
        usuario_home = usuario_home_entry.get()
        contraseña_home = contraseña_home_entry.get()

        if not usuario_home or not contraseña_home:
            messagebox.showerror("Error", "Por favor ingrese usuario y contraseña de Home Banking")
            return

        ejecutar_bot(fecha_inicio, fecha_fin, usuario_home, contraseña_home)

    ventana_credenciales = tk.Toplevel()
    ventana_credenciales.title("Inicio de sesión en Home Banking")

    # Interfaz de ingreso de credenciales del home banking
    tk.Label(ventana_credenciales, text="Usuario de Home Banking").pack(pady=5)
    usuario_home_entry = tk.Entry(ventana_credenciales)
    usuario_home_entry.pack(pady=5)

    tk.Label(ventana_credenciales, text="Contraseña de Home Banking").pack(pady=5)
    contraseña_home_entry = tk.Entry(ventana_credenciales, show="*")
    contraseña_home_entry.pack(pady=5)

    tk.Button(ventana_credenciales, text="Iniciar sesión", command=iniciar_bot).pack(pady=10)

# Función principal que ejecuta el bot
def ejecutar_bot(fecha_inicio, fecha_fin, usuario_home, contraseña_home):
    chrome_options = Options()
      # Ejecutar sin abrir el navegador
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver_path = os.path.join(os.getcwd(), "chromedriver.exe")
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://wsec06.bancogalicia.com.ar/Users/LogIn")
        time.sleep(10)  # Esperar a que la página cargue

        # Verificar si la página se ha cargado correctamente
        if "Office Banking" not in driver.title:
            raise Exception("La página de inicio de sesión no se cargó correctamente.")

        # Esperar a que el campo de usuario sea visible y clickeable
        wait = WebDriverWait(driver,0)  # Espera máxima de 10 segundos
        campo_usuario = wait.until(EC.element_to_be_clickable((By.ID, "UserID")))
        blocking_div = driver.find_element(By.CLASS_NAME, "placeholder")

        # Usa JavaScript para eliminar el elemento del DOM
        driver.execute_script("arguments[0].remove();", blocking_div)

        campo_usuario.click()  # Hacer clic primero
        campo_usuario.send_keys(usuario_home)

        campo_contraseña = wait = WebDriverWait(driver,0) (
            wait.until(EC.element_to_be_clickable((By.ID, "password"))))

        blocking_div = driver.find_element(By.CLASS_NAME, "placeholder")

        # Usa JavaScript para eliminar el elemento del DOM
        driver.execute_script("arguments[0].remove();", blocking_div)

        campo_contraseña.click()  # Hacer clic primero
        campo_contraseña.send_keys(contraseña_home)

        # Localizar y hacer clic en el botón de inicio de sesión
        boton_login = WebDriverWait(driver,  0 ).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.next"))
        )
        boton_login.click()

        time.sleep(7)

        if "Office Banking" in driver.title:
            raise Exception("hubo un problema con el inicio de sesion")

        # Ir a la página de transacciones
        driver.get("https://wsec06.bancogalicia.com.ar/Transaction/List")
        time.sleep(10)

        # Esperar a que los filtros sean clickeables antes de interactuar con ellos
        # Filtrar por fecha de inicio y fin
        campo_fecha_inicio = wait.until(EC.element_to_be_clickable((By.ID, "StartDateFilter")))

        campo_fecha_inicio.send_keys(fecha_inicio)

        campo_fecha_fin = wait.until(EC.element_to_be_clickable((By.ID, "EndDateFilter")))
        campo_fecha_fin.send_keys(fecha_fin)

        # Filtrar por tipo de operación
        campo_tipo_operacion = WebDriverWait(driver, 0).until(
            EC.element_to_be_clickable((By.ID, "SelectedOperationTypeFilter"))
        )
        campo_tipo_operacion.send_keys("Haberes - Envios")

        # Hacer clic en el botón de "Consultar"
        boton_consultar = WebDriverWait(driver, 0).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Consultar']"))
        )
        boton_consultar.click()
        time.sleep(5)

        # Guardar captura de pantalla
        ruta_captura = os.path.join("capturas", "resultado.png")
        driver.save_screenshot(ruta_captura)
        messagebox.showinfo("Completado", f"Tarea completada. Captura guardada en {ruta_captura}")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")
    finally:
        driver.quit()

# Función principal para iniciar la interfaz gráfica
def ventana_principal():
    ventana_principal = tk.Tk()
    ventana_principal.title("Sistema de Verificación de Haberes")

    tk.Button(ventana_principal, text="Login", command=lambda: autenticar_usuario(ventana_principal)).pack(pady=20)
    ventana_principal.mainloop()

if __name__ == "__main__":
    ventana_principal()
