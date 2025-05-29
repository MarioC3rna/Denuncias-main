"""
Agente IA Mejorado para análisis avanzado de denuncias.
Incluye detección de urgencia, análisis de sentimientos y alertas automáticas.
"""

import re
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
from enum import Enum

class NivelUrgencia(Enum):
    """Niveles de urgencia para las denuncias."""
    BAJA = 1
    MEDIA = 2
    ALTA = 3
    CRITICA = 4
    EMERGENCIA = 5

class TipoAlerta(Enum):
    """Tipos de alertas automáticas."""
    URGENCIA_CRITICA = "urgencia_critica"
    CONTENIDO_VIOLENTO = "contenido_violento"
    AMENAZA_DIRECTA = "amenaza_directa"
    SITUACION_RIESGO = "situacion_riesgo"
    EVIDENCIA_SOLIDA = "evidencia_solida"

class AgenteIAMejorado:
    """Agente IA avanzado para análisis profundo de denuncias."""
    
    def __init__(self):
        """Inicializa el agente IA con patrones y configuraciones."""
        self._inicializar_patrones()
        self._inicializar_categorias()
        self._inicializar_alertas()
    
    def _inicializar_patrones(self):
        """Inicializa patrones de análisis."""
        # Patrones de urgencia crítica
        self.patrones_urgencia_critica = [
            r'\b(emergencia|urgente|inmediato|ya|ahora|rápido)\b',
            r'\b(peligro|amenaza|riesgo|violencia|agresión)\b',
            r'\b(socorro|ayuda|auxilio|emergencia)\b',
            r'\b(crítico|grave|serio|importante)\b'
        ]
        
        # Patrones de contenido violento
        self.patrones_violencia = [
            r'\b(golpe|pegar|lastimar|dañar|herir)\b',
            r'\b(amenaza|intimidar|acosar|perseguir)\b',
            r'\b(violencia|agresión|ataque|maltrato)\b',
            r'\b(arma|cuchillo|pistola|navaja)\b'
        ]
        
        # Patrones de evidencia
        self.patrones_evidencia = [
            r'\b(prueba|evidencia|documento|foto|video)\b',
            r'\b(testigo|vio|escuchó|presenció)\b',
            r'\b(fecha|hora|día|momento)\b',
            r'\b(lugar|ubicación|sitio|donde)\b',
            r'\b(nombre|persona|quien|sujeto)\b'
        ]
        
        # Patrones temporales
        self.patrones_tiempo = [
            r'\b(\d{1,2}[:/]\d{1,2}|\d{1,2}\s*(am|pm))\b',  # Horas
            r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b',  # Fechas
            r'\b(ayer|hoy|mañana|anoche|esta\s*(mañana|tarde|noche))\b',
            r'\b(lunes|martes|miércoles|jueves|viernes|sábado|domingo)\b'
        ]
        
        # Patrones de lugares
        self.patrones_lugares = [
            r'\b(oficina|sala|baño|estacionamiento|pasillo)\b',
            r'\b(piso\s*\d+|planta\s*\d+|edificio)\b',
            r'\b(departamento|área|sección|división)\b',
            r'\b(cerca\s*de|junto\s*a|en\s*el|en\s*la)\b'
        ]
        
        # Patrones emocionales
        self.patrones_emociones = {
            'miedo': [r'\b(miedo|temor|asustado|aterrado|pánico)\b'],
            'enojo': [r'\b(enojado|furioso|molesto|indignado|irritado)\b'],
            'tristeza': [r'\b(triste|deprimido|desanimado|abatido)\b'],
            'ansiedad': [r'\b(ansioso|nervioso|preocupado|estresado)\b'],
            'frustración': [r'\b(frustrado|desesperado|harto|cansado)\b']
        }
    
    def _inicializar_categorias(self):
        """Inicializa patrones mejorados para categorización."""
        self.patrones_categorias = {
            'acoso_laboral': [
                r'\b(acoso|hostigamiento|intimidación|presión)\b',
                r'\b(jefe|supervisor|compañero|colega)\b',
                r'\b(trabajo|laboral|oficina|empleado)\b'
            ],
            'discriminacion': [
                r'\b(discriminación|racismo|sexismo|prejuicio)\b',
                r'\b(género|raza|edad|religión|orientación)\b',
                r'\b(trato\s*diferente|exclusión|marginación)\b'
            ],
            'fraude': [
                r'\b(fraude|estafa|robo|hurto|malversación)\b',
                r'\b(dinero|efectivo|fondos|recursos|presupuesto)\b',
                r'\b(factura|cuenta|pago|cobro)\b'
            ],
            'seguridad': [
                r'\b(seguridad|riesgo|peligro|accidente)\b',
                r'\b(equipo|herramienta|máquina|instalación)\b',
                r'\b(norma|protocolo|procedimiento|regla)\b'
            ],
            'violencia': [
                r'\b(violencia|agresión|golpe|maltrato)\b',
                r'\b(físico|verbal|psicológico|sexual)\b',
                r'\b(amenaza|intimidación|hostigamiento)\b'
            ],
            'corrupcion': [
                r'\b(corrupción|soborno|coima|mordida)\b',
                r'\b(favoritismo|nepotismo|tráfico\s*de\s*influencias)\b',
                r'\b(ilegal|irregular|indebido|inapropiado)\b'
            ]
        }
    
    def _inicializar_alertas(self):
        """Inicializa configuración de alertas automáticas."""
        self.umbrales_alerta = {
            TipoAlerta.URGENCIA_CRITICA: 3,  # Nivel mínimo de urgencia
            TipoAlerta.CONTENIDO_VIOLENTO: 2,  # Cantidad de patrones violentos
            TipoAlerta.AMENAZA_DIRECTA: 1,  # Una sola amenaza directa
            TipoAlerta.SITUACION_RIESGO: 2,  # Patrones de riesgo
            TipoAlerta.EVIDENCIA_SOLIDA: 3  # Cantidad de evidencias
        }
    
    def analizar_denuncia_completa(self, mensaje: str, categoria_sugerida: str = None) -> Dict[str, Any]:
        """
        Realiza análisis completo de una denuncia.
        
        Args:
            mensaje: Contenido de la denuncia
            categoria_sugerida: Categoría previamente sugerida (opcional)
        
        Returns:
            Dict con análisis completo
        """
        timestamp = datetime.now().isoformat()
        
        # Análisis básico
        urgencia = self.detectar_urgencia(mensaje)
        categoria = self.sugerir_categoria_mejorada(mensaje)
        prioridad = self.calcular_prioridad(mensaje, urgencia)
        
        # Análisis avanzado
        entidades = self.extraer_entidades(mensaje)
        sentimientos = self.analizar_sentimientos(mensaje)
        evidencias = self.evaluar_evidencias(mensaje)
        
        # Alertas automáticas
        alertas = self.generar_alertas(mensaje, urgencia, prioridad)
        
        # Recomendaciones
        recomendaciones = self.generar_recomendaciones(urgencia, categoria, evidencias, alertas)
        
        return {
            'timestamp_analisis': timestamp,
            'urgencia': {
                'nivel': urgencia.name,
                'valor': urgencia.value,
                'descripcion': self._get_descripcion_urgencia(urgencia)
            },
            'categoria': {
                'sugerida': categoria,
                'confianza': self._calcular_confianza_categoria(mensaje, categoria),
                'alternativas': self._get_categorias_alternativas(mensaje)
            },
            'prioridad': {
                'puntuacion': prioridad,
                'nivel': self._get_nivel_prioridad(prioridad),
                'justificacion': self._get_justificacion_prioridad(prioridad)
            },
            'entidades': entidades,
            'sentimientos': sentimientos,
            'evidencias': evidencias,
            'alertas': alertas,
            'recomendaciones': recomendaciones,
            'requiere_atencion_inmediata': self._requiere_atencion_inmediata(urgencia, alertas),
            'puntuacion_veracidad': self._calcular_veracidad(evidencias, entidades),
            'resumen_ejecutivo': self._generar_resumen_ejecutivo(mensaje, urgencia, categoria, alertas)
        }
    
    def detectar_urgencia(self, mensaje: str) -> NivelUrgencia:
        """Detecta el nivel de urgencia basado en patrones del mensaje."""
        mensaje_lower = mensaje.lower()
        puntuacion_urgencia = 0
        
        # Verificar patrones de urgencia crítica
        for patron in self.patrones_urgencia_critica:
            matches = len(re.findall(patron, mensaje_lower, re.IGNORECASE))
            puntuacion_urgencia += matches * 2
        
        # Verificar patrones de violencia
        for patron in self.patrones_violencia:
            matches = len(re.findall(patron, mensaje_lower, re.IGNORECASE))
            puntuacion_urgencia += matches * 3
        
        # Verificar longitud y repetición de palabras críticas
        palabras_criticas = ['urgente', 'inmediato', 'emergencia', 'ayuda', 'socorro']
        for palabra in palabras_criticas:
            if palabra in mensaje_lower:
                # Bonus por repetición
                count = mensaje_lower.count(palabra)
                puntuacion_urgencia += count * 1.5
        
        # Verificar signos de exclamación múltiples
        exclamaciones = mensaje.count('!')
        if exclamaciones >= 3:
            puntuacion_urgencia += 2
        
        # Verificar palabras en mayúsculas (gritando)
        palabras_mayusculas = len([p for p in mensaje.split() if p.isupper() and len(p) > 2])
        if palabras_mayusculas >= 3:
            puntuacion_urgencia += 1
        
        # Determinar nivel de urgencia
        if puntuacion_urgencia >= 12:
            return NivelUrgencia.EMERGENCIA
        elif puntuacion_urgencia >= 8:
            return NivelUrgencia.CRITICA
        elif puntuacion_urgencia >= 5:
            return NivelUrgencia.ALTA
        elif puntuacion_urgencia >= 2:
            return NivelUrgencia.MEDIA
        else:
            return NivelUrgencia.BAJA
    
    def sugerir_categoria_mejorada(self, mensaje: str) -> str:
        """Sugiere categoría con análisis mejorado."""
        mensaje_lower = mensaje.lower()
        puntuaciones = {}
        
        # Calcular puntuación para cada categoría
        for categoria, patrones in self.patrones_categorias.items():
            puntuacion = 0
            for patron in patrones:
                matches = len(re.findall(patron, mensaje_lower, re.IGNORECASE))
                puntuacion += matches
            
            # Bonus por contexto
            if categoria == 'acoso_laboral' and any(word in mensaje_lower for word in ['trabajo', 'oficina', 'jefe']):
                puntuacion += 2
            elif categoria == 'violencia' and any(word in mensaje_lower for word in ['golpe', 'amenaza', 'miedo']):
                puntuacion += 3
            elif categoria == 'fraude' and any(word in mensaje_lower for word in ['dinero', 'factura', 'pago']):
                puntuacion += 2
            
            puntuaciones[categoria] = puntuacion
        
        # Retornar la categoría con mayor puntuación
        if puntuaciones:
            categoria_sugerida = max(puntuaciones, key=puntuaciones.get)
            if puntuaciones[categoria_sugerida] > 0:
                return categoria_sugerida
        
        return 'otros'
    
    def calcular_prioridad(self, mensaje: str, urgencia: NivelUrgencia) -> int:
        """Calcula prioridad (1-5) basada en múltiples factores."""
        prioridad_base = urgencia.value
        
        # Factores adicionales
        factores = 0
        
        # Factor de evidencia
        evidencias = len(re.findall(r'\b(prueba|evidencia|documento|testigo)\b', mensaje.lower()))
        factores += min(evidencias * 0.5, 1)
        
        # Factor de tiempo (qué tan reciente)
        tiempo_inmediato = len(re.findall(r'\b(ahora|hoy|ayer|esta\s*(mañana|tarde))\b', mensaje.lower()))
        factores += min(tiempo_inmediato * 0.3, 0.8)
        
        # Factor de personas involucradas
        personas = len(re.findall(r'\b(persona|gente|todos|muchos|varios)\b', mensaje.lower()))
        factores += min(personas * 0.2, 0.6)
        
        # Factor de impacto organizacional
        impacto_org = len(re.findall(r'\b(empresa|organización|departamento|todos)\b', mensaje.lower()))
        factores += min(impacto_org * 0.3, 0.7)
        
        prioridad_final = min(prioridad_base + factores, 5)
        return round(prioridad_final)
    
    def extraer_entidades(self, mensaje: str) -> Dict[str, List[str]]:
        """Extrae entidades importantes del mensaje."""
        entidades = {
            'tiempos': [],
            'lugares': [],
            'personas': [],
            'evidencias': []
        }
        
        # Extraer tiempos
        for patron in self.patrones_tiempo:
            matches = re.findall(patron, mensaje, re.IGNORECASE)
            entidades['tiempos'].extend(matches)
        
        # Extraer lugares
        for patron in self.patrones_lugares:
            matches = re.findall(patron, mensaje, re.IGNORECASE)
            entidades['lugares'].extend(matches)
        
        # Extraer evidencias mencionadas
        for patron in self.patrones_evidencia:
            matches = re.findall(patron, mensaje, re.IGNORECASE)
            entidades['evidencias'].extend(matches)
        
        # Buscar nombres propios (palabras capitalizadas que no sean primeras de oración)
        palabras = mensaje.split()
        for i, palabra in enumerate(palabras):
            if i > 0 and palabra[0].isupper() and len(palabra) > 2:
                # Filtrar palabras que no son nombres
                if palabra.lower() not in ['que', 'pero', 'porque', 'cuando', 'donde']:
                    entidades['personas'].append(palabra)
        
        # Limpiar duplicados
        for key in entidades:
            entidades[key] = list(set(entidades[key]))
        
        return entidades
    
    def analizar_sentimientos(self, mensaje: str) -> Dict[str, Any]:
        """Analiza sentimientos y emociones en el mensaje."""
        mensaje_lower = mensaje.lower()
        emociones_detectadas = {}
        
        # Detectar emociones específicas
        for emocion, patrones in self.patrones_emociones.items():
            intensidad = 0
            for patron in patrones:
                matches = len(re.findall(patron, mensaje_lower, re.IGNORECASE))
                intensidad += matches
            
            if intensidad > 0:
                emociones_detectadas[emocion] = min(intensidad, 5)
        
        # Calcular polaridad general
        palabras_negativas = ['malo', 'terrible', 'horrible', 'odio', 'detesto', 'molesto']
        palabras_positivas = ['bueno', 'bien', 'excelente', 'contento', 'feliz', 'satisfecho']
        
        negatividad = sum(1 for palabra in palabras_negativas if palabra in mensaje_lower)
        positividad = sum(1 for palabra in palabras_positivas if palabra in mensaje_lower)
        
        if negatividad > positividad:
            polaridad = 'negativa'
        elif positividad > negatividad:
            polaridad = 'positiva'
        else:
            polaridad = 'neutral'
        
        # Calcular intensidad emocional general
        intensidad_total = sum(emociones_detectadas.values())
        nivel_intensidad = 'baja' if intensidad_total <= 2 else 'media' if intensidad_total <= 5 else 'alta'
        
        return {
            'emociones_detectadas': emociones_detectadas,
            'polaridad': polaridad,
            'intensidad': nivel_intensidad,
            'requiere_apoyo_emocional': intensidad_total >= 4 or 'miedo' in emociones_detectadas
        }
    
    def evaluar_evidencias(self, mensaje: str) -> Dict[str, Any]:
        """Evalúa la calidad y cantidad de evidencias mencionadas."""
        mensaje_lower = mensaje.lower()
        
        tipos_evidencia = {
            'documental': r'\b(documento|papel|archivo|reporte|email|mensaje)\b',
            'visual': r'\b(foto|imagen|video|grabación|captura)\b',
            'testimonial': r'\b(testigo|vio|escuchó|presenció|dijo)\b',
            'física': r'\b(objeto|cosa|elemento|marca|señal)\b'
        }
        
        evidencias_encontradas = {}
        puntuacion_total = 0
        
        for tipo, patron in tipos_evidencia.items():
            matches = len(re.findall(patron, mensaje_lower, re.IGNORECASE))
            if matches > 0:
                evidencias_encontradas[tipo] = matches
                puntuacion_total += matches
        
        # Verificar especificidad (fechas, horas, lugares específicos)
        especificidad = 0
        especificidad += len(re.findall(r'\d{1,2}[:/]\d{1,2}', mensaje))  # Horas
        especificidad += len(re.findall(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', mensaje))  # Fechas
        especificidad += len(re.findall(r'\b(sala|oficina|piso)\s*\d+\b', mensaje_lower))  # Lugares específicos
        
        puntuacion_total += especificidad * 0.5
        
        # Determinar nivel de credibilidad
        if puntuacion_total >= 5:
            credibilidad = 'alta'
        elif puntuacion_total >= 3:
            credibilidad = 'media'
        elif puntuacion_total >= 1:
            credibilidad = 'baja'
        else:
            credibilidad = 'muy_baja'
        
        return {
            'tipos_evidencia': evidencias_encontradas,
            'puntuacion_evidencia': round(puntuacion_total, 1),
            'nivel_credibilidad': credibilidad,
            'especificidad': especificidad,
            'requiere_mas_evidencia': puntuacion_total < 2
        }
    
    def generar_alertas(self, mensaje: str, urgencia: NivelUrgencia, prioridad: int) -> List[Dict[str, Any]]:
        """Genera alertas automáticas basadas en el análisis."""
        alertas = []
        mensaje_lower = mensaje.lower()
        
        # Alerta de urgencia crítica
        if urgencia.value >= self.umbrales_alerta[TipoAlerta.URGENCIA_CRITICA]:
            alertas.append({
                'tipo': TipoAlerta.URGENCIA_CRITICA.value,
                'mensaje': f'Denuncia con urgencia {urgencia.name} - Requiere atención inmediata',
                'prioridad': 'alta',
                'accion_sugerida': 'Contactar inmediatamente al denunciante o autoridades competentes'
            })
        
        # Alerta de contenido violento
        patrones_violencia_count = sum(1 for patron in self.patrones_violencia 
                                     if re.search(patron, mensaje_lower, re.IGNORECASE))
        if patrones_violencia_count >= self.umbrales_alerta[TipoAlerta.CONTENIDO_VIOLENTO]:
            alertas.append({
                'tipo': TipoAlerta.CONTENIDO_VIOLENTO.value,
                'mensaje': 'Contenido con indicadores de violencia detectados',
                'prioridad': 'alta',
                'accion_sugerida': 'Evaluar riesgo para la seguridad personal del denunciante'
            })
        
        # Alerta de amenaza directa
        amenazas_directas = re.findall(r'\b(amenaza|amenazar|lastimar|dañar|hacer\s*daño)\b', mensaje_lower)
        if len(amenazas_directas) >= self.umbrales_alerta[TipoAlerta.AMENAZA_DIRECTA]:
            alertas.append({
                'tipo': TipoAlerta.AMENAZA_DIRECTA.value,
                'mensaje': 'Posible amenaza directa identificada',
                'prioridad': 'crítica',
                'accion_sugerida': 'Notificar a seguridad y considerar medidas de protección'
            })
        
        # Alerta de situación de riesgo
        indicadores_riesgo = re.findall(r'\b(peligro|riesgo|inseguro|vulnerable|expuesto)\b', mensaje_lower)
        if len(indicadores_riesgo) >= self.umbrales_alerta[TipoAlerta.SITUACION_RIESGO]:
            alertas.append({
                'tipo': TipoAlerta.SITUACION_RIESGO.value,
                'mensaje': 'Situación de riesgo potencial detectada',
                'prioridad': 'media',
                'accion_sugerida': 'Evaluar medidas de seguridad preventivas'
            })
        
        # Alerta de evidencia sólida
        evidencias_count = len(re.findall(r'\b(prueba|evidencia|documento|testigo|foto|video)\b', mensaje_lower))
        if evidencias_count >= self.umbrales_alerta[TipoAlerta.EVIDENCIA_SOLIDA]:
            alertas.append({
                'tipo': TipoAlerta.EVIDENCIA_SOLIDA.value,
                'mensaje': 'Denuncia con evidencia sólida disponible',
                'prioridad': 'media',
                'accion_sugerida': 'Priorizar para investigación detallada'
            })
        
        return alertas
    
    def generar_recomendaciones(self, urgencia: NivelUrgencia, categoria: str, 
                              evidencias: Dict, alertas: List) -> List[str]:
        """Genera recomendaciones de acciones basadas en el análisis."""
        recomendaciones = []
        
        # Recomendaciones basadas en urgencia
        if urgencia.value >= 4:
            recomendaciones.append("🚨 ACCIÓN INMEDIATA: Contactar al denunciante en las próximas 2 horas")
            recomendaciones.append("📞 Notificar a autoridades competentes si hay riesgo inmediato")
        elif urgencia.value >= 3:
            recomendaciones.append("⏰ Responder dentro de las próximas 24 horas")
            recomendaciones.append("🔍 Iniciar investigación preliminar")
        
        # Recomendaciones basadas en categoría
        if categoria == 'violencia':
            recomendaciones.append("🛡️ Evaluar necesidad de medidas de protección")
            recomendaciones.append("👥 Involucrar a recursos humanos y seguridad")
        elif categoria == 'fraude':
            recomendaciones.append("💰 Revisar registros financieros relacionados")
            recomendaciones.append("🔒 Asegurar documentación contable")
        elif categoria == 'acoso_laboral':
            recomendaciones.append("📋 Documentar patrones de comportamiento")
            recomendaciones.append("🤝 Ofrecer apoyo psicológico al denunciante")
        
        # Recomendaciones basadas en evidencias
        if evidencias['nivel_credibilidad'] == 'alta':
            recomendaciones.append("📁 Recopilar y preservar evidencias mencionadas")
            recomendaciones.append("⚖️ Considerar para proceso formal de investigación")
        elif evidencias['requiere_mas_evidencia']:
            recomendaciones.append("🔍 Solicitar evidencia adicional al denunciante")
            recomendaciones.append("👥 Buscar testigos o fuentes corroborativas")
        
        # Recomendaciones basadas en alertas
        for alerta in alertas:
            if alerta['prioridad'] == 'crítica':
                recomendaciones.append(f"🚨 CRÍTICO: {alerta['accion_sugerida']}")
            elif alerta['prioridad'] == 'alta':
                recomendaciones.append(f"⚠️ ALTA: {alerta['accion_sugerida']}")
        
        # Recomendaciones generales
        recomendaciones.append("📝 Registrar todas las acciones tomadas")
        recomendaciones.append("🔄 Programar seguimiento según cronograma establecido")
        
        return list(set(recomendaciones))  # Eliminar duplicados
    
    def _get_descripcion_urgencia(self, urgencia: NivelUrgencia) -> str:
        """Retorna descripción del nivel de urgencia."""
        descripciones = {
            NivelUrgencia.BAJA: "Situación que puede esperar proceso normal",
            NivelUrgencia.MEDIA: "Requiere atención en tiempo razonable",
            NivelUrgencia.ALTA: "Necesita atención prioritaria",
            NivelUrgencia.CRITICA: "Requiere acción inmediata",
            NivelUrgencia.EMERGENCIA: "EMERGENCIA - Acción inmediata crítica"
        }
        return descripciones.get(urgencia, "Nivel no definido")
    
    def _calcular_confianza_categoria(self, mensaje: str, categoria: str) -> float:
        """Calcula confianza en la categorización sugerida."""
        if categoria not in self.patrones_categorias:
            return 0.5
        
        mensaje_lower = mensaje.lower()
        patrones = self.patrones_categorias[categoria]
        matches = sum(len(re.findall(patron, mensaje_lower, re.IGNORECASE)) for patron in patrones)
        
        # Normalizar confianza entre 0.0 y 1.0
        confianza = min(matches / len(patrones), 1.0)
        return round(confianza, 2)
    
    def _get_categorias_alternativas(self, mensaje: str) -> List[str]:
        """Obtiene categorías alternativas con puntuación."""
        mensaje_lower = mensaje.lower()
        puntuaciones = {}
        
        for categoria, patrones in self.patrones_categorias.items():
            puntuacion = sum(len(re.findall(patron, mensaje_lower, re.IGNORECASE)) for patron in patrones)
            if puntuacion > 0:
                puntuaciones[categoria] = puntuacion
        
        # Retornar top 3 alternativas
        alternativas = sorted(puntuaciones.items(), key=lambda x: x[1], reverse=True)[:3]
        return [categoria for categoria, _ in alternativas]
    
    def _get_nivel_prioridad(self, prioridad: int) -> str:
        """Convierte puntuación numérica a nivel descriptivo."""
        if prioridad >= 5:
            return "EMERGENCIA"
        elif prioridad >= 4:
            return "ALTA"
        elif prioridad >= 3:
            return "MEDIA"
        elif prioridad >= 2:
            return "BAJA"
        else:
            return "MÍNIMA"
    
    def _get_justificacion_prioridad(self, prioridad: int) -> str:
        """Proporciona justificación para el nivel de prioridad."""
        justificaciones = {
            5: "Múltiples factores críticos detectados",
            4: "Urgencia alta con factores agravantes",
            3: "Situación importante que requiere atención",
            2: "Caso que merece seguimiento regular",
            1: "Situación menor para proceso normal"
        }
        return justificaciones.get(prioridad, "Evaluación estándar")
    
    def _requiere_atencion_inmediata(self, urgencia: NivelUrgencia, alertas: List) -> bool:
        """Determina si la denuncia requiere atención inmediata."""
        if urgencia.value >= 4:
            return True
        
        alertas_criticas = [a for a in alertas if a.get('prioridad') in ['crítica', 'alta']]
        return len(alertas_criticas) > 0
    
    def _calcular_veracidad(self, evidencias: Dict, entidades: Dict) -> float:
        """Calcula puntuación de veracidad basada en evidencias y entidades."""
        puntuacion_base = evidencias.get('puntuacion_evidencia', 0)
        
        # Bonus por entidades específicas
        bonus_entidades = 0
        bonus_entidades += len(entidades.get('tiempos', [])) * 0.2
        bonus_entidades += len(entidades.get('lugares', [])) * 0.3
        bonus_entidades += len(entidades.get('personas', [])) * 0.1
        
        puntuacion_total = min(puntuacion_base + bonus_entidades, 10)
        return round(puntuacion_total / 10, 2)
    
    def _generar_resumen_ejecutivo(self, mensaje: str, urgencia: NivelUrgencia, 
                                 categoria: str, alertas: List) -> str:
        """Genera un resumen ejecutivo de la denuncia."""
        longitud = len(mensaje.split())
        
        resumen = f"Denuncia de {categoria.replace('_', ' ')} con urgencia {urgencia.name.lower()}"
        
        if alertas:
            tipos_alerta = [a['tipo'] for a in alertas]
            if 'urgencia_critica' in tipos_alerta:
                resumen += " - REQUIERE ATENCIÓN INMEDIATA"
            elif 'contenido_violento' in tipos_alerta:
                resumen += " - Contiene indicadores de violencia"
        
        resumen += f". Mensaje de {longitud} palabras"
        
        if longitud > 200:
            resumen += " con descripción detallada"
        elif longitud < 50:
            resumen += " - requiere más información"
        
        return resumen

    def obtener_estadisticas_analisis(self) -> Dict[str, Any]:
        """Obtiene estadísticas del agente IA para el dashboard."""
        return {
            'categorias_disponibles': list(self.patrones_categorias.keys()),
            'niveles_urgencia': [nivel.name for nivel in NivelUrgencia],
            'tipos_alerta': [tipo.value for tipo in TipoAlerta],
            'version_agente': "2.0 - Mejorado",
            'capacidades': [
                "Detección de urgencia avanzada",
                "Análisis de sentimientos",
                "Extracción de entidades",
                "Alertas automáticas",
                "Recomendaciones inteligentes",
                "Evaluación de evidencias"
            ]
        }