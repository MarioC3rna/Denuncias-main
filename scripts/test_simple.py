"""
Test simple para verificar que el sistema funciona sin imports circulares.
"""

import sys
import os
from pathlib import Path

# Agregar directorio padre al path
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

def test_componentes_basicos():
    """Prueba los componentes básicos del sistema."""
    print("🧪 PROBANDO COMPONENTES BÁSICOS...")
    
    try:
        # Test 1: Configuración
        from config.settings import ConfiguracionSistema
        config = ConfiguracionSistema()
        print("✅ ConfiguracionSistema: OK")
        
        # Test 2: Gestor de roles
        from auth.gestor_roles import GestorRoles
        gestor_roles = GestorRoles()
        print("✅ GestorRoles: OK")
        
        # Test 3: Validadores
        from utils.validators import ValidadorEntrada
        resultado = ValidadorEntrada.validar_opcion_menu("1", ["1", "2"])
        assert resultado == "1"
        print("✅ ValidadorEntrada: OK")
        
        # Test 4: Formatters
        from utils.formatters import FormateadorConsola
        formatter = FormateadorConsola()
        print("✅ FormateadorConsola: OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_navegacion():
    """Prueba el sistema de navegación."""
    print("\n🧪 PROBANDO NAVEGACIÓN...")
    
    try:
        # Test controlador (NUEVO: desde archivo separado)
        from interfaces.controlador_navegacion import ControladorNavegacion
        
        # Crear componentes básicos
        from config.settings import ConfiguracionSistema
        from auth.gestor_roles import GestorRoles
        
        config = ConfiguracionSistema()
        gestor_roles = GestorRoles()
        
        # Simular gestor de denuncias básico
        class GestorDenunciasFalso:
            def obtener_estadisticas(self):
                return {'Acoso': 1, 'Otros': 2}
        
        gestor_denuncias = GestorDenunciasFalso()
        
        # Crear controlador
        controlador = ControladorNavegacion(gestor_denuncias, gestor_roles)
        print("✅ ControladorNavegacion: OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en navegación: {e}")
        return False

def test_consola_base():
    """Prueba la clase base de consola."""
    print("\n🧪 PROBANDO CONSOLA BASE...")
    
    try:
        # Test clase base (NUEVO: sin imports circulares)
        from interfaces.consola_base import InterfazConsolaBase
        print("✅ InterfazConsolaBase: OK (importación exitosa)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en consola base: {e}")
        return False

def main():
    """Función principal de test."""
    print("🚀 TEST SIMPLE DEL SISTEMA REFACTORIZADO")
    print("=" * 45)
    
    test1 = test_componentes_basicos()
    test2 = test_navegacion()
    test3 = test_consola_base()
    
    print("\n" + "=" * 45)
    if test1 and test2 and test3:
        print("🎉 ¡TODOS LOS TESTS PASARON!")
        print("✅ El sistema está listo para ejecutar")
        print("🚀 Ejecuta: python main.py")
        return 0
    else:
        print("❌ Algunos tests fallaron")
        print("💡 Revisa los errores anteriores")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)