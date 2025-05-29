"""
Sistema Anónimo de Denuncias Internas - Versión Final
Arquitectura consolidada con agente IA simplificado integrado.
"""

import sys
import os
from pathlib import Path

# AGREGAR ESTAS LÍNEAS ANTES DE OTROS IMPORTS
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

# Verificar que utils existe
utils_path = current_dir / "utils"
if not utils_path.exists():
    print(f"❌ Error: Directorio utils no encontrado en {utils_path}")
    sys.exit(1)

# Agregar el directorio actual al path para imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

def verificar_dependencias():
    """Verifica que las dependencias básicas estén disponibles."""
    dependencias_requeridas = [
        'config.settings',
        'auth.gestor_roles',
        'interfaces.controlador_navegacion',
        'src.core.gestor_denuncias'  # NUEVO: GestorDenuncias integrado
    ]
    
    dependencias_faltantes = []
    
    for dep in dependencias_requeridas:
        try:
            __import__(dep)
        except ImportError as e:
            dependencias_faltantes.append(f"{dep}: {e}")
    
    if dependencias_faltantes:
        print("❌ DEPENDENCIAS FALTANTES:")
        for dep in dependencias_faltantes:
            print(f"   • {dep}")
        return False
    
    return True

def inicializar_sistema():
    """Inicializa los componentes principales del sistema."""
    try:
        # Importar componentes principales
        from config.settings import ConfiguracionSistema
        from auth.gestor_roles import GestorRoles
        from interfaces.controlador_navegacion import ControladorNavegacion
        from src.core.gestor_denuncias import GestorDenuncias  # NUEVO
        
        print("🔧 Inicializando sistema...")
        
        # Inicializar componentes
        gestor_denuncias = GestorDenuncias()
        print("✅ GestorDenuncias con IA: OK")
        
        gestor_roles = GestorRoles()
        print("✅ GestorRoles: OK")
        
        controlador = ControladorNavegacion(gestor_denuncias, gestor_roles)
        print("✅ ControladorNavegacion: OK")
        
        return gestor_denuncias, gestor_roles, controlador
        
    except Exception as e:
        print(f"❌ Error inicializando sistema: {e}")
        return None, None, None

def mostrar_informacion_inicio():
    """Muestra información inicial del sistema."""
    from config.settings import ConfiguracionSistema
    
    config = ConfiguracionSistema()
    banner = config.BANNER
    
    print("=" * banner['ancho'])
    print(banner['titulo'])
    print("=" * banner['ancho'])
    print("🎉 SISTEMA CONSOLIDADO - VERSIÓN FINAL")
    print("🤖 Agente IA Simplificado Integrado")
    print("🔧 Arquitectura Optimizada y Mantenible")
    print("🔒 Privacidad y Anonimato Garantizados")
    print("=" * banner['ancho'])
    print()

def main():
    """Función principal del sistema consolidado."""
    try:
        # Mostrar información de inicio
        mostrar_informacion_inicio()
        
        # Verificar dependencias
        print("🔍 Verificando dependencias...")
        if not verificar_dependencias():
            print("\n❌ No se puede continuar sin las dependencias requeridas")
            return 1
        
        print("✅ Todas las dependencias están disponibles")
        print()
        
        # Inicializar sistema
        gestor_denuncias, gestor_roles, controlador = inicializar_sistema()
        
        if not all([gestor_denuncias, gestor_roles, controlador]):
            print("\n❌ Error crítico en la inicialización")
            return 1
        
        print("🚀 Sistema consolidado inicializado correctamente")
        
        # Mostrar info del agente IA
        info_ia = gestor_denuncias.obtener_info_agente_ia()
        if info_ia.get('disponible', False):
            print("🤖 Agente IA simplificado: ACTIVO")
        else:
            print("⚠️ Agente IA: MODO BÁSICO")
        
        print("📱 Iniciando interfaz de usuario...")
        print()
        
        # Ejecutar navegación principal
        controlador.ejecutar_navegacion_principal()
        
        print("\n👋 Sistema finalizado correctamente")
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupción detectada")
        print("👋 Cerrando sistema de forma segura...")
        return 0
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        print("💡 Contacta al administrador del sistema")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
