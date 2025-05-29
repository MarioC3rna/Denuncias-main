"""
Gestor de roles y autenticación para el Sistema de Denuncias.
"""

import hashlib
import os
from typing import Optional, Dict
from enum import Enum

class TipoUsuario(Enum):
    """Tipos de usuario del sistema."""
    ANONIMO = "anonimo"
    ADMINISTRADOR = "administrador"

class GestorRoles:
    """
    Gestiona la autenticación y permisos de usuarios.
    """
    
    def __init__(self):
        """Inicializa el gestor de roles."""
        # Credenciales por defecto (cambiar en producción)
        self.credenciales_admin = {
            "usuario": "admin",
            "password_hash": self._generar_hash("admin123")  # Cambiar esta contraseña
        }
        
        # Estado de sesión actual
        self.usuario_actual = TipoUsuario.ANONIMO
        self.sesion_activa = False
        
        # Configuración
        self.intentos_maximos = 3
        self.intentos_fallidos = 0
    
    def _generar_hash(self, password: str) -> str:
        """Genera hash seguro de la contraseña."""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def autenticar_administrador(self) -> bool:
        """
        Autentica al administrador.
        
        Returns:
            bool: True si la autenticación es exitosa
        """
        print("\n👨‍💼 ACCESO DE ADMINISTRADOR")
        print("=" * 40)
        print("🔐 Ingresa tus credenciales de administrador")
        print("⚠️  Tienes 3 intentos máximo")
        print()
        
        for intento in range(1, self.intentos_maximos + 1):
            try:
                print(f"Intento {intento}/{self.intentos_maximos}")
                usuario = input("👤 Usuario: ").strip()
                password = input("🔑 Contraseña: ").strip()
                
                if self._verificar_credenciales(usuario, password):
                    self.usuario_actual = TipoUsuario.ADMINISTRADOR
                    self.sesion_activa = True
                    self.intentos_fallidos = 0
                    
                    print("\n✅ AUTENTICACIÓN EXITOSA")
                    print("👨‍💼 Bienvenido, Administrador")
                    print("🔓 Acceso completo al sistema activado")
                    return True
                else:
                    self.intentos_fallidos += 1
                    intentos_restantes = self.intentos_maximos - intento
                    
                    if intentos_restantes > 0:
                        print(f"❌ Credenciales incorrectas")
                        print(f"⚠️  Te quedan {intentos_restantes} intentos")
                        print()
                    else:
                        print("❌ ACCESO DENEGADO")
                        print("🔒 Máximo de intentos alcanzado")
                        print("💡 Regresando al modo anónimo...")
                        
            except KeyboardInterrupt:
                print("\n\n❌ Autenticación cancelada")
                print("🔄 Regresando al modo anónimo...")
                break
        
        return False
    
    def _verificar_credenciales(self, usuario: str, password: str) -> bool:
        """Verifica las credenciales del administrador."""
        if not usuario or not password:
            return False
        
        return (usuario == self.credenciales_admin["usuario"] and 
                self._generar_hash(password) == self.credenciales_admin["password_hash"])
    
    def cerrar_sesion(self):
        """Cierra la sesión del administrador."""
        if self.sesion_activa:
            print("\n👋 CERRANDO SESIÓN DE ADMINISTRADOR")
            print("🔄 Regresando al modo anónimo...")
            
        self.usuario_actual = TipoUsuario.ANONIMO
        self.sesion_activa = False
        self.intentos_fallidos = 0
    
    def es_administrador(self) -> bool:
        """Verifica si el usuario actual es administrador."""
        return self.usuario_actual == TipoUsuario.ADMINISTRADOR and self.sesion_activa
    
    def es_anonimo(self) -> bool:
        """Verifica si el usuario actual es anónimo."""
        return self.usuario_actual == TipoUsuario.ANONIMO
    
    def obtener_tipo_usuario(self) -> TipoUsuario:
        """Obtiene el tipo de usuario actual."""
        return self.usuario_actual
    
    def obtener_permisos(self) -> Dict[str, bool]:
        """Obtiene los permisos del usuario actual."""
        if self.es_administrador():
            return {
                "enviar_denuncia": True,
                "ver_estadisticas": True,
                "generar_reportes": True,
                "configurar_sistema": True,
                "gestionar_agente_ia": True,
                "acceso_completo": True
            }
        else:
            return {
                "enviar_denuncia": True,
                "ver_estadisticas": False,
                "generar_reportes": False,
                "configurar_sistema": False,
                "gestionar_agente_ia": False,
                "acceso_completo": False
            }
    
    def cambiar_credenciales(self, nuevo_usuario: str, nueva_password: str) -> bool:
        """
        Cambia las credenciales del administrador.
        Solo disponible para administradores autenticados.
        """
        if not self.es_administrador():
            return False
        
        if not nuevo_usuario or not nueva_password:
            return False
        
        self.credenciales_admin = {
            "usuario": nuevo_usuario,
            "password_hash": self._generar_hash(nueva_password)
        }
        
        print("✅ Credenciales actualizadas exitosamente")
        return True