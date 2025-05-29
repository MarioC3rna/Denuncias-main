"""
Clasificador simplificado que mantiene funcionalidad pero reduce complejidad.
"""

from .base import AgenteIABase, UtilsTexto
from typing import Dict, List, Any
import re

class ClasificadorSimplificado(AgenteIABase):
    """Clasificador de denuncias simplificado pero efectivo."""
    
    def __init__(self):
        super().__init__()
        self.categorias = {
            'acoso': {
                'palabras_clave': ['acoso', 'hostigamiento', 'molesta', 'incomoda', 'persigue', 'insulta'],
                'patrones': [r'me\s+acosa', r'hostigamiento', r'comportamiento\s+inadecuado'],
                'peso': 1.0
            },
            'discriminacion': {
                'palabras_clave': ['discrimina', 'raza', 'genero', 'religion', 'edad', 'discapacidad'],
                'patrones': [r'por\s+ser\s+\w+', r'discrimina', r'trata\s+diferente'],
                'peso': 1.0
            },
            'corrupcion': {
                'palabras_clave': ['dinero', 'soborno', 'pago', 'beneficio', 'favor', 'trampa'],
                'patrones': [r'pide\s+dinero', r'soborno', r'corrupcion'],
                'peso': 1.0
            },
            'problemas_tecnicos': {
                'palabras_clave': ['sistema', 'error', 'falla', 'problema', 'tecnico', 'computadora'],
                'patrones': [r'no\s+funciona', r'error\s+de', r'falla\s+el'],
                'peso': 0.8
            },
            'otros': {
                'palabras_clave': ['otro', 'diferente', 'varios', 'general'],
                'patrones': [r'otros?', r'general'],
                'peso': 0.5
            }
        }
        self.configurado = True
    
    def clasificar_denuncia(self, mensaje: str) -> Dict[str, Any]:
        """Clasifica una denuncia de manera simplificada pero efectiva."""
        if not mensaje:
            return self._resultado_clasificacion_vacio()
        
        texto_limpio = UtilsTexto.limpiar_texto(mensaje)
        texto_lower = texto_limpio.lower()
        
        # Calcular puntuaciones por categoría
        puntuaciones = {}
        
        for categoria, config in self.categorias.items():
            puntuacion = 0.0
            
            # Puntuación por palabras clave
            for palabra in config['palabras_clave']:
                if palabra in texto_lower:
                    puntuacion += 0.1
            
            # Puntuación por patrones
            for patron in config['patrones']:
                if re.search(patron, texto_lower):
                    puntuacion += 0.2
            
            # Aplicar peso de categoría
            puntuaciones[categoria] = puntuacion * config['peso']
        
        # Encontrar mejor categoría
        if not puntuaciones or max(puntuaciones.values()) == 0:
            categoria_final = 'otros'
            confianza = 0.3
        else:
            categoria_final = max(puntuaciones, key=puntuaciones.get)
            confianza = min(0.95, max(0.1, puntuaciones[categoria_final]))
        
        return {
            'categoria': categoria_final,
            'confianza': confianza,
            'puntuaciones_todas': puntuaciones,
            'palabras_clave_encontradas': UtilsTexto.extraer_palabras_clave(texto_limpio),
            'metodo': 'clasificacion_simplificada',
            'timestamp': self._obtener_timestamp()
        }
    
    def analizar_veracidad(self, mensaje: str) -> Dict[str, Any]:
        """Análisis simplificado de veracidad."""
        if not mensaje:
            return self._resultado_veracidad_vacio()
        
        texto_limpio = UtilsTexto.limpiar_texto(mensaje)
        
        # Factores de veracidad simplificados
        factores = {}
        
        # Longitud del mensaje
        longitud = len(texto_limpio.split())
        if longitud < 5:
            factores['longitud'] = 0.2
        elif longitud > 50:
            factores['longitud'] = 0.9
        else:
            factores['longitud'] = 0.5 + (longitud / 100)
        
        # Especificidad (fechas, nombres, lugares)
        especificidad = 0.5
        if re.search(r'\d{1,2}/\d{1,2}/\d{4}', mensaje):  # Fechas
            especificidad += 0.2
        if re.search(r'[A-Z][a-z]+\s+[A-Z][a-z]+', mensaje):  # Nombres propios
            especificidad += 0.15
        if re.search(r'en\s+[A-Z][a-z]+', mensaje):  # Lugares
            especificidad += 0.1
        
        factores['especificidad'] = min(1.0, especificidad)
        
        # Coherencia (sin análisis complejo)
        factores['coherencia'] = 0.7  # Asumimos coherencia media por defecto
        
        # Calcular veracidad final
        confianza_veracidad = UtilsTexto.calcular_confianza_basica(factores)
        
        # Determinar nivel
        if confianza_veracidad >= 0.7:
            nivel = 'ALTA'
        elif confianza_veracidad >= 0.4:
            nivel = 'MEDIA'
        else:
            nivel = 'BAJA'
        
        return {
            'nivel_veracidad': nivel,
            'confianza': confianza_veracidad,
            'factores_analizados': factores,
            'metodo': 'analisis_simplificado',
            'timestamp': self._obtener_timestamp()
        }
    
    def _resultado_clasificacion_vacio(self) -> Dict[str, Any]:
        """Resultado para clasificación de mensaje vacío."""
        return {
            'categoria': 'otros',
            'confianza': 0.1,
            'puntuaciones_todas': {},
            'palabras_clave_encontradas': [],
            'metodo': 'clasificacion_simplificada',
            'timestamp': self._obtener_timestamp()
        }
    
    def _resultado_veracidad_vacio(self) -> Dict[str, Any]:
        """Resultado para análisis de veracidad de mensaje vacío."""
        return {
            'nivel_veracidad': 'BAJA',
            'confianza': 0.1,
            'factores_analizados': {},
            'metodo': 'analisis_simplificado',
            'timestamp': self._obtener_timestamp()
        }
    
    def _obtener_timestamp(self) -> str:
        """Obtiene timestamp actual."""
        from datetime import datetime
        return datetime.now().isoformat()
