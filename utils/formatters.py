"""
Utilidades para formateo de salida en consola.
Centraliza toda la presentación visual del sistema.
"""

import os
from typing import Dict, List, Any
from tabulate import tabulate
from config.settings import ConfiguracionSistema

class FormateadorConsola:
    """Formateador para salida en consola."""
    
    def __init__(self):
        """Inicializa el formateador con configuración del sistema."""
        self.config = ConfiguracionSistema()
    
    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def solicitar_confirmacion(self, mensaje: str) -> bool:
        """Solicita confirmación al usuario."""
        try:
            respuesta = input(f"{mensaje} (s/n): ").strip().lower()
            return respuesta in ['s', 'si', 'sí', 'y', 'yes']
        except (EOFError, KeyboardInterrupt):
            return False
    
    def mostrar_banner(self, titulo: str):
        """Muestra un banner."""
        print("=" * 50)
        print(titulo.center(50))
        print("=" * 50)

    def mostrar_menu(self, titulo: str, opciones: List[str], ancho: int = 30):
        """
        Muestra un menú con opciones de forma consistente.
        
        Args:
            titulo: Título del menú
            opciones: Lista de opciones del menú
            ancho: Ancho de la línea separadora
        """
        print(f"\n📋 {titulo}")
        print("-" * ancho)
        
        for opcion in opciones:
            print(opcion)
        
        print("-" * ancho)

    def mostrar_separador(self, titulo: str = "", ancho: int = 40, estilo: str = "="):
        """
        Muestra un separador con título opcional.
        
        Args:
            titulo: Título opcional del separador
            ancho: Ancho del separador
            estilo: Carácter para el separador ('=', '-', '*')
        """
        if titulo:
            print(f"\n{titulo}")
            print(estilo * ancho)
        else:
            print(estilo * ancho)

    def mostrar_mensaje_exito(self, mensaje: str):
        """Muestra un mensaje de éxito con formato consistente."""
        print(f"\n✅ {mensaje}")

    def mostrar_mensaje_error(self, mensaje: str):
        """Muestra un mensaje de error con formato consistente."""
        print(f"\n❌ {mensaje}")

    def mostrar_mensaje_advertencia(self, mensaje: str):
        """Muestra un mensaje de advertencia con formato consistente."""
        print(f"\n⚠️  {mensaje}")

    def mostrar_mensaje_info(self, mensaje: str):
        """Muestra un mensaje informativo con formato consistente."""
        print(f"\n💡 {mensaje}")

    def mostrar_resultado_validacion(self, resultado: Dict):
        """
        Formatea y muestra el resultado de validación de denuncia.
        
        Args:
            resultado: Diccionario con resultado de validación
        """
        self.mostrar_separador("📋 VALIDACIÓN DE DENUNCIA", 30)
        
        if resultado.get("es_denuncia_valida", False):
            print("✅ Contenido VÁLIDO - Es una denuncia real")
            confianza = resultado.get("confianza", 0.5)
            print(f"📈 Confianza de validez: {confianza:.1%}")
        else:
            print("❌ Contenido NO VÁLIDO - No es una denuncia")
            tipo_contenido = resultado.get('tipo_contenido', 'Desconocido')
            print(f"📋 Tipo detectado: {tipo_contenido}")
            
            # Mostrar razón de invalidez si existe
            if 'razon_invalidez' in resultado:
                print(f"🔍 Razón: {resultado['razon_invalidez']}")

    def mostrar_analisis_veracidad(self, resultado: Dict):
        """
        Formatea y muestra el análisis de veracidad.
        
        Args:
            resultado: Diccionario con análisis de veracidad
        """
        self.mostrar_separador("🎯 ANÁLISIS DE VERACIDAD", 30)
        
        nivel = resultado.get("nivel_veracidad", "MEDIA")
        confianza = resultado.get("confianza", 0.5)
        urgencia = resultado.get("nivel_urgencia", "MEDIA")
        
        # Obtener emojis desde configuración
        emoji_veracidad = self.config.obtener_emoji_veracidad(nivel)
        emoji_urgencia = self.config.obtener_emoji_urgencia(urgencia)
        
        print(f"{emoji_veracidad} Nivel de veracidad: {nivel}")
        print(f"📈 Confianza general: {confianza:.1%}")
        print(f"{emoji_urgencia} Urgencia: {urgencia}")
        
        # Mostrar indicadores de riesgo si existen
        indicadores = resultado.get("indicadores_riesgo", [])
        if indicadores:
            print(f"\n⚠️  INDICADORES DE RIESGO DETECTADOS:")
            for indicador in indicadores[:3]:  # Mostrar máximo 3
                print(f"  • {indicador}")
        
        # Mostrar contexto adicional si existe
        if 'contexto_veracidad' in resultado:
            print(f"\n🔍 Contexto: {resultado['contexto_veracidad']}")

    def mostrar_resultado_clasificacion(self, resultado: Dict):
        """
        Formatea y muestra el resultado de clasificación.
        
        Args:
            resultado: Diccionario con resultado de clasificación
        """
        categoria = resultado.get("categoria_sugerida")
        if not categoria or categoria == "NO_APLICA":
            return
        
        self.mostrar_separador("📂 CLASIFICACIÓN AUTOMÁTICA", 30)
        
        # Información principal
        emoji_categoria = self.config.obtener_emoji_categoria(categoria)
        print(f"📂 Categoría detectada: {emoji_categoria} {categoria}")
        print(f"📈 Confianza: {resultado.get('confianza', 0):.1%}")
        print(f"🤖 Método: {resultado.get('metodo_usado', 'IA Local')}")
        
        # Razones de clasificación
        if resultado.get('razones'):
            print(f"\n🔍 ¿Por qué se clasificó así?")
            for razon in resultado['razones'][:3]:  # Máximo 3 razones
                print(f"  • {razon}")
        
        # Categorías alternativas consideradas
        alternativas = resultado.get('alternativas', [])
        if alternativas:
            print(f"\n🔄 Otras categorías consideradas:")
            for alt in alternativas[:2]:  # Máximo 2 alternativas
                emoji_alt = self.config.obtener_emoji_categoria(alt)
                print(f"  • {emoji_alt} {alt}")

    def mostrar_confirmacion_procesamiento(self, resultado: Dict) -> str:
        """
        Muestra confirmación de procesamiento y retorna la respuesta del usuario.
        
        Args:
            resultado: Diccionario con información del análisis
            
        Returns:
            str: Respuesta del usuario
        """
        nivel_veracidad = resultado.get("nivel_veracidad", "MEDIA")
        nivel_urgencia = resultado.get("nivel_urgencia", "MEDIA")
        categoria = resultado.get('categoria_sugerida', 'N/A')
        metodo = resultado.get('metodo_usado', 'IA Local')
        
        self.mostrar_separador("🤔 CONFIRMACIÓN DE REGISTRO", 30)
        
        # Información del análisis
        emoji_categoria = self.config.obtener_emoji_categoria(categoria)
        print(f"📂 Categoría: {emoji_categoria} {categoria}")
        print(f"🎯 Veracidad: {nivel_veracidad}")
        print(f"⚡ Urgencia: {nivel_urgencia}")
        print(f"🤖 Método: {metodo}")
        
        # Advertencias especiales según el análisis
        self._mostrar_advertencias_especiales(nivel_veracidad, nivel_urgencia)
        
        return input("\n🔹 ¿Confirmas el registro de tu denuncia? (s/n): ").strip().lower()

    def _mostrar_advertencias_especiales(self, nivel_veracidad: str, nivel_urgencia: str):
        """Muestra advertencias especiales según el análisis."""
        if nivel_veracidad in ["MUY_BAJA", "SOSPECHOSA"]:
            self.mostrar_mensaje_advertencia(
                "Se detectaron indicadores de posible falsedad"
            )
            print("   La denuncia será marcada para revisión adicional")
        
        if nivel_urgencia == "CRÍTICA":
            print("\n🚨 URGENTE: Esta denuncia requiere atención inmediata")
            print("   Será procesada con prioridad máxima")

    def mostrar_estadisticas_tabla(self, estadisticas: Dict, total: int, agente_ia_activo: bool = True):
        """
        Muestra estadísticas en formato tabla profesional.
        
        Args:
            estadisticas: Diccionario con estadísticas por categoría
            total: Total de denuncias
            agente_ia_activo: Estado del agente IA
        """
        self.mostrar_separador("📊 ESTADÍSTICAS DE DENUNCIAS", 40)
        
        if total == 0:
            print("📭 No hay denuncias registradas aún.")
            print("💡 Las estadísticas aparecerán cuando se registren denuncias.")
            return
        
        # Información general
        print(f"📈 Total de denuncias: {total}")
        
        # Mostrar método de procesamiento
        modo_procesamiento = "🤖 Procesadas automáticamente por IA" if agente_ia_activo else "👤 Procesadas con revisión manual"
        print(f"⚙️  Método actual: {modo_procesamiento}")
        print()
        
        # Crear tabla de estadísticas
        datos_tabla = []
        for categoria, cantidad in estadisticas.items():
            porcentaje = (cantidad / total) * 100
            emoji_cat = self.config.obtener_emoji_categoria(categoria)
            
            # Barra de progreso visual simple
            barra_longitud = int(porcentaje / 5)  # Escala a 20 caracteres máximo
            barra = "█" * barra_longitud + "░" * (20 - barra_longitud)
            
            datos_tabla.append([
                f"{emoji_cat} {categoria}",
                cantidad,
                f"{porcentaje:.1f}%",
                barra
            ])
        
        # Ordenar por cantidad (descendente)
        datos_tabla.sort(key=lambda x: x[1], reverse=True)
        
        # Mostrar tabla
        headers = ["Categoría", "Cantidad", "Porcentaje", "Distribución"]
        print(tabulate(
            datos_tabla,
            headers=headers,
            tablefmt="grid",
            stralign="left"
        ))
        
        # Mostrar categoría más común
        if datos_tabla:
            categoria_principal = datos_tabla[0][0]
            cantidad_principal = datos_tabla[0][1]
            print(f"\n🏆 Categoría más frecuente: {categoria_principal} ({cantidad_principal} denuncias)")

    def mostrar_ayuda_sistema(self, categorias_disponibles: List[str]):
        """
        Muestra información de ayuda del sistema para usuarios anónimos.
        
        Args:
            categorias_disponibles: Lista de categorías disponibles
        """
        self.mostrar_separador("❓ ¿CÓMO FUNCIONA EL SISTEMA?", 40)
        
        # Sección de anonimato
        print("🔒 ANONIMATO GARANTIZADO:")
        print("   • No se solicita ni almacena información personal")
        print("   • No hay registro de usuarios")
        print("   • No se rastrea la identidad")
        print("   • Procesamiento completamente seguro")
        
        # Proceso de denuncia
        print("\n📝 PROCESO DE DENUNCIA:")
        print("   • Describe detalladamente la situación")
        print("   • El sistema clasifica automáticamente")
        print("   • Tu denuncia se guarda de forma segura")
        print("   • Los administradores pueden revisar estadísticas")
        
        # Clasificación automática
        print("\n🤖 CLASIFICACIÓN AUTOMÁTICA:")
        print("   • IA analiza el contenido de la denuncia")
        print("   • Determina la categoría apropiada")
        print("   • Evalúa el nivel de urgencia")
        print("   • Todo sin comprometer tu anonimato")
        
        # Categorías disponibles
        print("\n🛡️ CATEGORÍAS DISPONIBLES:")
        for categoria in categorias_disponibles:
            emoji = self.config.obtener_emoji_categoria(categoria)
            print(f"   • {emoji} {categoria}")
        
        # Consejos
        print("\n💡 CONSEJOS PARA UNA BUENA DENUNCIA:")
        print("   • Sé específico con fechas y lugares")
        print("   • Incluye detalles relevantes")
        print("   • Menciona si hay testigos")
        print("   • Describe el impacto de la situación")
        print("   • Proporciona contexto suficiente")
        
        # Seguridad
        print("\n🔐 GARANTÍAS DE SEGURIDAD:")
        print("   • Encriptación de datos")
        print("   • Sin logs de identificación")
        print("   • Procesamiento local cuando es posible")
        print("   • Cumplimiento con normativas de privacidad")

    def mostrar_estado_sistema(self, estado: Dict, agente_ia_activo: bool):
        """
        Muestra el estado completo del sistema para administradores.
        
        Args:
            estado: Diccionario con estado del sistema
            agente_ia_activo: Estado del agente IA
        """
        self.mostrar_separador("🔧 ESTADO DEL SISTEMA DE IA", 40)
        
        # Estado principal
        estado_agente = "✅ ACTIVADO" if agente_ia_activo else "❌ DESACTIVADO"
        print(f"🤖 Agente IA: {estado_agente}")
        
        # Componentes del sistema
        componentes = {
            'Componentes': estado.get('componentes_disponibles', False),
            'OpenAI': estado.get('openai_configurado', False),
            'Clasificador local': estado.get('clasificador_local_activo', False),
            'Analizadores': estado.get('analizadores_disponibles', False)
        }
        
        for componente, activo in componentes.items():
            icono = "✅" if activo else "❌"
            print(f"{icono} {componente}")
        
        # Estadísticas de uso si están disponibles
        if 'estadisticas' in estado:
            stats = estado['estadisticas']
            print(f"\n📊 ESTADÍSTICAS DE USO:")
            print(f"   Clasificaciones realizadas: {stats.get('clasificaciones_realizadas', 0)}")
            print(f"   Denuncias válidas: {stats.get('denuncias_validas', 0)}")
            print(f"   Precisión promedio: {stats.get('precision_promedio', 0):.1%}")
        
        # Recomendaciones según estado
        self._mostrar_recomendaciones_sistema(componentes, agente_ia_activo)

    def _mostrar_recomendaciones_sistema(self, componentes: Dict, agente_ia_activo: bool):
        """Muestra recomendaciones según el estado del sistema."""
        print(f"\n💡 RECOMENDACIONES:")
        
        if not agente_ia_activo:
            print("   • Considera activar el Agente IA para procesamiento automático")
        
        if not componentes.get('OpenAI', False):
            print("   • Configura OpenAI para clasificación más precisa (opcional)")
        
        if not componentes.get('Clasificador local', False):
            print("   • Verificar instalación del clasificador local")
        
        if all(componentes.values()) and agente_ia_activo:
            print("   • ✅ Sistema funcionando óptimamente")

class FormateadorArchivos:
    """Formatea contenido para archivos de salida."""
    
    @staticmethod
    def formatear_reporte_resumen(estadisticas: Dict, agente_ia_activo: bool) -> str:
        """
        Formatea un reporte de resumen para archivo.
        
        Args:
            estadisticas: Diccionario con estadísticas
            agente_ia_activo: Estado del agente IA
            
        Returns:
            str: Reporte formateado
        """
        from datetime import datetime
        
        total = sum(estadisticas.values()) if estadisticas else 0
        
        reporte = f"""
{"=" * 60}
📊 REPORTE DE RESUMEN - SISTEMA DE DENUNCIAS ANÓNIMAS
{"=" * 60}
📅 Fecha de generación: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
⚙️  Modo de procesamiento: {"Automático (IA)" if agente_ia_activo else "Manual"}

📋 DISTRIBUCIÓN POR CATEGORÍAS:
{"-" * 40}
"""
        
        # Agregar estadísticas por categoría
        if total > 0:
            for categoria, cantidad in sorted(estadisticas.items(), key=lambda x: x[1], reverse=True):
                porcentaje = (cantidad / total) * 100
                reporte += f"{categoria}: {cantidad} ({porcentaje:.1f}%)\n"
        else:
            reporte += "No hay denuncias registradas.\n"
        
        reporte += f"""
{"-" * 40}
📊 RESUMEN ESTADÍSTICO:
- Total de denuncias: {total}
- Categoría más frecuente: {max(estadisticas.items(), key=lambda x: x[1])[0] if estadisticas else "N/A"}
- Promedio por categoría: {total / len(estadisticas) if estadisticas else 0:.1f}
- Modo de procesamiento actual: {"Procesamiento automático con IA" if agente_ia_activo else "Procesamiento manual por supervisores"}

🔐 NOTA DE PRIVACIDAD:
Este reporte contiene únicamente estadísticas agregadas.
No se incluye información que pueda identificar a los denunciantes.
El anonimato está garantizado en todo momento.

{"=" * 60}
Fin del reporte
"""
        
        return reporte