"""
Clase base para interfaces de consola.
Funcionalidad común para todos los tipos de menú.
"""

from typing import Optional
from abc import ABC, abstractmethod

class InterfazConsolaBase(ABC):
    """
    Clase base abstracta para interfaces de consola.
    Define la estructura común para todos los menús.
    """
    
    def __init__(self, gestor_denuncias, gestor_roles):
        """
        Inicializa la interfaz base.
        
        Args:
            gestor_denuncias: Instancia del gestor de denuncias
            gestor_roles: Instancia del gestor de roles
        """
        self.gestor_denuncias = gestor_denuncias
        self.gestor_roles = gestor_roles
        
        # Importar aquí para evitar imports circulares
        from config.settings import ConfiguracionSistema
        from utils.formatters import FormateadorConsola
        
        self.config = ConfiguracionSistema()
        self.formatter = FormateadorConsola()
        
        # Estado de la interfaz
        self.ejecutando = False
        self.agente_ia_activo = True
        
        # Cache de estadísticas para evitar recálculos
        self._cache_estadisticas = None
        self._cache_timestamp = None
    
    @abstractmethod
    def mostrar_menu(self):
        """Muestra el menú específico del tipo de usuario."""
        pass
    
    @abstractmethod
    def procesar_opcion(self, opcion: str) -> bool:
        """
        Procesa una opción del menú.
        
        Args:
            opcion: Opción seleccionada por el usuario
            
        Returns:
            bool: True para continuar, False para salir
        """
        pass
    
    @abstractmethod
    def obtener_opciones_validas(self) -> list:
        """Obtiene la lista de opciones válidas para el menú."""
        pass
    
    def ejecutar_loop_principal(self):
        """
        Ejecuta el loop principal de la interfaz.
        Común para todos los tipos de menú.
        """
        self.ejecutando = True
        
        while self.ejecutando:
            try:
                # Validar sesión antes de cada iteración
                if not self.gestor_roles.validar_sesion():
                    self.manejar_sesion_invalida()
                    continue
                
                # Mostrar menú y procesar entrada
                self.mostrar_menu()
                opcion = self.solicitar_opcion()
                
                if opcion is None:
                    continue  # Opción inválida, continuar
                
                # Procesar opción
                continuar = self.procesar_opcion(opcion)
                if not continuar:
                    self.ejecutando = False
                    
            except KeyboardInterrupt:
                self.manejar_interrupcion_usuario()
                break
            except Exception as e:
                self.manejar_error_inesperado(e)
                
        self.cleanup_al_salir()
    
    def solicitar_opcion(self) -> Optional[str]:
        """
        Solicita y valida una opción del menú.
        
        Returns:
            str: Opción válida o None si es inválida
        """
        try:
            from utils.validators import ValidadorEntrada
            
            opcion = input("🔹 Selecciona una opción: ").strip()
            
            if not opcion:
                self.formatter.mostrar_mensaje_error("Por favor, ingresa una opción")
                return None
            
            opciones_validas = self.obtener_opciones_validas()
            opcion_validada = ValidadorEntrada.validar_opcion_menu(opcion, opciones_validas)
            
            if opcion_validada is None:
                self.formatter.mostrar_mensaje_error(
                    f"Opción inválida. Opciones válidas: {', '.join(opciones_validas)}"
                )
                return None
            
            return opcion_validada
            
        except (EOFError, KeyboardInterrupt):
            return None
    
    def manejar_sesion_invalida(self):
        """Maneja el caso de sesión inválida o expirada."""
        self.formatter.mostrar_mensaje_advertencia("Sesión inválida o expirada")
        print("🔄 Regresando al menú principal...")
        self.ejecutando = False
    
    def manejar_interrupcion_usuario(self):
        """Maneja la interrupción por parte del usuario (Ctrl+C)."""
        print("\n\n👋 Saliendo del sistema...")
        self.formatter.mostrar_mensaje_info("Gracias por usar el sistema de denuncias")
        self.ejecutando = False
    
    def manejar_error_inesperado(self, error: Exception):
        """
        Maneja errores inesperados en el sistema.
        
        Args:
            error: Excepción capturada
        """
        print(f"\n❌ Error inesperado: {error}")
        print("🔄 El sistema continuará funcionando...")
        print("💡 Si el problema persiste, contacta al administrador")
    
    def cleanup_al_salir(self):
        """Limpieza al salir de la interfaz."""
        # Limpiar cache
        self._cache_estadisticas = None
        self._cache_timestamp = None
    
    def pausar_para_continuar(self):
        """Pausa la ejecución hasta que el usuario presione Enter."""
        try:
            input("\n📱 Presiona Enter para continuar...")
        except (EOFError, KeyboardInterrupt):
            pass
    
    def mostrar_banner_contextual(self):
        """Muestra el banner con información contextual del usuario."""
        tipo_usuario = "administrador" if self.gestor_roles.es_administrador() else "anonimo"
        self.formatter.mostrar_banner(tipo_usuario, self.agente_ia_activo)