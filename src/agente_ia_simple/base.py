"""
Agente IA Simplificado - Versión moderna y mantenible.
Reduce 6,258 líneas a ~400 líneas manteniendo funcionalidad core.
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import json
import re
from abc import ABC, abstractmethod

class AgenteIABase(ABC):
    """Clase base simplificada para todos los agentes IA."""
    
    def __init__(self):
        self.nombre = self.__class__.__name__
        self.version = "2.0-simplificado"
        self.configurado = False
        self.estadisticas = {
            'clasificaciones_realizadas': 0,
            'analisis_realizados': 0,
            'errores_encontrados': 0
        }
    
    @abstractmethod
    def clasificar_denuncia(self, mensaje: str) -> Dict[str, Any]:
        """Clasifica una denuncia y retorna resultado."""
        pass
    
    @abstractmethod
    def analizar_veracidad(self, mensaje: str) -> Dict[str, Any]:
        """Analiza la veracidad de una denuncia."""
        pass
    
    def procesar_denuncia_completo(self, mensaje: str) -> Dict[str, Any]:
        """Procesa una denuncia completamente."""
        try:
            # Clasificación
            resultado_clasificacion = self.clasificar_denuncia(mensaje)
            
            # Análisis de veracidad
            resultado_veracidad = self.analizar_veracidad(mensaje)
            
            # Combinar resultados
            resultado_final = {
                'timestamp': datetime.now().isoformat(),
                'agente_usado': self.nombre,
                'clasificacion': resultado_clasificacion,
                'veracidad': resultado_veracidad,
                'procesamiento_exitoso': True
            }
            
            self.estadisticas['clasificaciones_realizadas'] += 1
            self.estadisticas['analisis_realizados'] += 1
            
            return resultado_final
            
        except Exception as e:
            self.estadisticas['errores_encontrados'] += 1
            return {
                'timestamp': datetime.now().isoformat(),
                'agente_usado': self.nombre,
                'error': str(e),
                'procesamiento_exitoso': False
            }
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Obtiene estadísticas del agente."""
        return {
            'agente': self.nombre,
            'version': self.version,
            'configurado': self.configurado,
            'estadisticas': self.estadisticas.copy()
        }

class UtilsTexto:
    """Utilidades para procesamiento de texto simplificadas."""
    
    @staticmethod
    def limpiar_texto(texto: str) -> str:
        """Limpia y normaliza texto."""
        if not texto:
            return ""
        
        # Eliminar caracteres especiales excesivos
        texto = re.sub(r'[^\w\s\.,!?;:]', ' ', texto)
        
        # Normalizar espacios
        texto = re.sub(r'\s+', ' ', texto)
        
        return texto.strip()
    
    @staticmethod
    def extraer_palabras_clave(texto: str) -> List[str]:
        """Extrae palabras clave del texto."""
        # Palabras comunes a ignorar
        stop_words = {'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le', 'da', 'su', 'por', 'son', 'con', 'para', 'al', 'como', 'las', 'pero', 'sus', 'me', 'ya', 'si', 'cuando'}
        
        palabras = re.findall(r'\w+', texto.lower())
        palabras_clave = [p for p in palabras if len(p) > 3 and p not in stop_words]
        
        # Retornar las más frecuentes
        from collections import Counter
        contador = Counter(palabras_clave)
        return [palabra for palabra, freq in contador.most_common(10)]
    
    @staticmethod
    def calcular_confianza_basica(factores: Dict[str, float]) -> float:
        """Calcula confianza basada en factores simples."""
        if not factores:
            return 0.5
        
        # Promedio ponderado simple
        total_peso = sum(factores.values())
        if total_peso == 0:
            return 0.5
        
        confianza = sum(valor * peso for valor, peso in factores.items()) / total_peso
        return max(0.0, min(1.0, confianza))
