"""
Sistema de búsqueda y filtros avanzados para denuncias.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from utils.formatters import FormateadorConsola

class BuscadorDenuncias:
    """Clase para búsqueda y filtrado avanzado de denuncias."""
    
    def __init__(self, gestor_denuncias):
        """Inicializa el buscador de denuncias."""
        self.gestor_denuncias = gestor_denuncias
        self.formatter = FormateadorConsola()
    
    def mostrar_menu_busqueda(self):
        """Muestra el menú principal de búsqueda."""
        while True:
            self.formatter.limpiar_pantalla()
            
            print("🔍 BUSCADOR DE DENUNCIAS")
            print("=" * 30)
            print("1. 🔤 Buscar por palabra clave")
            print("2. 📂 Filtrar por categoría")
            print("3. 📅 Filtrar por fecha")
            print("4. 🆕 Ver denuncias sin revisar")
            print("5. 🔍 Búsqueda combinada")
            print("6. 📊 Búsqueda por relevancia")
            print("0. ↩️ Volver al menú principal")
            
            opcion = input("\n👉 Selecciona una opción: ").strip()
            
            if opcion == "1":
                self.buscar_por_palabra_clave()
            elif opcion == "2":
                self.filtrar_por_categoria()
            elif opcion == "3":
                self.filtrar_por_fecha()
            elif opcion == "4":
                self.ver_denuncias_sin_revisar()
            elif opcion == "5":
                self.busqueda_combinada()
            elif opcion == "6":
                self.busqueda_por_relevancia()
            elif opcion == "0":
                break
            else:
                print("❌ Opción no válida")
                input("Presiona Enter para continuar...")
    
    def buscar_por_palabra_clave(self):
        """Busca denuncias por palabras clave."""
        self.formatter.limpiar_pantalla()
        
        print("🔤 BÚSQUEDA POR PALABRA CLAVE")
        print("=" * 35)
        
        palabra_clave = input("📝 Ingresa la palabra o frase a buscar: ").strip()
        
        if not palabra_clave:
            print("❌ Debes ingresar una palabra clave")
            input("Presiona Enter para continuar...")
            return
        
        resultados = self._buscar_en_contenido(palabra_clave)
        self._mostrar_resultados(resultados, f"Resultados para: '{palabra_clave}'")
    
    def filtrar_por_categoria(self):
        """Filtra denuncias por categoría específica."""
        self.formatter.limpiar_pantalla()
        
        print("📂 FILTRAR POR CATEGORÍA")
        print("=" * 25)
        
        # Obtener categorías disponibles
        categorias = self._obtener_categorias_disponibles()
        
        if not categorias:
            print("📭 No hay categorías disponibles")
            input("Presiona Enter para continuar...")
            return
        
        print("📋 Categorías disponibles:")
        for i, categoria in enumerate(categorias, 1):
            print(f"{i}. {categoria.replace('_', ' ').title()}")
        
        try:
            seleccion = int(input("\n👉 Selecciona una categoría: ")) - 1
            
            if 0 <= seleccion < len(categorias):
                categoria_seleccionada = categorias[seleccion]
                resultados = self._filtrar_por_categoria_especifica(categoria_seleccionada)
                self._mostrar_resultados(resultados, f"Categoría: {categoria_seleccionada.replace('_', ' ').title()}")
            else:
                print("❌ Selección no válida")
                input("Presiona Enter para continuar...")
        
        except ValueError:
            print("❌ Ingresa un número válido")
            input("Presiona Enter para continuar...")
    
    def filtrar_por_fecha(self):
        """Filtra denuncias por rango de fechas."""
        self.formatter.limpiar_pantalla()
        
        print("📅 FILTRAR POR FECHA")
        print("=" * 20)
        print("1. 📆 Últimos 7 días")
        print("2. 📆 Último mes")
        print("3. 📆 Últimos 3 meses")
        print("4. 📆 Rango personalizado")
        
        opcion = input("\n👉 Selecciona período: ").strip()
        
        if opcion == "1":
            fecha_inicio = datetime.now() - timedelta(days=7)
            resultados = self._filtrar_por_rango_fecha(fecha_inicio)
            self._mostrar_resultados(resultados, "Últimos 7 días")
        
        elif opcion == "2":
            fecha_inicio = datetime.now() - timedelta(days=30)
            resultados = self._filtrar_por_rango_fecha(fecha_inicio)
            self._mostrar_resultados(resultados, "Último mes")
        
        elif opcion == "3":
            fecha_inicio = datetime.now() - timedelta(days=90)
            resultados = self._filtrar_por_rango_fecha(fecha_inicio)
            self._mostrar_resultados(resultados, "Últimos 3 meses")
        
        elif opcion == "4":
            self._busqueda_fecha_personalizada()
        
        else:
            print("❌ Opción no válida")
            input("Presiona Enter para continuar...")
    
    def ver_denuncias_sin_revisar(self):
        """Muestra denuncias que aún no han sido revisadas."""
        self.formatter.limpiar_pantalla()
        
        print("🆕 DENUNCIAS SIN REVISAR")
        print("=" * 25)
        
        resultados = self._obtener_denuncias_sin_revisar()
        self._mostrar_resultados(resultados, "Denuncias pendientes de revisión")
    
    def busqueda_combinada(self):
        """Realiza búsqueda con múltiples filtros."""
        self.formatter.limpiar_pantalla()
        
        print("🔍 BÚSQUEDA COMBINADA")
        print("=" * 22)
        
        # Obtener criterios de búsqueda
        palabra_clave = input("📝 Palabra clave (opcional): ").strip()
        
        # Categoría
        categorias = self._obtener_categorias_disponibles()
        categoria_seleccionada = None
        
        if categorias:
            print("\n📂 Categorías disponibles:")
            print("0. Todas las categorías")
            for i, categoria in enumerate(categorias, 1):
                print(f"{i}. {categoria.replace('_', ' ').title()}")
            
            try:
                seleccion = int(input("👉 Selecciona categoría: "))
                if 1 <= seleccion <= len(categorias):
                    categoria_seleccionada = categorias[seleccion - 1]
            except ValueError:
                pass
        
        # Período de tiempo
        print("\n📅 Período de tiempo:")
        print("1. Últimos 7 días")
        print("2. Último mes")
        print("3. Todo el tiempo")
        
        fecha_inicio = None
        try:
            periodo = int(input("👉 Selecciona período: "))
            if periodo == 1:
                fecha_inicio = datetime.now() - timedelta(days=7)
            elif periodo == 2:
                fecha_inicio = datetime.now() - timedelta(days=30)
        except ValueError:
            pass
        
        # Realizar búsqueda combinada
        resultados = self._busqueda_combinada_logica(palabra_clave, categoria_seleccionada, fecha_inicio)
        
        # Crear descripción de filtros
        filtros = []
        if palabra_clave:
            filtros.append(f"'{palabra_clave}'")
        if categoria_seleccionada:
            filtros.append(f"categoría {categoria_seleccionada.replace('_', ' ').title()}")
        if fecha_inicio:
            dias = (datetime.now() - fecha_inicio).days
            filtros.append(f"últimos {dias} días")
        
        descripcion = "Búsqueda combinada: " + " + ".join(filtros) if filtros else "Sin filtros específicos"
        self._mostrar_resultados(resultados, descripcion)
    
    def busqueda_por_relevancia(self):
        """Busca denuncias ordenadas por relevancia/importancia."""
        self.formatter.limpiar_pantalla()
        
        print("📊 BÚSQUEDA POR RELEVANCIA")
        print("=" * 28)
        print("1. 🚨 Denuncias críticas")
        print("2. ⚡ Denuncias urgentes")
        print("3. 🎯 Alta veracidad")
        print("4. 📈 Más recientes")
        
        opcion = input("\n👉 Selecciona criterio: ").strip()
        
        if opcion == "1":
            resultados = self._obtener_denuncias_criticas()
            self._mostrar_resultados(resultados, "Denuncias críticas")
        elif opcion == "2":
            resultados = self._obtener_denuncias_urgentes()
            self._mostrar_resultados(resultados, "Denuncias urgentes")
        elif opcion == "3":
            resultados = self._obtener_alta_veracidad()
            self._mostrar_resultados(resultados, "Alta veracidad")
        elif opcion == "4":
            resultados = self._obtener_mas_recientes()
            self._mostrar_resultados(resultados, "Más recientes")
        else:
            print("❌ Opción no válida")
            input("Presiona Enter para continuar...")
    
    def _buscar_en_contenido(self, palabra_clave: str) -> List[Dict]:
        """Busca palabra clave en el contenido de las denuncias."""
        if not hasattr(self.gestor_denuncias, 'denuncias'):
            return []
        
        resultados = []
        palabra_clave_lower = palabra_clave.lower()
        
        for denuncia in self.gestor_denuncias.denuncias:
            mensaje = denuncia.get('mensaje', '').lower()
            categoria = denuncia.get('categoria', '').lower()
            
            if palabra_clave_lower in mensaje or palabra_clave_lower in categoria:
                resultados.append(denuncia)
        
        return resultados
    
    def _obtener_categorias_disponibles(self) -> List[str]:
        """Obtiene lista de categorías disponibles."""
        if not hasattr(self.gestor_denuncias, 'denuncias'):
            return []
        
        categorias = set()
        for denuncia in self.gestor_denuncias.denuncias:
            categoria = denuncia.get('categoria')
            if categoria:
                categorias.add(categoria)
        
        return sorted(list(categorias))
    
    def _filtrar_por_categoria_especifica(self, categoria: str) -> List[Dict]:
        """Filtra denuncias por una categoría específica."""
        if not hasattr(self.gestor_denuncias, 'denuncias'):
            return []
        
        resultados = []
        for denuncia in self.gestor_denuncias.denuncias:
            if denuncia.get('categoria') == categoria:
                resultados.append(denuncia)
        
        return resultados
    
    def _filtrar_por_rango_fecha(self, fecha_inicio: datetime, fecha_fin: Optional[datetime] = None) -> List[Dict]:
        """Filtra denuncias por rango de fechas."""
        if not hasattr(self.gestor_denuncias, 'denuncias'):
            return []
        
        if fecha_fin is None:
            fecha_fin = datetime.now()
        
        resultados = []
        for denuncia in self.gestor_denuncias.denuncias:
            timestamp_str = denuncia.get('timestamp', '')
            try:
                fecha_denuncia = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                if fecha_inicio <= fecha_denuncia <= fecha_fin:
                    resultados.append(denuncia)
            except (ValueError, AttributeError):
                continue
        
        return resultados
    
    def _busqueda_fecha_personalizada(self):
        """Búsqueda con rango de fechas personalizado."""
        print("\n📅 RANGO PERSONALIZADO")
        print("Formato: YYYY-MM-DD")
        
        try:
            fecha_inicio_str = input("📅 Fecha inicio: ").strip()
            fecha_fin_str = input("📅 Fecha fin (opcional): ").strip()
            
            fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
            fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d") if fecha_fin_str else datetime.now()
            
            resultados = self._filtrar_por_rango_fecha(fecha_inicio, fecha_fin)
            descripcion = f"Desde {fecha_inicio_str} hasta {fecha_fin_str or 'hoy'}"
            self._mostrar_resultados(resultados, descripcion)
        
        except ValueError:
            print("❌ Formato de fecha inválido")
            input("Presiona Enter para continuar...")
    
    def _obtener_denuncias_sin_revisar(self) -> List[Dict]:
        """Obtiene denuncias que no han sido revisadas."""
        if not hasattr(self.gestor_denuncias, 'denuncias'):
            return []
        
        resultados = []
        for denuncia in self.gestor_denuncias.denuncias:
            # Consideramos sin revisar si no tiene estado o está marcada como nueva
            estado = denuncia.get('estado', 'nueva')
            if estado in ['nueva', 'sin_revisar', None]:
                resultados.append(denuncia)
        
        return resultados
    
    def _busqueda_combinada_logica(self, palabra_clave: str, categoria: str, fecha_inicio: datetime) -> List[Dict]:
        """Lógica de búsqueda combinada con múltiples filtros."""
        if not hasattr(self.gestor_denuncias, 'denuncias'):
            return []
        
        resultados = []
        
        for denuncia in self.gestor_denuncias.denuncias:
            cumple_criterios = True
            
            # Filtro por palabra clave
            if palabra_clave:
                mensaje = denuncia.get('mensaje', '').lower()
                if palabra_clave.lower() not in mensaje:
                    cumple_criterios = False
            
            # Filtro por categoría
            if categoria and cumple_criterios:
                if denuncia.get('categoria') != categoria:
                    cumple_criterios = False
            
            # Filtro por fecha
            if fecha_inicio and cumple_criterios:
                timestamp_str = denuncia.get('timestamp', '')
                try:
                    fecha_denuncia = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    if fecha_denuncia < fecha_inicio:
                        cumple_criterios = False
                except (ValueError, AttributeError):
                    cumple_criterios = False
            
            if cumple_criterios:
                resultados.append(denuncia)
        
        return resultados
    
    def _obtener_denuncias_criticas(self) -> List[Dict]:
        """Obtiene denuncias marcadas como críticas."""
        # Esta función requeriría integración con el analizador de IA
        # Por ahora retornamos denuncias con palabras clave críticas
        palabras_criticas = ['urgente', 'crítico', 'peligro', 'amenaza', 'violencia', 'inmediato']
        resultados = []
        
        if hasattr(self.gestor_denuncias, 'denuncias'):
            for denuncia in self.gestor_denuncias.denuncias:
                mensaje = denuncia.get('mensaje', '').lower()
                if any(palabra in mensaje for palabra in palabras_criticas):
                    resultados.append(denuncia)
        
        return resultados
    
    def _obtener_denuncias_urgentes(self) -> List[Dict]:
        """Obtiene denuncias urgentes."""
        palabras_urgentes = ['urgente', 'rápido', 'pronto', 'inmediato', 'ya', 'ahora']
        resultados = []
        
        if hasattr(self.gestor_denuncias, 'denuncias'):
            for denuncia in self.gestor_denuncias.denuncias:
                mensaje = denuncia.get('mensaje', '').lower()
                if any(palabra in mensaje for palabra in palabras_urgentes):
                    resultados.append(denuncia)
        
        return resultados
    
    def _obtener_alta_veracidad(self) -> List[Dict]:
        """Obtiene denuncias con indicadores de alta veracidad."""
        indicadores_veracidad = ['evidencia', 'prueba', 'testigo', 'documento', 'fecha', 'hora', 'lugar']
        resultados = []
        
        if hasattr(self.gestor_denuncias, 'denuncias'):
            for denuncia in self.gestor_denuncias.denuncias:
                mensaje = denuncia.get('mensaje', '').lower()
                count_indicadores = sum(1 for indicador in indicadores_veracidad if indicador in mensaje)
                if count_indicadores >= 2:  # Al menos 2 indicadores
                    resultados.append(denuncia)
        
        return resultados
    
    def _obtener_mas_recientes(self) -> List[Dict]:
        """Obtiene denuncias más recientes."""
        if not hasattr(self.gestor_denuncias, 'denuncias'):
            return []
        
        # Ordenar por timestamp (más recientes primero)
        denuncias_ordenadas = sorted(
            self.gestor_denuncias.denuncias,
            key=lambda x: x.get('timestamp', ''),
            reverse=True
        )
        
        # Retornar las últimas 10
        return denuncias_ordenadas[:10]
    
    def _mostrar_resultados(self, resultados: List[Dict], titulo: str):
        """Muestra los resultados de búsqueda."""
        self.formatter.limpiar_pantalla()
        
        print(f"📋 {titulo.upper()}")
        print("=" * 50)
        
        if not resultados:
            print("📭 No se encontraron denuncias que coincidan con los criterios")
            input("\nPresiona Enter para continuar...")
            return
        
        print(f"✅ {len(resultados)} denuncia(s) encontrada(s)")
        print("-" * 30)
        
        for i, denuncia in enumerate(resultados, 1):
            print(f"\n📄 #{i} - ID: {denuncia.get('id', 'N/A')}")
            print(f"📅 Fecha: {denuncia.get('timestamp', 'N/A')[:19]}")
            print(f"📂 Categoría: {denuncia.get('categoria', 'N/A')}")
            
            mensaje = denuncia.get('mensaje', '')
            preview = mensaje[:100] + "..." if len(mensaje) > 100 else mensaje
            print(f"📝 Contenido: {preview}")
            
            if i < len(resultados):
                continuar = input("\n🔹 Ver siguiente resultado? (s/n): ").strip().lower()
                if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
                    break
                print("\n" + "-" * 50)
        
        input("\n✅ Presiona Enter para volver al menú de búsqueda...")