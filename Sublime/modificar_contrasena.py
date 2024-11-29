import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
from db_connection import conectar_db
from tkinter.simpledialog import askstring
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import hashlib

# Función para modificar la contraseña
def modificar_contrasena(usuario_id, id_contrasena):
    def cargar_datos_actuales():
        conexion = conectar_db()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT servicio, contrasena FROM contraseñas WHERE id = %s", (id_contrasena,))
                return cursor.fetchone()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                return None
            finally:
                if conexion:
                    cursor.close()
                    conexion.close()

    def actualizar_contrasena():
        nuevo_servicio = servicio_var.get()
        nueva_contrasena = contrasena_var.get()
        
        # Si no se modifican los campos, mantener los valores originales
        if nuevo_servicio == servicio_actual:
            nuevo_servicio = servicio_actual
        if nueva_contrasena == contrasena_actual:
            nueva_contrasena = contrasena_actual
        
        conexion = conectar_db()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("UPDATE contraseñas SET servicio = %s, contrasena = %s WHERE id = %s", 
                               (nuevo_servicio, nueva_contrasena, id_contrasena))
                conexion.commit()
                messagebox.showinfo("Actualización exitosa", "La contraseña y servicio han sido modificados.")
                ventana_modificar.destroy()
            except Exception as e:
                messagebox.showerror("Error de Conexión", str(e))
            finally:
                if conexion:
                    cursor.close()
                    conexion.close()

    # Ventana para modificar contraseña y servicio
    ventana_modificar = tk.Toplevel()
    ventana_modificar.title("Modificar Contraseña y Servicio")
    ventana_modificar.geometry("400x400")
    ventana_modificar.config(bg="#2A2B2A")

    # Cargar datos actuales
    datos_actuales = cargar_datos_actuales()
    if not datos_actuales:
        messagebox.showerror("Error", "No se pudieron cargar los datos de la contraseña")
        return

    servicio_actual, contrasena_actual = datos_actuales

    # Etiqueta de advertencia
    advertencia_label = tk.Label(ventana_modificar, 
                                 text="Advertencia de Seguridad", 
                                 bg="#2A2B2A", 
                                 fg="red", 
                                 font=("Arial", 12, "bold"))
    advertencia_label.pack(pady=(10, 5))

    # Mensaje de advertencia
    tk.Label(ventana_modificar, 
             text="Si modifica la contraseña sin usar nuestro generador,\n"
                  "puede que no tenga la misma seguridad.", 
             bg="#2A2B2A", 
             fg="white",
             wraplength=350).pack(pady=(0, 10))

    # Servicio actual
    tk.Label(ventana_modificar, text="Servicio Actual:", bg="#2A2B2A", fg="white").pack(pady=(10, 0))
    tk.Label(ventana_modificar, text=servicio_actual, bg="#2A2B2A", fg="yellow", font=("Arial", 12)).pack(pady=(0, 5))

    # Nuevo Servicio
    tk.Label(ventana_modificar, text="Nuevo Servicio (opcional):", bg="#2A2B2A", fg="white").pack(pady=(10, 0))
    servicio_var = tk.StringVar(value=servicio_actual)
    servicio_entry = tk.Entry(ventana_modificar, 
                               textvariable=servicio_var, 
                               bg="#2A2B2A", 
                               fg="white", 
                               insertbackground="white",
                               width=40)
    servicio_entry.pack(pady=5)

    # Contraseña actual
    tk.Label(ventana_modificar, text="Contraseña Actual:", bg="#2A2B2A", fg="white").pack(pady=(10, 0))
    tk.Label(ventana_modificar, text=contrasena_actual, bg="#2A2B2A", fg="yellow", font=("Arial", 12)).pack(pady=(0, 5))

    # Nueva Contraseña
    tk.Label(ventana_modificar, text="Nueva Contraseña (opcional):", bg="#2A2B2A", fg="white").pack(pady=(10, 0))
    contrasena_var = tk.StringVar(value=contrasena_actual)
    contrasena_entry = tk.Entry(ventana_modificar, 
                                 textvariable=contrasena_var, 
                                 bg="#2A2B2A", 
                                 fg="white", 
                                 insertbackground="white", 
                                 show="*",
                                 width=40)
    contrasena_entry.pack(pady=5)

    modificar_btn = tk.Button(ventana_modificar, 
                               text="Modificar", 
                               command=actualizar_contrasena, 
                               bg="#4CAF50", 
                               fg="white")
    modificar_btn.pack(pady=10)

    # Mostrar la ventana
    ventana_modificar.transient(None)  # Establecer como ventana secundaria
    ventana_modificar.grab_set()  # Hacer la ventana modal
    ventana_modificar.focus_set()  # Establecer foco

# Función principal que se usa en el código original
def ver_contrasenas(frame_principal, usuario_id):
    def configurar_tabla_contrasenas():
        # Crear frame para la tabla
        frame_tabla = tk.Frame(frame_principal)
        frame_tabla.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Crear tabla con Treeview
        columnas = ("Servicio", "Contraseña", "Fecha de Creación")
        tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        
        # Configurar encabezados
        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, width=200, anchor=tk.CENTER)
        
        # Estilo de la tabla
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview", 
            background="#2A2A2B",  # Color de fondo personalizado
            foreground="white",    # Texto blanco
            rowheight=25,
            fieldbackground="#2A2A2B"
        )
        style.map('Treeview', background=[('selected', '#347083')])

        # Variable para almacenar datos de contraseñas
        contrasenas_data = []

        # Cargar contraseñas
        conexion = conectar_db()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT id, servicio, contrasena, fecha_creacion, iv FROM contraseñas WHERE usuario_id = %s", (usuario_id,))
                contrasenas_data = cursor.fetchall()

                # Insertar contraseñas en la tabla (se mostrarán encriptadas inicialmente)
                for (id_contrasena, servicio, contrasena_encriptada, fecha_creacion, iv_base64) in contrasenas_data:
                    tabla.insert("", tk.END, values=(servicio, "********", fecha_creacion), tags=(id_contrasena, iv_base64, contrasena_encriptada))
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                if conexion:
                    cursor.close()
                    conexion.close()

        # Colocar tabla en el frame
        tabla.pack(fill=tk.BOTH, expand=True)

        # Frame para botones de acción
        frame_botones = tk.Frame(frame_principal, bg="#2A2B2A")
        frame_botones.pack(pady=10)

        # Botones deshabilitados inicialmente
        def habilitar_botones():
            boton_copiar.config(state=tk.NORMAL)
            boton_modificar.config(state=tk.NORMAL)
            boton_eliminar.config(state=tk.NORMAL)

        def mostrar_contrasenas():
            # Solicitar contraseña de usuario
            password_usuario = askstring("Validación", "Introduce tu contraseña para ver las contraseñas:", show='*')
            if not password_usuario:
                return
            
            # Validar contraseña
            conexion = conectar_db()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    cursor.execute("SELECT contrasena FROM usuarios WHERE id = %s", (usuario_id,))
                    resultado = cursor.fetchone()
                    
                    if resultado and resultado[0] == password_usuario:
                        # Mostrar contraseñas reales (desencriptadas)
                        for item in tabla.get_children():
                            # Obtener los valores de la fila actual
                            id_contrasena, iv_base64, contrasena_encriptada = tabla.item(item, 'tags')
                            
                            # Desencriptar la contraseña
                            iv = base64.b64decode(iv_base64)
                            contrasena_real = desencriptar_contrasena(contrasena_encriptada, iv)
                            
                            # Actualizar la tabla con la contraseña desencriptada
                            tabla.item(item, values=(tabla.item(item, 'values')[0], contrasena_real, tabla.item(item, 'values')[2]))

                        # Habilitar botones
                        habilitar_botones()
                    else:
                        messagebox.showerror("Error", "Contraseña incorrecta")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                finally:
                    if conexion:
                        cursor.close()
                        conexion.close()

        def copiar_contrasena():
            seleccion = tabla.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Selecciona una contraseña para copiar")
                return
            
            index = tabla.get_children().index(seleccion[0])
            id_contrasena = contrasenas_data[index][0]
            iv_base64 = contrasenas_data[index][4]  # Obtener el IV base64 desde los datos

            # Desencriptar la contraseña
            iv = base64.b64decode(iv_base64)
            contrasena_encriptada = contrasenas_data[index][2]
            contrasena_real = desencriptar_contrasena(contrasena_encriptada, iv)
            
            # Copiar la contraseña desencriptada
            pyperclip.copy(contrasena_real)
            messagebox.showinfo("Éxito", "Contraseña copiada al portapapeles")

        def eliminar_contrasena():
            seleccion = tabla.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Selecciona una contraseña para eliminar")
                return
            
            # Confirmar contraseña de usuario
            password_usuario = askstring("Validación", "Introduce tu contraseña para eliminar:", show='*')
            if not password_usuario:
                return
            
            conexion = conectar_db()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    # Verificar contraseña de usuario
                    cursor.execute("SELECT contrasena FROM usuarios WHERE id = %s", (usuario_id,))
                    resultado = cursor.fetchone()
                    
                    if resultado and resultado[0] == password_usuario:
                        index = tabla.get_children().index(seleccion[0])
                        id_contrasena = contrasenas_data[index][0]
                        
                        # Confirmar eliminación
                        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta contraseña?"):
                            cursor.execute("DELETE FROM contraseñas WHERE id = %s", (id_contrasena,))
                            conexion.commit()
                            messagebox.showinfo("Éxito", "Contraseña eliminada")
                            # Eliminar de la tabla
                            tabla.delete(seleccion[0])
                    else:
                        messagebox.showerror("Error", "Contraseña incorrecta")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                finally:
                    if conexion:
                        cursor.close()
                        conexion.close()

        # Crear botones
        boton_mostrar = tk.Button(frame_botones, text="Mostrar", command=mostrar_contrasenas)
        boton_mostrar.pack(side=tk.LEFT, padx=5)

        boton_copiar = tk.Button(frame_botones, text="Copiar", state=tk.DISABLED, command=copiar_contrasena)
        boton_copiar.pack(side=tk.LEFT, padx=5)

        boton_modificar = tk.Button(frame_botones, text="Modificar", state=tk.DISABLED, command=modificar_contrasena_btn)
        boton_modificar.pack(side=tk.LEFT, padx=5)

        boton_eliminar = tk.Button(frame_botones, text="Eliminar", state=tk.DISABLED, command=eliminar_contrasena)
        boton_eliminar.pack(side=tk.LEFT, padx=5)

    # Función para desencriptar la contraseña usando AES
    def desencriptar_contrasena(contrasena_encriptada, iv):
        clave_secreta = obtener_clave_secreta()
        cipher = AES.new(clave_secreta, AES.MODE_CBC, iv)
        contrasena_bytes = base64.b64decode(contrasena_encriptada)
        contrasena_padded = unpad(cipher.decrypt(contrasena_bytes), AES.block_size)
        return contrasena_padded.decode('utf-8')

    # Función para obtener la clave secreta (SHA256 de una clave base)
    def obtener_clave_secreta():
        clave_secreta = "mi_clave_secreta"  # Aquí puedes cambiar a la clave que desees
        return hashlib.sha256(clave_secreta.encode()).digest()  # Usamos un SHA-256 para generar una clave de 256 bits

    # Iniciar configuración de tabla de contraseñas
    configurar_tabla_contrasenas()
