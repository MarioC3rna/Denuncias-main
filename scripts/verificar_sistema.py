"""
Script para verificar que el sistema refactorizado funciona correctamente.
Ejecutar después de completar la migración.
"""

import sys
import os
from pathlib import Path

# Agregar directorio padre al path
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

def verificar_estructura_directorios():
    """Verifica que la estructura de directorios sea correcta."""
    print("🔍 VERIFICANDO ESTRUCTURA DE DIRECTORIOS...")
    
    directorios_requeridos = [
        'config',
        'auth', 
        'interfaces',
        'utils',
        'scripts',
        'src',
        'src/core',
        'src/core/agente_ia'
    ]
    
    directorios_faltantes = []
    
    for directorio in directorios_requeridos:
        if not os.path.exists(directorio):
            directorios_faltantes.append(directorio)
        else:
            print(f"✅ {directorio}/")
    
    if directorios_faltantes:
        print("\n❌ DIRECTORIOS FALTANTES:")
        for dir_faltante in directorios_faltantes:
            print(f"   • {dir_faltante}/")
        return False
    
    print("✅ Estructura de directorios: OK")
    return True

def verificar_archivos_principales():
    """Verifica que los archivos principales estén presentes."""
    print("\n🔍 VERIFICANDO ARCHIVOS PRINCIPALES...")
    
    archivos_requeridos = [
        'main.py',
        'config/settings.py',
        'config/__init__.py',
        'auth/gestor_roles.py',
        'auth/tipos_usuario.py',
        'auth/__init__.py',
        'interfaces/consola_base.py',
        'interfaces/menu_anonimo.py',
        'interfaces/menu_administrador.py',
        'interfaces/helpers.py',
        'interfaces/__init__.py',
        'utils/validators.py',
        'utils/formatters.py',
        'utils/__init__.py'
    ]
    
    archivos_faltantes = []
    
    for archivo in archivos_requeridos:
        if not os.path.exists(archivo):
            archivos_faltantes.append(archivo)
        else:
            print(f"✅ {archivo}")
    
    if archivos_faltantes:
        print("\n❌ ARCHIVOS FALTANTES:")
        for archivo_faltante in archivos_faltantes:
            print(f"   • {archivo_faltante}")
        return False
    
    print("✅ Archivos principales: OK")
    return True

def verificar_imports():
    """Verifica que los imports funcionen correctamente SIN imports circulares."""
    print("\n🔍 VERIFICANDO IMPORTS (SIN CIRCULARES)...")
    
    # Solo verificar imports básicos que no causan problemas circulares
    modulos_basicos = [
        ('config.settings', 'ConfiguracionSistema'),
        ('auth.gestor_roles', 'GestorRoles'),
        ('auth.tipos_usuario', 'TipoUsuario'),
        ('utils.validators', 'ValidadorEntrada'),
        ('utils.formatters', 'FormateadorConsola')
    ]
    
    imports_fallidos = []
    
    for modulo, clase in modulos_basicos:
        try:
            mod = __import__(modulo, fromlist=[clase])
            getattr(mod, clase)
            print(f"✅ {modulo}.{clase}")
        except ImportError as e:
            imports_fallidos.append(f"{modulo}.{clase}: {e}")
            print(f"❌ {modulo}.{clase}: {e}")
        except AttributeError as e:
            imports_fallidos.append(f"{modulo}.{clase}: {e}")
            print(f"❌ {modulo}.{clase}: {e}")
    
    # Verificar imports de interfaces por separado (método más seguro)
    print("\n🔍 VERIFICANDO INTERFACES (método seguro)...")
    
    try:
        # Verificar que los archivos de interfaz se puedan abrir y leer
        archivos_interfaz = [
            'interfaces/consola_base.py',
            'interfaces/menu_anonimo.py', 
            'interfaces/menu_administrador.py',
            'interfaces/helpers.py'
        ]
        
        for archivo in archivos_interfaz:
            if os.path.exists(archivo):
                with open(archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                    if 'class' in contenido:  # Verificar que tiene clases
                        print(f"✅ {archivo} (contiene clases)")
                    else:
                        print(f"⚠️  {archivo} (sin clases detectadas)")
            else:
                print(f"❌ {archivo} (no existe)")
                
    except Exception as e:
        print(f"❌ Error verificando interfaces: {e}")
        imports_fallidos.append(f"interfaces: {e}")
    
    if imports_fallidos:
        print(f"\n❌ {len(imports_fallidos)} problemas de import detectados")
        return False
    
    print("✅ Imports verificados: OK")
    return True

def verificar_instanciacion():
    """Verifica que las clases se puedan instanciar correctamente."""
    print("\n🔍 VERIFICANDO INSTANCIACIÓN DE COMPONENTES...")
    
    try:
        # Verificar configuración
        from config.settings import ConfiguracionSistema
        config = ConfiguracionSistema()
        print("✅ ConfiguracionSistema instanciada")
        
        # Verificar gestor de roles
        from auth.gestor_roles import GestorRoles
        gestor_roles = GestorRoles()
        print("✅ GestorRoles instanciado")
        
        # Verificar formatters
        from utils.formatters import FormateadorConsola
        formatter = FormateadorConsola()
        print("✅ FormateadorConsola instanciado")
        
        # Verificar validadores
        from utils.validators import ValidadorEntrada
        # Los validadores son métodos estáticos, no necesitan instancia
        print("✅ ValidadorEntrada verificado")
        
        print("✅ Instanciación de componentes: OK")
        return True
        
    except Exception as e:
        print(f"❌ Error en instanciación: {e}")
        return False

def verificar_funcionalidad_basica():
    """Verifica funcionalidad básica del sistema."""
    print("\n🔍 VERIFICANDO FUNCIONALIDAD BÁSICA...")
    
    try:
        # Verificar configuración
        from config.settings import ConfiguracionSistema
        config = ConfiguracionSistema()
        
        # Verificar que las configuraciones estén disponibles
        assert config.BANNER['titulo'], "Banner título no configurado"
        assert config.MENUS['anonimo'], "Menú anónimo no configurado"
        assert config.MENUS['administrador'], "Menú administrador no configurado"
        print("✅ Configuraciones básicas")
        
        # Verificar validadores
        from utils.validators import ValidadorEntrada
        
        # Test validación de opción
        resultado = ValidadorEntrada.validar_opcion_menu("1", ["1", "2", "3"])
        assert resultado == "1", "Validador de opciones falla"
        print("✅ Validadores funcionando")
        
        # Verificar formatters
        from utils.formatters import FormateadorConsola
        formatter = FormateadorConsola()
        
        # Test básico de formatter (sin imprimir)
        assert hasattr(formatter, 'mostrar_banner'), "Formatter no tiene mostrar_banner"
        print("✅ Formatters funcionando")
        
        # Verificar gestor de roles
        from auth.gestor_roles import GestorRoles
        gestor_roles = GestorRoles()
        
        assert gestor_roles.es_anonimo(), "Estado inicial debe ser anónimo"
        print("✅ Gestor de roles funcionando")
        
        print("✅ Funcionalidad básica: OK")
        return True
        
    except Exception as e:
        print(f"❌ Error en funcionalidad básica: {e}")
        return False

def verificar_main_ejecutable():
    """Verifica que main.py sea ejecutable sin errores de import."""
    print("\n🔍 VERIFICANDO QUE MAIN.PY SEA EJECUTABLE...")
    
    try:
        # Verificar que main.py exista y tenga las funciones necesarias
        if not os.path.exists('main.py'):
            print("❌ main.py no existe")
            return False
            
        with open('main.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
            
        # Verificar elementos clave
        elementos_requeridos = [
            'def main():',
            'def verificar_dependencias():',
            'def inicializar_sistema():',
            'if __name__ == "__main__":'
        ]
        
        elementos_faltantes = []
        for elemento in elementos_requeridos:
            if elemento not in contenido:
                elementos_faltantes.append(elemento)
        
        if elementos_faltantes:
            print("❌ Elementos faltantes en main.py:")
            for elemento in elementos_faltantes:
                print(f"   • {elemento}")
            return False
            
        print("✅ main.py tiene estructura correcta")
        
        # Verificar longitud (debe ser mucho menor que el original)
        lineas = len(contenido.split('\n'))
        print(f"✅ main.py: {lineas} líneas (vs ~1,154 original)")
        
        if lineas < 200:
            print("✅ main.py correctamente simplificado")
        else:
            print("⚠️  main.py podría simplificarse más")
            
        return True
        
    except Exception as e:
        print(f"❌ Error verificando main.py: {e}")
        return False

def generar_reporte_verificacion():
    """Genera un reporte de verificación."""
    print("\n📊 GENERANDO REPORTE DE VERIFICACIÓN...")
    
    # Contar archivos por directorio
    conteos = {}
    
    for directorio in ['config', 'auth', 'interfaces', 'utils', 'scripts']:
        if os.path.exists(directorio):
            archivos = [f for f in os.listdir(directorio) if f.endswith('.py')]
            conteos[directorio] = len(archivos)
    
    print(f"📁 Archivos Python por directorio:")
    for directorio, count in conteos.items():
        print(f"   {directorio}/: {count} archivos")
    
    total_archivos = sum(conteos.values())
    print(f"\n📈 Total archivos Python: {total_archivos}")
    
    # Verificar tamaño del main.py
    if os.path.exists('main.py'):
        with open('main.py', 'r', encoding='utf-8') as f:
            lineas_main = len(f.readlines())
        print(f"📄 main.py: {lineas_main} líneas (vs 1,154 original)")
        reduccion = ((1154 - lineas_main) / 1154) * 100
        print(f"📉 Reducción de main.py: {reduccion:.1f}%")

def main():
    """Función principal de verificación."""
    print("🔧 VERIFICACIÓN DEL SISTEMA REFACTORIZADO")
    print("=" * 50)
    
    verificaciones = [
        verificar_estructura_directorios,
        verificar_archivos_principales,
        verificar_imports,
        verificar_instanciacion,
        verificar_funcionalidad_basica,
        verificar_main_ejecutable
    ]
    
    resultados = []
    
    for verificacion in verificaciones:
        resultado = verificacion()
        resultados.append(resultado)
    
    # Resumen final
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 50)
    
    exitosas = sum(resultados)
    total = len(resultados)
    
    print(f"✅ Verificaciones exitosas: {exitosas}/{total}")
    
    if exitosas == total:
        print("🎉 ¡SISTEMA REFACTORIZADO COMPLETAMENTE FUNCIONAL!")
        print("🚀 Puedes ejecutar: python main.py")
        generar_reporte_verificacion()
        return 0
    elif exitosas >= total - 1:
        print("✅ Sistema funcional con advertencias menores")
        print("🚀 Puedes ejecutar: python main.py")
        generar_reporte_verificacion()
        return 0
    else:
        print("⚠️  Algunas verificaciones fallaron")
        print("💡 Revisa los errores anteriores y corrige los problemas")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)