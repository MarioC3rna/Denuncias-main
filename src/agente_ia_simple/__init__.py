"""
Agente IA Simplificado para Sistema de Denuncias.
Versión optimizada con funcionalidad completa en pocas líneas.
"""

from typing import Optional, Dict, Any
from .gestor import GestorAgenteIASimplificado

def crear_agente_ia(api_key_openai: Optional[str] = None) -> GestorAgenteIASimplificado:
    """
    Función factory para crear instancia del agente IA simplificado.
    
    Args:
        api_key_openai: API key opcional para OpenAI
        
    Returns:
        Instancia del gestor de agente IA
    """
    return GestorAgenteIASimplificado(api_key_openai)

# Configuración del módulo
__version__ = "1.0.0"
__author__ = "Sistema de Denuncias"

__all__ = [
    'crear_agente_ia',
    'GestorAgenteIASimplificado'
]
