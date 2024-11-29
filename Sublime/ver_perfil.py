import tkinter as tk
from PIL import Image, ImageTk
import random
from db_connection import conectar_db

def ver_perfil(frame_principal, usuario_id):
    # Conectar a la base de datos y obtener los datos del perfil
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre, email, telefono FROM usuarios WHERE id = %s", (usuario_id,))
        perfil = cursor.fetchone()
        cursor.close()
        conexion.close()

        # Destruir los widgets previos en el frame principal
        for widget in frame_principal.winfo_children():
            widget.destroy()

        # Crear el nuevo frame para mostrar el perfil
        frame_perfil = tk.Frame(frame_principal, bg="#2A2B2A")
        frame_perfil.pack(pady=20)

        # Seleccionar una foto de perfil aleatoria
        img_dir = "img_perfiles/"
        img_files = [f"{i}.png" for i in range(1, 9)]  # Asumiendo que las imágenes son .png
        current_image = random.choice(img_files)
        image_path = img_dir + current_image

        # Cargar y mostrar la foto de perfil
        def cargar_imagen(imagen_path):
            img = Image.open(imagen_path).resize((120, 120))  # Redimensionar a 120x120 píxeles
            return ImageTk.PhotoImage(img)

        photo = cargar_imagen(image_path)

        label_image = tk.Label(frame_perfil, image=photo, bg="#2A2B2A")
        label_image.image = photo  # Referencia para evitar que se elimine el objeto
        label_image.pack(pady=10, side="top")

        # Botón para cambiar la foto de perfil de forma aleatoria
        def cambiar_foto():
            nonlocal current_image
            new_image = random.choice([img for img in img_files if img != current_image])
            current_image = new_image
            new_image_path = img_dir + new_image
            new_photo = cargar_imagen(new_image_path)
            label_image.configure(image=new_photo)
            label_image.image = new_photo

        tk.Button(frame_perfil, text="Cambiar Foto", command=cambiar_foto, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)

        # Mostrar los datos del perfil debajo de la foto
        tk.Label(frame_perfil, text="Nombre: " + perfil[0], bg="#2A2B2A", fg="white", font=("Arial", 14)).pack(pady=5)
        tk.Label(frame_perfil, text="Correo: " + perfil[1], bg="#2A2B2A", fg="white", font=("Arial", 14)).pack(pady=5)
        tk.Label(frame_perfil, text="Teléfono: " + perfil[2], bg="#2A2B2A", fg="white", font=("Arial", 14)).pack(pady=5)
