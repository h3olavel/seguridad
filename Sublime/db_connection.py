import mysql.connector
from tkinter import messagebox
from crypt_utils import cifrar_contrasena, descifrar_contrasena, generar_clave  # Importar funciones de cifrado
from datetime import datetime

# Configuración de la base de datos
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_USER = "root"
DB_PASS = ""
DB_NAME = "usuarios_db"

def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        return conexion
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al conectar a la base de datos: {err}")
        return None

# Función para guardar una nueva contraseña cifrada en la base de datos
def guardar_contrasena(usuario_id, contrasena, servicio, clave_secreta):
    contrasena_cifrada = cifrar_contrasena(contrasena, clave_secreta)  # Cifrar la contraseña antes de guardar
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            fecha_creacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("INSERT INTO contraseñas (usuario_id, contrasena, fecha_creacion, servicio) VALUES (%s, %s, %s, %s)", 
                           (usuario_id, contrasena_cifrada, fecha_creacion, servicio))
            conexion.commit()
            cursor.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al guardar la contraseña: {err}")
        finally:
            conexion.close()

# Función para obtener contraseñas y desencriptarlas
def obtener_contrasenas(usuario_id, clave_secreta):
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT servicio, contrasena, fecha_creacion FROM contraseñas WHERE usuario_id = %s", (usuario_id,))
            contrasenas_data = cursor.fetchall()

            # Desencriptar las contraseñas antes de devolverlas
            contrasenas_descifradas = []
            for servicio, contrasena_cifrada, fecha_creacion in contrasenas_data:
                contrasena_descifrada = descifrar_contrasena(contrasena_cifrada, clave_secreta)
                contrasenas_descifradas.append((servicio, contrasena_descifrada, fecha_creacion))
            
            return contrasenas_descifradas

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al obtener las contraseñas: {err}")
        finally:
            conexion.close()

    return []
