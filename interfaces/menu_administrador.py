"""
Menú de administrador corregido sin bucles infinitos.
"""

import sys
from typing import Optional
from utils.validators import ValidadorSistema
from utils.formatters import FormateadorConsola
from config.settings import ConfiguracionSistema

class MenuAdministrador:
    """Menú principal para administradores con lógica corregida."""
    
    def __init__(self, gestor_denuncias, gestor_roles):
        """Inicializa el menú de administrador."""
        self.gestor_denuncias = gestor_denuncias
        self.gestor_roles = gestor_roles
        self.validador = ValidadorSistema()
        self.formatter = FormateadorConsola()
        self.config = ConfiguracionSistema()
        
        # Estado del agente IA
        self.agente_ia_activo = True
    
    def ejecutar_loop_principal(self):
        """Ejecuta el loop principal del menú de administrador."""
        print("👨‍💼 Acceso de administrador iniciado")
        
        while True:
            try:
                # Mostrar menú y obtener opción
                opcion = self._mostrar_menu_principal()
                
                # Procesar opción INMEDIATAMENTE
                if not self._procesar_opcion(opcion):
                    break  # Salir del loop
                    
                # Pausa obligatoria para evitar bucle rápido
                input("\nPresiona Enter para continuar...")
                
            except KeyboardInterrupt:
                print("\n👋 Saliendo del panel de administrador...")
                break
            except Exception as e:
                print(f"\n❌ Error inesperado: {e}")
                input("Presiona Enter para continuar...")
        
        print("👋 Sesión de administrador cerrada")
    
    def _mostrar_menu_principal(self) -> str:
        """Muestra el menú principal y retorna la opción seleccionada."""
        self.formatter.limpiar_pantalla()
        
        # Banner del sistema (solo una vez)
        print("=" * 60)
        print("🔒 SISTEMA ANÓNIMO DE DENUNCIAS INTERNAS 🔒")
        print("=" * 60)
        print("🛡️  Tu identidad está protegida")
        print("🔐 Procesamiento seguro con MCP")
        print("👤 Modo: ADMINISTRADOR")
        print("=" * 60)
        print()
        
        # Menú de opciones
        print("📋 MENÚ ADMINISTRADOR")
        print("-" * 30)
        print("📝 1. Enviar denuncia")
        print("📊 2. Ver estadísticas de denuncias")
        print("📈 3. Generar reporte de resumen")
        
        if self.agente_ia_activo:
            print("🤖 4. 🔴 Desactivar Agente IA")
        else:
            print("🤖 4. 🟢 Activar Agente IA")
        
        print("⚙️ 5. Configurar OpenAI (opcional)")
        print("🔧 6. Verificar estado del sistema")
        print("🔍 7. Probar clasificador de IA")
        print("🔑 8. Cambiar credenciales de administrador")
        print("👤 9. Cerrar sesión (modo anónimo)")
        print("❌ 10. Salir del sistema")
        print("-" * 30)
        
        estado_ia = "🤖 ACTIVADO" if self.agente_ia_activo else "👤 DESACTIVADO"
        print(f"🔧 Estado del sistema: {estado_ia}")
        print()
        
        # Solicitar opción
        return input("🔹 Selecciona una opción: ").strip()
    
    def _procesar_opcion(self, opcion: str) -> bool:
        """
        Procesa la opción seleccionada.
        
        Args:
            opcion: Opción seleccionada por el usuario
            
        Returns:
            bool: True para continuar, False para salir
        """
        try:
            if opcion == "1":
                self._enviar_denuncia()
            elif opcion == "2":
                self._ver_estadisticas()
            elif opcion == "3":
                self._generar_reporte()
            elif opcion == "4":
                self._toggle_agente_ia()
            elif opcion == "5":
                self._configurar_openai()
            elif opcion == "6":
                self._verificar_estado_sistema()
            elif opcion == "7":
                self._probar_clasificador()
            elif opcion == "8":
                self._cambiar_credenciales()
            elif opcion == "9":
                print("👤 Cerrando sesión de administrador...")
                return False  # Cerrar sesión
            elif opcion == "10":
                print("❌ Saliendo del sistema...")
                sys.exit(0)  # Salir completamente
            else:
                print(f"❌ Opción inválida: '{opcion}'")
                print("💡 Opciones válidas: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10")
            
            return True  # Continuar en el menú
            
        except Exception as e:
            print(f"❌ Error procesando opción '{opcion}': {e}")
            return True  # Continuar aunque haya error
    
    def _enviar_denuncia(self):
        """Permite al administrador enviar una denuncia."""
        print("\n📝 ENVIAR DENUNCIA (Modo Administrador)")
        print("=" * 40)
        
        mensaje = input("Describe la denuncia: ").strip()
        
        if not mensaje:
            print("❌ No se puede enviar una denuncia vacía")
            return
        
        try:
            resultado = self.gestor_denuncias.registrar_denuncia(mensaje)
            
            if resultado.get('exito', False):
                print("✅ DENUNCIA REGISTRADA EXITOSAMENTE")
                print(f"🆔 ID: {resultado.get('id_denuncia', 'N/A')}")
                print(f"📂 Categoría: {resultado.get('categoria', 'N/A')}")
                print(f"📅 Fecha: {resultado.get('timestamp', 'N/A')[:19]}")
                print(f"🤖 Procesada con IA: {'Sí' if resultado.get('procesada_con_ia', False) else 'No'}")
            else:
                print("❌ ERROR AL REGISTRAR DENUNCIA")
                print(f"Razón: {resultado.get('error', 'Error desconocido')}")
                
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
    
    def _ver_estadisticas(self):
        """Muestra estadísticas detalladas."""
        print("\n📊 ESTADÍSTICAS DE DENUNCIAS")
        print("=" * 35)
        
        try:
            stats = self.gestor_denuncias.obtener_estadisticas()
            
            print(f"📝 Total de denuncias: {stats.get('total', 0)}")
            print(f"🤖 Procesadas con IA: {stats.get('procesadas_ia', 0)}")
            print(f"📈 Porcentaje con IA: {stats.get('porcentaje_ia', 0):.1f}%")
            
            if stats.get('por_categoria'):
                print("\n📂 Por categoría:")
                for categoria, cantidad in stats['por_categoria'].items():
                    categoria_display = categoria.replace('_', ' ').title()
                    print(f"   • {categoria_display}: {cantidad}")
            
            if stats.get('por_veracidad'):
                print("\n🎯 Por nivel de veracidad:")
                for nivel, cantidad in stats['por_veracidad'].items():
                    print(f"   • {nivel}: {cantidad}")
            
            print(f"\n📅 Última actualización: {stats.get('ultima_actualizacion', 'N/A')[:19]}")
            
        except Exception as e:
            print(f"❌ Error obteniendo estadísticas: {e}")
    
    def _generar_reporte(self):
        """Genera un reporte de resumen."""
        print("\n📈 GENERAR REPORTE DE RESUMEN")
        print("=" * 30)
        
        try:
            stats = self.gestor_denuncias.obtener_estadisticas()
            
            if stats.get('total', 0) == 0:
                print("📭 No hay denuncias para generar reporte")
                return
            
            from utils.formatters import FormateadorArchivos
            
            reporte = FormateadorArchivos.formatear_reporte_resumen(
                stats.get('por_categoria', {}), 
                self.agente_ia_activo
            )
            
            # Guardar reporte
            nombre_archivo = f"reporte_denuncias_{stats.get('ultima_actualizacion', 'N/A')[:10]}.txt"
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                f.write(reporte)
            
            print(f"✅ Reporte generado: {nombre_archivo}")
            print("📄 El archivo contiene estadísticas agregadas (sin datos personales)")
            
        except Exception as e:
            print(f"❌ Error generando reporte: {e}")
    
    def _toggle_agente_ia(self):
        """Activa o desactiva el agente IA."""
        estado_actual = "ACTIVADO" if self.agente_ia_activo else "DESACTIVADO"
        nueva_accion = "desactivar" if self.agente_ia_activo else "activar"
        
        print(f"\n🤖 GESTIÓN DEL AGENTE IA")
        print("=" * 25)
        print(f"Estado actual: {estado_actual}")
        print(f"¿Deseas {nueva_accion} el agente IA?")
        
        confirmacion = input("Confirmar (s/n): ").strip().lower()
        
        if confirmacion in ['s', 'si', 'sí', 'y', 'yes']:
            self.agente_ia_activo = not self.agente_ia_activo
            nuevo_estado = "ACTIVADO" if self.agente_ia_activo else "DESACTIVADO"
            print(f"✅ Agente IA: {nuevo_estado}")
            
            if self.agente_ia_activo:
                print("🤖 Procesamiento automático habilitado")
            else:
                print("👤 Modo manual activado - Revisión humana requerida")
        else:
            print("❌ Operación cancelada")
    
    def _configurar_openai(self):
        """Configura la API de OpenAI."""
        print("\n⚙️ CONFIGURAR OPENAI")
        print("=" * 20)
        print("💡 Opcional: Mejora la precisión del clasificador")
        print("🔑 Necesitas una API Key de OpenAI")
        print()
        
        api_key = input("Ingresa tu API Key (o Enter para omitir): ").strip()
        
        if api_key:
            try:
                if self.gestor_denuncias.configurar_agente_ia(api_key):
                    print("✅ OpenAI configurado correctamente")
                    print("🎯 Precisión del clasificador mejorada")
                else:
                    print("❌ Error configurando OpenAI")
                    print("🔍 Verifica que la API Key sea válida")
            except Exception as e:
                print(f"❌ Error: {e}")
        else:
            print("💡 Configuración omitida - El sistema funcionará en modo básico")
    
    def _verificar_estado_sistema(self):
        """Verifica el estado completo del sistema."""
        print("\n🔧 ESTADO DEL SISTEMA")
        print("=" * 25)
        
        try:
            # Estado del agente IA
            info_ia = self.gestor_denuncias.obtener_info_agente_ia()
            
            print("🤖 AGENTE IA:")
            if info_ia.get('disponible', False):
                print("   ✅ Estado: DISPONIBLE")
                if 'estadisticas' in info_ia:
                    stats = info_ia['estadisticas']
                    print(f"   📊 Estadísticas disponibles: {len(stats)} métricas")
            else:
                print("   ❌ Estado: NO DISPONIBLE")
                print(f"   📝 Motivo: {info_ia.get('motivo', 'Desconocido')}")
            
            # Estado general del sistema
            stats = self.gestor_denuncias.obtener_estadisticas()
            print(f"\n📊 SISTEMA GENERAL:")
            print(f"   📝 Total denuncias: {stats.get('total', 0)}")
            print(f"   🤖 Procesadas con IA: {stats.get('procesadas_ia', 0)}")
            print(f"   📈 Agente activo: {'Sí' if self.agente_ia_activo else 'No'}")
            
        except Exception as e:
            print(f"❌ Error verificando sistema: {e}")
    
    def _probar_clasificador(self):
        """Prueba el clasificador de IA con texto de ejemplo."""
        print("\n🔍 PROBAR CLASIFICADOR DE IA")
        print("=" * 30)
        
        if not self.agente_ia_activo:
            print("⚠️ El agente IA está desactivado")
            print("💡 Actívalo primero para probar el clasificador")
            return
        
        print("💡 Ingresa un texto de prueba para clasificar:")
        texto_prueba = input("Texto: ").strip()
        
        if not texto_prueba:
            print("❌ No se puede clasificar texto vacío")
            return
        
        try:
            resultado = self.gestor_denuncias.registrar_denuncia(texto_prueba)
            
            print("\n🎯 RESULTADO DE LA PRUEBA:")
            print(f"📂 Categoría detectada: {resultado.get('categoria', 'N/A')}")
            print(f"🤖 Procesado con IA: {'Sí' if resultado.get('procesada_con_ia', False) else 'No'}")
            print(f"🆔 ID asignado: {resultado.get('id_denuncia', 'N/A')}")
            
            if resultado.get('exito', False):
                print("\n✅ Clasificación exitosa")
                print("💡 La denuncia de prueba fue registrada en el sistema")
            else:
                print("\n❌ Error en la clasificación")
                
        except Exception as e:
            print(f"❌ Error probando clasificador: {e}")
    
    def _cambiar_credenciales(self):
        """Cambia las credenciales de administrador."""
        print("\n🔑 CAMBIAR CREDENCIALES")
        print("=" * 25)
        print("🔒 Función de seguridad - En desarrollo")
        print("💡 Contacta al administrador del sistema")
        print("📧 Para cambios de credenciales críticas")
