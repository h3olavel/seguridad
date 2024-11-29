# main.py
import tkinter as tk
from tkinter import messagebox
from db_connection import conectar_db
import menu
import register
import confirmar  # Importa confirmar para invocar la verificación

def validar_login():
    email = entrada_email.get()
    contraseña = entrada_contraseña.get()
    conexion = conectar_db()

    if conexion:
        cursor = conexion.cursor()
        # Se consulta la base de datos para verificar el correo y la contraseña
        cursor.execute("SELECT id, nombre FROM usuarios WHERE email=%s", (email,))
        usuario = cursor.fetchone()
        cursor.close()

        if usuario:
            usuario_id, nombre_usuario = usuario
            # Ahora, comparamos la contraseña ingresada con la almacenada en la base de datos
            conexion = conectar_db()  # Volvemos a abrir la conexión para comparar la contraseña
            cursor = conexion.cursor()
            cursor.execute("SELECT contrasena FROM usuarios WHERE id=%s", (usuario_id,))
            usuario_contrasena = cursor.fetchone()[0]
            cursor.close()
            conexion.close()

            if usuario_contrasena == contraseña:
                messagebox.showinfo("Inicio de sesión", "Inicio de sesión exitoso. Procediendo a verificación.")
                
                # Cerrar la ventana principal inmediatamente
                ventana.destroy()  # Esto cierra la ventana principal
                
                # Iniciar la verificación
                confirmar.iniciar_verificacion(email, nombre_usuario, usuario_id)
            else:
                messagebox.showerror("Error", "Contraseña incorrecta.")
        else:
            messagebox.showerror("Error", "Correo electrónico no registrado.")
    else:
        messagebox.showerror("Error", "Error de conexión a la base de datos.")

def mostrar_registro():
    register.abrir_registro(ventana)

def centrar_ventana(ventana, ancho, alto):
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    x = int((screen_width / 2) - (ancho / 2))
    y = int((screen_height / 2) - (alto / 2))
    ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Inicio de sesión")
ancho_ventana = 400
alto_ventana = 300
ventana.geometry(f"{ancho_ventana}x{alto_ventana}")
ventana.config(bg="#2b2b2b")

centrar_ventana(ventana, ancho_ventana, alto_ventana)

# Funciones para limpiar texto predeterminado
def limpiar_texto(event, campo, texto_default):
    if campo.get() == texto_default:
        campo.delete(0, tk.END)
        campo.config(fg="white")

# Marco único de la ventana
frame_principal = tk.Frame(ventana, bg="#333333", bd=1, relief="solid")
frame_principal.place(relx=0, rely=0, anchor="nw", width=400, height=300)

label_titulo = tk.Label(frame_principal, text="Inicio de sesión", font=("Poppins", 18), fg="white", bg="#333333")
label_titulo.pack(pady=20)

# Campo de entrada para el email
frame_email = tk.Frame(frame_principal, bg="#333333")
frame_email.pack(pady=10)
icono_email = tk.Label(frame_email, text="📧", font=("Arial", 18), bg="#333333", fg="white")
icono_email.pack(side="left", padx=5)
entrada_email = tk.Entry(frame_email, font=("Poppins", 14), fg="grey", bg="#333333", insertbackground="white", width=25)
entrada_email.insert(0, 'Ingrese su email')
entrada_email.bind("<FocusIn>", lambda event: limpiar_texto(event, entrada_email, 'Ingrese su email'))
entrada_email.pack(side="left", padx=10)

# Campo de entrada para la contraseña
frame_contraseña = tk.Frame(frame_principal, bg="#333333")
frame_contraseña.pack(pady=10)
icono_contraseña = tk.Label(frame_contraseña, text="🔒", font=("Arial", 18), bg="#333333", fg="white")
icono_contraseña.pack(side="left", padx=5)
entrada_contraseña = tk.Entry(frame_contraseña, font=("Poppins", 14), fg="grey", bg="#333333", insertbackground="white", width=25, show="*")
entrada_contraseña.insert(0, '*********')
entrada_contraseña.bind("<FocusIn>", lambda event: limpiar_texto(event, entrada_contraseña, '*********'))
entrada_contraseña.pack(side="left", padx=10)

# Botón de inicio de sesión
boton_login = tk.Button(frame_principal, text="Continuar", font=("Poppins", 12), bg="white", fg="black", width=25, command=validar_login)
boton_login.pack(pady=20)

# Opción para crear una cuenta
label_crear_cuenta = tk.Label(frame_principal, text="Registrarse", font=("Arial", 10), fg="white", bg="#333333", cursor="hand2", underline=True)
label_crear_cuenta.pack()
label_crear_cuenta.bind("<Button-1>", lambda e: mostrar_registro())

ventana.mainloop()
