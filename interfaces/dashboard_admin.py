"""
Dashboard avanzado para administradores con análisis detallado.
"""

from typing import Dict, List, Any
from utils.formatters import FormateadorConsola
from src.agente_ia_simple.analizador_avanzado import AnalizadorAvanzado

class DashboardAdmin:
    """Dashboard avanzado para administradores."""
    
    def __init__(self, gestor_denuncias, gestor_roles):
        """Inicializa el dashboard."""
        self.gestor_denuncias = gestor_denuncias
        self.gestor_roles = gestor_roles
        self.formatter = FormateadorConsola()
        self.analizador = AnalizadorAvanzado()
    
    def mostrar_dashboard_principal(self):
        """Muestra el dashboard principal con resumen."""
        self.formatter.limpiar_pantalla()
        
        print("📊 DASHBOARD DE ADMINISTRACIÓN")
        print("=" * 50)
        
        # Obtener estadísticas
        stats = self.gestor_denuncias.obtener_estadisticas()
        total = stats.get('total', 0)
        
        if total == 0:
            print("📭 No hay denuncias para mostrar")
            return
        
        # Resumen general
        print(f"📈 RESUMEN GENERAL:")
        print(f"   • Total denuncias: {total}")
        print(f"   • Procesadas con IA: {stats.get('procesadas_ia', 0)}")
        print(f"   • Última actualización: {stats.get('ultima_actualizacion', 'N/A')[:19]}")
        
        # Distribución por categorías
        print(f"\n📂 DISTRIBUCIÓN POR CATEGORÍAS:")
        por_categoria = stats.get('por_categoria', {})
        for categoria, cantidad in sorted(por_categoria.items(), key=lambda x: x[1], reverse=True):
            porcentaje = (cantidad / total) * 100
            print(f"   • {categoria.replace('_', ' ').title()}: {cantidad} ({porcentaje:.1f}%)")
        
        # Análisis de calidad
        self._mostrar_analisis_calidad()
        
        input("\nPresiona Enter para continuar...")
    
    def _mostrar_analisis_calidad(self):
        """Muestra análisis de calidad de las denuncias."""
        print(f"\n🎯 ANÁLISIS DE CALIDAD:")
        
        # Obtener todas las denuncias para análisis
        if not hasattr(self.gestor_denuncias, 'denuncias'):
            print("   • No hay datos disponibles para análisis")
            return
        
        denuncias = self.gestor_denuncias.denuncias
        
        if not denuncias:
            print("   • No hay denuncias para analizar")
            return
        
        # Contadores
        spam_count = 0
        alta_veracidad = 0
        urgentes = 0
        
        for denuncia in denuncias:
            mensaje = denuncia.get('mensaje', '')
            if len(mensaje) > 0:
                analisis = self.analizador.analisis_completo(mensaje)
                
                if not analisis['es_denuncia_valida']:
                    spam_count += 1
                
                if analisis['veracidad']['nivel_veracidad'] in ['ALTA', 'MUY_ALTA']:
                    alta_veracidad += 1
                
                if analisis['urgencia']['nivel_urgencia'] in ['CRÍTICA', 'ALTA']:
                    urgentes += 1
        
        total = len(denuncias)
        print(f"   • Denuncias válidas: {total - spam_count}/{total} ({((total - spam_count)/total)*100:.1f}%)")
        print(f"   • Alta veracidad: {alta_veracidad}/{total} ({(alta_veracidad/total)*100:.1f}%)")
        print(f"   • Requieren atención urgente: {urgentes}/{total} ({(urgentes/total)*100:.1f}%)")
    
    def ver_denuncias_detalladas(self):
        """Muestra todas las denuncias con análisis detallado."""
        self.formatter.limpiar_pantalla()
        
        print("📋 DENUNCIAS DETALLADAS")
        print("=" * 40)
        
        if not hasattr(self.gestor_denuncias, 'denuncias') or not self.gestor_denuncias.denuncias:
            print("📭 No hay denuncias registradas")
            input("\nPresiona Enter para continuar...")
            return
        
        denuncias = self.gestor_denuncias.denuncias
        
        for i, denuncia in enumerate(denuncias, 1):
            self._mostrar_denuncia_individual(i, denuncia)
            
            if i < len(denuncias):
                continuar = input("\n🔹 Ver siguiente denuncia? (s/n): ").strip().lower()
                if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
                    break
                print("\n" + "="*60)
    
    def _mostrar_denuncia_individual(self, numero: int, denuncia: Dict):
        """Muestra una denuncia individual con análisis completo."""
        mensaje = denuncia.get('mensaje', '')
        
        print(f"\n📄 DENUNCIA #{numero}")
        print("-" * 30)
        print(f"🆔 ID: {denuncia.get('id', 'N/A')}")
        print(f"📅 Fecha: {denuncia.get('timestamp', 'N/A')[:19]}")
        print(f"📂 Categoría: {denuncia.get('categoria', 'N/A')}")
        print(f"🤖 Procesada con IA: {'Sí' if denuncia.get('procesada_con_ia', False) else 'No'}")
        
        # Mostrar mensaje completo
        print(f"\n📝 CONTENIDO COMPLETO:")
        print(f"   {mensaje}")
        
        # Realizar análisis avanzado si no existe
        if len(mensaje) > 0:
            print(f"\n🔍 ANÁLISIS AVANZADO:")
            analisis = self.analizador.analisis_completo(mensaje)
            
            # Estado general
            estado = "✅ VÁLIDA" if analisis['es_denuncia_valida'] else "❌ SPAM/INVÁLIDA"
            print(f"   Estado: {estado}")
            print(f"   Confianza: {analisis['confianza_validez']:.1%}")
            
            # Análisis de spam
            spam = analisis['spam']
            if spam['es_spam']:
                print(f"   🚫 SPAM: {spam['razon']}")
            
            # Análisis de veracidad
            veracidad = analisis['veracidad']
            emoji_veracidad = self._get_emoji_veracidad(veracidad['nivel_veracidad'])
            print(f"   {emoji_veracidad} Veracidad: {veracidad['nivel_veracidad']}")
            print(f"   📊 Detalles específicos: {veracidad['detalles_especificos']}")
            
            # Análisis de urgencia
            urgencia = analisis['urgencia']
            emoji_urgencia = self._get_emoji_urgencia(urgencia['nivel_urgencia'])
            print(f"   {emoji_urgencia} Urgencia: {urgencia['nivel_urgencia']}")
            
            if urgencia['indicadores_encontrados']:
                print(f"   ⚠️ Indicadores: {', '.join(urgencia['indicadores_encontrados'][:3])}")
            
            # Recomendaciones
            if analisis['requiere_atencion_inmediata']:
                print(f"   🚨 REQUIERE ATENCIÓN INMEDIATA")
            
            if analisis['requiere_revision_humana']:
                print(f"   👁️ Requiere revisión humana adicional")
    
    def _get_emoji_veracidad(self, nivel: str) -> str:
        """Retorna emoji según nivel de veracidad."""
        emojis = {
            'MUY_ALTA': '🟢',
            'ALTA': '🔵', 
            'MEDIA': '🟡',
            'BAJA': '🟠',
            'MUY_BAJA': '🔴'
        }
        return emojis.get(nivel, '⚪')
    
    def _get_emoji_urgencia(self, nivel: str) -> str:
        """Retorna emoji según nivel de urgencia."""
        emojis = {
            'CRÍTICA': '🚨',
            'ALTA': '⚡',
            'MEDIA': '📋',
            'BAJA': '📝'
        }
        return emojis.get(nivel, '📄')
    
    def filtrar_denuncias_por_estado(self):
        """Permite filtrar denuncias por estado."""
        self.formatter.limpiar_pantalla()
        
        print("🔍 FILTRAR DENUNCIAS")
        print("=" * 25)
        print("1. Ver solo denuncias válidas")
        print("2. Ver solo spam/inválidas") 
        print("3. Ver denuncias urgentes")
        print("4. Ver denuncias de alta veracidad")
        print("5. Ver todas")
        
        opcion = input("\nSelecciona filtro: ").strip()
        
        if not hasattr(self.gestor_denuncias, 'denuncias') or not self.gestor_denuncias.denuncias:
            print("📭 No hay denuncias para filtrar")
            input("\nPresiona Enter para continuar...")
            return
        
        denuncias_filtradas = self._aplicar_filtro(opcion)
        
        if not denuncias_filtradas:
            print("📭 No hay denuncias que coincidan con el filtro")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"\n📋 {len(denuncias_filtradas)} denuncias encontradas")
        print("=" * 40)
        
        for i, denuncia in enumerate(denuncias_filtradas, 1):
            self._mostrar_denuncia_individual(i, denuncia)
            
            if i < len(denuncias_filtradas):
                continuar = input("\n🔹 Ver siguiente? (s/n): ").strip().lower()
                if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
                    break
                print("\n" + "="*60)
    
    def _aplicar_filtro(self, opcion: str) -> List[Dict]:
        """Aplica filtro a las denuncias."""
        denuncias = self.gestor_denuncias.denuncias
        filtradas = []
        
        for denuncia in denuncias:
            mensaje = denuncia.get('mensaje', '')
            if len(mensaje) == 0:
                continue
            
            analisis = self.analizador.analisis_completo(mensaje)
            
            if opcion == "1" and analisis['es_denuncia_valida']:
                filtradas.append(denuncia)
            elif opcion == "2" and not analisis['es_denuncia_valida']:
                filtradas.append(denuncia)
            elif opcion == "3" and analisis['urgencia']['nivel_urgencia'] in ['CRÍTICA', 'ALTA']:
                filtradas.append(denuncia)
            elif opcion == "4" and analisis['veracidad']['nivel_veracidad'] in ['ALTA', 'MUY_ALTA']:
                filtradas.append(denuncia)
            elif opcion == "5":
                filtradas.append(denuncia)
        
        return filtradas
    
    def generar_reporte_avanzado(self):
        """Genera un reporte avanzado con análisis de IA."""
        print("\n📈 GENERANDO REPORTE AVANZADO...")
        
        if not hasattr(self.gestor_denuncias, 'denuncias') or not self.gestor_denuncias.denuncias:
            print("📭 No hay denuncias para el reporte")
            return
        
        denuncias = self.gestor_denuncias.denuncias
        
        # Análisis masivo
        analisis_resultados = []
        for denuncia in denuncias:
            mensaje = denuncia.get('mensaje', '')
            if len(mensaje) > 0:
                analisis = self.analizador.analisis_completo(mensaje)
                analisis_resultados.append({
                    'denuncia': denuncia,
                    'analisis': analisis
                })
        
        # Generar reporte
        reporte = self._generar_reporte_texto(analisis_resultados)
        
        # Guardar archivo
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"reporte_avanzado_{timestamp}.txt"
        
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                f.write(reporte)
            
            print(f"✅ Reporte generado: {nombre_archivo}")
            print("📄 Incluye análisis completo de spam, veracidad y urgencia")
            
        except Exception as e:
            print(f"❌ Error guardando reporte: {e}")
    
    def _generar_reporte_texto(self, analisis_resultados: List[Dict]) -> str:
        """Genera el texto del reporte avanzado."""
        from datetime import datetime
        
        total = len(analisis_resultados)
        validas = sum(1 for r in analisis_resultados if r['analisis']['es_denuncia_valida'])
        spam = total - validas
        
        # Contadores por nivel
        veracidad_alta = sum(1 for r in analisis_resultados 
                           if r['analisis']['veracidad']['nivel_veracidad'] in ['ALTA', 'MUY_ALTA'])
        urgentes = sum(1 for r in analisis_resultados 
                      if r['analisis']['urgencia']['nivel_urgencia'] in ['CRÍTICA', 'ALTA'])
        
        reporte = f"""
{'='*80}
📊 REPORTE AVANZADO DE ANÁLISIS DE DENUNCIAS
{'='*80}
📅 Fecha de generación: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
🤖 Análisis realizado con IA avanzada anti-spam

📈 RESUMEN EJECUTIVO:
{'-'*50}
• Total de denuncias analizadas: {total}
• Denuncias válidas: {validas} ({(validas/total)*100:.1f}%)
• Spam/Contenido inválido: {spam} ({(spam/total)*100:.1f}%)
• Alta veracidad: {veracidad_alta} ({(veracidad_alta/total)*100:.1f}%)
• Requieren atención urgente: {urgentes} ({(urgentes/total)*100:.1f}%)

🔍 ANÁLISIS DETALLADO POR DENUNCIA:
{'-'*50}
"""
        
        # Agregar cada denuncia
        for i, resultado in enumerate(analisis_resultados, 1):
            denuncia = resultado['denuncia']
            analisis = resultado['analisis']
            
            reporte += f"""
📄 DENUNCIA #{i}
ID: {denuncia.get('id', 'N/A')}
Fecha: {denuncia.get('timestamp', 'N/A')[:19]}
Categoría: {denuncia.get('categoria', 'N/A')}

📝 Contenido: {denuncia.get('mensaje', '')[:200]}{"..." if len(denuncia.get('mensaje', '')) > 200 else ""}

🎯 Análisis:
• Válida: {'SÍ' if analisis['es_denuncia_valida'] else 'NO'}
• Veracidad: {analisis['veracidad']['nivel_veracidad']}
• Urgencia: {analisis['urgencia']['nivel_urgencia']}
• Requiere atención: {'SÍ' if analisis['requiere_atencion_inmediata'] else 'NO'}

{'-'*60}
"""
        
        reporte += f"""
🔐 NOTA DE CONFIDENCIALIDAD:
Este reporte contiene análisis automatizado de denuncias anónimas.
Se mantiene la confidencialidad de los denunciantes en todo momento.
El análisis de IA es una herramienta de apoyo, no un juicio definitivo.

{'='*80}
Fin del reporte
"""
        
        return reporte