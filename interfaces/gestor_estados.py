"""
Gestor de estados para denuncias con seguimiento y historial.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
from utils.formatters import FormateadorConsola

class EstadoDenuncia(Enum):
    """Estados disponibles para las denuncias."""
    NUEVA = "nueva"
    REVISADA = "revisada"
    EN_PROCESO = "en_proceso"
    RESUELTA = "resuelta"
    ARCHIVADA = "archivada"

class GestorEstados:
    """Gestor para manejar estados de denuncias."""
    
    def __init__(self, gestor_denuncias):
        """Inicializa el gestor de estados."""
        self.gestor_denuncias = gestor_denuncias
        self.formatter = FormateadorConsola()
        
        # Configuración de estados
        self.estados_info = {
            EstadoDenuncia.NUEVA: {
                "emoji": "🆕",
                "color": "nuevo",
                "descripcion": "Denuncia recién recibida"
            },
            EstadoDenuncia.REVISADA: {
                "emoji": "👁️",
                "color": "revisado",
                "descripcion": "Denuncia revisada por administrador"
            },
            EstadoDenuncia.EN_PROCESO: {
                "emoji": "⚙️",
                "color": "proceso",
                "descripcion": "Denuncia en proceso de investigación"
            },
            EstadoDenuncia.RESUELTA: {
                "emoji": "✅",
                "color": "resuelto",
                "descripcion": "Denuncia resuelta exitosamente"
            },
            EstadoDenuncia.ARCHIVADA: {
                "emoji": "📁",
                "color": "archivado",
                "descripcion": "Denuncia archivada"
            }
        }
    
    def mostrar_menu_estados(self):
        """Muestra el menú principal de gestión de estados."""
        while True:
            self.formatter.limpiar_pantalla()
            
            print("📊 GESTIÓN DE ESTADOS")
            print("=" * 25)
            print("1. 📋 Ver dashboard de estados")
            print("2. 🔄 Cambiar estado de denuncia")
            print("3. 📊 Filtrar por estado")
            print("4. ⏱️ Ver historial de cambios")
            print("5. 📈 Estadísticas por estado")
            print("6. 🔍 Buscar denuncias por estado")
            print("7. ⚡ Gestión rápida de estados")
            print("0. ↩️ Volver al menú principal")
            
            opcion = input("\n👉 Selecciona una opción: ").strip()
            
            if opcion == "1":
                self.mostrar_dashboard_estados()
            elif opcion == "2":
                self.cambiar_estado_denuncia()
            elif opcion == "3":
                self.filtrar_por_estado()
            elif opcion == "4":
                self.ver_historial_cambios()
            elif opcion == "5":
                self.mostrar_estadisticas()
            elif opcion == "6":
                self.buscar_por_estado()
            elif opcion == "7":
                self.gestion_rapida_estados()
            elif opcion == "0":
                break
            else:
                print("❌ Opción no válida")
                input("Presiona Enter para continuar...")
    
    def mostrar_dashboard_estados(self):
        """Muestra un dashboard completo con información de estados."""
        self.formatter.limpiar_pantalla()
        
        print("📊 DASHBOARD DE ESTADOS")
        print("=" * 30)
        
        if not hasattr(self.gestor_denuncias, 'denuncias') or not self.gestor_denuncias.denuncias:
            print("📭 No hay denuncias para mostrar")
            input("\nPresiona Enter para continuar...")
            return
        
        # Contar denuncias por estado
        contadores = self._contar_por_estado()
        total = sum(contadores.values())
        
        print(f"📈 RESUMEN GENERAL: {total} denuncias")
        print("-" * 40)
        
        # Mostrar contadores por estado
        for estado in EstadoDenuncia:
            cantidad = contadores.get(estado.value, 0)
            porcentaje = (cantidad / total * 100) if total > 0 else 0
            info = self.estados_info[estado]
            
            print(f"{info['emoji']} {estado.value.replace('_', ' ').title()}: {cantidad} ({porcentaje:.1f}%)")
        
        # Alertas importantes
        print(f"\n🚨 ALERTAS:")
        nuevas = contadores.get('nueva', 0)
        en_proceso = contadores.get('en_proceso', 0)
        
        if nuevas > 5:
            print(f"   ⚠️ {nuevas} denuncias nuevas requieren atención")
        if en_proceso > 10:
            print(f"   ⚠️ {en_proceso} denuncias en proceso (revisar progreso)")
        if nuevas == 0 and en_proceso == 0:
            print(f"   ✅ Todo al día - no hay pendientes críticos")
        
        # Denuncias más antiguas sin procesar
        print(f"\n⏰ DENUNCIAS MÁS ANTIGUAS SIN PROCESAR:")
        denuncias_pendientes = self._obtener_denuncias_pendientes()
        
        if denuncias_pendientes:
            for i, denuncia in enumerate(denuncias_pendientes[:3], 1):
                fecha = denuncia.get('timestamp', '')[:19]
                categoria = denuncia.get('categoria', 'N/A')
                print(f"   {i}. {fecha} - {categoria}")
        else:
            print("   ✅ No hay denuncias pendientes")
        
        input("\n✅ Presiona Enter para continuar...")
    
    def cambiar_estado_denuncia(self):
        """Permite cambiar el estado de una denuncia específica."""
        self.formatter.limpiar_pantalla()
        
        print("🔄 CAMBIAR ESTADO DE DENUNCIA")
        print("=" * 35)
        
        if not hasattr(self.gestor_denuncias, 'denuncias') or not self.gestor_denuncias.denuncias:
            print("📭 No hay denuncias disponibles")
            input("Presiona Enter para continuar...")
            return
        
        # Listar denuncias disponibles
        print("📋 DENUNCIAS DISPONIBLES:")
        for i, denuncia in enumerate(self.gestor_denuncias.denuncias, 1):
            estado_actual = denuncia.get('estado', 'nueva')
            emoji = self.estados_info.get(EstadoDenuncia(estado_actual), {}).get('emoji', '❓')
            fecha = denuncia.get('timestamp', '')[:19]
            categoria = denuncia.get('categoria', 'N/A')
            
            print(f"{i}. {emoji} [{estado_actual.replace('_', ' ').title()}] - {fecha} - {categoria}")
        
        try:
            seleccion = int(input("\n👉 Selecciona denuncia (número): ")) - 1
            
            if 0 <= seleccion < len(self.gestor_denuncias.denuncias):
                denuncia_seleccionada = self.gestor_denuncias.denuncias[seleccion]
                self._cambiar_estado_individual(denuncia_seleccionada, seleccion)
            else:
                print("❌ Selección no válida")
                input("Presiona Enter para continuar...")
        
        except ValueError:
            print("❌ Ingresa un número válido")
            input("Presiona Enter para continuar...")
    
    def _cambiar_estado_individual(self, denuncia: Dict, indice: int):
        """Cambia el estado de una denuncia individual."""
        estado_actual = denuncia.get('estado', 'nueva')
        
        print(f"\n📄 DENUNCIA SELECCIONADA:")
        print(f"   📅 Fecha: {denuncia.get('timestamp', '')[:19]}")
        print(f"   📂 Categoría: {denuncia.get('categoria', 'N/A')}")
        print(f"   📊 Estado actual: {estado_actual.replace('_', ' ').title()}")
        
        mensaje = denuncia.get('mensaje', '')
        preview = mensaje[:100] + "..." if len(mensaje) > 100 else mensaje
        print(f"   📝 Contenido: {preview}")
        
        print(f"\n🔄 NUEVOS ESTADOS DISPONIBLES:")
        estados_validos = []
        
        for i, estado in enumerate(EstadoDenuncia, 1):
            if estado.value != estado_actual:
                info = self.estados_info[estado]
                print(f"{i}. {info['emoji']} {estado.value.replace('_', ' ').title()} - {info['descripcion']}")
                estados_validos.append(estado)
        
        try:
            seleccion_estado = int(input("\n👉 Selecciona nuevo estado: ")) - 1
            
            if 0 <= seleccion_estado < len(estados_validos):
                nuevo_estado = estados_validos[seleccion_estado]
                
                # Solicitar comentario opcional
                comentario = input("💬 Comentario sobre el cambio (opcional): ").strip()
                
                # Confirmar cambio
                confirmar = input(f"\n✅ ¿Confirmar cambio a '{nuevo_estado.value.replace('_', ' ').title()}'? (s/n): ").strip().lower()
                
                if confirmar in ['s', 'si', 'sí', 'y', 'yes']:
                    self._ejecutar_cambio_estado(denuncia, indice, nuevo_estado.value, comentario)
                    print("✅ Estado cambiado exitosamente")
                else:
                    print("❌ Cambio cancelado")
            else:
                print("❌ Selección no válida")
        
        except ValueError:
            print("❌ Ingresa un número válido")
        
        input("Presiona Enter para continuar...")
    
    def _ejecutar_cambio_estado(self, denuncia: Dict, indice: int, nuevo_estado: str, comentario: str = ""):
        """Ejecuta el cambio de estado y registra el historial."""
        estado_anterior = denuncia.get('estado', 'nueva')
        timestamp_cambio = datetime.now().isoformat()
        
        # Actualizar estado en la denuncia
        denuncia['estado'] = nuevo_estado
        denuncia['ultima_modificacion'] = timestamp_cambio
        
        # Crear entrada de historial
        if 'historial_estados' not in denuncia:
            denuncia['historial_estados'] = []
        
        entrada_historial = {
            'timestamp': timestamp_cambio,
            'estado_anterior': estado_anterior,
            'estado_nuevo': nuevo_estado,
            'comentario': comentario,
            'usuario': 'administrador'
        }
        
        denuncia['historial_estados'].append(entrada_historial)
        
        # Guardar cambios
        if hasattr(self.gestor_denuncias, 'guardar_denuncias'):
            self.gestor_denuncias.guardar_denuncias()
    
    def filtrar_por_estado(self):
        """Filtra y muestra denuncias por estado específico."""
        self.formatter.limpiar_pantalla()
        
        print("📊 FILTRAR POR ESTADO")
        print("=" * 22)
        
        # Mostrar estados disponibles
        print("📋 Estados disponibles:")
        for i, estado in enumerate(EstadoDenuncia, 1):
            info = self.estados_info[estado]
            print(f"{i}. {info['emoji']} {estado.value.replace('_', ' ').title()}")
        
        try:
            seleccion = int(input("\n👉 Selecciona estado: ")) - 1
            estados_lista = list(EstadoDenuncia)
            
            if 0 <= seleccion < len(estados_lista):
                estado_seleccionado = estados_lista[seleccion]
                denuncias_filtradas = self._obtener_por_estado(estado_seleccionado.value)
                self._mostrar_denuncias_por_estado(denuncias_filtradas, estado_seleccionado)
            else:
                print("❌ Selección no válida")
                input("Presiona Enter para continuar...")
        
        except ValueError:
            print("❌ Ingresa un número válido")
            input("Presiona Enter para continuar...")
    
    def ver_historial_cambios(self):
        """Muestra el historial de cambios de estados."""
        self.formatter.limpiar_pantalla()
        
        print("⏱️ HISTORIAL DE CAMBIOS")
        print("=" * 25)
        
        cambios_recientes = self._obtener_historial_reciente()
        
        if not cambios_recientes:
            print("📭 No hay historial de cambios disponible")
            input("Presiona Enter para continuar...")
            return
        
        print(f"📈 ÚLTIMOS {len(cambios_recientes)} CAMBIOS:")
        print("-" * 50)
        
        for cambio in cambios_recientes:
            fecha = cambio['timestamp'][:19]
            anterior = cambio['estado_anterior'].replace('_', ' ').title()
            nuevo = cambio['estado_nuevo'].replace('_', ' ').title()
            comentario = cambio.get('comentario', '')
            
            print(f"📅 {fecha}")
            print(f"   🔄 {anterior} → {nuevo}")
            if comentario:
                print(f"   💬 {comentario}")
            print("-" * 30)
        
        input("\n✅ Presiona Enter para continuar...")
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas detalladas por estado."""
        self.formatter.limpiar_pantalla()
        
        print("📈 ESTADÍSTICAS POR ESTADO")
        print("=" * 30)
        
        contadores = self._contar_por_estado()
        total = sum(contadores.values())
        
        if total == 0:
            print("📭 No hay denuncias para analizar")
            input("Presiona Enter para continuar...")
            return
        
        print(f"📊 ANÁLISIS DETALLADO ({total} denuncias):")
        print("-" * 40)
        
        for estado in EstadoDenuncia:
            cantidad = contadores.get(estado.value, 0)
            porcentaje = (cantidad / total * 100) if total > 0 else 0
            info = self.estados_info[estado]
            
            # Barra visual simple
            barra_longitud = int(porcentaje / 5)  # Cada 5% = 1 caracter
            barra = "█" * barra_longitud + "░" * (20 - barra_longitud)
            
            print(f"{info['emoji']} {estado.value.replace('_', ' ').title()}")
            print(f"   {barra} {cantidad:3d} ({porcentaje:5.1f}%)")
            print()
        
        # Métricas adicionales
        print("🎯 MÉTRICAS DE RENDIMIENTO:")
        resueltas = contadores.get('resuelta', 0)
        tasa_resolucion = (resueltas / total * 100) if total > 0 else 0
        print(f"   ✅ Tasa de resolución: {tasa_resolucion:.1f}%")
        
        pendientes = contadores.get('nueva', 0) + contadores.get('en_proceso', 0)
        print(f"   ⏳ Denuncias pendientes: {pendientes}")
        
        input("\n✅ Presiona Enter para continuar...")
    
    def buscar_por_estado(self):
        """Búsqueda rápida por estado con opciones adicionales."""
        self.formatter.limpiar_pantalla()
        
        print("🔍 BÚSQUEDA POR ESTADO")
        print("=" * 24)
        print("1. 🆕 Solo denuncias nuevas")
        print("2. ⚙️ Solo en proceso")
        print("3. ✅ Solo resueltas")
        print("4. 👁️ Solo revisadas")
        print("5. 📁 Solo archivadas")
        print("6. 🔄 Comparar dos estados")
        
        opcion = input("\n👉 Selecciona opción: ").strip()
        
        if opcion == "1":
            resultados = self._obtener_por_estado('nueva')
            self._mostrar_denuncias_por_estado(resultados, EstadoDenuncia.NUEVA)
        elif opcion == "2":
            resultados = self._obtener_por_estado('en_proceso')
            self._mostrar_denuncias_por_estado(resultados, EstadoDenuncia.EN_PROCESO)
        elif opcion == "3":
            resultados = self._obtener_por_estado('resuelta')
            self._mostrar_denuncias_por_estado(resultados, EstadoDenuncia.RESUELTA)
        elif opcion == "4":
            resultados = self._obtener_por_estado('revisada')
            self._mostrar_denuncias_por_estado(resultados, EstadoDenuncia.REVISADA)
        elif opcion == "5":
            resultados = self._obtener_por_estado('archivada')
            self._mostrar_denuncias_por_estado(resultados, EstadoDenuncia.ARCHIVADA)
        elif opcion == "6":
            self._comparar_estados()
        else:
            print("❌ Opción no válida")
            input("Presiona Enter para continuar...")
    
    def gestion_rapida_estados(self):
        """Gestión rápida de múltiples estados."""
        self.formatter.limpiar_pantalla()
        
        print("⚡ GESTIÓN RÁPIDA DE ESTADOS")
        print("=" * 33)
        print("1. 🔄 Marcar todas las nuevas como revisadas")
        print("2. ✅ Resolver denuncias en proceso (selección múltiple)")
        print("3. 📁 Archivar denuncias resueltas antiguas")
        print("4. 🆕 Resetear estados problemáticos")
        
        opcion = input("\n👉 Selecciona acción: ").strip()
        
        if opcion == "1":
            self._marcar_nuevas_como_revisadas()
        elif opcion == "2":
            self._resolver_multiples()
        elif opcion == "3":
            self._archivar_antiguas()
        elif opcion == "4":
            self._resetear_problematicos()
        else:
            print("❌ Opción no válida")
            input("Presiona Enter para continuar...")
    
    def _contar_por_estado(self) -> Dict[str, int]:
        """Cuenta denuncias por estado."""
        contadores = {}
        
        if hasattr(self.gestor_denuncias, 'denuncias'):
            for denuncia in self.gestor_denuncias.denuncias:
                estado = denuncia.get('estado', 'nueva')
                contadores[estado] = contadores.get(estado, 0) + 1
        
        return contadores
    
    def _obtener_denuncias_pendientes(self) -> List[Dict]:
        """Obtiene denuncias pendientes ordenadas por antigüedad."""
        if not hasattr(self.gestor_denuncias, 'denuncias'):
            return []
        
        pendientes = []
        for denuncia in self.gestor_denuncias.denuncias:
            estado = denuncia.get('estado', 'nueva')
            if estado in ['nueva', 'en_proceso']:
                pendientes.append(denuncia)
        
        # Ordenar por timestamp (más antiguos primero)
        pendientes.sort(key=lambda x: x.get('timestamp', ''))
        
        return pendientes
    
    def _obtener_por_estado(self, estado: str) -> List[Dict]:
        """Obtiene denuncias por estado específico."""
        if not hasattr(self.gestor_denuncias, 'denuncias'):
            return []
        
        return [d for d in self.gestor_denuncias.denuncias if d.get('estado', 'nueva') == estado]
    
    def _obtener_historial_reciente(self, limite: int = 10) -> List[Dict]:
        """Obtiene historial reciente de cambios."""
        cambios = []
        
        if hasattr(self.gestor_denuncias, 'denuncias'):
            for denuncia in self.gestor_denuncias.denuncias:
                historial = denuncia.get('historial_estados', [])
                cambios.extend(historial)
        
        # Ordenar por timestamp más reciente
        cambios.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return cambios[:limite]
    
    def _mostrar_denuncias_por_estado(self, denuncias: List[Dict], estado: EstadoDenuncia):
        """Muestra denuncias filtradas por estado."""
        self.formatter.limpiar_pantalla()
        
        info = self.estados_info[estado]
        titulo = f"{info['emoji']} {estado.value.replace('_', ' ').title()}"
        
        print(f"📋 {titulo.upper()}")
        print("=" * 50)
        
        if not denuncias:
            print(f"📭 No hay denuncias en estado '{estado.value.replace('_', ' ')}'")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"✅ {len(denuncias)} denuncia(s) encontrada(s)")
        print("-" * 30)
        
        for i, denuncia in enumerate(denuncias, 1):
            fecha = denuncia.get('timestamp', '')[:19]
            categoria = denuncia.get('categoria', 'N/A')
            
            print(f"\n📄 #{i} - {fecha}")
            print(f"📂 Categoría: {categoria}")
            
            mensaje = denuncia.get('mensaje', '')
            preview = mensaje[:100] + "..." if len(mensaje) > 100 else mensaje
            print(f"📝 Contenido: {preview}")
            
            # Mostrar última modificación si existe
            if 'ultima_modificacion' in denuncia:
                print(f"🔄 Última modificación: {denuncia['ultima_modificacion'][:19]}")
            
            if i < len(denuncias):
                continuar = input("\n🔹 Ver siguiente? (s/n): ").strip().lower()
                if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
                    break
                print("\n" + "-" * 50)
        
        input(f"\n✅ Presiona Enter para volver al menú...")
    
    def _marcar_nuevas_como_revisadas(self):
        """Marca todas las denuncias nuevas como revisadas."""
        nuevas = self._obtener_por_estado('nueva')
        
        if not nuevas:
            print("📭 No hay denuncias nuevas para marcar")
            input("Presiona Enter para continuar...")
            return
        
        print(f"🔄 Se marcarán {len(nuevas)} denuncias como revisadas")
        confirmar = input("¿Continuar? (s/n): ").strip().lower()
        
        if confirmar in ['s', 'si', 'sí', 'y', 'yes']:
            for denuncia in nuevas:
                indice = self.gestor_denuncias.denuncias.index(denuncia)
                self._ejecutar_cambio_estado(denuncia, indice, 'revisada', 'Marcado masivamente como revisada')
            
            print(f"✅ {len(nuevas)} denuncias marcadas como revisadas")
        else:
            print("❌ Operación cancelada")
        
        input("Presiona Enter para continuar...")
    
    def _resolver_multiples(self):
        """Permite resolver múltiples denuncias en proceso."""
        en_proceso = self._obtener_por_estado('en_proceso')
        
        if not en_proceso:
            print("📭 No hay denuncias en proceso")
            input("Presiona Enter para continuar...")
            return
        
        print(f"⚙️ DENUNCIAS EN PROCESO ({len(en_proceso)}):")
        for i, denuncia in enumerate(en_proceso, 1):
            fecha = denuncia.get('timestamp', '')[:19]
            categoria = denuncia.get('categoria', 'N/A')
            print(f"{i}. {fecha} - {categoria}")
        
        indices = input("\n📝 Números a resolver (ej: 1,3,5): ").strip()
        
        try:
            selecciones = [int(x.strip()) - 1 for x in indices.split(',')]
            denuncias_a_resolver = [en_proceso[i] for i in selecciones if 0 <= i < len(en_proceso)]
            
            if denuncias_a_resolver:
                comentario = input("💬 Comentario de resolución: ").strip()
                
                for denuncia in denuncias_a_resolver:
                    indice = self.gestor_denuncias.denuncias.index(denuncia)
                    self._ejecutar_cambio_estado(denuncia, indice, 'resuelta', comentario)
                
                print(f"✅ {len(denuncias_a_resolver)} denuncias resueltas")
            else:
                print("❌ No se seleccionaron denuncias válidas")
        
        except ValueError:
            print("❌ Formato inválido")
        
        input("Presiona Enter para continuar...")
    
    def _archivar_antiguas(self):
        """Archiva denuncias resueltas antiguas."""
        resueltas = self._obtener_por_estado('resuelta')
        
        # Filtrar las que tienen más de 30 días resueltas
        from datetime import timedelta
        limite_fecha = datetime.now() - timedelta(days=30)
        
        antiguas = []
        for denuncia in resueltas:
            if 'ultima_modificacion' in denuncia:
                try:
                    fecha_mod = datetime.fromisoformat(denuncia['ultima_modificacion'])
                    if fecha_mod < limite_fecha:
                        antiguas.append(denuncia)
                except ValueError:
                    continue
        
        if not antiguas:
            print("📭 No hay denuncias antiguas para archivar")
            input("Presiona Enter para continuar...")
            return
        
        print(f"📁 Se archivarán {len(antiguas)} denuncias resueltas hace más de 30 días")
        confirmar = input("¿Continuar? (s/n): ").strip().lower()
        
        if confirmar in ['s', 'si', 'sí', 'y', 'yes']:
            for denuncia in antiguas:
                indice = self.gestor_denuncias.denuncias.index(denuncia)
                self._ejecutar_cambio_estado(denuncia, indice, 'archivada', 'Archivado automáticamente (>30 días resuelto)')
            
            print(f"✅ {len(antiguas)} denuncias archivadas")
        else:
            print("❌ Operación cancelada")
        
        input("Presiona Enter para continuar...")
    
    def _resetear_problematicos(self):
        """Resetea estados problemáticos o corruptos."""
        print("🔧 RESETEO DE ESTADOS PROBLEMÁTICOS")
        print("Esta función revisar denuncias sin estado válido")
        
        problematicas = []
        estados_validos = [e.value for e in EstadoDenuncia]
        
        if hasattr(self.gestor_denuncias, 'denuncias'):
            for denuncia in self.gestor_denuncias.denuncias:
                estado = denuncia.get('estado', 'nueva')
                if estado not in estados_validos:
                    problematicas.append(denuncia)
        
        if not problematicas:
            print("✅ No se encontraron estados problemáticos")
            input("Presiona Enter para continuar...")
            return
        
        print(f"⚠️ {len(problematicas)} denuncias con estados inválidos")
        confirmar = input("¿Resetear a 'nueva'? (s/n): ").strip().lower()
        
        if confirmar in ['s', 'si', 'sí', 'y', 'yes']:
            for denuncia in problematicas:
                indice = self.gestor_denuncias.denuncias.index(denuncia)
                self._ejecutar_cambio_estado(denuncia, indice, 'nueva', 'Estado reseteado por inconsistencia')
            
            print(f"✅ {len(problematicas)} estados corregidos")
        else:
            print("❌ Operación cancelada")
        
        input("Presiona Enter para continuar...")
    
    def _comparar_estados(self):
        """Compara denuncias entre dos estados."""
        print("\n🔄 COMPARAR ESTADOS")
        print("Selecciona dos estados para comparar")
        
        # Implementación básica para comparar estados
        # Se puede expandir según necesidades específicas
        print("⚠️ Función en desarrollo")
        input("Presiona Enter para continuar...")