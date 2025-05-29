"""
GestorDenuncias simplificado para el sistema de denuncias.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

class GestorDenuncias:
    """Gestor principal de denuncias."""
    
    def __init__(self, archivo_datos: str = 'src/data/denuncias.json'):
        """Inicializa el gestor de denuncias."""
        self.archivo_datos = archivo_datos
        self.denuncias = []
        
        # Crear directorio de datos
        os.makedirs(os.path.dirname(archivo_datos), exist_ok=True)
        
        # Cargar denuncias existentes
        self._cargar_denuncias()
        
        print("✅ GestorDenuncias con IA: OK")
    
    def _cargar_denuncias(self):
        """Carga denuncias desde archivo."""
        try:
            if os.path.exists(self.archivo_datos):
                with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                    self.denuncias = json.load(f)
                print(f"✅ Cargadas {len(self.denuncias)} denuncias")
            else:
                self.denuncias = []
                print("📝 Archivo de denuncias nuevo")
        except Exception as e:
            print(f"⚠️ Error cargando denuncias: {e}")
            self.denuncias = []
    
    def _guardar_denuncias(self):
        """Guarda denuncias en archivo."""
        try:
            with open(self.archivo_datos, 'w', encoding='utf-8') as f:
                json.dump(self.denuncias, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ Error guardando denuncias: {e}")
            return False
    
    def registrar_denuncia(self, mensaje: str, **kwargs) -> Dict[str, Any]:
        """Registra una nueva denuncia."""
        if not mensaje or not mensaje.strip():
            return {
                'exito': False,
                'error': 'Mensaje vacío',
                'timestamp': datetime.now().isoformat()
            }
        
        # Crear denuncia
        denuncia = {
            'id': self._generar_id(),
            'mensaje': mensaje.strip(),
            'timestamp': datetime.now().isoformat(),
            'categoria': self._clasificacion_basica(mensaje),
            'procesada_con_ia': False
        }
        
        # Guardar denuncia
        self.denuncias.append(denuncia)
        
        if self._guardar_denuncias():
            return {
                'exito': True,
                'id_denuncia': denuncia['id'],
                'categoria': denuncia['categoria'],
                'timestamp': denuncia['timestamp'],
                'procesada_con_ia': False
            }
        else:
            return {
                'exito': False,
                'error': 'Error guardando datos',
                'timestamp': datetime.now().isoformat()
            }
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Obtiene estadísticas de denuncias."""
        if not self.denuncias:
            return {
                'total': 0,
                'por_categoria': {},
                'procesadas_ia': 0,
                'porcentaje_ia': 0.0,
                'ultima_actualizacion': datetime.now().isoformat()
            }
        
        # Contar por categoría
        por_categoria = {}
        
        for denuncia in self.denuncias:
            categoria = denuncia.get('categoria', 'otros')
            por_categoria[categoria] = por_categoria.get(categoria, 0) + 1
        
        return {
            'total': len(self.denuncias),
            'por_categoria': por_categoria,
            'procesadas_ia': 0,
            'porcentaje_ia': 0.0,
            'agente_ia_activo': False,
            'ultima_actualizacion': datetime.now().isoformat()
        }
    
    def obtener_info_agente_ia(self) -> Dict[str, Any]:
        """Obtiene información del agente IA."""
        return {
            'disponible': False,
            'motivo': 'Modo básico - sin IA avanzada'
        }
    
    def configurar_agente_ia(self, api_key_openai: Optional[str] = None) -> bool:
        """Configura el agente IA."""
        print("💡 Agente IA avanzado no disponible en modo básico")
        return False
    
    def _generar_id(self) -> str:
        """Genera ID único para denuncia."""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def _clasificacion_basica(self, mensaje: str) -> str:
        """Clasificación básica sin IA."""
        mensaje_lower = mensaje.lower()
        
        if any(palabra in mensaje_lower for palabra in ['acoso', 'hostigamiento', 'molesta']):
            return 'acoso'
        elif any(palabra in mensaje_lower for palabra in ['discrimina', 'discriminación', 'raza', 'género']):
            return 'discriminacion'
        elif any(palabra in mensaje_lower for palabra in ['dinero', 'soborno', 'corrupción']):
            return 'corrupcion'
        elif any(palabra in mensaje_lower for palabra in ['sistema', 'error', 'falla', 'técnico']):
            return 'problemas_tecnicos'
        else:
            return 'otros'
