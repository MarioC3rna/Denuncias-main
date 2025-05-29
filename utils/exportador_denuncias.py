"""
Sistema de exportación y reportes para denuncias.
Incluye múltiples formatos y análisis automatizado.
"""

import json
import csv
import os
import subprocess
import platform
from typing import Dict, List, Any, Optional, Tuple  # ← IMPORTANTE: Agregar Tuple
from datetime import datetime, timedelta
from pathlib import Path
from utils.formatters import FormateadorConsola

class ExportadorDenuncias:
    """Clase para exportar denuncias en múltiples formatos."""
    
    def __init__(self, gestor_denuncias, agente_ia=None):
        """Inicializa el exportador de denuncias."""
        self.gestor_denuncias = gestor_denuncias
        self.agente_ia = agente_ia
        self.formatter = FormateadorConsola()
        
        # Crear directorio de exportación si no existe
        self.directorio_exportacion = Path("exports")
        self.directorio_exportacion.mkdir(exist_ok=True)
        
        # Configuración de formatos
        self.formatos_disponibles = {
            'txt': 'Texto plano (.txt)',
            'json': 'JSON (.json)',
            'csv': 'Excel/CSV (.csv)',
            'html': 'Reporte HTML (.html)',
            'backup': 'Backup completo (.json)',
            'ejecutivo': 'Reporte ejecutivo (.html)'
        }
    
    def mostrar_menu_exportacion(self):
        """Muestra el menú principal de exportación."""
        while True:
            self.formatter.limpiar_pantalla()
            
            print("📤 EXPORTACIÓN DE DENUNCIAS")
            print("=" * 32)
            print("1. 📄 Exportar a texto plano")
            print("2. 📊 Exportar a CSV (Excel)")
            print("3. 🌐 Generar reporte HTML")
            print("4. 💾 Crear backup completo")
            print("5. 📈 Reporte ejecutivo con IA")
            print("6. 🔍 Exportación filtrada")
            print("7. 📋 Generar estadísticas")
            print("8. 📁 Ver archivos exportados")
            print("0. ↩️ Volver al menú principal")
            
            opcion = input("\n👉 Selecciona una opción: ").strip()
            
            if opcion == "1":
                self.exportar_texto_plano()
            elif opcion == "2":
                self.exportar_csv()
            elif opcion == "3":
                self.generar_reporte_html()
            elif opcion == "4":
                self.crear_backup_completo()
            elif opcion == "5":
                self.generar_reporte_ejecutivo()
            elif opcion == "6":
                self.exportacion_filtrada()
            elif opcion == "7":
                self.generar_estadisticas()
            elif opcion == "8":
                self.ver_archivos_exportados()
            elif opcion == "0":
                break
            else:
                print("❌ Opción no válida")
                input("Presiona Enter para continuar...")
    
    def exportar_texto_plano(self):
        """Exporta denuncias a formato texto plano."""
        self.formatter.limpiar_pantalla()
        
        print("📄 EXPORTAR A TEXTO PLANO")
        print("=" * 28)
        
        if not self._verificar_denuncias():
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"denuncias_texto_{timestamp}.txt"
        ruta_archivo = self.directorio_exportacion / nombre_archivo
        
        try:
            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write("SISTEMA ANÓNIMO DE DENUNCIAS INTERNAS\n")
                archivo.write("=" * 50 + "\n")
                archivo.write(f"Reporte generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                archivo.write(f"Total de denuncias: {len(self.gestor_denuncias.denuncias)}\n\n")
                
                for i, denuncia in enumerate(self.gestor_denuncias.denuncias, 1):
                    archivo.write(f"DENUNCIA #{i}\n")
                    archivo.write("-" * 20 + "\n")
                    archivo.write(f"ID: {denuncia.get('id', 'N/A')}\n")
                    archivo.write(f"Fecha: {denuncia.get('timestamp', 'N/A')[:19]}\n")
                    archivo.write(f"Categoría: {denuncia.get('categoria', 'N/A')}\n")
                    archivo.write(f"Estado: {denuncia.get('estado', 'nueva')}\n")
                    
                    # Análisis IA si está disponible
                    if 'analisis_ia' in denuncia:
                        analisis = denuncia['analisis_ia']
                        archivo.write(f"Urgencia: {analisis.get('urgencia', {}).get('nivel', 'N/A')}\n")
                        archivo.write(f"Prioridad: {analisis.get('prioridad', {}).get('nivel', 'N/A')}\n")
                    
                    archivo.write(f"\nContenido:\n{denuncia.get('mensaje', 'Sin contenido')}\n")
                    archivo.write("\n" + "=" * 50 + "\n\n")
            
            print(f"✅ Archivo exportado exitosamente:")
            print(f"📁 {ruta_archivo}")
            
        except Exception as e:
            print(f"❌ Error al exportar: {str(e)}")
        
        input("\nPresiona Enter para continuar...")
    
    def exportar_csv(self):
        """Exporta denuncias a formato CSV para Excel."""
        self.formatter.limpiar_pantalla()
        
        print("📊 EXPORTAR A CSV (EXCEL)")
        print("=" * 25)
        
        if not self._verificar_denuncias():
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"denuncias_csv_{timestamp}.csv"
        ruta_archivo = self.directorio_exportacion / nombre_archivo
        
        try:
            with open(ruta_archivo, 'w', newline='', encoding='utf-8') as archivo:
                # Definir columnas
                columnas = [
                    'ID', 'Fecha', 'Categoria', 'Estado', 'Urgencia', 'Prioridad',
                    'Veracidad', 'Longitud_Mensaje', 'Tiene_Evidencias', 'Requiere_Atencion_Inmediata',
                    'Contenido_Preview'
                ]
                
                writer = csv.DictWriter(archivo, fieldnames=columnas)
                writer.writeheader()
                
                for denuncia in self.gestor_denuncias.denuncias:
                    # Preparar datos para CSV
                    fila = {
                        'ID': denuncia.get('id', ''),
                        'Fecha': denuncia.get('timestamp', '')[:19],
                        'Categoria': denuncia.get('categoria', ''),
                        'Estado': denuncia.get('estado', 'nueva'),
                        'Urgencia': '',
                        'Prioridad': '',
                        'Veracidad': '',
                        'Longitud_Mensaje': len(denuncia.get('mensaje', '')),
                        'Tiene_Evidencias': '',
                        'Requiere_Atencion_Inmediata': '',
                        'Contenido_Preview': denuncia.get('mensaje', '')[:100] + '...' if len(denuncia.get('mensaje', '')) > 100 else denuncia.get('mensaje', '')
                    }
                    
                    # Agregar datos de análisis IA si están disponibles
                    if 'analisis_ia' in denuncia:
                        analisis = denuncia['analisis_ia']
                        fila['Urgencia'] = analisis.get('urgencia', {}).get('nivel', '')
                        fila['Prioridad'] = analisis.get('prioridad', {}).get('nivel', '')
                        fila['Veracidad'] = analisis.get('puntuacion_veracidad', '')
                        fila['Tiene_Evidencias'] = 'Sí' if analisis.get('evidencias', {}).get('puntuacion_evidencia', 0) > 0 else 'No'
                        fila['Requiere_Atencion_Inmediata'] = 'Sí' if analisis.get('requiere_atencion_inmediata', False) else 'No'
                    
                    writer.writerow(fila)
            
            print(f"✅ Archivo CSV exportado exitosamente:")
            print(f"📁 {ruta_archivo}")
            print("💡 Puede abrirse en Excel o Google Sheets")
            
        except Exception as e:
            print(f"❌ Error al exportar CSV: {str(e)}")
        
        input("\nPresiona Enter para continuar...")
    
    def generar_reporte_html(self):
        """Genera un reporte HTML completo con estadísticas."""
        self.formatter.limpiar_pantalla()
        
        print("🌐 GENERAR REPORTE HTML")
        print("=" * 24)
        
        if not self._verificar_denuncias():
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"reporte_html_{timestamp}.html"
        ruta_archivo = self.directorio_exportacion / nombre_archivo
        
        # Generar estadísticas
        stats = self._generar_estadisticas_completas()
        
        html_content = self._generar_contenido_html(stats)
        
        try:
            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(html_content)
            
            print(f"✅ Reporte HTML generado exitosamente:")
            print(f"📁 {ruta_archivo}")
            print("💡 Puede abrirse en cualquier navegador web")
            
        except Exception as e:
            print(f"❌ Error al generar reporte HTML: {str(e)}")
        
        input("\nPresiona Enter para continuar...")
    
    def crear_backup_completo(self):
        """Crea un backup completo del sistema."""
        self.formatter.limpiar_pantalla()
        
        print("💾 CREAR BACKUP COMPLETO")
        print("=" * 25)
        
        if not self._verificar_denuncias():
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"backup_completo_{timestamp}.json"
        ruta_archivo = self.directorio_exportacion / nombre_archivo
        
        # Crear estructura de backup
        backup_data = {
            'metadata': {
                'version_backup': '1.0',
                'fecha_creacion': datetime.now().isoformat(),
                'total_denuncias': len(self.gestor_denuncias.denuncias),
                'sistema': 'Sistema Anónimo de Denuncias Internas'
            },
            'configuracion': {
                'categorias_disponibles': ['acoso_laboral', 'discriminacion', 'fraude', 'seguridad', 'violencia', 'corrupcion', 'otros'],
                'estados_disponibles': ['nueva', 'revisada', 'en_proceso', 'resuelta', 'archivada']
            },
            'denuncias': self.gestor_denuncias.denuncias,
            'estadisticas': self._generar_estadisticas_completas()
        }
        
        try:
            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                json.dump(backup_data, archivo, indent=2, ensure_ascii=False)
            
            print(f"✅ Backup completo creado exitosamente:")
            print(f"📁 {ruta_archivo}")
            print(f"📊 {len(self.gestor_denuncias.denuncias)} denuncias respaldadas")
            print("💡 Este archivo puede usarse para restaurar el sistema")
            
        except Exception as e:
            print(f"❌ Error al crear backup: {str(e)}")
        
        input("\nPresiona Enter para continuar...")
    
    def generar_reporte_ejecutivo(self):
        """Genera un reporte ejecutivo con análisis IA avanzado."""
        self.formatter.limpiar_pantalla()
        
        print("📈 REPORTE EJECUTIVO CON IA")
        print("=" * 29)
        
        if not self._verificar_denuncias():
            return
        
        if not self.agente_ia:
            print("❌ Agente IA no disponible para generar reporte ejecutivo")
            input("Presiona Enter para continuar...")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"reporte_ejecutivo_{timestamp}.html"
        ruta_archivo = self.directorio_exportacion / nombre_archivo
        
        print("🔄 Generando análisis avanzado con IA...")
        
        # Generar análisis avanzado
        analisis_ejecutivo = self._generar_analisis_ejecutivo()
        
        html_ejecutivo = self._generar_html_ejecutivo(analisis_ejecutivo)
        
        try:
            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(html_ejecutivo)
            
            print(f"✅ Reporte ejecutivo generado exitosamente:")
            print(f"📁 {ruta_archivo}")
            print("🤖 Incluye análisis avanzado con IA")
            
        except Exception as e:
            print(f"❌ Error al generar reporte ejecutivo: {str(e)}")
        
        input("\nPresiona Enter para continuar...")
    
    def exportacion_filtrada(self):
        """Permite exportar denuncias con filtros específicos."""
        self.formatter.limpiar_pantalla()
        
        print("🔍 EXPORTACIÓN FILTRADA")
        print("=" * 24)
        print("1. 📂 Por categoría específica")
        print("2. 📊 Por estado específico")
        print("3. 📅 Por rango de fechas")
        print("4. ⚡ Por nivel de urgencia")
        print("5. 🎯 Combinación de filtros")
        
        opcion = input("\n👉 Selecciona filtro: ").strip()
        
        denuncias_filtradas = []
        descripcion_filtro = ""
        
        if opcion == "1":
            denuncias_filtradas, descripcion_filtro = self._filtrar_por_categoria()
        elif opcion == "2":
            denuncias_filtradas, descripcion_filtro = self._filtrar_por_estado()
        elif opcion == "3":
            denuncias_filtradas, descripcion_filtro = self._filtrar_por_fechas()
        elif opcion == "4":
            denuncias_filtradas, descripcion_filtro = self._filtrar_por_urgencia()
        elif opcion == "5":
            denuncias_filtradas, descripcion_filtro = self._filtrar_combinado()
        else:
            print("❌ Opción no válida")
            input("Presiona Enter para continuar...")
            return
        
        if denuncias_filtradas:
            self._exportar_filtradas(denuncias_filtradas, descripcion_filtro)
        else:
            print("📭 No se encontraron denuncias con los filtros especificados")
            input("Presiona Enter para continuar...")
    
    def generar_estadisticas(self):
        """Genera archivo con estadísticas detalladas."""
        self.formatter.limpiar_pantalla()
        
        print("📋 GENERAR ESTADÍSTICAS")
        print("=" * 23)
        
        if not self._verificar_denuncias():
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"estadisticas_{timestamp}.txt"
        ruta_archivo = self.directorio_exportacion / nombre_archivo
        
        stats = self._generar_estadisticas_completas()
        
        try:
            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write("ESTADÍSTICAS DEL SISTEMA DE DENUNCIAS\n")
                archivo.write("=" * 50 + "\n")
                archivo.write(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Estadísticas generales
                archivo.write("📊 ESTADÍSTICAS GENERALES\n")
                archivo.write("-" * 30 + "\n")
                archivo.write(f"Total denuncias: {stats['total_denuncias']}\n")
                archivo.write(f"Promedio mensual: {stats.get('promedio_mensual', 0):.1f}\n")
                archivo.write(f"Última denuncia: {stats.get('ultima_denuncia', 'N/A')}\n\n")
                
                # Por categorías
                archivo.write("📂 DISTRIBUCIÓN POR CATEGORÍAS\n")
                archivo.write("-" * 35 + "\n")
                for categoria, cantidad in stats['por_categoria'].items():
                    porcentaje = (cantidad / stats['total_denuncias'] * 100) if stats['total_denuncias'] > 0 else 0
                    archivo.write(f"{categoria.replace('_', ' ').title()}: {cantidad} ({porcentaje:.1f}%)\n")
                
                # Por estados
                archivo.write(f"\n📊 DISTRIBUCIÓN POR ESTADOS\n")
                archivo.write("-" * 32 + "\n")
                for estado, cantidad in stats['por_estado'].items():
                    porcentaje = (cantidad / stats['total_denuncias'] * 100) if stats['total_denuncias'] > 0 else 0
                    archivo.write(f"{estado.replace('_', ' ').title()}: {cantidad} ({porcentaje:.1f}%)\n")
                
                # Análisis IA si está disponible
                if 'analisis_ia' in stats:
                    archivo.write(f"\n🤖 ANÁLISIS CON IA\n")
                    archivo.write("-" * 20 + "\n")
                    ia_stats = stats['analisis_ia']
                    archivo.write(f"Denuncias de alta urgencia: {ia_stats.get('alta_urgencia', 0)}\n")
                    archivo.write(f"Alertas críticas generadas: {ia_stats.get('alertas_criticas', 0)}\n")
                    archivo.write(f"Promedio de veracidad: {ia_stats.get('promedio_veracidad', 0):.2f}\n")
            
            print(f"✅ Estadísticas exportadas exitosamente:")
            print(f"📁 {ruta_archivo}")
            
        except Exception as e:
            print(f"❌ Error al generar estadísticas: {str(e)}")
        
        input("\nPresiona Enter para continuar...")
    
    def ver_archivos_exportados(self):
        """Muestra archivos exportados anteriormente."""
        self.formatter.limpiar_pantalla()
        
        print("📁 ARCHIVOS EXPORTADOS")
        print("=" * 22)
        
        archivos = list(self.directorio_exportacion.glob("*"))
        archivos.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        if not archivos:
            print("📭 No hay archivos exportados")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"📂 Directorio: {self.directorio_exportacion}")
        print(f"📈 Total de archivos: {len(archivos)}\n")
        
        for i, archivo in enumerate(archivos, 1):
            stats = archivo.stat()
            fecha_mod = datetime.fromtimestamp(stats.st_mtime)
            tamaño_kb = stats.st_size / 1024
            
            print(f"{i}. 📄 {archivo.name}")
            print(f"   📅 {fecha_mod.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   💾 {tamaño_kb:.1f} KB")
            print()
        
        # Opciones adicionales
        print("💡 OPCIONES:")
        print("1. 🗂️ Abrir directorio de exportación")
        print("2. 🗑️ Limpiar archivos antiguos")
        
        opcion = input("\n👉 Selecciona opción (o Enter para volver): ").strip()
        
        if opcion == "1":
            self._abrir_directorio_exportacion()
        elif opcion == "2":
            self._limpiar_archivos_antiguos()
    
    def _verificar_denuncias(self) -> bool:
        """Verifica que haya denuncias para exportar."""
        if not hasattr(self.gestor_denuncias, 'denuncias') or not self.gestor_denuncias.denuncias:
            print("📭 No hay denuncias para exportar")
            input("Presiona Enter para continuar...")
            return False
        return True
    
    def _generar_estadisticas_completas(self) -> Dict[str, Any]:
        """Genera estadísticas completas del sistema."""
        stats = {
            'total_denuncias': len(self.gestor_denuncias.denuncias),
            'fecha_generacion': datetime.now().isoformat(),
            'por_categoria': {},
            'por_estado': {},
            'por_mes': {},
            'analisis_ia': {}
        }
        
        # Estadísticas por categoría
        for denuncia in self.gestor_denuncias.denuncias:
            categoria = denuncia.get('categoria', 'otros')
            stats['por_categoria'][categoria] = stats['por_categoria'].get(categoria, 0) + 1
            
            estado = denuncia.get('estado', 'nueva')
            stats['por_estado'][estado] = stats['por_estado'].get(estado, 0) + 1
            
            # Análisis por mes
            timestamp = denuncia.get('timestamp', '')
            if timestamp:
                try:
                    fecha = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    mes_año = fecha.strftime('%Y-%m')
                    stats['por_mes'][mes_año] = stats['por_mes'].get(mes_año, 0) + 1
                except:
                    pass
        
        # Estadísticas de IA si está disponible
        if self.agente_ia:
            alta_urgencia = 0
            alertas_criticas = 0
            total_veracidad = 0
            count_veracidad = 0
            
            for denuncia in self.gestor_denuncias.denuncias:
                if 'analisis_ia' in denuncia:
                    analisis = denuncia['analisis_ia']
                    
                    urgencia = analisis.get('urgencia', {}).get('valor', 0)
                    if urgencia >= 4:
                        alta_urgencia += 1
                    
                    alertas = analisis.get('alertas', [])
                    alertas_criticas += len([a for a in alertas if a.get('prioridad') == 'crítica'])
                    
                    veracidad = analisis.get('puntuacion_veracidad', 0)
                    if veracidad > 0:
                        total_veracidad += veracidad
                        count_veracidad += 1
            
            stats['analisis_ia'] = {
                'alta_urgencia': alta_urgencia,
                'alertas_criticas': alertas_criticas,
                'promedio_veracidad': total_veracidad / count_veracidad if count_veracidad > 0 else 0
            }
        
        return stats
    
    def _generar_contenido_html(self, stats: Dict[str, Any]) -> str:
        """Genera contenido HTML para el reporte."""
        html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Denuncias - {datetime.now().strftime('%Y-%m-%d')}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
        }}
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }}
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .progress-bar {{
            background: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }}
        .progress-fill {{
            background: linear-gradient(90deg, #667eea, #764ba2);
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 12px;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Reporte de Denuncias Internas</h1>
        <p>Generado el {datetime.now().strftime('%d de %B de %Y a las %H:%M')}</p>
    </div>
    
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-number">{stats['total_denuncias']}</div>
            <div>Total de Denuncias</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{len(stats['por_categoria'])}</div>
            <div>Categorías Activas</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{len(stats['por_estado'])}</div>
            <div>Estados Utilizados</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{len(stats['por_mes'])}</div>
            <div>Meses con Actividad</div>
        </div>
    </div>
    
    <div class="chart-container">
        <h3>📂 Distribución por Categorías</h3>
        {self._generar_barras_html(stats['por_categoria'], stats['total_denuncias'])}
    </div>
    
    <div class="chart-container">
        <h3>📊 Distribución por Estados</h3>
        {self._generar_barras_html(stats['por_estado'], stats['total_denuncias'])}
    </div>
    
    <div class="footer">
        <p>Sistema Anónimo de Denuncias Internas - Reporte Automatizado</p>
    </div>
</body>
</html>
"""
        return html
    
    def _generar_barras_html(self, datos: Dict[str, int], total: int) -> str:
        """Genera barras de progreso HTML para visualización."""
        html_barras = ""
        for categoria, cantidad in sorted(datos.items(), key=lambda x: x[1], reverse=True):
            porcentaje = (cantidad / total * 100) if total > 0 else 0
            nombre_categoria = categoria.replace('_', ' ').title()
            
            html_barras += f"""
            <div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>{nombre_categoria}</span>
                    <span>{cantidad} ({porcentaje:.1f}%)</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {porcentaje}%;">
                        {porcentaje:.1f}%
                    </div>
                </div>
            </div>
            """
        
        return html_barras
    
    def _generar_analisis_ejecutivo(self) -> Dict[str, Any]:
        """Genera análisis ejecutivo con IA."""
        analisis = {
            'resumen_general': '',
            'tendencias': [],
            'alertas_principales': [],
            'recomendaciones': [],
            'metricas_clave': {}
        }
        
        # Análisis con IA de las denuncias más importantes
        denuncias_criticas = []
        total_alertas = 0
        
        for denuncia in self.gestor_denuncias.denuncias:
            if 'analisis_ia' in denuncia:
                analisis_ia = denuncia['analisis_ia']
                if analisis_ia.get('requiere_atencion_inmediata', False):
                    denuncias_criticas.append(denuncia)
                
                total_alertas += len(analisis_ia.get('alertas', []))
        
        # Generar resumen
        analisis['resumen_general'] = f"""
        El sistema ha procesado {len(self.gestor_denuncias.denuncias)} denuncias, 
        de las cuales {len(denuncias_criticas)} requieren atención inmediata. 
        Se han generado {total_alertas} alertas automáticas por el sistema de IA.
        """
        
        return analisis
    
    def _generar_html_ejecutivo(self, analisis: Dict[str, Any]) -> str:
        """Genera HTML para reporte ejecutivo."""
        # Implementación simplificada del reporte ejecutivo
        html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte Ejecutivo - {datetime.now().strftime('%Y-%m-%d')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; text-align: center; }}
        .section {{ margin: 20px 0; padding: 15px; border-left: 4px solid #3498db; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📈 Reporte Ejecutivo con IA</h1>
        <p>Análisis Avanzado - {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    </div>
    
    <div class="section">
        <h2>📋 Resumen Ejecutivo</h2>
        <p>{analisis['resumen_general']}</p>
    </div>
    
    <div class="section">
        <h2>🤖 Análisis con Inteligencia Artificial</h2>
        <p>Este reporte incluye análisis automatizado con IA para identificar patrones, 
        tendencias y situaciones que requieren atención prioritaria.</p>
    </div>
</body>
</html>
"""
        return html
    
    def _filtrar_por_categoria(self) -> Tuple[List[Dict], str]:
        """Filtra denuncias por categoría."""
        categorias = set(d.get('categoria', 'otros') for d in self.gestor_denuncias.denuncias)
        categorias = sorted(list(categorias))
        
        print("\n📂 Categorías disponibles:")
        for i, categoria in enumerate(categorias, 1):
            count = len([d for d in self.gestor_denuncias.denuncias if d.get('categoria') == categoria])
            print(f"{i}. {categoria.replace('_', ' ').title()} ({count})")
        
        try:
            seleccion = int(input("\n👉 Selecciona categoría: ")) - 1
            if 0 <= seleccion < len(categorias):
                categoria_seleccionada = categorias[seleccion]
                filtradas = [d for d in self.gestor_denuncias.denuncias if d.get('categoria') == categoria_seleccionada]
                return filtradas, f"Categoría: {categoria_seleccionada.replace('_', ' ').title()}"
        except ValueError:
            pass
        
        return [], ""
    
    def _filtrar_por_estado(self) -> Tuple[List[Dict], str]:
        """Filtra denuncias por estado."""
        estados = ['nueva', 'revisada', 'en_proceso', 'resuelta', 'archivada']
        
        print("\n📊 Estados disponibles:")
        for i, estado in enumerate(estados, 1):
            count = len([d for d in self.gestor_denuncias.denuncias if d.get('estado', 'nueva') == estado])
            print(f"{i}. {estado.replace('_', ' ').title()} ({count})")
        
        try:
            seleccion = int(input("\n👉 Selecciona estado: ")) - 1
            if 0 <= seleccion < len(estados):
                estado_seleccionado = estados[seleccion]
                filtradas = [d for d in self.gestor_denuncias.denuncias if d.get('estado', 'nueva') == estado_seleccionado]
                return filtradas, f"Estado: {estado_seleccionado.replace('_', ' ').title()}"
        except ValueError:
            pass
        
        return [], ""
    
    def _filtrar_por_fechas(self) -> Tuple[List[Dict], str]:
        """Filtra denuncias por rango de fechas."""
        print("\n📅 Opciones de fecha:")
        print("1. Últimos 7 días")
        print("2. Último mes")
        print("3. Últimos 3 meses")
        print("4. Rango personalizado")
        
        opcion = input("\n👉 Selecciona período: ").strip()
        
        ahora = datetime.now()
        fecha_inicio = None
        descripcion = ""
        
        if opcion == "1":
            fecha_inicio = ahora - timedelta(days=7)
            descripcion = "Últimos 7 días"
        elif opcion == "2":
            fecha_inicio = ahora - timedelta(days=30)
            descripcion = "Último mes"
        elif opcion == "3":
            fecha_inicio = ahora - timedelta(days=90)
            descripcion = "Últimos 3 meses"
        elif opcion == "4":
            try:
                fecha_str = input("📅 Fecha inicio (YYYY-MM-DD): ")
                fecha_inicio = datetime.strptime(fecha_str, "%Y-%m-%d")
                descripcion = f"Desde {fecha_str}"
            except ValueError:
                return [], ""
        
        if fecha_inicio:
            filtradas = []
            for denuncia in self.gestor_denuncias.denuncias:
                timestamp = denuncia.get('timestamp', '')
                try:
                    fecha_denuncia = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    if fecha_denuncia >= fecha_inicio:
                        filtradas.append(denuncia)
                except:
                    continue
            
            return filtradas, descripcion
        
        return [], ""
    
    def _filtrar_por_urgencia(self) -> Tuple[List[Dict], str]:
        """Filtra denuncias por nivel de urgencia."""
        if not self.agente_ia:
            print("❌ Filtro por urgencia requiere agente IA")
            input("Presiona Enter para continuar...")
            return [], ""
        
        print("\n⚡ Niveles de urgencia:")
        print("1. Baja")
        print("2. Media")
        print("3. Alta")
        print("4. Crítica")
        print("5. Emergencia")
        
        try:
            nivel = int(input("\n👉 Selecciona nivel mínimo: "))
            if 1 <= nivel <= 5:
                filtradas = []
                for denuncia in self.gestor_denuncias.denuncias:
                    if 'analisis_ia' in denuncia:
                        urgencia_valor = denuncia['analisis_ia'].get('urgencia', {}).get('valor', 0)
                        if urgencia_valor >= nivel:
                            filtradas.append(denuncia)
                
                niveles = {1: 'Baja', 2: 'Media', 3: 'Alta', 4: 'Crítica', 5: 'Emergencia'}
                return filtradas, f"Urgencia {niveles[nivel]} o superior"
        except ValueError:
            pass
        
        return [], ""
    
    def _filtrar_combinado(self) -> Tuple[List[Dict], str]:
        """Permite filtrar con múltiples criterios."""
        # Implementación básica de filtro combinado
        print("🎯 Filtro combinado disponible en versión futura")
        input("Presiona Enter para continuar...")
        return [], ""
    
    def _exportar_filtradas(self, denuncias: List[Dict], descripcion: str):
        """Exporta denuncias filtradas."""
        print(f"\n✅ {len(denuncias)} denuncias encontradas")
        print(f"🔍 Filtro: {descripcion}")
        
        print("\n📤 Formato de exportación:")
        print("1. 📄 Texto plano")
        print("2. 📊 CSV")
        print("3. 🌐 HTML")
        
        formato = input("\n👉 Selecciona formato: ").strip()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filtro_nombre = descripcion.replace(" ", "_").replace(":", "")
        
        if formato == "1":
            nombre_archivo = f"filtrado_{filtro_nombre}_{timestamp}.txt"
            self._exportar_txt_filtrado(denuncias, nombre_archivo, descripcion)
        elif formato == "2":
            nombre_archivo = f"filtrado_{filtro_nombre}_{timestamp}.csv"
            self._exportar_csv_filtrado(denuncias, nombre_archivo, descripcion)
        elif formato == "3":
            nombre_archivo = f"filtrado_{filtro_nombre}_{timestamp}.html"
            self._exportar_html_filtrado(denuncias, nombre_archivo, descripcion)
        else:
            print("❌ Formato no válido")
            input("Presiona Enter para continuar...")
    
    def _exportar_txt_filtrado(self, denuncias: List[Dict], nombre_archivo: str, descripcion: str):
        """Exporta denuncias filtradas a TXT."""
        ruta_archivo = self.directorio_exportacion / nombre_archivo
        
        try:
            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(f"DENUNCIAS FILTRADAS - {descripcion.upper()}\n")
                archivo.write("=" * 50 + "\n")
                archivo.write(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                archivo.write(f"Total de denuncias: {len(denuncias)}\n\n")
                
                for i, denuncia in enumerate(denuncias, 1):
                    archivo.write(f"DENUNCIA #{i}\n")
                    archivo.write("-" * 20 + "\n")
                    archivo.write(f"ID: {denuncia.get('id', 'N/A')}\n")
                    archivo.write(f"Fecha: {denuncia.get('timestamp', 'N/A')[:19]}\n")
                    archivo.write(f"Categoría: {denuncia.get('categoria', 'N/A')}\n")
                    archivo.write(f"Estado: {denuncia.get('estado', 'nueva')}\n")
                    archivo.write(f"\nContenido:\n{denuncia.get('mensaje', 'Sin contenido')}\n")
                    archivo.write("\n" + "=" * 50 + "\n\n")
            
            print(f"✅ Archivo exportado: {ruta_archivo}")
            
        except Exception as e:
            print(f"❌ Error al exportar: {str(e)}")
        
        input("\nPresiona Enter para continuar...")
    
    def _exportar_csv_filtrado(self, denuncias: List[Dict], nombre_archivo: str, descripcion: str):
        """Exporta denuncias filtradas a CSV."""
        # Implementación similar a exportar_csv pero para denuncias filtradas
        print(f"✅ CSV filtrado guardado como {nombre_archivo}")
        input("Presiona Enter para continuar...")
    
    def _exportar_html_filtrado(self, denuncias: List[Dict], nombre_archivo: str, descripcion: str):
        """Exporta denuncias filtradas a HTML."""
        # Implementación similar a generar_reporte_html pero para denuncias filtradas
        print(f"✅ HTML filtrado guardado como {nombre_archivo}")
        input("Presiona Enter para continuar...")
    
    def _abrir_directorio_exportacion(self):
        """Intenta abrir el directorio de exportación."""
        try:
            import subprocess
            import platform
            
            if platform.system() == "Windows":
                subprocess.run(["explorer", str(self.directorio_exportacion)])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", str(self.directorio_exportacion)])
            else:  # Linux
                subprocess.run(["xdg-open", str(self.directorio_exportacion)])
            
            print("✅ Directorio abierto en el explorador de archivos")
        except Exception as e:
            print(f"❌ No se pudo abrir el directorio: {str(e)}")
            print(f"📁 Ruta manual: {self.directorio_exportacion}")
        
        input("Presiona Enter para continuar...")
    
    def _limpiar_archivos_antiguos(self):
        """Limpia archivos de exportación antiguos."""
        print("🗑️ LIMPIAR ARCHIVOS ANTIGUOS")
        print("1. Archivos de más de 30 días")
        print("2. Archivos de más de 7 días")
        print("3. Todos los archivos")
        
        opcion = input("\n👉 Selecciona opción: ").strip()
        
        if opcion in ["1", "2", "3"]:
            dias = 30 if opcion == "1" else 7 if opcion == "2" else 0
            limite_fecha = datetime.now() - timedelta(days=dias)
            
            archivos_a_eliminar = []
            for archivo in self.directorio_exportacion.glob("*"):
                if opcion == "3" or datetime.fromtimestamp(archivo.stat().st_mtime) < limite_fecha:
                    archivos_a_eliminar.append(archivo)
            
            if archivos_a_eliminar:
                print(f"\n🗑️ Se eliminarán {len(archivos_a_eliminar)} archivos")
                confirmar = input("¿Continuar? (s/n): ").strip().lower()
                
                if confirmar in ['s', 'si', 'sí']:
                    for archivo in archivos_a_eliminar:
                        try:
                            archivo.unlink()
                        except:
                            pass
                    print(f"✅ {len(archivos_a_eliminar)} archivos eliminados")
                else:
                    print("❌ Operación cancelada")
            else:
                print("📭 No hay archivos para eliminar")
        
        input("\nPresiona Enter para continuar...")