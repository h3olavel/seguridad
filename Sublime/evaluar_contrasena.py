import tkinter as tk
from tkinter import messagebox, ttk
from password_strength import PasswordStats
import zxcvbn
import re

class EvaluadorContrasenasApp:
    def __init__(self, frame_principal, contrasena, usuario_id=None):
        """
        Inicializa la vista de evaluación de contraseñas.
        
        Args:
            frame_principal (tk.Frame): Frame donde se mostrará la vista.
            contrasena (str): Contraseña a evaluar.
            usuario_id (int, optional): ID del usuario actual.
        """
        self.frame_principal = frame_principal
        self.usuario_id = usuario_id
        
        # Limpiar el frame
        for widget in self.frame_principal.winfo_children():
            widget.destroy()
        
        # Configurar fondo
        self.frame_principal.config(bg="#2A2A2B")
        
        self.mostrar_resultados(contrasena)
    
    def mostrar_resultados(self, contrasena):
        """
        Muestra los resultados de la evaluación de contraseña.
        
        Args:
            contrasena (str): Contraseña a evaluar.
        """
        if not contrasena:
            messagebox.showwarning("Advertencia", "Por favor, ingrese una contraseña.")
            return
        
        resultado = self._analizar_contrasena(contrasena)
        
        # Mostrar resultados
        tk.Label(
            self.frame_principal, 
            text="Resultado de Evaluación", 
            font=("Arial", 16), 
            bg="#2A2A2B", 
            fg="white"
        ).pack(pady=(20, 10))
        
        marco_resultados = tk.Frame(self.frame_principal, bg="#333232", padx=20, pady=20)
        marco_resultados.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)
        
        # Contraseña ingresada
        tk.Label(
            marco_resultados, 
            text=f"Contraseña: {contrasena}", 
            font=("Arial", 12), 
            bg="#333232", 
            fg="white"
        ).pack(pady=(10, 5))
        
        # Fortaleza
        tk.Label(
            marco_resultados, 
            text=f"Fortaleza: {resultado['estado']}", 
            font=("Arial", 14, "bold"), 
            bg="#333232", 
            fg="white"
        ).pack(pady=(10, 5))
        
        # Puntuación
        tk.Label(
            marco_resultados, 
            text=f"Puntuación: {resultado['puntuacion']}%", 
            font=("Arial", 12), 
            bg="#333232", 
            fg="white"
        ).pack(pady=(0, 5))
        
        # Consejos
        tk.Label(
            marco_resultados, 
            text="Consejos para mejorar:", 
            font=("Arial", 12, "bold"), 
            bg="#333232", 
            fg="yellow"
        ).pack(pady=(10, 5))
        
        for consejo in resultado['feedback']:
            tk.Label(
                marco_resultados, 
                text=f"• {consejo}", 
                font=("Arial", 10), 
                bg="#333232", 
                fg="white", 
                wraplength=400, 
                justify=tk.LEFT
            ).pack(anchor="w", padx=20)
        
        # Botón de cerrar
        boton_cerrar = tk.Button(
            self.frame_principal, 
            text="Cerrar", 
            command=self.cerrar_ventana,
            font=("Arial", 12),
            bg="#FF6347",
            fg="white"
        )
        boton_cerrar.pack(pady=20)
    
    def cerrar_ventana(self):
        """
        Cierra la ventana actual.
        """
        for widget in self.frame_principal.winfo_children():
            widget.destroy()
    
    def _analizar_contrasena(self, contrasena):
        """
        Analiza la fortaleza de la contraseña.
        
        Args:
            contrasena (str): Contraseña a evaluar.
        
        Returns:
            Dict: Resultados del análisis de contraseña.
        """
        # Evaluar con password_strength
        stats = PasswordStats(contrasena)
        puntuacion_ps = round(stats.strength() * 100)
        
        # Evaluar con zxcvbn
        resultado_zxcvbn = zxcvbn.zxcvbn(contrasena)
        puntuacion_zxcvbn = resultado_zxcvbn['score'] * 25
        
        # Combinar puntuaciones
        puntuacion_final = (puntuacion_ps + puntuacion_zxcvbn) / 2
        
        # Determinar estado
        estado = (
            "Muy Débil" if puntuacion_final < 30 else
            "Débil" if puntuacion_final < 50 else
            "Moderada" if puntuacion_final < 70 else
            "Fuerte" if puntuacion_final < 90 else
            "Muy Fuerte"
        )
        
        # Generar feedback detallado
        feedback = self._generar_feedback(contrasena, stats)
        
        return {
            "puntuacion": round(puntuacion_final),
            "estado": estado,
            "feedback": feedback
        }
    
    def _generar_feedback(self, contrasena, stats):
        """
        Genera consejos para mejorar la contraseña.
        
        Args:
            contrasena (str): Contraseña a evaluar.
            stats (PasswordStats): Estadísticas de la contraseña.
        
        Returns:
            List[str]: Lista de consejos.
        """
        feedback = []
        
        if len(contrasena) < 12:
            feedback.append("Usa al menos 12 caracteres para mayor seguridad.")
        
        if not re.search(r'[A-Z]', contrasena):
            feedback.append("Incluye al menos una letra mayúscula.")
        
        if not re.search(r'[a-z]', contrasena):
            feedback.append("Incluye letras minúsculas.")
        
        if not re.search(r'\d', contrasena):
            feedback.append("Añade números para aumentar la complejidad.")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', contrasena):
            feedback.append("Usa caracteres especiales como !@#$%.")
        
        if stats.repeated_patterns_length > 0:
            feedback.append("Evita usar patrones repetitivos.")
        
        return feedback if feedback else ["¡Tu contraseña es bastante segura!"]

def mostrar_resultado(frame_principal, contrasena, usuario_id=None):
    """
    Función para ser llamada desde el menú principal.
    
    Args:
        frame_principal (tk.Frame): Frame donde se mostrará la vista.
        contrasena (str): Contraseña a evaluar.
        usuario_id (int, optional): ID del usuario actual.
    """
    EvaluadorContrasenasApp(frame_principal, contrasena, usuario_id)