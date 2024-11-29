import tkinter as tk
from tkinter import messagebox
from db_connection import conectar_db
from generar_contrasena import generar_contrasena
from ver_contrasenas import ver_contrasenas
from ver_perfil import ver_perfil
from modificar_contrasena import modificar_contrasena
from evaluar_contrasena import mostrar_resultado

# Obtener nombre de usuario
def obtener_nombre_usuario(usuario_id):
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre FROM usuarios WHERE id = %s", (usuario_id,))
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        return resultado[0] if resultado else "Usuario Desconocido"
    return "Usuario Desconocido"

# Función para limpiar el contenido del frame principal
def limpiar_frame(frame):
    """
    Elimina todos los widgets del frame proporcionado.
    """
    for widget in frame.winfo_children():
        widget.destroy()

# Nueva función para la vista de evaluar contraseñas
def evaluar_contrasena_menu(frame_principal, usuario_id):
    """
    Crea una vista en el menú para evaluar contraseñas.
    """
    limpiar_frame(frame_principal)  # Limpiar el frame antes de cargar la vista

    tk.Label(frame_principal, text="Evaluar Contraseña", font=("Arial", 16), bg="#2A2B2A", fg="white").pack(pady=20)

    contrasena_var = tk.StringVar()
    tk.Label(frame_principal, text="Introduce tu contraseña:", bg="#2A2B2A", fg="white").pack(pady=5)
    contrasena_entry = tk.Entry(frame_principal, textvariable=contrasena_var, show="*", bg="#2A2B2A", fg="white", width=30)
    contrasena_entry.pack(pady=10)

    tk.Button(frame_principal, text="Evaluar", bg="#4CAF50", fg="white", 
          command=lambda: mostrar_resultado(frame_principal, contrasena_var.get())).pack(pady=20)


# Función principal para inicializar la ventana
def main(usuario_id=1):
    """
    Inicializa la ventana principal y configura el menú.
    """
    # Crear la ventana principal
    ventana_principal = tk.Tk()
    ventana_principal.title("Gestor de Contraseñas")
    ventana_principal.geometry("1000x600")
    ventana_principal.config(bg="#2b2b2b")

    # Obtener nombre del usuario
    nombre_usuario = obtener_nombre_usuario(usuario_id)

    # Crear barra lateral
    frame_sidebar = tk.Frame(ventana_principal, bg="#333333", width=200, height=600)
    frame_sidebar.pack(side="left", fill="y")

    # Título de la barra lateral
    titulo_sidebar = tk.Label(frame_sidebar, text=f"Menú - {nombre_usuario}", font=("Arial", 18), fg="white", bg="#333333")
    titulo_sidebar.pack(pady=20)

    # Frame principal donde se mostrarán las vistas
    frame_principal = tk.Frame(ventana_principal, bg="#2A2B2A")
    frame_principal.pack(side="right", expand=True, fill="both")

    # Funciones para cada vista, limpiando el frame antes de mostrar la nueva
    def mostrar_generar_contrasena():
        limpiar_frame(frame_principal)
        generar_contrasena(frame_principal, usuario_id)

    def mostrar_ver_contrasenas():
        limpiar_frame(frame_principal)
        ver_contrasenas(frame_principal, usuario_id)

    def mostrar_ver_perfil():
        limpiar_frame(frame_principal)
        ver_perfil(frame_principal, usuario_id)

    def mostrar_evaluar_contrasena():
        limpiar_frame(frame_principal)
        evaluar_contrasena_menu(frame_principal, usuario_id)

    # Opciones del menú
    opciones_menu = [
        ("Crear Contraseña", mostrar_generar_contrasena),
        ("Ver Contraseñas", mostrar_ver_contrasenas),
        ("Evaluar Contraseña", mostrar_evaluar_contrasena),
        ("Ver Perfil", mostrar_ver_perfil),
        ("Cerrar Sesión", ventana_principal.destroy)
    ]

    # Crear botones para las opciones
    for texto, comando in opciones_menu:
        boton = tk.Button(frame_sidebar, text=texto, font=("Poppins", 12), bg="#555555", fg="white", width=20, command=comando)
        boton.pack(pady=10)

    # Iniciar la interfaz gráfica
    ventana_principal.mainloop()

# Ejecutar la función principal con un ID de usuario predeterminado
if __name__ == "__main__":
    main(usuario_id=1)
