"""
Configuración centralizada del sistema de denuncias.
"""

import os
from typing import Dict, Any

class ConfiguracionSistema:
    """Configuración central del sistema de denuncias."""
    
    # 🎨 CONFIGURACIÓN DE INTERFAZ
    BANNER = {
        'titulo': '🔒 SISTEMA ANÓNIMO DE DENUNCIAS INTERNAS 🔒',
        'ancho': 60,
        'subtitulos': [
            '🛡️  Tu identidad está protegida',
            '🔐 Procesamiento seguro con MCP'
        ]
    }
    
    # 🤖 CONFIGURACIÓN DEL AGENTE IA
    AGENTE_IA = {
        'activo_por_defecto': True,
        'usar_openai_por_defecto': False,
        'timeout_analisis': 30,
        'confianza_minima': 0.7
    }
    
    # 🔐 CONFIGURACIÓN DE AUTENTICACIÓN
    AUTENTICACION = {
        'intentos_maximos': 3,
        'longitud_minima_password': 6,
        'credenciales_por_defecto': {
            'usuario': 'admin',
            'password': 'admin123'
        }
    }
    
    # 📁 CONFIGURACIÓN DE ARCHIVOS
    ARCHIVOS = {
        'directorio_output': 'src/output',
        'archivo_resumen': 'resumen.txt',
        'encoding': 'utf-8'
    }
    
    # 🎨 EMOJIS POR CATEGORÍA
    EMOJIS_CATEGORIA = {
        "Acoso": "🔴",
        "Discriminación": "🟠", 
        "Corrupción": "🟡",
        "Problemas técnicos": "🔵",
        "Pendiente de clasificación": "⏳",
        "Otros": "⚪"
    }
    
    # 🎯 EMOJIS POR NIVEL DE VERACIDAD
    EMOJIS_VERACIDAD = {
        "ALTA": "🟢",
        "MEDIA": "🟡", 
        "BAJA": "🟠",
        "MUY_BAJA": "🔴",
        "SOSPECHOSA": "🔴"
    }
    
    # ⚡ EMOJIS POR URGENCIA
    EMOJIS_URGENCIA = {
        "CRÍTICA": "🚨",
        "ALTA": "⚠️",
        "MEDIA": "📋",
        "BAJA": "📝"
    }
    
    # 📋 MENSAJES DEL SISTEMA
    MENSAJES = {
        'bienvenida_anonimo': '👤 Modo: USUARIO ANÓNIMO (Garantía total de privacidad)',
        'bienvenida_admin': '👨‍💼 Modo: ADMINISTRADOR (Acceso completo)',
        'denuncia_exitosa': '✅ DENUNCIA REGISTRADA EXITOSAMENTE',
        'error_acceso': '❌ Acceso denegado: Se requieren permisos de administrador',
        'sesion_cerrada': '👋 CERRANDO SESIÓN DE ADMINISTRADOR'
    }
    
    # 📊 CONFIGURACIÓN DE MENÚS
    MENUS = {
        'anonimo': [
            '📝 1. Enviar denuncia anónima',
            '❓ 2. ¿Cómo funciona el sistema?',
            '🔄 3. Cambiar a administrador',
            '❌ 4. Salir del sistema'
        ],
        'administrador': [
            '📝 1. Enviar denuncia',
            '📊 2. Ver estadísticas de denuncias',
            '📈 3. Generar reporte de resumen',
            '🤖 4. {estado_agente} Agente IA',
            '⚙️ 5. Configurar OpenAI (opcional)',
            '🔧 6. Verificar estado del sistema',
            '🔍 7. Probar clasificador de IA',
            '🔑 8. Cambiar credenciales de administrador',
            '👤 9. Cerrar sesión (modo anónimo)',
            '❌ 10. Salir del sistema'
        ],
        'seleccion_rol': [
            '👤 1. Usuario Anónimo (Enviar denuncia)',
            '👨‍💼 2. Administrador (Gestión del sistema)',
            '❌ 3. Salir'
        ]
    }
    
    @classmethod
    def obtener_configuracion(cls) -> Dict[str, Any]:
        """Obtiene toda la configuración como diccionario."""
        return {
            'banner': cls.BANNER,
            'agente_ia': cls.AGENTE_IA,
            'autenticacion': cls.AUTENTICACION,
            'archivos': cls.ARCHIVOS,
            'emojis': {
                'categoria': cls.EMOJIS_CATEGORIA,
                'veracidad': cls.EMOJIS_VERACIDAD,
                'urgencia': cls.EMOJIS_URGENCIA
            },
            'mensajes': cls.MENSAJES,
            'menus': cls.MENUS
        }
    
    @classmethod
    def obtener_emoji_categoria(cls, categoria: str) -> str:
        """Obtiene el emoji para una categoría específica."""
        return cls.EMOJIS_CATEGORIA.get(categoria, "📂")
    
    @classmethod
    def obtener_emoji_veracidad(cls, nivel: str) -> str:
        """Obtiene el emoji para un nivel de veracidad."""
        return cls.EMOJIS_VERACIDAD.get(nivel, "⚪")
    
    @classmethod
    def obtener_emoji_urgencia(cls, urgencia: str) -> str:
        """Obtiene el emoji para un nivel de urgencia."""
        return cls.EMOJIS_URGENCIA.get(urgencia, "📋")