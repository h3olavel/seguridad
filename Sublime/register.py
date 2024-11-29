import tkinter as tk
from tkinter import messagebox
import mysql.connector
import random
import string
from db_connection import conectar_db

# Genera una contraseña segura entre 12 y 20 caracteres
def generar_contrasena():
    longitud = random.randint(12, 20)
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(caracteres) for _ in range(longitud))

# Función para registrar un nuevo usuario
def registrar_usuario(ventana_registro, entrada_email, entrada_nombre, entrada_telefono, contraseña_generada):
    nuevo_email = entrada_email.get()
    nuevo_nombre = entrada_nombre.get()
    nuevo_telefono = entrada_telefono.get()

    # Validación del campo de correo: debe contener un '@'
    if "@" not in nuevo_email:
        messagebox.showerror("Error", "No se puede asegurar que es un correo electronico")
        return

    # Verificar que todos los campos estén completos
    if not (nuevo_email and nuevo_nombre and nuevo_telefono):
        messagebox.showerror("Error", "Por favor, complete todos los campos")
        return

    # Conectar a la base de datos y registrar al usuario
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        # Verificamos si el email ya existe en la base de datos
        cursor.execute("SELECT * FROM usuarios WHERE email=%s", (nuevo_email,))
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            messagebox.showerror("Error", "El correo ya está registrado")
        else:
            # Insertar el nuevo usuario en la base de datos
            cursor.execute("INSERT INTO usuarios (nombre, email, telefono, contrasena, fecha_creacion) VALUES (%s, %s, %s, %s, NOW())",
                           (nuevo_nombre, nuevo_email, nuevo_telefono, contraseña_generada))
            conexion.commit()
            messagebox.showinfo("Registro", "Usuario registrado exitosamente")
            ventana_registro.destroy()  # Cierra la ventana de registro después de un registro exitoso

        cursor.close()
        conexion.close()


# Función para copiar la contraseña al portapapeles sin mostrarla
def copiar_contrasena(ventana_registro, contraseña):
    ventana_registro.clipboard_clear()
    ventana_registro.clipboard_append(contraseña)

# Función para abrir la ventana de registro
def abrir_registro(ventana_padre):
    ventana_registro = tk.Toplevel(ventana_padre)
    ventana_registro.title("Registrar Usuario")
    ventana_registro.geometry("400x500")
    ventana_registro.config(bg="#2b2b2b")

    # Generar una contraseña segura automáticamente
    contraseña_generada = generar_contrasena()

    # Función para limpiar el texto cuando el usuario hace clic en el campo
    def limpiar_texto(event, campo, texto_inicial):
        if campo.get() == texto_inicial:
            campo.delete(0, tk.END)
            campo.config(fg="white")  # Cambiar color de texto a blanco

    # Función para restaurar el texto si el campo está vacío
    def restaurar_texto(event, campo, texto_inicial):
        if campo.get() == "":
            campo.insert(0, texto_inicial)
            campo.config(fg="grey")  # Cambiar color de texto a gris

    # Campo para el email
    frame_email = tk.Frame(ventana_registro, bg="#333333")
    frame_email.pack(pady=10, anchor='center')
    icono_email = tk.Label(frame_email, text="📧", font=("Arial", 18), bg="#333333", fg="white")
    icono_email.pack(side="left", padx=5)
    entrada_email = tk.Entry(frame_email, font=("Poppins", 14), fg="grey", bg="#2b2b2b", insertbackground="white", width=25)
    texto_inicial_email = "Ingrese su email"
    entrada_email.insert(0, texto_inicial_email)
    entrada_email.pack(side="left", padx=10)
    entrada_email.bind("<FocusIn>", lambda e: limpiar_texto(e, entrada_email, texto_inicial_email))
    entrada_email.bind("<FocusOut>", lambda e: restaurar_texto(e, entrada_email, texto_inicial_email))

    # Campo para el nombre
    frame_nombre = tk.Frame(ventana_registro, bg="#333333")
    frame_nombre.pack(pady=10, anchor='center')
    icono_nombre = tk.Label(frame_nombre, text="👤", font=("Arial", 18), bg="#333333", fg="white")
    icono_nombre.pack(side="left", padx=5)
    entrada_nombre = tk.Entry(frame_nombre, font=("Poppins", 14), fg="grey", bg="#2b2b2b", insertbackground="white", width=25)
    texto_inicial_nombre = "Ingrese su nombre"
    entrada_nombre.insert(0, texto_inicial_nombre)
    entrada_nombre.pack(side="left", padx=10)
    entrada_nombre.bind("<FocusIn>", lambda e: limpiar_texto(e, entrada_nombre, texto_inicial_nombre))
    entrada_nombre.bind("<FocusOut>", lambda e: restaurar_texto(e, entrada_nombre, texto_inicial_nombre))

    # Campo para el teléfono
    frame_telefono = tk.Frame(ventana_registro, bg="#333333")
    frame_telefono.pack(pady=10, anchor='center')
    icono_telefono = tk.Label(frame_telefono, text="📞", font=("Arial", 18), bg="#333333", fg="white")
    icono_telefono.pack(side="left", padx=5)
    entrada_telefono = tk.Entry(frame_telefono, font=("Poppins", 14), fg="grey", bg="#2b2b2b", insertbackground="white", width=25)
    texto_inicial_telefono = "Ingrese su teléfono"
    entrada_telefono.insert(0, texto_inicial_telefono)
    entrada_telefono.pack(side="left", padx=10)
    entrada_telefono.bind("<FocusIn>", lambda e: limpiar_texto(e, entrada_telefono, texto_inicial_telefono))
    entrada_telefono.bind("<FocusOut>", lambda e: restaurar_texto(e, entrada_telefono, texto_inicial_telefono))

    # Campo de Contraseña (sin mostrar la contraseña generada)
    frame_contraseña = tk.Frame(ventana_registro, bg="#333333")
    frame_contraseña.pack(pady=10, anchor='center')
    icono_contraseña = tk.Label(frame_contraseña, text="🔒", font=("Arial", 18), bg="#333333", fg="white")
    icono_contraseña.pack(side="left", padx=5)
    entrada_contraseña = tk.Entry(frame_contraseña, font=("Poppins", 14), fg="grey", bg="#2b2b2b", insertbackground="white", width=25, show="*")
    entrada_contraseña.insert(0, 'Contraseña generada')
    entrada_contraseña.config(state="readonly")
    entrada_contraseña.pack(side="left", padx=10)

    # Botón para copiar la contraseña al portapapeles
    boton_copiar = tk.Button(ventana_registro, text="📄 Copiar contraseña generada", font=("Poppins", 12), bg="white", fg="black",
                             command=lambda: copiar_contrasena(ventana_registro, contraseña_generada))
    boton_copiar.pack(pady=5)

    # Botón de registro
    boton_registro = tk.Button(ventana_registro, text="Registrar", font=("Poppins", 12), bg="white", fg="black", width=25,
                               command=lambda: registrar_usuario(ventana_registro, entrada_email, entrada_nombre, entrada_telefono, contraseña_generada))
    boton_registro.pack(pady=20, anchor='center')

    # Función para centrar la ventana
    def centrar_ventana():
        screen_width = ventana_registro.winfo_screenwidth()
        screen_height = ventana_registro.winfo_screenheight()
        x = int((screen_width / 2) - (ventana_registro.winfo_width() / 2))
        y = int((screen_height / 2) - (ventana_registro.winfo_height() / 2))
        ventana_registro.geometry(f'{ventana_registro.winfo_width()}x{ventana_registro.winfo_height()}+{x}+{y}')
    
    ventana_registro.after(100, centrar_ventana)

    ventana_registro.mainloop()
