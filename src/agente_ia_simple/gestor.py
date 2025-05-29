"""
Gestor principal del agente IA simplificado.
Coordina todos los componentes de manera sencilla.
"""

from .clasificador import ClasificadorSimplificado
from .agente_openai import AgenteOpenAISimplificado
from typing import Dict, Any, Optional

class GestorAgenteIASimplificado:
    """Gestor principal simplificado del agente IA."""
    
    def __init__(self, api_key_openai: Optional[str] = None):
        self.api_key_openai = api_key_openai
        self.agente_local = ClasificadorSimplificado()
        self.agente_openai = AgenteOpenAISimplificado(api_key_openai) if api_key_openai else None
        self.modo = 'hibrido' if self.agente_openai else 'local'
        self.configurado = True
        
        print(f"🤖 Gestor IA inicializado en modo: {self.modo}")
    
    def procesar_denuncia(self, mensaje: str, forzar_modo: Optional[str] = None) -> Dict[str, Any]:
        """
        Procesa una denuncia usando el mejor agente disponible.
        
        Args:
            mensaje: Texto de la denuncia
            forzar_modo: 'local', 'openai' o None para automático
            
        Returns:
            Resultado del procesamiento
        """
        if not mensaje or not mensaje.strip():
            return self._resultado_mensaje_vacio()
        
        # Determinar agente a usar
        if forzar_modo == 'local' or not self.agente_openai:
            agente = self.agente_local
            modo_usado = 'local'
        elif forzar_modo == 'openai' and self.agente_openai:
            agente = self.agente_openai
            modo_usado = 'openai'
        else:
            # Modo híbrido: usar OpenAI para mensajes complejos, local para simples
            if len(mensaje.split()) > 20:  # Mensaje complejo
                agente = self.agente_openai if self.agente_openai else self.agente_local
                modo_usado = 'openai_complejo' if self.agente_openai else 'local_fallback'
            else:
                agente = self.agente_local
                modo_usado = 'local_simple'
        
        # Procesar con el agente seleccionado
        try:
            resultado = agente.procesar_denuncia_completo(mensaje)
            resultado['modo_procesamiento'] = modo_usado
            resultado['gestor_version'] = 'simplificado_v2.0'
            return resultado
            
        except Exception as e:
            return {
                'error': str(e),
                'modo_procesamiento': f'{modo_usado}_error',
                'procesamiento_exitoso': False,
                'timestamp': self._obtener_timestamp()
            }
    
    def obtener_estadisticas_completas(self) -> Dict[str, Any]:
        """Obtiene estadísticas de todos los agentes."""
        stats = {
            'gestor_version': 'simplificado_v2.0',
            'modo_configurado': self.modo,
            'agentes_disponibles': ['local'],
            'estadisticas_local': self.agente_local.obtener_estadisticas()
        }
        
        if self.agente_openai:
            stats['agentes_disponibles'].append('openai')
            stats['estadisticas_openai'] = self.agente_openai.obtener_estadisticas()
        
        return stats
    
    def cambiar_modo(self, nuevo_modo: str) -> bool:
        """Cambia el modo de operación."""
        if nuevo_modo == 'local':
            self.modo = 'local'
            return True
        elif nuevo_modo == 'openai' and self.agente_openai:
            self.modo = 'openai'
            return True
        elif nuevo_modo == 'hibrido' and self.agente_openai:
            self.modo = 'hibrido'
            return True
        else:
            print(f"❌ No se puede cambiar a modo: {nuevo_modo}")
            return False
    
    def configurar_openai(self, api_key: str) -> bool:
        """Configura OpenAI con nueva API key."""
        try:
            self.agente_openai = AgenteOpenAISimplificado(api_key)
            self.api_key_openai = api_key
            self.modo = 'hibrido'
            print("✅ OpenAI configurado correctamente")
            return True
        except Exception as e:
            print(f"❌ Error configurando OpenAI: {e}")
            return False
    
    def _resultado_mensaje_vacio(self) -> Dict[str, Any]:
        """Resultado para mensaje vacío."""
        return {
            'error': 'Mensaje vacío',
            'procesamiento_exitoso': False,
            'modo_procesamiento': 'validacion',
            'timestamp': self._obtener_timestamp()
        }
    
    def _obtener_timestamp(self) -> str:
        """Obtiene timestamp actual."""
        from datetime import datetime
        return datetime.now().isoformat()

# Factory simplificado
def crear_agente_ia(api_key_openai: Optional[str] = None) -> GestorAgenteIASimplificado:
    """Factory function para crear agente IA."""
    return GestorAgenteIASimplificado(api_key_openai)
