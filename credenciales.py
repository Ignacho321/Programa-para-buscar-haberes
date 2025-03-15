import os
import json
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet

# Ruta de los archivos de credenciales y clave
ruta_sistema = "C://Program Files//Sistema de verificacion de haberes"
os.makedirs(ruta_sistema, exist_ok=True)
archivo_credenciales = os.path.join(ruta_sistema, "credenciales.dat")
clave_file = os.path.join(ruta_sistema, "clave.key")
log_file = os.path.join(ruta_sistema, "logs.txt")

# Clase GestorCredenciales para manejar las credenciales
class GestorCredenciales:
    def __init__(self, archivo="C://Program Files//Sistema de verificacion de haberes//credenciales.dat",
                 clave_file="C://Program Files//Sistema de verificacion de haberes//clave.key"):
        self.archivo = archivo
        self.clave_file = clave_file
        self.clave = self._obtener_o_generar_clave()
        self.fernet = Fernet(self.clave)

    def _obtener_o_generar_clave(self):
        if os.path.exists(self.clave_file):
            with open(self.clave_file, "rb") as f:
                return f.read()
        clave = Fernet.generate_key()
        with open(self.clave_file, "wb") as f:
            f.write(clave)
        return clave

    def agregar_credencial(self, usuario, contraseña, rol):
        datos = self.leer_credenciales()
        datos[usuario] = {"contraseña": contraseña, "rol": rol}
        self._guardar_credenciales(datos)

    def leer_credenciales(self):
        if not os.path.exists(self.archivo):
            return {}
        with open(self.archivo, "rb") as f:
            datos_cifrados = f.read()
        datos_json = self.fernet.decrypt(datos_cifrados).decode()
        return json.loads(datos_json)

    def verificar_credencial(self, usuario, contraseña):
        datos = self.leer_credenciales()
        if usuario in datos and datos[usuario]["contraseña"] == contraseña:
            return datos[usuario]["rol"]
        return None

    def _guardar_credenciales(self, datos):
        datos_json = json.dumps(datos).encode()
        datos_cifrados = self.fernet.encrypt(datos_json)
        with open(self.archivo, "wb") as f:
            f.write(datos_cifrados)

    def eliminar_credencial(self, usuario):
        datos = self.leer_credenciales()
        if usuario in datos:
            del datos[usuario]
            self._guardar_credenciales(datos)
            return True
        return False

    def cambiar_rol(self, usuario, nuevo_rol):
        datos = self.leer_credenciales()
        if usuario in datos:
            datos[usuario]["rol"] = nuevo_rol
            self._guardar_credenciales(datos)
            return True
        return False

    def log_acceso(self, usuario, mensaje):
        # Registrar el log de acceso
        with open(log_file, "a") as log:
            log.write(f"{usuario} - {mensaje}\n")


# Función para agregar un usuario
def agregar_usuario():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()
    rol = entry_rol.get()

    if usuario and contraseña and rol:
        gestor.agregar_credencial(usuario, contraseña, rol)
        gestor.log_acceso("admin", f"Agregó el usuario {usuario} con rol {rol}")
        messagebox.showinfo("Éxito", f"Usuario {usuario} agregado correctamente.")
        limpiar_campos()
    else:
        messagebox.showerror("Error", "Por favor, complete todos los campos.")


# Función para eliminar un usuario
def eliminar_usuario():
    usuario = entry_usuario.get()

    if usuario:
        if gestor.eliminar_credencial(usuario):
            gestor.log_acceso("admin", f"Eliminó el usuario {usuario}")
            messagebox.showinfo("Éxito", f"Usuario {usuario} eliminado correctamente.")
            limpiar_campos()
        else:
            messagebox.showerror("Error", f"Usuario {usuario} no encontrado.")
    else:
        messagebox.showerror("Error", "Por favor, ingrese el nombre de usuario.")


# Función para cambiar el rol de un usuario
def cambiar_rol():
    usuario = entry_usuario.get()
    nuevo_rol = entry_rol.get()

    if usuario and nuevo_rol:
        if gestor.cambiar_rol(usuario, nuevo_rol):
            gestor.log_acceso("admin", f"Cambió el rol de {usuario} a {nuevo_rol}")
            messagebox.showinfo("Éxito", f"Rol de {usuario} cambiado a {nuevo_rol}.")
            limpiar_campos()
        else:
            messagebox.showerror("Error", f"Usuario {usuario} no encontrado.")
    else:
        messagebox.showerror("Error", "Por favor, ingrese el nombre de usuario y el nuevo rol.")


# Función para limpiar los campos de texto
def limpiar_campos():
    entry_usuario.delete(0, tk.END)
    entry_contraseña.delete(0, tk.END)
    entry_rol.delete(0, tk.END)


# Crear ventana principal
ventana = tk.Tk()
ventana.title("Gestor de Credenciales")
ventana.geometry("400x300")

# Crear instancias de la clase GestorCredenciales
gestor = GestorCredenciales()

# Crear elementos de la interfaz
label_usuario = tk.Label(ventana, text="Usuario:")
label_usuario.pack(pady=5)

entry_usuario = tk.Entry(ventana)
entry_usuario.pack(pady=5)

label_contraseña = tk.Label(ventana, text="Contraseña:")
label_contraseña.pack(pady=5)

entry_contraseña = tk.Entry(ventana, show="*")
entry_contraseña.pack(pady=5)

label_rol = tk.Label(ventana, text="Rol (admin/usuario):")
label_rol.pack(pady=5)

entry_rol = tk.Entry(ventana)
entry_rol.pack(pady=5)

# Botones para agregar, eliminar, cambiar rol
button_agregar = tk.Button(ventana, text="Agregar Usuario", command=agregar_usuario)
button_agregar.pack(pady=5)

button_eliminar = tk.Button(ventana, text="Eliminar Usuario", command=eliminar_usuario)
button_eliminar.pack(pady=5)

button_cambiar_rol = tk.Button(ventana, text="Cambiar Rol", command=cambiar_rol)
button_cambiar_rol.pack(pady=5)

# Ejecutar la interfaz
ventana.mainloop()
