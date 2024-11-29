import tkinter as tk
from tkinter import messagebox
import random
import string
from datetime import datetime
from db_connection import conectar_db
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import hashlib

# Función para generar una contraseña normal
def generar_contrasena_normal(longitud, usar_mayusculas, usar_minusculas, usar_numeros, usar_simbolos):
    caracteres = ""
    if usar_minusculas:
        caracteres += string.ascii_lowercase
    if usar_mayusculas:
        caracteres += string.ascii_uppercase
    if usar_numeros:
        caracteres += string.digits
    if usar_simbolos:
        caracteres += string.punctuation

    if not caracteres:
        return "Debes seleccionar al menos un tipo de carácter."
    
    return ''.join(random.choice(caracteres) for _ in range(longitud))

# Función para generar una contraseña tipo XKCD (usando palabras aleatorias)
def generar_contrasena_xkcd():
    palabras = ["gato", "piano", "silla", "sol", "luna", "puerta", "feliz", "rojo", "zapato", "flor", "perro", "pelota"]
    contrasena = " ".join(random.sample(palabras, 4))  # Elegir 4 palabras aleatorias
    return contrasena

# Función para obtener la clave secreta (SHA256 de una clave base)
def obtener_clave_secreta():
    clave_secreta = "mi_clave_secreta"  # Aquí puedes cambiar a la clave que desees
    return hashlib.sha256(clave_secreta.encode()).digest()  # Usamos un SHA-256 para generar una clave de 256 bits

# Función para encriptar la contraseña con AES
def encriptar_contrasena(contrasena, clave_secreta):
    cipher = AES.new(clave_secreta, AES.MODE_CBC)  # Modo CBC de AES
    contrasena_padded = pad(contrasena.encode(), AES.block_size)  # Padding para que la longitud sea múltiplo del bloque
    encrypted = cipher.encrypt(contrasena_padded)
    
    # Codificar en Base64 para almacenamiento
    iv_base64 = base64.b64encode(cipher.iv).decode('utf-8')
    encrypted_base64 = base64.b64encode(encrypted).decode('utf-8')
    return iv_base64, encrypted_base64

# Función para guardar la contraseña en la base de datos
def guardar_contrasena(contrasena, servicio, usuario_id):
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        fecha_creacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Encriptar la contraseña antes de guardarla
        clave_secreta = obtener_clave_secreta()
        iv, contrasena_encriptada = encriptar_contrasena(contrasena, clave_secreta)

        cursor.execute("INSERT INTO contraseñas (usuario_id, contrasena, fecha_creacion, servicio, iv) VALUES (%s, %s, %s, %s, %s)", 
                       (usuario_id, contrasena_encriptada, fecha_creacion, servicio, iv))
        conexion.commit()
        cursor.close()
        conexion.close()

# Función principal para generar la contraseña y gestionar la interfaz gráfica
def generar_contrasena(frame_principal, usuario_id):
    # Limpiar la pantalla y configurar el layout
    for widget in frame_principal.winfo_children():
        widget.destroy()

    frame_opciones = tk.Frame(frame_principal, bg="#2A2B2A")
    frame_opciones.pack(pady=20)

    tk.Label(frame_opciones, text="Longitud:", bg="#2A2B2A", fg="white", font=("Arial", 14)).grid(row=0, column=0, padx=5, pady=5)
    longitud_var = tk.IntVar(value=12)
    longitud_slider = tk.Scale(frame_opciones, from_=12, to=30, orient="horizontal", variable=longitud_var, bg="#2A2B2A", fg="white", highlightthickness=0)
    longitud_slider.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_opciones, text="Servicio:", bg="#2A2B2A", fg="white", font=("Arial", 14)).grid(row=1, column=0, padx=5, pady=5)
    entrada_servicio = tk.Entry(frame_opciones, bg="#2A2B2A", fg="white", insertbackground="white")
    entrada_servicio.grid(row=1, column=1, padx=5, pady=5)

    var_mayusculas = tk.BooleanVar(value=True)
    var_minusculas = tk.BooleanVar(value=True)
    var_numeros = tk.BooleanVar(value=True)
    var_simbolos = tk.BooleanVar(value=False)

    def actualizar_label_checkboxes():
        for chk, label in zip([var_mayusculas, var_minusculas, var_numeros, var_simbolos], [label_mayusculas, label_minusculas, label_numeros, label_simbolos]):
            if chk.get():
                label.config(text="✅")
            else:
                label.config(text="❌")

    label_mayusculas = tk.Label(frame_opciones, text="❌", bg="#2A2B2A", fg="white", font=("Arial", 14))
    label_mayusculas.grid(row=2, column=0, sticky="w", padx=5, pady=2)
    tk.Checkbutton(frame_opciones, text="Incluir mayúsculas", variable=var_mayusculas, bg="#2A2B2A", fg="white", command=actualizar_label_checkboxes).grid(row=2, column=1, sticky="w", padx=5, pady=2)

    label_minusculas = tk.Label(frame_opciones, text="❌", bg="#2A2B2A", fg="white", font=("Arial", 14))
    label_minusculas.grid(row=3, column=0, sticky="w", padx=5, pady=2)
    tk.Checkbutton(frame_opciones, text="Incluir minúsculas", variable=var_minusculas, bg="#2A2B2A", fg="white", command=actualizar_label_checkboxes).grid(row=3, column=1, sticky="w", padx=5, pady=2)

    label_numeros = tk.Label(frame_opciones, text="❌", bg="#2A2B2A", fg="white", font=("Arial", 14))
    label_numeros.grid(row=4, column=0, sticky="w", padx=5, pady=2)
    tk.Checkbutton(frame_opciones, text="Incluir números", variable=var_numeros, bg="#2A2B2A", fg="white", command=actualizar_label_checkboxes).grid(row=4, column=1, sticky="w", padx=5, pady=2)

    label_simbolos = tk.Label(frame_opciones, text="❌", bg="#2A2B2A", fg="white", font=("Arial", 14))
    label_simbolos.grid(row=5, column=0, sticky="w", padx=5, pady=2)
    tk.Checkbutton(frame_opciones, text="Incluir caracteres especiales", variable=var_simbolos, bg="#2A2B2A", fg="white", command=actualizar_label_checkboxes).grid(row=5, column=1, sticky="w", padx=5, pady=2)

    # Variable para mostrar la contraseña generada
    resultado_var = tk.StringVar()

    # Etiqueta para mostrar la contraseña generada
    resultado_label = tk.Label(frame_principal, textvariable=resultado_var, bg="#2A2B2A", fg="white", font=("Arial", 14), wraplength=400)
    resultado_label.pack(pady=10)

    def on_generar_normal():
        longitud = longitud_var.get()
        servicio = entrada_servicio.get()

        if not servicio:
            messagebox.showwarning("Advertencia", "Por favor, ingresa el nombre del servicio.")
            return
        
        contrasena = generar_contrasena_normal(longitud, var_mayusculas.get(), var_minusculas.get(), var_numeros.get(), var_simbolos.get())
        guardar_contrasena(contrasena, servicio, usuario_id)
        resultado_var.set(f"Tu nueva contraseña es:\n{contrasena}")

    def on_generar_xkcd():
        servicio = entrada_servicio.get()

        if not servicio:
            messagebox.showwarning("Advertencia", "Por favor, ingresa el nombre del servicio.")
            return
        
        contrasena = generar_contrasena_xkcd()
        guardar_contrasena(contrasena, servicio, usuario_id)
        resultado_var.set(f"Tu nueva contraseña es:\n{contrasena}")

    # Frame para los botones
    frame_botones = tk.Frame(frame_principal, bg="#2A2B2A")
    frame_botones.pack(pady=10)

    tk.Button(frame_botones, text="Generar Contraseña Normal", command=on_generar_normal, bg="#555555", fg="white").pack(side="left", padx=5)
    tk.Button(frame_botones, text="Generar Contraseña XKCD", command=on_generar_xkcd, bg="#555555", fg="white").pack(side="left", padx=5)
