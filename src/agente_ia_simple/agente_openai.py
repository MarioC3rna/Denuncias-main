"""
Agente OpenAI simplificado - mantiene funcionalidad, reduce complejidad.
"""

from .clasificador import ClasificadorSimplificado
from typing import Dict, Any, Optional
import json

class AgenteOpenAISimplificado(ClasificadorSimplificado):
    """Agente que usa OpenAI de manera simplificada."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__()
        self.api_key = api_key
        self.openai_disponible = False
        self.cliente_openai = None
        self._configurar_openai()
    
    def _configurar_openai(self):
        """Configura cliente OpenAI si está disponible."""
        try:
            import openai
            if self.api_key:
                self.cliente_openai = openai
                openai.api_key = self.api_key
                self.openai_disponible = True
                print("✅ OpenAI configurado correctamente")
            else:
                print("⚠️ OpenAI sin API key - usando clasificación local")
        except ImportError:
            print("⚠️ OpenAI no disponible - usando clasificación local")
    
    def clasificar_denuncia(self, mensaje: str) -> Dict[str, Any]:
        """Clasifica usando OpenAI si está disponible, sino usa método local."""
        if self.openai_disponible and self.cliente_openai:
            return self._clasificar_con_openai(mensaje)
        else:
            # Fallback a clasificación local
            resultado = super().clasificar_denuncia(mensaje)
            resultado['metodo'] = 'local_fallback'
            return resultado
    
    def _clasificar_con_openai(self, mensaje: str) -> Dict[str, Any]:
        """Clasificación usando OpenAI."""
        try:
            prompt = f"""
Clasifica la siguiente denuncia en una de estas categorías:
- acoso
- discriminacion
- corrupcion
- problemas_tecnicos
- otros

Denuncia: "{mensaje}"

Responde SOLO con un JSON con este formato:
{{"categoria": "categoria_elegida", "confianza": 0.85, "razon": "explicacion_breve"}}
"""
            
            respuesta = self.cliente_openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.1
            )
            
            contenido = respuesta.choices[0].message.content.strip()
            resultado_openai = json.loads(contenido)
            
            return {
                'categoria': resultado_openai.get('categoria', 'otros'),
                'confianza': resultado_openai.get('confianza', 0.5),
                'razon_openai': resultado_openai.get('razon', ''),
                'metodo': 'openai_gpt35',
                'timestamp': self._obtener_timestamp()
            }
            
        except Exception as e:
            print(f"Error con OpenAI: {e}")
            # Fallback a método local
            resultado = super().clasificar_denuncia(mensaje)
            resultado['metodo'] = 'local_error_fallback'
            resultado['error_openai'] = str(e)
            return resultado
    
    def analizar_veracidad(self, mensaje: str) -> Dict[str, Any]:
        """Análisis de veracidad con OpenAI si está disponible."""
        if self.openai_disponible and self.cliente_openai:
            return self._analizar_veracidad_openai(mensaje)
        else:
            return super().analizar_veracidad(mensaje)
    
    def _analizar_veracidad_openai(self, mensaje: str) -> Dict[str, Any]:
        """Análisis de veracidad usando OpenAI."""
        try:
            prompt = f"""
Analiza la veracidad de esta denuncia considerando:
- Nivel de detalle
- Coherencia
- Especificidad

Denuncia: "{mensaje}"

Responde SOLO con JSON:
{{"nivel_veracidad": "ALTA|MEDIA|BAJA", "confianza": 0.85, "factores": "explicacion"}}
"""
            
            respuesta = self.cliente_openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.1
            )
            
            contenido = respuesta.choices[0].message.content.strip()
            resultado_openai = json.loads(contenido)
            
            return {
                'nivel_veracidad': resultado_openai.get('nivel_veracidad', 'MEDIA'),
                'confianza': resultado_openai.get('confianza', 0.5),
                'factores_openai': resultado_openai.get('factores', ''),
                'metodo': 'openai_veracidad',
                'timestamp': self._obtener_timestamp()
            }
            
        except Exception as e:
            print(f"Error en análisis OpenAI: {e}")
            resultado = super().analizar_veracidad(mensaje)
            resultado['error_openai'] = str(e)
            return resultado
