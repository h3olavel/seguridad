# confirmar.py
import tkinter as tk
from tkinter import messagebox
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import menu  # Asegúrate de que este import sea correcto
from db_connection import conectar_db  # Usamos la función de conexión desde db_connection.py

# Función para enviar el código de verificación por correo
def enviar_codigo_email(email, codigo):
    remitente = "liam77973@gmail.com"  
    destinatario = email
    asunto = "Código de verificación"
    
    cuerpo_html = f"""
<html>
  <head>
    <style>
      body {{
        font-family: Arial, sans-serif;
        background-color: #2b2b2b;
        color: #ffffff;
        margin: 0;
        padding: 20px;
      }}
      .container {{
        background-color: #333333;
        border-radius: 8px;
        padding: 20px;
      }}
      .header {{
        font-size: 24px;
        margin-bottom: 10px;
        color: #d0d0d0;
      }}
      .footer {{
        margin-top: 20px;
        font-size: 12px;
        color: #aaaaaa;
      }}
      .button {{
        background-color: #4CAF50;
        color: white;
        padding: 10px 15px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        border-radius: 5px;
        margin-top: 10px;
      }}
      .code {{
        font-size: 22px;
        font-weight: bold;
        color: #4CAF50;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <p class="header">Hola,</p>
      <p>Tu código de verificación es: <span class="code">{codigo}</span></p>
      <p>¡Utiliza este código para verificar tu cuenta!</p>
      <p>¡Ingresa el código en la aplicación!</p>
      <p class="footer">Saludos,<br>El equipo de PasswordPalace</p>
    </div>
  </body>
</html>
"""

    # Crear el mensaje MIME
    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto
    mensaje.attach(MIMEText(cuerpo_html, 'html'))

    try:
        # Configuración del servidor SMTP
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remitente, "svzl qmtt qkiz bsav")  # Cambia por la contraseña correcta o utiliza un "App Password"
        texto = mensaje.as_string()
        servidor.sendmail(remitente, destinatario, texto)
        servidor.quit()
        return True
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return False

# Generar lista de códigos aleatorios
def generar_codigos():
    return [random.randint(100000, 999999) for _ in range(20)]

# Función para verificar el código ingresado
def verificar_codigo(email, codigo_ingresado, codigos_enviados, nombre_usuario, usuario_id):
    if int(codigo_ingresado) in codigos_enviados:
        messagebox.showinfo("Verificación exitosa", "Código correcto. Verificación completada.")
        ventana_verificacion.destroy()  

        # Aquí se debería redirigir al menú correctamente, pasando el usuario_id
        # Llamamos a la función main() del archivo menu.py y pasamos el usuario_id
        menu.main(usuario_id)  # Asegúrate de que esta función esté preparada para recibir usuario_id

        return True  
    else:
        messagebox.showerror("Error", "Código incorrecto. Por favor, inténtalo de nuevo.")
        return False  

# Función para manejar el cambio de foco entre campos
def cambiar_foco(event, siguiente_entrada):
    if len(event.widget.get()) == 1:
        siguiente_entrada.focus_set()

# Función para iniciar la verificación
def iniciar_verificacion(email_usuario, nombre_usuario, usuario_id):
    global ventana_verificacion
    ventana_verificacion = tk.Tk()
    ventana_verificacion.title("Verificación")
    ventana_verificacion.geometry("400x350")
    ventana_verificacion.config(bg="#2b2b2b")

    # Generar y enviar código
    codigos_enviados = generar_codigos()
    codigo = random.choice(codigos_enviados)
    enviar_codigo_email(email_usuario, codigo)

    # Título de la ventana
    label_titulo = tk.Label(ventana_verificacion, text="Verificación de correo", font=("Poppins", 18), fg="white", bg="#2b2b2b")
    label_titulo.pack(pady=20)

    # Instrucciones
    label_instrucciones = tk.Label(ventana_verificacion, text="Ingresa el código enviado a tu correo:", bg="#2b2b2b", fg="white", font=("Poppins", 12))
    label_instrucciones.pack(pady=10)

    # Entrada del código de verificación
    entrada_codigo = tk.Entry(ventana_verificacion, font=("Poppins", 14), width=25, justify="center", fg="white", bg="#333333", insertbackground="white")
    entrada_codigo.pack(pady=10)

    # Agregar máscara de separación de números en el código
    def validar_input(event):
        texto = entrada_codigo.get()
        # Asegurarse de que solo se ingresen números
        entrada_codigo.delete(0, tk.END)
        # Formatear la entrada con un espacio cada 3 caracteres
        entrada_codigo.insert(0, " ".join([texto[i:i+3] for i in range(0, len(texto), 3)]))
    
    # Asociar el evento de tecla para dar formato en tiempo real
    entrada_codigo.bind("<KeyRelease>", validar_input)

    # Botón de verificar código
    boton_verificar = tk.Button(ventana_verificacion, text="Verificar", font=("Poppins", 12), bg="#4CAF50", fg="white", width=20,
                                 command=lambda: verificar_codigo(email_usuario, entrada_codigo.get().replace(" ", ""), codigos_enviados, nombre_usuario, usuario_id))
    boton_verificar.pack(pady=20)

    # Configurar el evento de cambio de foco
    entrada_codigo.bind("<KeyRelease>", lambda e: cambiar_foco(e, boton_verificar))

    # Centramos la ventana
    def centrar_ventana():
        screen_width = ventana_verificacion.winfo_screenwidth()
        screen_height = ventana_verificacion.winfo_screenheight()
        x = int((screen_width / 2) - (ventana_verificacion.winfo_width() / 2))
        y = int((screen_height / 2) - (ventana_verificacion.winfo_height() / 2))
        ventana_verificacion.geometry(f'{ventana_verificacion.winfo_width()}x{ventana_verificacion.winfo_height()}+{x}+{y}')
    
    ventana_verificacion.after(100, centrar_ventana)

    ventana_verificacion.mainloop()
