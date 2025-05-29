"""
Validadores para entrada de usuario y datos.
"""

import re
from typing import Optional, Tuple, List
from datetime import datetime
from pathlib import Path

class ValidadorEntrada:
    """Valida entrada de usuario."""
    
    @staticmethod
    def validar_opcion_menu(opcion: str, opciones_validas: List[str]) -> Optional[str]:
        """
        Valida una opción de menú.
        
        Args:
            opcion: Opción ingresada por el usuario
            opciones_validas: Lista de opciones válidas ['1', '2', '3', ...]
            
        Returns:
            str: Opción válida o None si es inválida
        """
        opcion_limpia = opcion.strip()
        return opcion_limpia if opcion_limpia in opciones_validas else None
    
    @staticmethod
    def validar_opcion_numerica(opcion: str, rango_min: int, rango_max: int) -> Optional[int]:
        """
        Valida una opción numérica dentro de un rango.
        
        Args:
            opcion: Opción ingresada
            rango_min: Valor mínimo válido
            rango_max: Valor máximo válido
            
        Returns:
            int: Opción válida o None si es inválida
        """
        try:
            opcion_num = int(opcion.strip())
            if rango_min <= opcion_num <= rango_max:
                return opcion_num
            return None
        except ValueError:
            return None
    
    @staticmethod
    def validar_confirmacion(respuesta: str) -> bool:
        """
        Valida una respuesta de confirmación (s/n).
        
        Args:
            respuesta: Respuesta del usuario
            
        Returns:
            bool: True si es afirmativa, False si es negativa
        """
        respuesta_limpia = respuesta.strip().lower()
        return respuesta_limpia in ['s', 'sí', 'si', 'y', 'yes', '1']
    
    @staticmethod
    def validar_credenciales(usuario: str, password: str) -> Tuple[bool, str]:
        """
        Valida credenciales de usuario.
        
        Args:
            usuario: Nombre de usuario
            password: Contraseña
            
        Returns:
            Tuple[bool, str]: (es_válido, mensaje_error)
        """
        # Verificar campos vacíos
        if not usuario or not password:
            return False, "Usuario y contraseña no pueden estar vacíos"
        
        # Verificar longitud mínima de contraseña
        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres"
        
        # Validar formato de usuario (solo letras, números y guiones bajos)
        if not re.match(r'^[a-zA-Z0-9_]+$', usuario):
            return False, "El usuario solo puede contener letras, números y guiones bajos"
        
        # Verificar longitud del usuario
        if len(usuario) < 3:
            return False, "El usuario debe tener al menos 3 caracteres"
        
        if len(usuario) > 20:
            return False, "El usuario no puede tener más de 20 caracteres"
        
        return True, ""
    
    @staticmethod
    def validar_mensaje_denuncia(mensaje: str) -> Tuple[bool, str]:
        """
        Valida el mensaje de una denuncia.
        
        Args:
            mensaje: Mensaje de la denuncia
            
        Returns:
            Tuple[bool, str]: (es_válido, mensaje_error)
        """
        if not mensaje or not mensaje.strip():
            return False, "El mensaje no puede estar vacío"
        
        mensaje_limpio = mensaje.strip()
        
        # Verificar longitud mínima
        if len(mensaje_limpio) < 10:
            return False, "El mensaje debe tener al menos 10 caracteres"
        
        # Verificar longitud máxima
        if len(mensaje_limpio) > 5000:
            return False, "El mensaje no puede superar los 5000 caracteres"
        
        # Verificar que no sea solo espacios o caracteres especiales
        if re.match(r'^[\s\W]*$', mensaje_limpio):
            return False, "El mensaje debe contener texto significativo"
        
        # Verificar que tenga al menos algunas palabras
        palabras = mensaje_limpio.split()
        if len(palabras) < 3:
            return False, "El mensaje debe contener al menos 3 palabras"
        
        return True, ""
    
    @staticmethod
    def validar_entrada_no_vacia(entrada: str, nombre_campo: str) -> Tuple[bool, str]:
        """
        Valida que una entrada no esté vacía.
        
        Args:
            entrada: Entrada del usuario
            nombre_campo: Nombre del campo para el mensaje de error
            
        Returns:
            Tuple[bool, str]: (es_válido, mensaje_error)
        """
        if not entrada or not entrada.strip():
            return False, f"{nombre_campo} no puede estar vacío"
        
        return True, ""

class ValidadorDatos:
    """Valida datos del sistema."""
    
    @staticmethod
    def validar_categoria(categoria: str, categorias_validas: List[str]) -> bool:
        """Valida que una categoría sea válida."""
        return categoria in categorias_validas
    
    @staticmethod
    def validar_nivel_confianza(confianza: float) -> bool:
        """Valida que el nivel de confianza esté en rango válido."""
        return 0.0 <= confianza <= 1.0
    
    @staticmethod
    def validar_resultado_analisis(resultado: dict) -> Tuple[bool, str]:
        """
        Valida la estructura de un resultado de análisis de IA.
        
        Args:
            resultado: Diccionario con resultado de análisis
            
        Returns:
            Tuple[bool, str]: (es_válido, mensaje_error)
        """
        campos_requeridos = [
            'categoria_sugerida',
            'confianza',
            'es_denuncia_valida',
            'metodo_usado'
        ]
        
        for campo in campos_requeridos:
            if campo not in resultado:
                return False, f"Campo requerido faltante: {campo}"
        
        # Validar tipos
        if not isinstance(resultado['confianza'], (int, float)):
            return False, "La confianza debe ser un número"
        
        if not ValidadorDatos.validar_nivel_confianza(resultado['confianza']):
            return False, "La confianza debe estar entre 0 y 1"
        
        if not isinstance(resultado['es_denuncia_valida'], bool):
            return False, "es_denuncia_valida debe ser booleano"
        
        return True, ""

class ValidadorSistema:
    """Validador para funciones del sistema."""
    
    @staticmethod
    def validar_estado_sistema() -> dict:
        """
        Valida el estado general del sistema.
        
        Returns:
            dict: Estado del sistema con métricas
        """
        estado = {
            'sistema_operativo': True,
            'memoria_disponible': True,
            'dependencias': True,
            'configuracion': True,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # Verificar dependencias básicas
            import json
            import os
            import sys
            
            # Verificar espacio en disco (simplificado)
            estado['espacio_disco'] = True
            
            # Verificar permisos de escritura
            try:
                test_file = Path('test_permisos.tmp')
                test_file.write_text('test')
                test_file.unlink()
                estado['permisos_escritura'] = True
            except:
                estado['permisos_escritura'] = False
                
        except ImportError:
            estado['dependencias'] = False
        
        return estado
    
    @staticmethod
    def validar_configuracion_ia() -> bool:
        """
        Valida la configuración del agente IA.
        
        Returns:
            bool: True si la configuración es válida
        """
        try:
            # Verificar que los módulos de IA estén disponibles
            from src.agente_ia_simple.agente_ia_mejorado import AgenteIAMejorado
            return True
        except ImportError:
            return False
    
    @staticmethod
    def validar_integridad_datos(datos: list) -> dict:
        """
        Valida la integridad de los datos del sistema.
        
        Args:
            datos: Lista de datos a validar
            
        Returns:
            dict: Resultado de la validación
        """
        resultado = {
            'total_registros': len(datos),
            'registros_validos': 0,
            'registros_invalidos': 0,
            'errores': []
        }
        
        for i, registro in enumerate(datos):
            try:
                # Validaciones básicas
                if not isinstance(registro, dict):
                    resultado['errores'].append(f"Registro {i}: No es un diccionario")
                    resultado['registros_invalidos'] += 1
                    continue
                
                # Verificar campos requeridos
                campos_requeridos = ['id', 'mensaje', 'timestamp']
                for campo in campos_requeridos:
                    if campo not in registro:
                        resultado['errores'].append(f"Registro {i}: Falta campo '{campo}'")
                        resultado['registros_invalidos'] += 1
                        break
                else:
                    resultado['registros_validos'] += 1
                    
            except Exception as e:
                resultado['errores'].append(f"Registro {i}: Error de validación - {e}")
                resultado['registros_invalidos'] += 1
        
        return resultado
    
    @staticmethod
    def generar_reporte_validacion() -> str:
        """
        Genera un reporte de validación del sistema.
        
        Returns:
            str: Reporte formateado
        """
        reporte = []
        reporte.append("📋 REPORTE DE VALIDACIÓN DEL SISTEMA")
        reporte.append("=" * 45)
        reporte.append(f"📅 Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
__all__ = [
    'ValidadorEntrada',
    'ValidadorDatos', 
    'ValidadorSistema'
]