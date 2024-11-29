from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

# Función para generar una clave secreta de 256 bits
def generar_clave():
    return os.urandom(32)  # 32 bytes = 256 bits

# Función para cifrar contraseñas
def cifrar_contrasena(contrasena, clave_secreta):
    iv = os.urandom(16)  # Vector de inicialización
    cipher = Cipher(algorithms.AES(clave_secreta), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Padding para que el tamaño sea múltiplo de 16
    padding_length = 16 - len(contrasena) % 16
    contrasena_padded = contrasena + chr(padding_length) * padding_length

    contrasena_cifrada = encryptor.update(contrasena_padded.encode()) + encryptor.finalize()
    return base64.b64encode(iv + contrasena_cifrada).decode()

# Función para descifrar contraseñas
def descifrar_contrasena(contrasena_cifrada, clave_secreta):
    data = base64.b64decode(contrasena_cifrada)
    iv = data[:16]  # Primeros 16 bytes son el IV
    contrasena_cifrada = data[16:]  # Resto es la contraseña cifrada

    cipher = Cipher(algorithms.AES(clave_secreta), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    contrasena_descifrada = decryptor.update(contrasena_cifrada) + decryptor.finalize()

    # Eliminar padding
    padding_length = ord(contrasena_descifrada[-1])
    return contrasena_descifrada[:-padding_length].decode()
