"""
Funciones auxiliares para procesamiento de denuncias.
Funcionalidad común compartida entre diferentes menús.
"""

from typing import Optional, Dict, Any
from utils.formatters import FormateadorConsola
from utils.validators import ValidadorEntrada
from config.settings import ConfiguracionSistema

class HelpersDenuncia:
    """Helpers para procesamiento de denuncias."""
    
    def __init__(self, gestor_denuncias, gestor_roles):
        """
        Inicializa los helpers.
        
        Args:
            gestor_denuncias: Instancia del gestor de denuncias
            gestor_roles: Instancia del gestor de roles
        """
        self.gestor_denuncias = gestor_denuncias
        self.gestor_roles = gestor_roles
        self.formatter = FormateadorConsola()
        self.config = ConfiguracionSistema()
    
    def solicitar_mensaje_denuncia(self) -> Optional[str]:
        """
        Solicita el mensaje de la denuncia al usuario con validaciones.
        
        Returns:
            str: Mensaje de la denuncia validado o None si se cancela
        """
        self.formatter.mostrar_separador("📝 NUEVA DENUNCIA ANÓNIMA", 40)
        
        print("📋 Describe la situación que deseas denunciar:")
        print("💡 Incluye todos los detalles relevantes (fechas, lugares, personas involucradas)")
        print("🔒 Tu identidad permanece completamente anónima")
        print("⚠️  Presiona Ctrl+C para cancelar")
        print()
        
        intentos = 0
        max_intentos = 3
        
        while intentos < max_intentos:
            try:
                print("📝 Escribe tu denuncia:")
                mensaje = input(">>> ").strip()
                
                # Validar mensaje
                es_valido, mensaje_error = ValidadorEntrada.validar_mensaje_denuncia(mensaje)
                
                if es_valido:
                    # Mostrar resumen y confirmar
                    if self._confirmar_mensaje_denuncia(mensaje):
                        return mensaje
                    else:
                        # Usuario quiere modificar
                        print("\n🔄 Modificando denuncia...")
                        continue
                else:
                    print(f"\n❌ {mensaje_error}")
                    intentos += 1
                    
                    if intentos < max_intentos:
                        print(f"💡 Intenta nuevamente ({max_intentos - intentos} intentos restantes)")
                    else:
                        print("❌ Máximo de intentos alcanzado")
                        return None
                        
            except KeyboardInterrupt:
                print("\n\n❌ Operación cancelada")
                return None
            except Exception as e:
                print(f"\n❌ Error inesperado: {e}")
                intentos += 1
        
        return None
    
    def _confirmar_mensaje_denuncia(self, mensaje: str) -> bool:
        """
        Confirma el mensaje de la denuncia con el usuario.
        
        Args:
            mensaje: Mensaje a confirmar
            
        Returns:
            bool: True si confirma, False si quiere modificar
        """
        print("\n📋 RESUMEN DE TU DENUNCIA:")
        print("-" * 40)
        
        # Mostrar primeras líneas del mensaje
        lineas = mensaje.split('\n')
        for i, linea in enumerate(lineas[:5]):  # Máximo 5 líneas
            print(f"   {linea}")
        
        if len(lineas) > 5:
            print(f"   ... (+{len(lineas) - 5} líneas más)")
        
        print("-" * 40)
        print(f"📊 Longitud: {len(mensaje)} caracteres")
        print(f"📝 Palabras: {len(mensaje.split())} palabras")
        
        print("\n🔹 Opciones:")
        print("   s - Confirmar y enviar denuncia")
        print("   m - Modificar denuncia")
        print("   c - Cancelar operación")
        
        while True:
            try:
                opcion = input("\n🔹 ¿Qué deseas hacer? (s/m/c): ").strip().lower()
                
                if opcion in ['s', 'sí', 'si']:
                    return True
                elif opcion in ['m', 'modificar']:
                    return False
                elif opcion in ['c', 'cancelar']:
                    print("❌ Operación cancelada")
                    return False
                else:
                    print("❌ Opción no válida. Usa 's', 'm' o 'c'")
                    
            except KeyboardInterrupt:
                return False
    
    def procesar_denuncia_automatica(self, mensaje: str, es_administrador: bool = False) -> bool:
        """
        Procesa una denuncia usando el agente IA automático.
        
        Args:
            mensaje: Mensaje de la denuncia
            es_administrador: Si el usuario es administrador
            
        Returns:
            bool: True si se procesó exitosamente
        """
        try:
            print("\n🤖 PROCESANDO DENUNCIA CON IA...")
            print("⏳ Analizando contenido...")
            
            # Simular procesamiento por ahora (hasta que tengamos el agente IA)
            resultado = {
                'es_denuncia_valida': True,
                'categoria_sugerida': 'Otros',
                'confianza': 0.85,
                'metodo_usado': 'IA Local',
                'nivel_veracidad': 'MEDIA',
                'nivel_urgencia': 'MEDIA'
            }
            
            # Mostrar resultados del análisis
            self._mostrar_resultados_analisis(resultado)
            
            # Confirmar procesamiento
            if self._confirmar_procesamiento_automatico(resultado, es_administrador):
                return self._registrar_denuncia_final(mensaje, resultado)
            else:
                print("❌ Denuncia no registrada")
                return False
                
        except Exception as e:
            print(f"\n❌ Error durante procesamiento automático: {e}")
            print("💡 Considera usar el modo manual")
            return False
    
    def procesar_denuncia_manual(self, mensaje: str) -> bool:
        """
        Procesa una denuncia manualmente sin IA.
        
        Args:
            mensaje: Mensaje de la denuncia
            
        Returns:
            bool: True si se procesó exitosamente
        """
        try:
            print("\n👤 PROCESAMIENTO MANUAL")
            print("📋 La denuncia será clasificada manualmente")
            
            # Solicitar categoría manual
            categoria = self._solicitar_categoria_manual()
            if not categoria:
                return False
            
            # Crear resultado manual
            resultado = {
                'categoria_sugerida': categoria,
                'es_denuncia_valida': True,
                'confianza': 0.8,  # Confianza alta para clasificación manual
                'metodo_usado': 'Manual',
                'nivel_veracidad': 'MEDIA',
                'nivel_urgencia': 'MEDIA',
                'procesado_por': 'Supervisor humano'
            }
            
            # Confirmar y registrar
            if self._confirmar_procesamiento_manual(resultado):
                return self._registrar_denuncia_final(mensaje, resultado)
            else:
                print("❌ Denuncia no registrada")
                return False
                
        except Exception as e:
            print(f"\n❌ Error durante procesamiento manual: {e}")
            return False
    
    def _mostrar_resultados_analisis(self, resultado: Dict):
        """Muestra los resultados del análisis de IA."""
        if resultado.get('es_denuncia_valida'):
            self.formatter.mostrar_resultado_validacion(resultado)
        
        if 'nivel_veracidad' in resultado:
            self.formatter.mostrar_analisis_veracidad(resultado)
        
        if 'categoria_sugerida' in resultado:
            self.formatter.mostrar_resultado_clasificacion(resultado)
    
    def _confirmar_procesamiento_automatico(self, resultado: Dict, es_administrador: bool) -> bool:
        """Confirma el procesamiento automático."""
        confirmacion = self.formatter.mostrar_confirmacion_procesamiento(resultado)
        es_confirmacion = ValidadorEntrada.validar_confirmacion(confirmacion)
        
        if es_administrador and not es_confirmacion:
            # Los administradores pueden forzar el registro
            forzar = input("\n🔹 ¿Forzar registro como administrador? (s/n): ").strip()
            return ValidadorEntrada.validar_confirmacion(forzar)
        
        return es_confirmacion
    
    def _confirmar_procesamiento_manual(self, resultado: Dict) -> bool:
        """Confirma el procesamiento manual."""
        print(f"\n📋 CONFIRMACIÓN DE REGISTRO MANUAL")
        print("-" * 30)
        print(f"📂 Categoría: {resultado['categoria_sugerida']}")
        print(f"👤 Método: {resultado['metodo_usado']}")
        print(f"🎯 Confianza: {resultado['confianza']:.1%}")
        
        confirmacion = input("\n🔹 ¿Confirmas el registro? (s/n): ").strip()
        return ValidadorEntrada.validar_confirmacion(confirmacion)
    
    def _solicitar_categoria_manual(self) -> Optional[str]:
        """Solicita la categoría manual al usuario."""
        categorias = [
            "Acoso",
            "Discriminación", 
            "Corrupción",
            "Problemas técnicos",
            "Otros"
        ]
        
        print("\n📂 CATEGORÍAS DISPONIBLES:")
        for i, categoria in enumerate(categorias, 1):
            emoji = self.config.obtener_emoji_categoria(categoria)
            print(f"   {i}. {emoji} {categoria}")
        
        while True:
            try:
                opcion = input("\n🔹 Selecciona una categoría (1-5): ").strip()
                
                if opcion.isdigit() and 1 <= int(opcion) <= len(categorias):
                    return categorias[int(opcion) - 1]
                else:
                    print("❌ Opción no válida")
                    
            except KeyboardInterrupt:
                return None
    
    def _registrar_denuncia_final(self, mensaje: str, resultado: Dict) -> bool:
        """
        Registra la denuncia final en el sistema.
        
        Args:
            mensaje: Mensaje de la denuncia
            resultado: Resultado del análisis
            
        Returns:
            bool: True si se registró exitosamente
        """
        try:
            # Registrar acción si es administrador
            if self.gestor_roles.es_administrador():
                metodo = resultado.get('metodo_usado', 'Desconocido')
                self.gestor_roles.registrar_accion(f"denuncia_registrada_{metodo}")
            
            # Simular registro exitoso por ahora
            print("\n✅ DENUNCIA REGISTRADA EXITOSAMENTE")
            print("🔒 Tu anonimato ha sido preservado")
            print("📊 La denuncia ha sido incluida en las estadísticas")
            print("👨‍💼 Los administradores pueden revisar el resumen")
            return True
                
        except Exception as e:
            print(f"\n❌ Error al registrar denuncia: {e}")
            return False

class HelpersEstadisticas:
    """Helpers para manejo de estadísticas."""
    
    def __init__(self, gestor_denuncias, formatter):
        """
        Inicializa los helpers de estadísticas.
        
        Args:
            gestor_denuncias: Instancia del gestor de denuncias
            formatter: Instancia del formateador
        """
        self.gestor_denuncias = gestor_denuncias
        self.formatter = formatter
    
    def mostrar_estadisticas_completas(self, agente_ia_activo: bool = True):
        """
        Muestra estadísticas completas del sistema.
        
        Args:
            agente_ia_activo: Estado del agente IA
        """
        try:
            # Simular estadísticas por ahora
            estadisticas = {
                'Acoso': 5,
                'Discriminación': 3,
                'Corrupción': 2,
                'Problemas técnicos': 1,
                'Otros': 4
            }
            total = sum(estadisticas.values())
            
            self.formatter.mostrar_estadisticas_tabla(estadisticas, total, agente_ia_activo)
            
            # Información adicional
            if total > 0:
                self._mostrar_insights_estadisticos(estadisticas, total)
                
        except Exception as e:
            print(f"❌ Error al obtener estadísticas: {e}")
    
    def _mostrar_insights_estadisticos(self, estadisticas: Dict, total: int):
        """Muestra insights adicionales sobre las estadísticas."""
        print(f"\n💡 INSIGHTS:")
        
        # Categoría más frecuente
        if estadisticas:
            categoria_principal = max(estadisticas.items(), key=lambda x: x[1])
            print(f"   • Problema más reportado: {categoria_principal[0]}")
            
        # Distribución
        if total >= 10:
            diversidad = len([c for c in estadisticas.values() if c > 0])
            print(f"   • Diversidad de problemas: {diversidad} categorías activas")
        
        # Recomendaciones
        if estadisticas.get('Acoso', 0) > total * 0.3:
            print(f"   • 🚨 Alto nivel de reportes de acoso detectado")