"""
Menú específico para usuarios anónimos.
Interfaz simplificada enfocada en el envío de denuncias.
"""

from typing import List
from interfaces.consola_base import InterfazConsolaBase
from interfaces.helpers import HelpersDenuncia

class MenuAnonimo(InterfazConsolaBase):
    """
    Menú específico para usuarios anónimos.
    Proporciona funcionalidad básica de envío de denuncias.
    """
    
    def __init__(self, gestor_denuncias, gestor_roles):
        """
        Inicializa el menú para usuarios anónimos.
        
        Args:
            gestor_denuncias: Instancia del gestor de denuncias
            gestor_roles: Instancia del gestor de roles
        """
        super().__init__(gestor_denuncias, gestor_roles)
        self.helpers_denuncia = HelpersDenuncia(gestor_denuncias, gestor_roles)
        
        # Configuración específica para usuarios anónimos
        self.agente_ia_activo = True  # Por defecto activo para usuarios anónimos
    
    def mostrar_menu(self):
        """Muestra el menú específico para usuarios anónimos."""
        self.mostrar_banner_contextual()
        
        opciones = self.config.MENUS['anonimo']
        self.formatter.mostrar_menu("MENÚ USUARIO ANÓNIMO", opciones)
        
        # Mostrar información adicional
        print("🔒 Garantizamos tu privacidad y anonimato")
        print("🤖 Procesamiento automático con IA activado")
        print()
    
    def procesar_opcion(self, opcion: str) -> bool:
        """
        Procesa las opciones del menú anónimo.
        
        Args:
            opcion: Opción seleccionada
            
        Returns:
            bool: True para continuar, False para salir
        """
        if opcion == "1":
            return self._enviar_denuncia_anonima()
        elif opcion == "2":
            return self._mostrar_ayuda_sistema()
        elif opcion == "3":
            return self._cambiar_a_administrador()
        elif opcion == "4":
            return self._salir_sistema()
        else:
            self.formatter.mostrar_mensaje_error("Opción no válida")
            return True
    
    def obtener_opciones_validas(self) -> List[str]:
        """Obtiene las opciones válidas para el menú anónimo."""
        return ["1", "2", "3", "4"]
    
    def _enviar_denuncia_anonima(self) -> bool:
        """
        Procesa el envío de una denuncia anónima.
        
        Returns:
            bool: True para continuar en el menú
        """
        try:
            # Solicitar mensaje de denuncia
            mensaje = self.helpers_denuncia.solicitar_mensaje_denuncia()
            
            if mensaje is None:
                print("💡 Puedes intentar enviar tu denuncia nuevamente cuando desees")
                self.pausar_para_continuar()
                return True
            
            # Procesar con IA (siempre automático para usuarios anónimos)
            if self.agente_ia_activo:
                exito = self.helpers_denuncia.procesar_denuncia_automatica(mensaje, False)
            else:
                # Fallback a procesamiento manual si IA no está disponible
                exito = self.helpers_denuncia.procesar_denuncia_manual(mensaje)
            
            if exito:
                self._mostrar_mensaje_exito_anonimo()
            else:
                self._mostrar_mensaje_error_envio()
            
            self.pausar_para_continuar()
            return True
            
        except Exception as e:
            print(f"\n❌ Error al procesar denuncia: {e}")
            print("💡 Inténtalo nuevamente o contacta al administrador")
            self.pausar_para_continuar()
            return True
    
    def _mostrar_mensaje_exito_anonimo(self):
        """Muestra mensaje de éxito específico para usuarios anónimos."""
        self.formatter.mostrar_separador("✅ DENUNCIA ENVIADA EXITOSAMENTE", 40)
        
        print("🎉 Tu denuncia ha sido registrada correctamente")
        print("🔒 Tu identidad permanece completamente anónima")
        print("📊 La información será incluida en estadísticas agregadas")
        print("👨‍💼 Los administradores pueden revisar tendencias generales")
        print("🔐 Sin posibilidad de rastreo o identificación")
        
        print("\n💡 ¿QUÉ PASA AHORA?")
        print("   • Tu denuncia está segura en el sistema")
        print("   • Se incluirá en reportes estadísticos")
        print("   • Los administradores pueden tomar acciones correctivas")
        print("   • Tu anonimato está garantizado para siempre")
        
        print("\n🙏 GRACIAS POR CONTRIBUIR A UN MEJOR AMBIENTE")
    
    def _mostrar_mensaje_error_envio(self):
        """Muestra mensaje de error en el envío."""
        self.formatter.mostrar_mensaje_error("No se pudo procesar tu denuncia")
        print("💡 Posibles causas:")
        print("   • Problema técnico temporal")
        print("   • Sistema de IA no disponible")
        print("   • Error en la validación del contenido")
        print("\n🔄 Te recomendamos:")
        print("   • Intentar nuevamente en unos minutos")
        print("   • Verificar que la denuncia sea válida")
        print("   • Contactar al administrador si persiste el problema")
    
    def _mostrar_ayuda_sistema(self) -> bool:
        """
        Muestra la ayuda del sistema para usuarios anónimos.
        
        Returns:
            bool: True para continuar en el menú
        """
        categorias_disponibles = [
            "Acoso",
            "Discriminación",
            "Corrupción", 
            "Problemas técnicos",
            "Otros"
        ]
        
        self.formatter.mostrar_ayuda_sistema(categorias_disponibles)
        
        # Información adicional específica para anónimos
        print("\n🎯 ESPECÍFICO PARA USUARIOS ANÓNIMOS:")
        print("   • No necesitas crear cuenta ni proporcionar datos")
        print("   • El sistema NO almacena información identificable")
        print("   • Puedes enviar múltiples denuncias si es necesario")
        print("   • No hay límite en el número de reportes")
        print("   • Cada denuncia se procesa independientemente")
        
        print("\n⚖️  ASPECTOS LEGALES:")
        print("   • Las denuncias falsas pueden tener consecuencias")
        print("   • Proporciona información veraz y detallada")
        print("   • El anonimato no protege contra denuncias malintencionadas")
        print("   • El sistema puede detectar patrones sospechosos")
        
        self.pausar_para_continuar()
        return True
    
    def _cambiar_a_administrador(self) -> bool:
        """
        Intenta cambiar al modo administrador.
        
        Returns:
            bool: False para salir del menú anónimo, True para continuar
        """
        print("\n🔄 CAMBIO A MODO ADMINISTRADOR")
        print("Se cerrará el modo anónimo y se solicitarán credenciales")
        
        # Confirmar cambio
        if not self.formatter.solicitar_confirmacion("¿Deseas continuar?"):
            print("🔄 Permaneciendo en modo anónimo")
            return True
        
        # Salir del menú anónimo (el controlador principal manejará la autenticación)
        print("🔄 Regresando al menú principal...")
        return False
    
    def _salir_sistema(self) -> bool:
        """
        Sale completamente del sistema.
        
        Returns:
            bool: False para salir
        """
        print("\n👋 SALIENDO DEL SISTEMA")
        
        # Confirmar salida
        if self.formatter.solicitar_confirmacion("¿Estás seguro de que deseas salir?"):
            self.formatter.mostrar_mensaje_info("Gracias por usar el Sistema de Denuncias Anónimas")
            print("🔒 Tu privacidad ha sido protegida en todo momento")
            print("💼 Si necesitas funciones administrativas, inicia sesión como administrador")
            return False
        else:
            print("🔄 Regresando al menú")
            return True
    
    def cleanup_al_salir(self):
        """Limpieza específica para usuarios anónimos."""
        super().cleanup_al_salir()
        
        # No hay sesión que cerrar para usuarios anónimos
        print("🔒 Modo anónimo finalizado")
        print("💭 No se conservan datos de la sesión")