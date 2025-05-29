"""
Gestor de roles y autenticación refactorizado.
Maneja la autenticación, sesiones y permisos de usuarios.
"""

import hashlib
from typing import Optional
from auth.tipos_usuario import TipoUsuario, Permisos, GestorPermisos
from config.settings import ConfiguracionSistema
from utils.validators import ValidadorEntrada

class GestorRoles:
    """
    Gestiona la autenticación y permisos de usuarios del sistema.
    Refactorizado para ser más modular y mantenible.
    """
    
    def __init__(self):
        """Inicializa el gestor de roles con configuración centralizada."""
        self.config = ConfiguracionSistema()
        self.auth_config = self.config.AUTENTICACION
        
        # Configurar credenciales por defecto
        self._configurar_credenciales_iniciales()
        
        # Estado de sesión actual
        self.usuario_actual = TipoUsuario.ANONIMO
        self.sesion_activa = False
        self.intentos_fallidos = 0
        
        # Información de sesión
        self.info_sesion = {
            'hora_inicio': None,
            'ultimo_acceso': None,
            'acciones_realizadas': []
        }
    
    def _configurar_credenciales_iniciales(self):
        """Configura las credenciales iniciales del administrador."""
        credenciales_default = self.auth_config['credenciales_por_defecto']
        self.credenciales_admin = {
            "usuario": credenciales_default['usuario'],
            "password_hash": self._generar_hash(credenciales_default['password'])
        }
    
    def _generar_hash(self, password: str) -> str:
        """
        Genera hash seguro de la contraseña usando SHA-256.
        
        Args:
            password: Contraseña en texto plano
            
        Returns:
            str: Hash de la contraseña
        """
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def autenticar_administrador(self) -> bool:
        """
        Autentica al administrador con validaciones mejoradas y manejo de errores.
        
        Returns:
            bool: True si la autenticación es exitosa, False en caso contrario
        """
        self._mostrar_pantalla_autenticacion()
        
        intentos_maximos = self.auth_config['intentos_maximos']
        
        for intento in range(1, intentos_maximos + 1):
            try:
                if self._procesar_intento_autenticacion(intento, intentos_maximos):
                    self._activar_sesion_administrador()
                    return True
                    
            except KeyboardInterrupt:
                self._manejar_cancelacion_autenticacion()
                break
            except Exception as e:
                print(f"\n❌ Error inesperado durante autenticación: {e}")
                continue
        
        self._manejar_autenticacion_fallida()
        return False
    
    def _mostrar_pantalla_autenticacion(self):
        """Muestra la pantalla inicial de autenticación."""
        print("\n👨‍💼 ACCESO DE ADMINISTRADOR")
        print("=" * 40)
        print("🔐 Ingresa tus credenciales de administrador")
        print(f"⚠️  Tienes {self.auth_config['intentos_maximos']} intentos máximo")
        print("💡 Presiona Ctrl+C para cancelar")
        print()
    
    def _procesar_intento_autenticacion(self, intento: int, intentos_maximos: int) -> bool:
        """
        Procesa un intento individual de autenticación.
        
        Args:
            intento: Número del intento actual
            intentos_maximos: Máximo número de intentos permitidos
            
        Returns:
            bool: True si la autenticación es exitosa
        """
        print(f"🔑 Intento {intento}/{intentos_maximos}")
        usuario = input("👤 Usuario: ").strip()
        password = input("🔑 Contraseña: ").strip()
        
        # Validar formato de credenciales
        es_valido, mensaje_error = ValidadorEntrada.validar_credenciales(usuario, password)
        if not es_valido:
            print(f"❌ {mensaje_error}")
            self._pausar_entre_intentos()
            return False
        
        # Verificar credenciales
        if self._verificar_credenciales(usuario, password):
            return True
        else:
            self._manejar_intento_fallido(intento, intentos_maximos)
            return False
    
    def _verificar_credenciales(self, usuario: str, password: str) -> bool:
        """
        Verifica las credenciales contra las almacenadas.
        
        Args:
            usuario: Nombre de usuario
            password: Contraseña en texto plano
            
        Returns:
            bool: True si las credenciales son correctas
        """
        return (usuario == self.credenciales_admin["usuario"] and 
                self._generar_hash(password) == self.credenciales_admin["password_hash"])
    
    def _activar_sesion_administrador(self):
        """Activa la sesión de administrador y registra el evento."""
        from datetime import datetime
        
        self.usuario_actual = TipoUsuario.ADMINISTRADOR
        self.sesion_activa = True
        self.intentos_fallidos = 0
        
        # Registrar información de sesión
        ahora = datetime.now()
        self.info_sesion = {
            'hora_inicio': ahora,
            'ultimo_acceso': ahora,
            'acciones_realizadas': ['login_exitoso']
        }
        
        self._mostrar_mensaje_bienvenida()
    
    def _mostrar_mensaje_bienvenida(self):
        """Muestra mensaje de bienvenida al administrador."""
        print("\n✅ AUTENTICACIÓN EXITOSA")
        print("👨‍💼 Bienvenido, Administrador")
        print("🔓 Acceso completo al sistema activado")
        
        # Mostrar información de sesión
        if self.info_sesion['hora_inicio']:
            hora_inicio = self.info_sesion['hora_inicio'].strftime("%H:%M:%S")
            print(f"⏰ Sesión iniciada: {hora_inicio}")
    
    def _manejar_intento_fallido(self, intento_actual: int, intentos_maximos: int):
        """
        Maneja un intento de autenticación fallido.
        
        Args:
            intento_actual: Número del intento actual
            intentos_maximos: Máximo número de intentos
        """
        self.intentos_fallidos += 1
        intentos_restantes = intentos_maximos - intento_actual
        
        if intentos_restantes > 0:
            print(f"❌ Credenciales incorrectas")
            print(f"⚠️  Te quedan {intentos_restantes} intentos")
            self._pausar_entre_intentos()
        else:
            print("❌ ACCESO DENEGADO")
            print("🔒 Máximo de intentos alcanzado")
            print("💡 Regresando al modo anónimo...")
    
    def _pausar_entre_intentos(self):
        """Pausa breve entre intentos para evitar ataques de fuerza bruta."""
        import time
        print("⏳ Esperando...")
        time.sleep(1)  # Pausa de 1 segundo
        print()
    
    def _manejar_cancelacion_autenticacion(self):
        """Maneja la cancelación de la autenticación por parte del usuario."""
        print("\n\n❌ Autenticación cancelada por el usuario")
        print("🔄 Regresando al modo anónimo...")
    
    def _manejar_autenticacion_fallida(self):
        """Maneja el caso de autenticación completamente fallida."""
        if self.intentos_fallidos > 0:
            print(f"\n🔒 Sesión bloqueada temporalmente")
            print("💡 Puedes intentar nuevamente más tarde")
    
    def cerrar_sesion(self):
        """
        Cierra la sesión del administrador y limpia el estado.
        """
        if self.sesion_activa:
            self._registrar_cierre_sesion()
            self._mostrar_mensaje_despedida()
            
        self._limpiar_estado_sesion()
    
    def _registrar_cierre_sesion(self):
        """Registra el evento de cierre de sesión."""
        from datetime import datetime
        
        if self.info_sesion['acciones_realizadas']:
            self.info_sesion['acciones_realizadas'].append('logout')
        
        duracion_sesion = None
        if self.info_sesion['hora_inicio']:
            duracion_sesion = datetime.now() - self.info_sesion['hora_inicio']
            minutos = int(duracion_sesion.total_seconds() / 60)
            print(f"⏱️  Duración de sesión: {minutos} minutos")
    
    def _mostrar_mensaje_despedida(self):
        """Muestra mensaje de despedida al cerrar sesión."""
        print("\n👋 CERRANDO SESIÓN DE ADMINISTRADOR")
        print("🔄 Regresando al modo anónimo...")
        print("🔒 Todas las funciones administrativas han sido desactivadas")
    
    def _limpiar_estado_sesion(self):
        """Limpia completamente el estado de la sesión."""
        self.usuario_actual = TipoUsuario.ANONIMO
        self.sesion_activa = False
        self.intentos_fallidos = 0
        self.info_sesion = {
            'hora_inicio': None,
            'ultimo_acceso': None,
            'acciones_realizadas': []
        }
    
    def registrar_accion(self, accion: str):
        """
        Registra una acción realizada durante la sesión.
        
        Args:
            accion: Descripción de la acción realizada
        """
        from datetime import datetime
        
        if self.sesion_activa:
            self.info_sesion['ultimo_acceso'] = datetime.now()
            self.info_sesion['acciones_realizadas'].append(accion)
    
    def es_administrador(self) -> bool:
        """
        Verifica si el usuario actual es administrador con sesión activa.
        
        Returns:
            bool: True si es administrador autenticado
        """
        return self.usuario_actual == TipoUsuario.ADMINISTRADOR and self.sesion_activa
    
    def es_anonimo(self) -> bool:
        """
        Verifica si el usuario actual es anónimo.
        
        Returns:
            bool: True si es usuario anónimo
        """
        return self.usuario_actual == TipoUsuario.ANONIMO
    
    def obtener_permisos(self) -> Permisos:
        """
        Obtiene los permisos del usuario actual.
        
        Returns:
            Permisos: Objeto con los permisos del usuario
        """
        return GestorPermisos.obtener_permisos(self.usuario_actual)
    
    def verificar_permiso(self, permiso_requerido: str) -> bool:
        """
        Verifica si el usuario actual tiene un permiso específico.
        
        Args:
            permiso_requerido: Nombre del permiso a verificar
            
        Returns:
            bool: True si tiene el permiso
        """
        if not self.sesion_activa and self.usuario_actual == TipoUsuario.ADMINISTRADOR:
            return False  # Sesión expirada
            
        permisos = self.obtener_permisos()
        return permisos.tiene_permiso(permiso_requerido)
    
    def requerir_permiso(self, permiso_requerido: str, mostrar_error: bool = True) -> bool:
        """
        Verifica un permiso y opcionalmente muestra error si no lo tiene.
        
        Args:
            permiso_requerido: Permiso requerido
            mostrar_error: Si mostrar mensaje de error
            
        Returns:
            bool: True si tiene el permiso
        """
        if self.verificar_permiso(permiso_requerido):
            return True
        
        if mostrar_error:
            self._mostrar_error_acceso_denegado(permiso_requerido)
        
        return False
    
    def _mostrar_error_acceso_denegado(self, permiso: str):
        """Muestra mensaje de error por acceso denegado."""
        print(f"\n❌ ACCESO DENEGADO")
        print(f"🔒 Se requiere permiso: {permiso}")
        print("💡 Inicia sesión como administrador para acceder a esta función")
    
    def cambiar_credenciales(self, nuevo_usuario: str, nueva_password: str) -> bool:
        """
        Cambia las credenciales del administrador.
        Solo disponible para administradores autenticados.
        
        Args:
            nuevo_usuario: Nuevo nombre de usuario
            nueva_password: Nueva contraseña
            
        Returns:
            bool: True si el cambio fue exitoso
        """
        if not self.requerir_permiso('cambiar_credenciales'):
            return False
        
        # Validar nuevas credenciales
        es_valido, mensaje_error = ValidadorEntrada.validar_credenciales(
            nuevo_usuario, nueva_password
        )
        if not es_valido:
            print(f"❌ {mensaje_error}")
            return False
        
        # Confirmar el cambio
        if not self._confirmar_cambio_credenciales(nuevo_usuario):
            return False
        
        # Aplicar cambio
        self.credenciales_admin = {
            "usuario": nuevo_usuario,
            "password_hash": self._generar_hash(nueva_password)
        }
        
        self.registrar_accion(f"credenciales_cambiadas_a_{nuevo_usuario}")
        print("\n✅ Credenciales actualizadas exitosamente")
        print("🔒 Las nuevas credenciales estarán vigentes en el próximo acceso")
        return True
    
    def _confirmar_cambio_credenciales(self, nuevo_usuario: str) -> bool:
        """
        Confirma el cambio de credenciales con el usuario.
        
        Args:
            nuevo_usuario: Nuevo nombre de usuario
            
        Returns:
            bool: True si el usuario confirma
        """
        print(f"\n⚠️  CONFIRMACIÓN DE CAMBIO DE CREDENCIALES")
        print(f"👤 Usuario actual: {self.credenciales_admin['usuario']}")
        print(f"👤 Nuevo usuario: {nuevo_usuario}")
        print("🔑 Nueva contraseña: [OCULTA]")
        print()
        print("💡 Este cambio afectará futuros inicios de sesión")
        
        confirmacion = input("🔹 ¿Confirmas el cambio? (s/n): ").strip().lower()
        return ValidadorEntrada.validar_confirmacion(confirmacion)
    
    def obtener_info_sesion(self) -> dict:
        """
        Obtiene información detallada de la sesión actual.
        
        Returns:
            dict: Información de la sesión
        """
        info = {
            'tipo_usuario': self.usuario_actual.value,
            'sesion_activa': self.sesion_activa,
            'intentos_fallidos': self.intentos_fallidos
        }
        
        if self.sesion_activa:
            info.update({
                'hora_inicio': self.info_sesion['hora_inicio'],
                'ultimo_acceso': self.info_sesion['ultimo_acceso'],
                'acciones_realizadas': len(self.info_sesion['acciones_realizadas']),
                'permisos': self.obtener_permisos().__dict__
            })
        
        return info
    
    def obtener_resumen_permisos(self) -> dict:
        """
        Obtiene un resumen legible de los permisos actuales.
        
        Returns:
            dict: Resumen de permisos
        """
        return GestorPermisos.obtener_descripcion_permisos(self.usuario_actual)
    
    def validar_sesion(self) -> bool:
        """
        Valida que la sesión actual sea válida y consistente.
        
        Returns:
            bool: True si la sesión es válida
        """
        # Verificar consistencia del estado
        if self.usuario_actual == TipoUsuario.ADMINISTRADOR and not self.sesion_activa:
            # Estado inconsistente, limpiar
            self._limpiar_estado_sesion()
            return False
        
        # Verificar si la sesión ha expirado (opcional)
        if self.sesion_activa and self.info_sesion['hora_inicio']:
            from datetime import datetime, timedelta
            ahora = datetime.now()
            tiempo_sesion = ahora - self.info_sesion['hora_inicio']
            
            # Sesión máxima de 8 horas
            if tiempo_sesion > timedelta(hours=8):
                print("\n⏰ Sesión expirada por tiempo")
                self.cerrar_sesion()
                return False
        
        return True

class DecoradorPermisos:
    """Decorador para verificar permisos antes de ejecutar funciones."""
    
    def __init__(self, gestor_roles: GestorRoles):
        """
        Inicializa el decorador con el gestor de roles.
        
        Args:
            gestor_roles: Instancia del gestor de roles
        """
        self.gestor_roles = gestor_roles
    
    def requiere_permiso(self, permiso: str):
        """
        Decorador que requiere un permiso específico.
        
        Args:
            permiso: Permiso requerido
        """
        def decorador(func):
            def wrapper(*args, **kwargs):
                if self.gestor_roles.requerir_permiso(permiso):
                    return func(*args, **kwargs)
                return None
            return wrapper
        return decorador
    
    def solo_administrador(self, func):
        """Decorador que requiere acceso de administrador."""
        def wrapper(*args, **kwargs):
            if self.gestor_roles.es_administrador():
                return func(*args, **kwargs)
            else:
                print("\n❌ ACCESO DENEGADO: Se requieren permisos de administrador")
                return None
        return wrapper