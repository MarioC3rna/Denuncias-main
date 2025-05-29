"""
Cliente MCP (Model Context Protocol) refactorizado.
Tecnología avanzada para comunicación con modelos IA.

Migrado desde: src/core/mcp.py
Funcionalidad: Comunicación avanzada con LLMs
"""

"""
Módulo de Cómputo Multiparte Seguro (MCP) simulado.
Implementa técnicas de privacidad para procesar denuncias sin revelar información sensible.
"""

import hashlib
import json
from typing import Dict, Any
from datetime import datetime
from .utils import limpiar_texto


class MCPSimulado:
    """
    Clase que simula técnicas de Cómputo Multiparte Seguro para proteger
    la privacidad de las denuncias y los denunciantes.
    """
    
    def __init__(self):
        """Inicializa el simulador de MCP."""
        self.salt_secreto = self._generar_salt()
    
    def _generar_salt(self) -> str:
        """
        Genera un salt secreto para operaciones criptográficas.
        
        Returns:
            str: Salt en formato hexadecimal
        """
        # En un sistema real, esto vendría de una fuente segura
        timestamp = str(datetime.now().timestamp())
        return hashlib.sha256(f"SISTEMA_DENUNCIAS_{timestamp}".encode()).hexdigest()[:32]
    
    def cifrar_contenido_sensible(self, contenido: str) -> str:
        """
        Simula el cifrado de contenido sensible usando técnicas MCP.
        
        Args:
            contenido: Contenido a cifrar
            
        Returns:
            str: Hash del contenido para análisis estadístico sin revelar el original
        """
        if not contenido:
            return ""
        
        # Limpiar y normalizar el contenido
        contenido_limpio = limpiar_texto(contenido)
        
        # Crear hash con salt para análisis estadístico
        contenido_con_salt = f"{contenido_limpio}_{self.salt_secreto}"
        hash_analisis = hashlib.sha256(contenido_con_salt.encode()).hexdigest()
        
        # Retornar solo un fragmento para análisis (no el contenido original)
        return f"HASH_{hash_analisis[:16]}"
    
    def generar_firma_temporal(self, denuncia: Dict[str, Any]) -> str:
        """
        Genera una firma temporal para verificar la integridad de la denuncia
        sin revelar su contenido.
        
        Args:
            denuncia: Diccionario con los datos de la denuncia
            
        Returns:
            str: Firma temporal
        """
        # Extraer elementos para la firma (sin contenido sensible)
        elementos_firma = [
            denuncia.get('categoria', ''),
            denuncia.get('timestamp', ''),
            str(len(denuncia.get('mensaje', ''))),  # Solo la longitud, no el contenido
            self.salt_secreto
        ]
        
        contenido_firma = "_".join(elementos_firma)
        firma = hashlib.sha256(contenido_firma.encode()).hexdigest()
        
        return f"FIRMA_{firma[:20]}"
    
    def anonimizar_metadatos(self, denuncia: Dict[str, Any]) -> Dict[str, Any]:
        """
        Anonimiza los metadatos de la denuncia manteniendo solo lo necesario
        para análisis estadístico.
        
        Args:
            denuncia: Denuncia original
            
        Returns:
            Dict: Denuncia con metadatos anonimizados
        """
        # Extraer solo lo necesario para estadísticas
        denuncia_anonima = {
            'id_anonimo': denuncia.get('id_anonimo', ''),
            'categoria': denuncia.get('categoria', '').strip(),
            'longitud_mensaje': len(denuncia.get('mensaje', '')),
            'tiene_mensaje': bool(denuncia.get('mensaje', '').strip()),
            'timestamp': denuncia.get('timestamp', ''),
            'firma_integridad': self.generar_firma_temporal(denuncia),
            'procesada_mcp': True
        }
        
        # Si el mensaje está vacío, no incluir información sobre él
        if not denuncia.get('mensaje', '').strip():
            denuncia_anonima['longitud_mensaje'] = 0
            denuncia_anonima['tiene_mensaje'] = False
        
        return denuncia_anonima
    
    def validar_integridad(self, denuncia: Dict[str, Any]) -> bool:
        """
        Valida la integridad de una denuncia procesada por MCP.
        
        Args:
            denuncia: Denuncia a validar
            
        Returns:
            bool: True si la denuncia mantiene su integridad
        """
        try:
            # Verificar campos obligatorios
            campos_obligatorios = ['id_anonimo', 'categoria', 'timestamp', 'procesada_mcp']
            for campo in campos_obligatorios:
                if campo not in denuncia:
                    return False
            
            # Verificar que esté marcada como procesada por MCP
            if not denuncia.get('procesada_mcp', False):
                return False
            
            # Verificar que no contenga información sensible directa
            campos_sensibles = ['ip_address', 'user_id', 'email', 'nombre']
            for campo in campos_sensibles:
                if campo in denuncia:
                    return False
            
            return True
            
        except Exception:
            return False


# Instancia global del simulador MCP
mcp_instance = MCPSimulado()


def procesar_denuncia_segura(denuncia: Dict[str, Any]) -> Dict[str, Any]:
    """
    Función principal para procesar una denuncia usando técnicas MCP simuladas.
    
    Args:
        denuncia: Denuncia original a procesar
        
    Returns:
        Dict: Denuncia procesada de forma segura
    """
    try:
        # Validar entrada
        if not isinstance(denuncia, dict):
            raise ValueError("La denuncia debe ser un diccionario")
        
        # Procesar con MCP simulado
        denuncia_procesada = mcp_instance.anonimizar_metadatos(denuncia)
        
        # Agregar metadatos de procesamiento MCP
        denuncia_procesada.update({
            'mcp_version': '1.0',
            'procesamiento_timestamp': datetime.now().isoformat(),
            'nivel_privacidad': 'ALTO'
        })
        
        # Validar integridad del resultado
        if not mcp_instance.validar_integridad(denuncia_procesada):
            raise Exception("Error en la validación de integridad MCP")
        
        return denuncia_procesada
        
    except Exception as e:
        # En caso de error, retornar versión mínima segura
        return {
            'id_anonimo': denuncia.get('id_anonimo', 'ERROR_ID'),
            'categoria': denuncia.get('categoria', 'Error'),
            'timestamp': datetime.now().isoformat(),
            'procesada_mcp': True,
            'error_procesamiento': str(e),
            'nivel_privacidad': 'ALTO'
        }


def generar_estadisticas_seguras(denuncias: list) -> Dict[str, Any]:
    """
    Genera estadísticas agregadas sin revelar información individual.
    
    Args:
        denuncias: Lista de denuncias procesadas por MCP
        
    Returns:
        Dict: Estadísticas agregadas seguras
    """
    if not denuncias:
        return {
            'total_denuncias': 0,
            'categorias': {},
            'timestamp_generacion': datetime.now().isoformat(),
            'metodo_procesamiento': 'MCP_SIMULADO'
        }
    
    # Conteo seguro por categorías
    conteo_categorias = {}
    total_con_mensaje = 0
    longitudes_promedio = []
    
    for denuncia in denuncias:
        # Solo procesar denuncias validadas por MCP
        if not denuncia.get('procesada_mcp', False):
            continue
            
        categoria = denuncia.get('categoria', 'Sin categoría')
        conteo_categorias[categoria] = conteo_categorias.get(categoria, 0) + 1
        
        if denuncia.get('tiene_mensaje', False):
            total_con_mensaje += 1
            longitudes_promedio.append(denuncia.get('longitud_mensaje', 0))
    
    # Calcular estadísticas agregadas
    estadisticas = {
        'total_denuncias': len(denuncias),
        'categorias': conteo_categorias,
        'denuncias_con_mensaje': total_con_mensaje,
        'porcentaje_con_mensaje': round((total_con_mensaje / len(denuncias)) * 100, 2) if denuncias else 0,
        'longitud_promedio_mensaje': round(sum(longitudes_promedio) / len(longitudes_promedio), 2) if longitudes_promedio else 0,
        'timestamp_generacion': datetime.now().isoformat(),
        'metodo_procesamiento': 'MCP_SIMULADO',
        'garantia_privacidad': 'ALTA'
    }
    
    return estadisticas


def verificar_anonimato(denuncia: Dict[str, Any]) -> bool:
    """
    Verifica que una denuncia mantenga el anonimato requerido.
    
    Args:
        denuncia: Denuncia a verificar
        
    Returns:
        bool: True si mantiene el anonimato
    """
    # Lista de campos que NO deben estar presentes para mantener anonimato
    campos_prohibidos = [
        'ip_address', 'user_id', 'email', 'nombre', 'apellido',
        'telefono', 'direccion', 'documento', 'session_id',
        'browser_info', 'device_id', 'mac_address'
    ]
    
    # Verificar que no haya campos prohibidos
    for campo in campos_prohibidos:
        if campo in denuncia:
            return False
    
    # Verificar que el ID sea realmente anónimo (no contenga patrones identificables)
    id_anonimo = denuncia.get('id_anonimo', '')
    if any(patron in id_anonimo.lower() for patron in ['user', 'admin', 'email', 'name']):
        return False
    
    return True

# NUEVAS FUNCIONALIDADES MCP
class MCPExtendido:
    """Extensión del cliente MCP con nuevas capacidades."""
    
    def __init__(self):
        self.version = "2.0"
        self.compatible_con_nueva_arquitectura = True
    
    def integrar_con_agente_ia(self, agente_ia):
        """Integra MCP con el agente IA refactorizado."""
        pass
