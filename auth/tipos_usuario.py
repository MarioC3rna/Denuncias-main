"""
Tipos de usuario y sistema de permisos.
"""

from enum import Enum
from typing import Dict
from dataclasses import dataclass

class TipoUsuario(Enum):
    """Tipos de usuario del sistema."""
    ANONIMO = "anonimo"
    ADMINISTRADOR = "administrador"

@dataclass
class Permisos:
    """Permisos de un usuario."""
    enviar_denuncia: bool = True
    ver_estadisticas: bool = False
    generar_reportes: bool = False
    configurar_sistema: bool = False
    gestionar_agente_ia: bool = False
    acceso_completo: bool = False
    cambiar_credenciales: bool = False
    
    def tiene_permiso(self, permiso: str) -> bool:
        """Verifica si tiene un permiso específico."""
        return getattr(self, permiso, False)
    
    @classmethod
    def crear_permisos_administrador(cls) -> 'Permisos':
        """Crea permisos completos para administrador."""
        return cls(
            enviar_denuncia=True,
            ver_estadisticas=True,
            generar_reportes=True,
            configurar_sistema=True,
            gestionar_agente_ia=True,
            acceso_completo=True,
            cambiar_credenciales=True
        )
    
    @classmethod
    def crear_permisos_anonimo(cls) -> 'Permisos':
        """Crea permisos básicos para usuario anónimo."""
        return cls(
            enviar_denuncia=True,
            ver_estadisticas=False,
            generar_reportes=False,
            configurar_sistema=False,
            gestionar_agente_ia=False,
            acceso_completo=False,
            cambiar_credenciales=False
        )

class GestorPermisos:
    """Gestiona los permisos según el tipo de usuario."""
    
    @staticmethod
    def obtener_permisos(tipo_usuario: TipoUsuario) -> Permisos:
        """Obtiene los permisos según el tipo de usuario."""
        if tipo_usuario == TipoUsuario.ADMINISTRADOR:
            return Permisos.crear_permisos_administrador()
        else:
            return Permisos.crear_permisos_anonimo()
    
    @staticmethod
    def verificar_acceso(tipo_usuario: TipoUsuario, permiso_requerido: str) -> bool:
        """Verifica si un tipo de usuario puede acceder a una funcionalidad."""
        permisos = GestorPermisos.obtener_permisos(tipo_usuario)
        return permisos.tiene_permiso(permiso_requerido)
    
    @staticmethod
    def obtener_descripcion_permisos(tipo_usuario: TipoUsuario) -> Dict[str, str]:
        """Obtiene una descripción legible de los permisos."""
        permisos = GestorPermisos.obtener_permisos(tipo_usuario)
        
        if tipo_usuario == TipoUsuario.ADMINISTRADOR:
            return {
                'tipo': 'Administrador',
                'descripcion': 'Acceso completo al sistema',
                'funcionalidades': [
                    '✅ Enviar denuncias',
                    '✅ Ver estadísticas',
                    '✅ Generar reportes',
                    '✅ Configurar sistema',
                    '✅ Gestionar Agente IA',
                    '✅ Cambiar credenciales'
                ]
            }
        else:
            return {
                'tipo': 'Usuario Anónimo',
                'descripcion': 'Acceso básico con privacidad garantizada',
                'funcionalidades': [
                    '✅ Enviar denuncias anónimas',
                    '❌ Ver estadísticas',
                    '❌ Generar reportes',
                    '❌ Configurar sistema',
                    '❌ Gestionar Agente IA',
                    '❌ Cambiar credenciales'
                ]
            }