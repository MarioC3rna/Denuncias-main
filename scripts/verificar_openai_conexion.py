"""
Verifica la configuración de OpenAI y archivo .env
"""

import os
from pathlib import Path

def verificar_archivo_env():
    """Verifica si existe el archivo .env y su contenido."""
    print("🔍 VERIFICANDO ARCHIVO .ENV")
    print("=" * 30)
    
    env_path = Path('.env')
    
    if env_path.exists():
        print("✅ Archivo .env encontrado")
        
        try:
            with open('.env', 'r') as f:
                contenido = f.read()
            
            if 'OPENAI_API_KEY' in contenido:
                print("✅ Variable OPENAI_API_KEY encontrada")
                
                # Verificar si tiene valor
                lines = contenido.split('\n')
                for line in lines:
                    if line.startswith('OPENAI_API_KEY'):
                        if '=' in line and line.split('=')[1].strip():
                            print("✅ API Key configurada")
                            # Mostrar solo los primeros y últimos caracteres
                            key = line.split('=')[1].strip()
                            if len(key) > 10:
                                masked_key = key[:8] + "..." + key[-4:]
                                print(f"🔑 Key: {masked_key}")
                            return True
                        else:
                            print("❌ API Key está vacía")
                            return False
            else:
                print("❌ Variable OPENAI_API_KEY no encontrada")
                return False
                
        except Exception as e:
            print(f"❌ Error leyendo .env: {e}")
            return False
    else:
        print("❌ Archivo .env no encontrado")
        print("💡 Creando archivo .env de ejemplo...")
        crear_env_ejemplo()
        return False

def crear_env_ejemplo():
    """Crea un archivo .env de ejemplo."""
    contenido_env = """# Configuración del Sistema de Denuncias
# Para usar funciones avanzadas de IA, configura tu API key de OpenAI

OPENAI_API_KEY=tu_api_key_aqui

# Ejemplo de API key válida:
# OPENAI_API_KEY=sk-1234567890abcdef1234567890abcdef1234567890abcdef

# Otras configuraciones opcionales
SISTEMA_DEBUG=false
NIVEL_LOG=info
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(contenido_env)
        print("✅ Archivo .env de ejemplo creado")
        print("📝 Edita el archivo .env para agregar tu API key de OpenAI")
    except Exception as e:
        print(f"❌ Error creando .env: {e}")

def verificar_python_dotenv():
    """Verifica si python-dotenv está instalado."""
    print("\n🔍 VERIFICANDO PYTHON-DOTENV")
    print("=" * 30)
    
    try:
        import dotenv
        print("✅ python-dotenv instalado")
        return True
    except ImportError:
        print("❌ python-dotenv NO instalado")
        print("💡 Instalar con: pip install python-dotenv")
        return False

def test_openai_connection():
    """Prueba la conexión con OpenAI."""
    print("\n🔍 PROBANDO CONEXIÓN OPENAI")
    print("=" * 30)
    
    try:
        # Cargar variables de entorno
        if verificar_python_dotenv():
            from dotenv import load_dotenv
            load_dotenv()
        
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key or api_key == 'tu_api_key_aqui':
            print("❌ API Key no configurada correctamente")
            return False
        
        # Intentar importar OpenAI
        try:
            import openai
            print("✅ Librería openai importada")
        except ImportError:
            print("❌ Librería openai NO instalada")
            print("💡 Instalar con: pip install openai")
            return False
        
        # Configurar cliente
        try:
            client = openai.OpenAI(api_key=api_key)
            print("✅ Cliente OpenAI configurado")
        except Exception as e:
            print(f"❌ Error configurando cliente: {e}")
            return False
        
        # Prueba simple
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Di 'conectado' si recibes esto"}],
                max_tokens=10
            )
            
            respuesta = response.choices[0].message.content.strip()
            print(f"✅ Conexión exitosa - Respuesta: {respuesta}")
            return True
            
        except Exception as e:
            print(f"❌ Error en prueba de conexión: {e}")
            if "invalid api key" in str(e).lower():
                print("🔑 API Key inválida")
            elif "quota" in str(e).lower():
                print("💳 Cuota agotada")
            elif "billing" in str(e).lower():
                print("💰 Problema de facturación")
            return False
            
    except Exception as e:
        print(f"❌ Error general: {e}")
        return False

def main():
    """Función principal de verificación."""
    print("🔍 DIAGNÓSTICO DE CONEXIÓN OPENAI")
    print("=" * 40)
    
    # Verificaciones
    env_ok = verificar_archivo_env()
    dotenv_ok = verificar_python_dotenv()
    
    if env_ok and dotenv_ok:
        openai_ok = test_openai_connection()
    else:
        openai_ok = False
    
    # Resumen
    print("\n📊 RESUMEN DEL DIAGNÓSTICO")
    print("=" * 30)
    print(f"📄 Archivo .env: {'✅' if env_ok else '❌'}")
    print(f"📦 python-dotenv: {'✅' if dotenv_ok else '❌'}")
    print(f"🤖 Conexión OpenAI: {'✅' if openai_ok else '❌'}")
    
    if all([env_ok, dotenv_ok, openai_ok]):
        print("\n🎉 ¡TODO CONFIGURADO CORRECTAMENTE!")
        print("🤖 El agente IA funcionará con OpenAI")
    else:
        print("\n⚠️ CONFIGURACIÓN INCOMPLETA")
        print("🔧 El sistema funcionará en modo básico")
        
        if not env_ok:
            print("💡 1. Configura tu API key en .env")
        if not dotenv_ok:
            print("💡 2. Instala: pip install python-dotenv")
        if not openai_ok and env_ok:
            print("💡 3. Verifica tu API key de OpenAI")

if __name__ == "__main__":
    main()