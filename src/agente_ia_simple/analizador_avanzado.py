"""
Analizador avanzado con detección de spam y análisis de veracidad.
"""

import re
from typing import Dict, List, Any
from datetime import datetime

class AnalizadorAvanzado:
    """Análisis avanzado de denuncias con detección de spam."""
    
    def __init__(self):
        """Inicializa el analizador avanzado."""
        self.patrones_spam = [
            r'\b(test|testing|prueba)\b',
            r'\b(hola|hello|hi)\s*$',
            r'^(.)\1{4,}',  # Caracteres repetidos
            r'\b(asdf|qwerty|123456)\b',
            r'^\s*[.,;!?]{2,}\s*$',  # Solo puntuación
        ]
        
        self.indicadores_falsedad = [
            'supuestamente', 'creo que', 'tal vez', 'posiblemente',
            'no estoy seguro', 'rumor', 'chisme', 'dicen que'
        ]
        
        self.indicadores_urgencia = [
            'urgente', 'inmediato', 'ahora', 'ya', 'rápido',
            'peligro', 'amenaza', 'violencia', 'acoso sexual'
        ]

    def analizar_spam(self, texto: str) -> Dict[str, Any]:
        """
        Analiza si el texto parece spam o contenido no válido.
        
        Args:
            texto: Texto a analizar
            
        Returns:
            Resultado del análisis de spam
        """
        texto_lower = texto.lower().strip()
        
        # Verificaciones básicas
        if len(texto_lower) < 10:
            return {
                'es_spam': True,
                'confianza': 0.9,
                'razon': 'Texto demasiado corto',
                'tipo_spam': 'contenido_insuficiente'
            }
        
        if len(texto_lower) > 5000:
            return {
                'es_spam': True,
                'confianza': 0.8,
                'razon': 'Texto excesivamente largo',
                'tipo_spam': 'contenido_excesivo'
            }
        
        # Verificar patrones de spam
        spam_score = 0
        razones_spam = []
        
        for patron in self.patrones_spam:
            if re.search(patron, texto_lower, re.IGNORECASE):
                spam_score += 0.3
                razones_spam.append(f"Patrón de prueba detectado: {patron}")
        
        # Verificar contenido repetitivo
        palabras = texto_lower.split()
        if len(set(palabras)) < len(palabras) * 0.3:  # Menos del 30% palabras únicas
            spam_score += 0.4
            razones_spam.append("Contenido muy repetitivo")
        
        # Verificar si es solo saludo
        if re.match(r'^\s*(hola|hello|hi|buenas|good)\s*[.,!]?\s*$', texto_lower):
            spam_score += 0.9
            razones_spam.append("Solo contiene saludo")
        
        # Verificar caracteres especiales excesivos
        caracteres_especiales = len(re.findall(r'[!@#$%^&*()_+={}[\]|\\:";\'<>?,./-]', texto))
        if caracteres_especiales > len(texto) * 0.3:
            spam_score += 0.3
            razones_spam.append("Exceso de caracteres especiales")
        
        es_spam = spam_score >= 0.6
        
        return {
            'es_spam': es_spam,
            'confianza': min(spam_score, 0.95),
            'razon': '; '.join(razones_spam) if razones_spam else 'Contenido válido',
            'tipo_spam': 'patron_spam' if es_spam else 'contenido_valido',
            'score_spam': spam_score
        }

    def analizar_veracidad(self, texto: str) -> Dict[str, Any]:
        """
        Analiza la veracidad aparente del texto.
        
        Args:
            texto: Texto a analizar
            
        Returns:
            Análisis de veracidad
        """
        texto_lower = texto.lower()
        
        # Contadores
        indicadores_falsedad_count = 0
        indicadores_certeza_count = 0
        detalles_especificos = 0
        
        # Buscar indicadores de falsedad
        for indicador in self.indicadores_falsedad:
            if indicador in texto_lower:
                indicadores_falsedad_count += 1
        
        # Buscar indicadores de certeza
        indicadores_certeza = ['vi', 'escuché', 'presencié', 'fue testigo', 'ocurrió', 'sucedió']
        for indicador in indicadores_certeza:
            if indicador in texto_lower:
                indicadores_certeza_count += 1
        
        # Buscar detalles específicos
        # Fechas
        if re.search(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', texto) or \
           re.search(r'\b(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\b', texto_lower):
            detalles_especificos += 1
        
        # Horas
        if re.search(r'\b\d{1,2}:\d{2}\b', texto):
            detalles_especificos += 1
        
        # Lugares específicos
        if re.search(r'\b(oficina|sala|piso|edificio|calle|avenida)\s+\w+', texto_lower):
            detalles_especificos += 1
        
        # Nombres (aunque sean anónimos)
        if re.search(r'\b(señor|señora|licenciado|doctor|ing\.|sr\.|sra\.)\s+\w+', texto_lower):
            detalles_especificos += 1
        
        # Calcular score de veracidad
        veracidad_score = 0.5  # Base
        
        # Ajustar por indicadores
        veracidad_score += indicadores_certeza_count * 0.15
        veracidad_score -= indicadores_falsedad_count * 0.2
        veracidad_score += detalles_especificos * 0.1
        
        # Longitud apropiada indica más credibilidad
        longitud = len(texto.split())
        if 20 <= longitud <= 200:
            veracidad_score += 0.1
        elif longitud < 10:
            veracidad_score -= 0.2
        
        # Determinar nivel
        if veracidad_score >= 0.8:
            nivel = 'MUY_ALTA'
        elif veracidad_score >= 0.6:
            nivel = 'ALTA'
        elif veracidad_score >= 0.4:
            nivel = 'MEDIA'
        elif veracidad_score >= 0.2:
            nivel = 'BAJA'
        else:
            nivel = 'MUY_BAJA'
        
        return {
            'nivel_veracidad': nivel,
            'confianza': min(max(veracidad_score, 0.0), 1.0),
            'indicadores_certeza': indicadores_certeza_count,
            'indicadores_falsedad': indicadores_falsedad_count,
            'detalles_especificos': detalles_especificos,
            'longitud_texto': longitud,
            'score_veracidad': veracidad_score
        }

    def analizar_urgencia(self, texto: str) -> Dict[str, Any]:
        """
        Analiza el nivel de urgencia de la denuncia.
        
        Args:
            texto: Texto a analizar
            
        Returns:
            Análisis de urgencia
        """
        texto_lower = texto.lower()
        
        urgencia_score = 0
        indicadores_encontrados = []
        
        # Buscar indicadores de urgencia
        for indicador in self.indicadores_urgencia:
            if indicador in texto_lower:
                urgencia_score += 0.2
                indicadores_encontrados.append(indicador)
        
        # Palabras que indican situación en curso
        situacion_en_curso = ['está pasando', 'ocurriendo ahora', 'en este momento', 'actualmente']
        for indicador in situacion_en_curso:
            if indicador in texto_lower:
                urgencia_score += 0.3
                indicadores_encontrados.append(indicador)
        
        # Términos legales graves
        terminos_graves = ['violación', 'amenaza de muerte', 'arma', 'violencia física', 'secuestro']
        for termino in terminos_graves:
            if termino in texto_lower:
                urgencia_score += 0.4
                indicadores_encontrados.append(termino)
        
        # Determinar nivel
        if urgencia_score >= 0.8:
            nivel = 'CRÍTICA'
        elif urgencia_score >= 0.5:
            nivel = 'ALTA'
        elif urgencia_score >= 0.3:
            nivel = 'MEDIA'
        else:
            nivel = 'BAJA'
        
        return {
            'nivel_urgencia': nivel,
            'confianza': min(urgencia_score, 1.0),
            'indicadores_encontrados': indicadores_encontrados,
            'requiere_atencion_inmediata': urgencia_score >= 0.8,
            'score_urgencia': urgencia_score
        }

    def analisis_completo(self, texto: str) -> Dict[str, Any]:
        """
        Realiza análisis completo del texto.
        
        Args:
            texto: Texto a analizar
            
        Returns:
            Análisis completo
        """
        # Realizar todos los análisis
        spam_analysis = self.analizar_spam(texto)
        veracidad_analysis = self.analizar_veracidad(texto)
        urgencia_analysis = self.analizar_urgencia(texto)
        
        # Análisis consolidado
        es_valida = not spam_analysis['es_spam']
        
        return {
            'timestamp_analisis': datetime.now().isoformat(),
            'texto_analizado': texto[:100] + "..." if len(texto) > 100 else texto,
            'longitud_original': len(texto),
            
            # Resultados principales
            'es_denuncia_valida': es_valida,
            'confianza_validez': 1.0 - spam_analysis['confianza'] if spam_analysis['es_spam'] else 0.8,
            
            # Análisis detallado
            'spam': spam_analysis,
            'veracidad': veracidad_analysis,
            'urgencia': urgencia_analysis,
            
            # Recomendaciones
            'requiere_revision_humana': (
                spam_analysis['es_spam'] or 
                veracidad_analysis['nivel_veracidad'] in ['MUY_BAJA', 'BAJA'] or
                urgencia_analysis['nivel_urgencia'] == 'CRÍTICA'
            ),
            'requiere_atencion_inmediata': urgencia_analysis['requiere_atencion_inmediata'],
            
            # Metadatos
            'version_analizador': '1.0',
            'metodo_analisis': 'avanzado_local'
        }