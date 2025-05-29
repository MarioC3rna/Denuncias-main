"""
Utilidades de procesamiento IA - Refactorizadas
Funciones especializadas para procesamiento de denuncias con IA.

Migrado desde: src/core/utils.py
"""

"""
Módulo de utilidades para el sistema de denuncias anónimas.
Contiene funciones auxiliares para validación, generación de IDs y helpers generales.
"""

import hashlib
import uuid
import re
from datetime import datetime
from typing import Optional


def validar_entrada(categoria: str, mensaje: str = "") -> bool:
    """
    Valida las entradas del usuario para evitar denuncias vacías o malformadas.
    
    Args:
        categoria: Categoría de la denuncia
        mensaje: Mensaje opcional de la denuncia
        
    Returns:
        bool: True si la entrada es válida
    """
    # Verificar que la categoría no esté vacía
    if not categoria or not categoria.strip():
        print("❌ Error: La categoría no puede estar vacía")
        return False
    
    # Verificar longitud mínima de categoría
    if len(categoria.strip()) < 3:
        print("❌ Error: La categoría debe tener al menos 3 caracteres")
        return False
    
    # Verificar longitud máxima de categoría
    if len(categoria.strip()) > 50:
        print("❌ Error: La categoría no puede exceder 50 caracteres")
        return False
    
    # Validar caracteres permitidos en categoría
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', categoria.strip()):
        print("❌ Error: La categoría solo puede contener letras y espacios")
        return False
    
    # Si hay mensaje, validar su longitud
    if mensaje and len(mensaje.strip()) > 1000:
        print("❌ Error: El mensaje no puede exceder 1000 caracteres")
        return False
    
    # Verificar que no sean solo espacios en blanco
    if mensaje and not mensaje.strip():
        print("❌ Error: El mensaje no puede contener solo espacios")
        return False
    
    return True


def generar_id_anonimo() -> str:
    """
    Genera un ID anónimo único para cada denuncia.
    Combina timestamp y UUID para garantizar unicidad sin revelar identidad.
    
    Returns:
        str: ID anónimo único
    """
    # Generar timestamp en milisegundos
    timestamp = int(datetime.now().timestamp() * 1000)
    
    # Generar UUID aleatorio
    random_uuid = str(uuid.uuid4())
    
    # Combinar y crear hash SHA-256
    combined = f"{timestamp}_{random_uuid}"
    hash_object = hashlib.sha256(combined.encode())
    
    # Retornar los primeros 16 caracteres del hash para mantenerlo corto
    return f"DEN_{hash_object.hexdigest()[:16].upper()}"


def limpiar_texto(texto: str) -> str:
    """
    Limpia y sanitiza texto de entrada para prevenir inyecciones o caracteres problemáticos.
    
    Args:
        texto: Texto a limpiar
        
    Returns:
        str: Texto limpiado
    """
    if not texto:
        return ""
    
    # Remover caracteres de control y espacios extras
    texto_limpio = re.sub(r'\s+', ' ', texto.strip())
    
    # Remover caracteres especiales problemáticos pero mantener acentos y ñ
    texto_limpio = re.sub(r'[<>"\'\\\x00-\x1f\x7f-\x9f]', '', texto_limpio)
    
    return texto_limpio


def validar_categoria_predefinida(categoria: str, categorias_validas: list) -> bool:
    """
    Valida si una categoría está dentro de las categorías predefinidas.
    
    Args:
        categoria: Categoría a validar
        categorias_validas: Lista de categorías válidas
        
    Returns:
        bool: True si la categoría es válida
    """
    if not categoria or not categorias_validas:
        return False
    
    # Normalizar categoría para comparación (minúsculas, sin espacios extra)
    categoria_normalizada = categoria.strip().lower()
    
    # Normalizar categorías válidas para comparación
    categorias_normalizadas = [cat.strip().lower() for cat in categorias_validas]
    
    return categoria_normalizada in categorias_normalizadas


def formatear_timestamp(timestamp_iso: str) -> str:
    """
    Formatea un timestamp ISO a formato legible en español.
    
    Args:
        timestamp_iso: Timestamp en formato ISO
        
    Returns:
        str: Timestamp formateado
    """
    try:
        dt = datetime.fromisoformat(timestamp_iso.replace('Z', '+00:00'))
        return dt.strftime("%d/%m/%Y %H:%M:%S")
    except:
        return "Fecha no válida"


def calcular_porcentaje(valor: int, total: int) -> float:
    """
    Calcula el porcentaje de un valor respecto al total.
    
    Args:
        valor: Valor específico
        total: Valor total
        
    Returns:
        float: Porcentaje calculado
    """
    if total == 0:
        return 0.0
    return round((valor / total) * 100, 2)


def generar_resumen_estadistico(estadisticas: dict) -> str:
    """
    Genera un resumen estadístico en formato texto.
    
    Args:
        estadisticas: Diccionario con estadísticas por categoría
        
    Returns:
        str: Resumen estadístico formateado
    """
    if not estadisticas:
        return "No hay denuncias registradas."
    
    total = sum(estadisticas.values())
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    resumen = f"=== RESUMEN ESTADÍSTICO DE DENUNCIAS ===\n"
    resumen += f"Fecha de generación: {fecha_actual}\n"
    resumen += f"Total de denuncias: {total}\n\n"
    resumen += "Distribución por categoría:\n"
    resumen += "-" * 40 + "\n"
    
    # Ordenar categorías por cantidad (descendente)
    categorias_ordenadas = sorted(estadisticas.items(), key=lambda x: x[1], reverse=True)
    
    for categoria, cantidad in categorias_ordenadas:
        porcentaje = calcular_porcentaje(cantidad, total)
        resumen += f"{categoria:<20}: {cantidad:>3} ({porcentaje:>5.1f}%)\n"
    
    resumen += "-" * 40 + "\n"
    
    return resumen


def validar_longitud_mensaje(mensaje: str, longitud_maxima: int = 1000) -> bool:
    """
    Valida que un mensaje no exceda la longitud máxima permitida.
    
    Args:
        mensaje: Mensaje a validar
        longitud_maxima: Longitud máxima permitida
        
    Returns:
        bool: True si el mensaje es válido
    """
    if not mensaje:
        return True
    
    return len(mensaje.strip()) <= longitud_maxima


def obtener_categoria_mas_frecuente(estadisticas: dict) -> Optional[str]:
    """
    Obtiene la categoría con más denuncias.
    
    Args:
        estadisticas: Diccionario con estadísticas por categoría
        
    Returns:
        str: Categoría más frecuente o None si no hay datos
    """
    if not estadisticas:
        return None
    
    return max(estadisticas.items(), key=lambda x: x[1])[0]

# NUEVAS UTILIDADES INTEGRADAS
def integrar_con_nueva_arquitectura():
    """Integra utilidades con nueva arquitectura."""
    pass
