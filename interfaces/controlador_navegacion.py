"""Controlador de navegación discreto y limpio.
Interfaz simple para usuarios, acceso discreto para administradores.
"""

import os
from typing import Optional

class ControladorNavegacion:
    """Controla la navegación entre diferentes tipos de menú."""
    
    def __init__(self, gestor_denuncias, gestor_roles):
        """
        Inicializa el controlador de navegación.
        
        Args:
            gestor_denuncias: Instancia del gestor de denuncias
            gestor_roles: Instancia del gestor de roles
        """
        self.gestor_denuncias = gestor_denuncias
        self.gestor_roles = gestor_roles
        
        # Importar aquí para evitar circulares
        from utils.formatters import FormateadorConsola
        from config.settings import ConfiguracionSistema
        
        self.formatter = FormateadorConsola()
        self.config = ConfiguracionSistema()
        
        self.usuario_actual = None
        self.es_admin = False
        
        # Códigos discretos para administrador
        self.CODIGOS_ADMIN = ["admin2024", "sistema123", "denuncias_admin"]
    
    def ejecutar_navegacion_principal(self):
        """Ejecuta el loop principal de navegación del sistema."""
        try:
            while True:
                tipo_usuario = self.mostrar_menu_seleccion_rol()
                
                if tipo_usuario is None:
                    break  # Salir del sistema
                
                # Manejar flujos directamente aquí
                if tipo_usuario == "anonimo":
                    self._manejar_flujo_anonimo()
                elif tipo_usuario == "administrador":
                    self._manejar_flujo_administrador()
        
            self._mostrar_despedida()
        
        except KeyboardInterrupt:
            self._mostrar_despedida()
        except Exception as e:
            print(f"\n❌ Error en el sistema: {e}")
            print("💡 Por favor, contacta al soporte técnico")
    
    def mostrar_menu_seleccion_rol(self) -> Optional[str]:
        """
        Muestra el menú de selección de rol con acceso discreto.
        
        Returns:
            str: Tipo de usuario seleccionado ('anonimo', 'administrador') o None para salir
        """
        while True:
            try:
                self.formatter.limpiar_pantalla()
                
                # Banner limpio y discreto
                print("🔒 SISTEMA DE DENUNCIAS INTERNAS")
                print("=" * 40)
                print("📝 Reporta situaciones de manera anónima")
                print("🛡️  Tu identidad está protegida")
                print("=" * 40)
                print()
                
                # Menú simplificado SIN opción visible de administrador
                print("📋 ¿Qué deseas hacer?")
                print("1. 📝 Enviar una denuncia")
                print("2. 📊 Ver estadísticas públicas") 
                print("3. ❓ Ayuda y soporte")
                print("4. 🚪 Salir")
                print()
                
                # Input que puede capturar códigos discretos
                opcion = input("Selecciona una opción: ").strip()
                
                # 🔐 VERIFICAR CÓDIGOS DISCRETOS DE ADMINISTRADOR
                if opcion in self.CODIGOS_ADMIN:
                    if self._acceso_administrador_discreto():
                        return "administrador"
                    else:
                        continue  # Volver al menú si falla autenticación
                
                # Opciones normales de usuario
                elif opcion == "1":
                    return "anonimo"  # Ir a flujo de denuncia
                elif opcion == "2":
                    self._mostrar_estadisticas_publicas()
                    continue  # Volver al menú
                elif opcion == "3":
                    self._mostrar_ayuda()
                    continue  # Volver al menú
                elif opcion == "4":
                    return None  # Salir
                else:
                    print("❌ Opción no válida. Presiona Enter para continuar...")
                    input()
                    continue
                    
            except KeyboardInterrupt:
                print("\n\n👋 Saliendo del sistema...")
                return None
            except Exception as e:
                print(f"\nError inesperado: {e}")
                continue
    
    def _manejar_flujo_anonimo(self):
        """Maneja el flujo completo para usuarios anónimos."""
        while True:
            self.formatter.limpiar_pantalla()
            
            print("📝 ENVIAR DENUNCIA ANÓNIMA")
            print("=" * 30)
            print("🛡️  Tu identidad permanecerá anónima")
            print("🔒 La información será tratada confidencialmente")
            print()
            
            print("📋 Describe la situación que deseas reportar:")
            print("(Escribe tu denuncia en múltiples líneas)")
            print("(Presiona Enter en una línea vacía para enviar)")
            print()
            
            # Capturar denuncia
            lineas = []
            print("💬 Tu denuncia:")
            while True:
                try:
                    linea = input("   ")
                    if linea.strip() == "":
                        if len(lineas) > 0:
                            break
                        else:
                            print("   (Escribe algo antes de enviar)")
                            continue
                    lineas.append(linea)
                except KeyboardInterrupt:
                    print("\n\n❌ Envío de denuncia cancelado")
                    return
            
            mensaje = "\n".join(lineas)
            
            print("\n🔄 Procesando tu denuncia...")
            
            # Registrar denuncia
            try:
                resultado = self.gestor_denuncias.registrar_denuncia(mensaje)
                
                self.formatter.limpiar_pantalla()
                
                if resultado.get('exito', False):
                    print("✅ DENUNCIA ENVIADA EXITOSAMENTE")
                    print("=" * 35)
                    print(f"📋 ID de seguimiento: {resultado.get('id_denuncia', 'N/A')}")
                    print(f"📂 Categoría detectada: {resultado.get('categoria', 'Por clasificar')}")
                    print(f"📅 Fecha de registro: {resultado.get('timestamp', 'N/A')[:19]}")
                    print()
                    print("💡 INFORMACIÓN IMPORTANTE:")
                    print("   • Tu denuncia ha sido registrada de forma anónima")
                    print("   • Será revisada por el equipo correspondiente")
                    print("   • Puedes usar el ID para dar seguimiento")
                    print("   • La confidencialidad está garantizada")
                else:
                    print("❌ ERROR AL ENVIAR LA DENUNCIA")
                    print("=" * 30)
                    print(f"Razón: {resultado.get('error', 'Error desconocido')}")
                    print("💡 Por favor, intenta nuevamente")
                
            except Exception as e:
                print("❌ ERROR INESPERADO")
                print("=" * 20)
                print(f"Error: {e}")
                print("💡 Contacta al soporte técnico")
            
            print("\n" + "=" * 40)
            print("📋 ¿Qué deseas hacer ahora?")
            print("1. Enviar otra denuncia")
            print("2. Volver al menú principal")
            print("3. Salir del sistema")
            
            while True:
                siguiente = input("\nSelecciona una opción: ").strip()
                if siguiente == "1":
                    break  # Continuar loop para nueva denuncia
                elif siguiente == "2":
                    return  # Volver al menú principal
                elif siguiente == "3":
                    exit()  # Salir completamente
                else:
                    print("❌ Opción no válida")
    
    def _manejar_flujo_administrador(self):
        """Maneja el flujo completo para administradores."""
        try:
            # LLAMAR AL MENÚ AVANZADO EN LUGAR DEL BÁSICO
            self._menu_administrador()  # ← ESTA es la línea clave
        
        except ImportError as e:
            print(f"⚠️ Funcionalidades avanzadas no disponibles: {e}")
            print("🔄 Usando menú básico...")
            input("Presiona Enter para continuar...")
            self._menu_administrador_basico()
        except Exception as e:
            print(f"❌ Error en menú administrador: {e}")
            print("🔄 Usando menú básico...")
            input("Presiona Enter para continuar...")
            self._menu_administrador_basico()
    
        # Cerrar sesión admin
        if hasattr(self.gestor_roles, 'cerrar_sesion'):
            self.gestor_roles.cerrar_sesion()
        self.es_admin = False
    
    def _menu_administrador_basico(self):
        """Menú básico de administrador si no existe el completo."""
        while True:
            self.formatter.limpiar_pantalla()
            
            print("👨‍💼 PANEL DE ADMINISTRADOR")
            print("=" * 30)
            
            # Información básica del sistema
            try:
                stats = self.gestor_denuncias.obtener_estadisticas()
                print(f"📊 Total denuncias: {stats.get('total', 0)}")
                
                info_agente = self.gestor_denuncias.obtener_info_agente_ia()
                if info_agente.get('disponible', False):
                    print("🤖 Agente IA: ACTIVO")
                else:
                    print("⚠️ Agente IA: MODO BÁSICO")
            except Exception as e:
                print(f"⚠️ Error obteniendo información: {e}")
            
            print()
            print("📋 OPCIONES ADMINISTRATIVAS:")
            print("1. 📊 Ver estadísticas detalladas")
            print("2. 📝 Ver todas las denuncias")
            print("3. 🤖 Información del agente IA")
            print("4. 🚪 Volver al menú principal")
            print()
            
            opcion = input("Selecciona una opción: ").strip()
            
            if opcion == "1":
                self._mostrar_estadisticas_admin()
            elif opcion == "2":
                self._ver_todas_denuncias()
            elif opcion == "3":
                self._info_agente_ia()
            elif opcion == "4":
                break
            else:
                print("❌ Opción no válida")
                input("Presiona Enter para continuar...")
    
    def _acceso_administrador_discreto(self) -> bool:
        """
        Maneja el acceso discreto de administrador.
        
        Returns:
            bool: True si autenticación exitosa, False si falla
        """
        self.formatter.limpiar_pantalla()
        
        print("🔐 ACCESO ADMINISTRATIVO")
        print("=" * 30)
        print()
        
        # Verificación adicional con contraseña
        password = input("Contraseña de administrador: ").strip()
        
        # Contraseñas válidas (simplificado para testing)
        passwords_validos = ["admin", "admin123", "administrador"]
        
        if password in passwords_validos:
            print("✅ Acceso concedido")
            self.es_admin = True
            input("\nPresiona Enter para continuar...")
            return True
        else:
            print("❌ Acceso denegado")
            print("🔒 Regresando al menú principal...")
            input("Presiona Enter para continuar...")
            return False
    
    def _mostrar_estadisticas_publicas(self):
        """Muestra estadísticas básicas para usuarios."""
        self.formatter.limpiar_pantalla()
        
        print("📊 ESTADÍSTICAS PÚBLICAS")
        print("=" * 25)
        print()
        
        try:
            stats = self.gestor_denuncias.obtener_estadisticas()
            
            print(f"📝 Total de denuncias recibidas: {stats.get('total', 0)}")
            
            if stats.get('por_categoria'):
                print("\n📂 Por categoría:")
                for categoria, cantidad in stats['por_categoria'].items():
                    categoria_display = categoria.replace('_', ' ').title()
                    print(f"   • {categoria_display}: {cantidad}")
            
            if stats.get('ultima_actualizacion'):
                fecha = stats['ultima_actualizacion'][:10]  # Solo fecha
                print(f"\n📅 Última actualización: {fecha}")
                
        except Exception as e:
            print(f"❌ Error obteniendo estadísticas: {e}")
        
        print("\n" + "=" * 40)
        input("Presiona Enter para continuar...")
    
    def _mostrar_estadisticas_admin(self):
        """Estadísticas detalladas para administrador."""
        self.formatter.limpiar_pantalla()
        
        print("📊 ESTADÍSTICAS ADMINISTRATIVAS")
        print("=" * 35)
        
        try:
            stats = self.gestor_denuncias.obtener_estadisticas()
            
            print(f"📝 Total denuncias: {stats.get('total', 0)}")
            print(f"🤖 Procesadas con IA: {stats.get('procesadas_ia', 0)}")
            print(f"📈 Porcentaje IA: {stats.get('porcentaje_ia', 0):.1f}%")
            
            if stats.get('por_categoria'):
                print("\n📂 Por categoría:")
                for categoria, cantidad in stats['por_categoria'].items():
                    categoria_display = categoria.replace('_', ' ').title()
                    porcentaje = (cantidad / stats['total']) * 100 if stats['total'] > 0 else 0
                    print(f"   • {categoria_display}: {cantidad} ({porcentaje:.1f}%)")
            
            if stats.get('por_veracidad'):
                print("\n🔍 Por nivel de veracidad:")
                for nivel, cantidad in stats['por_veracidad'].items():
                    print(f"   • {nivel}: {cantidad}")
        
        except Exception as e:
            print(f"❌ Error obteniendo estadísticas: {e}")
        
        input("\nPresiona Enter para continuar...")
    
    def _ver_todas_denuncias(self):
        """Ver todas las denuncias (solo admin)."""
        self.formatter.limpiar_pantalla()
        
        print("📋 TODAS LAS DENUNCIAS")
        print("=" * 25)
        
        try:
            if not hasattr(self.gestor_denuncias, 'denuncias') or not self.gestor_denuncias.denuncias:
                print("📝 No hay denuncias registradas")
            else:
                for i, denuncia in enumerate(self.gestor_denuncias.denuncias, 1):
                    print(f"\n📄 DENUNCIA #{i}")
                    print(f"ID: {denuncia.get('id', 'N/A')}")
                    print(f"Fecha: {denuncia.get('timestamp', 'N/A')[:19]}")
                    print(f"Categoría: {denuncia.get('categoria', 'N/A')}")
                    print(f"Mensaje: {denuncia.get('mensaje', '')[:100]}...")
                    print("-" * 40)
        except Exception as e:
            print(f"❌ Error obteniendo denuncias: {e}")
        
        input("\nPresiona Enter para continuar...")
    
    def _info_agente_ia(self):
        """Información del agente IA."""
        self.formatter.limpiar_pantalla()
        
        print("🤖 INFORMACIÓN DEL AGENTE IA")
        print("=" * 30)
        
        try:
            info_ia = self.gestor_denuncias.obtener_info_agente_ia()
            
            if info_ia.get('disponible'):
                print("✅ Estado: ACTIVO")
                print("🔧 Funcionalidades completas disponibles")
                
                if 'estadisticas' in info_ia:
                    print("\n📊 Estadísticas del agente:")
                    for key, value in info_ia['estadisticas'].items():
                        print(f"   • {key}: {value}")
            else:
                print("⚠️ Estado: MODO BÁSICO")
                print("💡 Para activar funciones avanzadas, configura OpenAI")
                print(f"   Motivo: {info_ia.get('motivo', 'Agente no inicializado')}")
        
        except Exception as e:
            print(f"❌ Error obteniendo información del agente: {e}")
        
        input("\nPresiona Enter para continuar...")
    
    def _mostrar_ayuda(self):
        """Muestra información de ayuda."""
        self.formatter.limpiar_pantalla()
        
        print("❓ AYUDA Y SOPORTE")
        print("=" * 20)
        print()
        
        print("🔒 ANONIMATO GARANTIZADO:")
        print("   • No se registra tu identidad")
        print("   • No se requiere información personal")
        print("   • Las denuncias son completamente anónimas")
        print()
        
        print("📝 TIPOS DE DENUNCIAS:")
        print("   • Acoso o hostigamiento")
        print("   • Discriminación")
        print("   • Corrupción")
        print("   • Problemas técnicos")
        print("   • Otros temas relevantes")
        print()
        
        print("🛡️ PROCESO:")
        print("   1. Escribe tu denuncia con detalles")
        print("   2. El sistema la clasifica automáticamente")
        print("   3. Se genera un ID de seguimiento")
        print("   4. Se envía al departamento correspondiente")
        print()
        
        print("📞 CONTACTO:")
        print("   • Email: denuncias@empresa.com")
        print("   • Teléfono: 555-DENUNCIA")
        
        print("\n" + "=" * 40)
        input("Presiona Enter para continuar...")
    
    def _mostrar_despedida(self):
        """Muestra mensaje de despedida."""
        self.formatter.limpiar_pantalla()
        print("👋 GRACIAS POR USAR EL SISTEMA")
        print("=" * 30)
        print("🔒 Tu privacidad ha sido protegida")
        print("📝 Tus denuncias son importantes")
        print("💪 Juntos construimos un mejor ambiente")
        print()
        print("¡Hasta pronto!")
    
    def _menu_administrador(self):
        """Menú completo de administrador con todas las mejoras."""
        try:
            # Importar las nuevas mejoras
            from interfaces.menu_administrador import MenuAdministrador
            from interfaces.dashboard_admin import DashboardAdmin
            from interfaces.gestor_estados import GestorEstados
            from interfaces.buscador_denuncias import BuscadorDenuncias
            from utils.exportador_denuncias import ExportadorDenuncias
            from src.agente_ia_simple.agente_ia_mejorado import AgenteIAMejorado
            
            # Crear instancias de las mejoras
            agente_ia_mejorado = AgenteIAMejorado()
            dashboard = DashboardAdmin(self.gestor_denuncias, self.gestor_roles)
            gestor_estados = GestorEstados(self.gestor_denuncias)
            buscador = BuscadorDenuncias(self.gestor_denuncias)
            exportador = ExportadorDenuncias(self.gestor_denuncias, agente_ia_mejorado)
            
            while True:
                self.formatter.limpiar_pantalla()
                
                print("👨‍💼 PANEL DE ADMINISTRADOR COMPLETO")
                print("=" * 45)
                print("🚀 NUEVAS FUNCIONALIDADES DISPONIBLES")
                print("=" * 45)
                
                # Mostrar estadísticas rápidas
                stats = self.gestor_denuncias.obtener_estadisticas()
                print(f"📊 Total denuncias: {stats.get('total', 0)}")
                print(f"🤖 Estado IA: {'ACTIVADO' if hasattr(self.gestor_denuncias, 'agente_ia') else 'BÁSICO'}")
                print()
                
                print("📋 MENÚ PRINCIPAL:")
                print("1. 📊 Dashboard Administrativo Avanzado")
                print("2. 🔍 Buscador Avanzado de Denuncias")
                print("3. 📊 Gestor de Estados")
                print("4. 📤 Exportación y Reportes")
                print("5. 🤖 Análisis con IA Mejorado")
                print("6. 📝 Gestión de Denuncias")
                print("7. ⚙️ Configuración del Sistema")
                print("8. 🚪 Volver al menú principal")
                print()
                
                opcion = input("👉 Selecciona una opción: ").strip()
                
                if opcion == "1":
                    dashboard.mostrar_dashboard_principal()
                    input("\nPresiona Enter para continuar...")
                elif opcion == "2":
                    buscador.mostrar_menu_busqueda()
                elif opcion == "3":
                    gestor_estados.mostrar_menu_estados()
                elif opcion == "4":
                    exportador.mostrar_menu_exportacion()
                elif opcion == "5":
                    self._menu_ia_mejorado(agente_ia_mejorado)
                elif opcion == "6":
                    self._menu_gestion_denuncias()
                elif opcion == "7":
                    self._menu_configuracion_avanzada()
                elif opcion == "8":
                    break
                else:
                    print("❌ Opción no válida")
                    input("Presiona Enter para continuar...")
            
        except ImportError as e:
            print(f"⚠️ Funcionalidades avanzadas no disponibles: {e}")
            print("🔄 Usando menú básico...")
            input("Presiona Enter para continuar...")
            self._menu_administrador_basico()
        except Exception as e:
            print(f"❌ Error en menú administrador: {e}")
            print("🔄 Usando menú básico...")
            input("Presiona Enter para continuar...")
            self._menu_administrador_basico()

    def _menu_ia_mejorado(self, agente_ia):
        """Menú para funciones de IA mejorado."""
        while True:
            self.formatter.limpiar_pantalla()
            
            print("🤖 ANÁLISIS CON IA MEJORADO")
            print("=" * 32)
            print("1. 🔍 Analizar denuncia específica")
            print("2. 📊 Estadísticas del agente IA")
            print("3. ⚡ Análisis masivo de denuncias")
            print("4. 🚨 Ver alertas críticas")
            print("5. 📈 Reporte de tendencias")
            print("0. ↩️ Volver")
            
            opcion = input("\n👉 Selecciona una opción: ").strip()
            
            if opcion == "1":
                self._analizar_denuncia_especifica(agente_ia)
            elif opcion == "2":
                self._mostrar_estadisticas_ia(agente_ia)
            elif opcion == "3":
                self._analisis_masivo(agente_ia)
            elif opcion == "4":
                self._ver_alertas_criticas(agente_ia)
            elif opcion == "5":
                self._reporte_tendencias(agente_ia)
            elif opcion == "0":
                break
            else:
                print("❌ Opción no válida")
                input("Presiona Enter para continuar...")

    def _analizar_denuncia_especifica(self, agente_ia):
        """Analiza una denuncia específica con IA."""
        print("\n🔍 ANÁLISIS ESPECÍFICO CON IA")
        print("=" * 35)
        
        if not hasattr(self.gestor_denuncias, 'denuncias') or not self.gestor_denuncias.denuncias:
            print("📭 No hay denuncias para analizar")
            input("Presiona Enter para continuar...")
            return
        
        # Mostrar denuncias disponibles
        print("📋 Denuncias disponibles:")
        for i, denuncia in enumerate(self.gestor_denuncias.denuncias, 1):
            fecha = denuncia.get('timestamp', '')[:19]
            categoria = denuncia.get('categoria', 'N/A')
            print(f"{i}. {fecha} - {categoria}")
        
        try:
            seleccion = int(input("\n👉 Selecciona denuncia (número): ")) - 1
            
            if 0 <= seleccion < len(self.gestor_denuncias.denuncias):
                denuncia = self.gestor_denuncias.denuncias[seleccion]
                mensaje = denuncia.get('mensaje', '')
                
                if mensaje:
                    print("\n🤖 Analizando con IA avanzado...")
                    analisis = agente_ia.analizar_denuncia_completa(mensaje)
                    
                    # Mostrar resultados
                    print(f"\n📊 RESULTADOS DEL ANÁLISIS:")
                    print(f"⚡ Urgencia: {analisis['urgencia']['nivel']} ({analisis['urgencia']['descripcion']})")
                    print(f"📂 Categoría: {analisis['categoria']['sugerida']} (Confianza: {analisis['categoria']['confianza']:.1%})")
                    print(f"📈 Prioridad: {analisis['prioridad']['nivel']} ({analisis['prioridad']['puntuacion']}/5)")
                    print(f"🎯 Veracidad: {analisis['puntuacion_veracidad']:.1%}")
                    
                    if analisis['alertas']:
                        print(f"\n🚨 ALERTAS GENERADAS:")
                        for alerta in analisis['alertas']:
                            print(f"   • {alerta['tipo']}: {alerta['mensaje']}")
                    
                    if analisis['recomendaciones']:
                        print(f"\n💡 RECOMENDACIONES:")
                        for recomendacion in analisis['recomendaciones'][:3]:
                            print(f"   • {recomendacion}")
                    
                    print(f"\n📝 RESUMEN: {analisis['resumen_ejecutivo']}")
                else:
                    print("❌ Denuncia sin contenido")
            else:
                print("❌ Selección no válida")
        except ValueError:
            print("❌ Ingresa un número válido")
        except Exception as e:
            print(f"❌ Error en análisis: {e}")
        
        input("\nPresiona Enter para continuar...")

    def _mostrar_estadisticas_ia(self, agente_ia):
        """Muestra estadísticas del agente IA."""
        print("\n📊 ESTADÍSTICAS DEL AGENTE IA")
        print("=" * 35)
        
        stats = agente_ia.obtener_estadisticas_analisis()
        
        print(f"🤖 Versión: {stats['version_agente']}")
        print(f"📂 Categorías disponibles: {len(stats['categorias_disponibles'])}")
        print(f"⚡ Niveles de urgencia: {len(stats['niveles_urgencia'])}")
        print(f"🚨 Tipos de alerta: {len(stats['tipos_alerta'])}")
        
        print(f"\n🎯 CAPACIDADES:")
        for capacidad in stats['capacidades']:
            print(f"   ✅ {capacidad}")
        
        print(f"\n📋 CATEGORÍAS SOPORTADAS:")
        for categoria in stats['categorias_disponibles']:
            print(f"   • {categoria.replace('_', ' ').title()}")
        
        input("\nPresiona Enter para continuar...")

    def _analisis_masivo(self, agente_ia):
        """Realiza análisis masivo de todas las denuncias."""
        print("\n⚡ ANÁLISIS MASIVO CON IA")
        print("=" * 30)
        
        if not hasattr(self.gestor_denuncias, 'denuncias') or not self.gestor_denuncias.denuncias:
            print("📭 No hay denuncias para analizar")
            input("Presiona Enter para continuar...")
            return
        
        denuncias = self.gestor_denuncias.denuncias
        total = len(denuncias)
        
        print(f"🔄 Procesando {total} denuncias...")
        
        resultados = {
            'total_procesadas': 0,
            'alta_urgencia': 0,
            'alertas_criticas': 0,
            'alta_veracidad': 0,
            'categorias': {}
        }
        
        for i, denuncia in enumerate(denuncias, 1):
            mensaje = denuncia.get('mensaje', '')
            if mensaje:
                print(f"⏳ Procesando {i}/{total}...", end='\r')
                
                try:
                    analisis = agente_ia.analizar_denuncia_completa(mensaje)
                    resultados['total_procesadas'] += 1
                    
                    # Estadísticas
                    if analisis['urgencia']['valor'] >= 4:
                        resultados['alta_urgencia'] += 1
                    
                    if analisis['alertas']:
                        resultados['alertas_criticas'] += len([a for a in analisis['alertas'] if a.get('prioridad') == 'crítica'])
                    
                    if analisis['puntuacion_veracidad'] >= 0.7:
                        resultados['alta_veracidad'] += 1
                    
                    categoria = analisis['categoria']['sugerida']
                    resultados['categorias'][categoria] = resultados['categorias'].get(categoria, 0) + 1
                    
                    # Guardar análisis en la denuncia
                    denuncia['analisis_ia'] = analisis
                    
                except Exception as e:
                    print(f"\n❌ Error procesando denuncia {i}: {e}")
        
        # Mostrar resultados
        print(f"\n✅ ANÁLISIS MASIVO COMPLETADO")
        print(f"📊 Total procesadas: {resultados['total_procesadas']}/{total}")
        print(f"⚡ Alta urgencia: {resultados['alta_urgencia']}")
        print(f"🚨 Alertas críticas: {resultados['alertas_criticas']}")
        print(f"🎯 Alta veracidad: {resultados['alta_veracidad']}")
        
        print(f"\n📂 DISTRIBUCIÓN POR CATEGORÍAS:")
        for categoria, cantidad in sorted(resultados['categorias'].items(), key=lambda x: x[1], reverse=True):
            porcentaje = (cantidad / resultados['total_procesadas'] * 100) if resultados['total_procesadas'] > 0 else 0
            print(f"   • {categoria.replace('_', ' ').title()}: {cantidad} ({porcentaje:.1f}%)")
        
        input("\nPresiona Enter para continuar...")

    def _ver_alertas_criticas(self, agente_ia):
        """Muestra denuncias con alertas críticas."""
        print("\n🚨 ALERTAS CRÍTICAS")
        print("=" * 20)
        
        if not hasattr(self.gestor_denuncias, 'denuncias'):
            print("📭 No hay denuncias")
            input("Presiona Enter para continuar...")
            return
        
        alertas_encontradas = []
        
        for denuncia in self.gestor_denuncias.denuncias:
            if 'analisis_ia' in denuncia:
                analisis = denuncia['analisis_ia']
                alertas_criticas = [a for a in analisis.get('alertas', []) if a.get('prioridad') in ['crítica', 'alta']]
                
                if alertas_criticas:
                    alertas_encontradas.append({
                        'denuncia': denuncia,
                        'alertas': alertas_criticas
                    })
        
        if not alertas_encontradas:
            print("✅ No hay alertas críticas activas")
        else:
            print(f"⚠️ {len(alertas_encontradas)} denuncias con alertas críticas:")
            print()
            
            for i, item in enumerate(alertas_encontradas, 1):
                denuncia = item['denuncia']
                alertas = item['alertas']
                
                fecha = denuncia.get('timestamp', '')[:19]
                categoria = denuncia.get('categoria', 'N/A')
                
                print(f"📄 #{i} - {fecha} - {categoria}")
                for alerta in alertas:
                    prioridad_emoji = "🚨" if alerta.get('prioridad') == 'crítica' else "⚠️"
                    print(f"   {prioridad_emoji} {alerta['tipo']}: {alerta['mensaje']}")
                    if 'accion_sugerida' in alerta:
                        print(f"      💡 Acción: {alerta['accion_sugerida']}")
                print()
        
        input("Presiona Enter para continuar...")

    def _reporte_tendencias(self, agente_ia):
        """Genera reporte de tendencias."""
        print("\n📈 REPORTE DE TENDENCIAS")
        print("=" * 28)
        
        print("📊 Funcionalidad en desarrollo")
        print("💡 Próximamente: análisis de patrones temporales y tendencias")
        
        input("\nPresiona Enter para continuar...")

    def _menu_gestion_denuncias(self):
        """Menú de gestión básica de denuncias."""
        while True:
            self.formatter.limpiar_pantalla()
            
            print("📝 GESTIÓN DE DENUNCIAS")
            print("=" * 25)
            print("1. 📋 Ver todas las denuncias")
            print("2. 📊 Estadísticas detalladas")
            print("3. 🗑️ Gestión de datos")
            print("0. ↩️ Volver")
            
            opcion = input("\n👉 Selecciona una opción: ").strip()
            
            if opcion == "1":
                self._ver_todas_denuncias()
            elif opcion == "2":
                self._mostrar_estadisticas_admin()
            elif opcion == "3":
                self._menu_gestion_datos()
            elif opcion == "0":
                break
            else:
                print("❌ Opción no válida")
                input("Presiona Enter para continuar...")

    def _menu_configuracion_avanzada(self):
        """Menú de configuración avanzada."""
        while True:
            self.formatter.limpiar_pantalla()
            
            print("⚙️ CONFIGURACIÓN AVANZADA")
            print("=" * 30)
            print("1. 🤖 Configurar Agente IA")
            print("2. 🔑 Gestión de usuarios")
            print("3. 📂 Configuración de categorías")
            print("4. 🔧 Parámetros del sistema")
            print("0. ↩️ Volver")
            
            opcion = input("\n👉 Selecciona una opción: ").strip()
            
            if opcion == "1":
                self._configurar_agente_ia()
            elif opcion == "2":
                print("🔑 Gestión de usuarios - En desarrollo")
                input("Presiona Enter para continuar...")
            elif opcion == "3":
                print("📂 Configuración de categorías - En desarrollo")
                input("Presiona Enter para continuar...")
            elif opcion == "4":
                print("🔧 Parámetros del sistema - En desarrollo")
                input("Presiona Enter para continuar...")
            elif opcion == "0":
                break
            else:
                print("❌ Opción no válida")
                input("Presiona Enter para continuar...")

    def _configurar_agente_ia(self):
        """Configura el agente IA."""
        print("\n🤖 CONFIGURACIÓN DEL AGENTE IA")
        print("=" * 35)
        
        print("💡 Opciones de configuración:")
        print("1. 🔧 Modo básico (sin API)")
        print("2. 🚀 Configurar OpenAI")
        print("3. 📊 Ver estado actual")
        
        opcion = input("\n👉 Selecciona opción: ").strip()
        
        if opcion == "1":
            print("✅ Modo básico activado")
            print("💡 El sistema funcionará con análisis local")
        elif opcion == "2":
            api_key = input("🔑 Ingresa API Key de OpenAI: ").strip()
            if api_key:
                print("⏳ Configurando OpenAI...")
                # Aquí se configuraría OpenAI
                print("✅ OpenAI configurado (simulado)")
            else:
                print("❌ API Key vacía")
        elif opcion == "3":
            info_ia = self.gestor_denuncias.obtener_info_agente_ia()
            print(f"📊 Estado: {'DISPONIBLE' if info_ia.get('disponible') else 'BÁSICO'}")
            print(f"💡 {info_ia.get('motivo', 'Sin información')}")
        
        input("\nPresiona Enter para continuar...")

    def _menu_gestion_datos(self):
        """Menú de gestión de datos."""
        print("\n🗑️ GESTIÓN DE DATOS")
        print("=" * 20)
        print("⚠️ Funcionalidad administrativa")
        print("💡 Opciones de limpieza y mantenimiento")
        print("🔒 Requiere confirmación adicional")
        
        input("\nPresiona Enter para continuar...")