# 🛡️ Sistema Anónimo de Denuncias Internas

Sistema integral para la gestión anónima de denuncias internas con análisis automatizado por IA y garantía total de privacidad. Diseñado para organizaciones que requieren un canal seguro y confidencial para reportar irregularidades.

## 🚀 Características Principales

- **🔒 Anonimato Garantizado**: Sin registro de usuarios ni rastreo de identidad
- **🤖 Análisis IA Integrado**: Clasificación automática y detección de spam
- **🎨 Interfaz Dual**: Modo anónimo y administrador con permisos diferenciados
- **📤 Exportación Completa**: Múltiples formatos (TXT, CSV, HTML, JSON)
- **📊 Reportes Avanzados**: Estadísticas y análisis ejecutivo con IA
- **⚡ Procesamiento en Tiempo Real**: Análisis instantáneo de denuncias
- **🔐 Seguridad Avanzada**: Encriptación local y protección de datos

## 📋 Requisitos del Sistema

- **Python**: 3.8 o superior
- **Dependencias opcionales**:
  - `openai` - Para análisis avanzado con GPT
  - `tabulate` - Para reportes formateados
  - `python-dotenv` - Gestión de variables de entorno


## 🏗️ Estructura del Proyecto

```
sistema-denuncias/
├── 📁 src/
│   ├── 📄 main.py              # Punto de entrada principal
│   ├── 📄 complaint_system.py  # Lógica del sistema de denuncias
│   ├── 📄 ai_analyzer.py       # Motor de análisis con IA
│   ├── 📄 export_manager.py    # Gestor de exportaciones
│   └── 📄 settings.py          # Configuración del sistema
├── 📁 data/
│   ├── 📄 complaints.json      # Base de datos de denuncias
│   └── 📁 exports/             # Archivos exportados
├── 📁 templates/
│   └── 📄 report_template.html # Plantilla de reportes
├── 📄 .env.example             # Variables de entorno ejemplo
├── 📄 requirements.txt         # Dependencias Python
└── 📄 README.md               # Este archivo
```

## 👤 Modos de Usuario

### 🔓 Usuario Anónimo
- ✅ Enviar denuncias anónimas
- ✅ Consultar ayuda del sistema
- ✅ Ver guías de uso
- ❌ Acceso a estadísticas o reportes
- ❌ Funciones administrativas

### 🔐 Administrador
- ✅ Todas las funciones de usuario anónimo
- ✅ Ver estadísticas completas y métricas
- ✅ Generar reportes y exportaciones
- ✅ Configurar sistema y gestionar IA
- ✅ Acceso al dashboard avanzado
- ✅ Gestión de configuraciones

**Credenciales por defecto:**
- **Usuario**: `admin`
- **Contraseña**: `admin123`

> ⚠️ **Importante**: Cambiar estas credenciales en producción

## 🤖 Sistema de IA

### Análisis Automático
- **🕵️ Detección de Spam**: Identifica contenido no válido o malicioso
- **🏷️ Clasificación Inteligente**: Asigna categoría automáticamente
- **🔍 Análisis de Veracidad**: Evalúa credibilidad del contenido
- **⚡ Nivel de Urgencia**: Determina prioridad de atención
- **📊 Análisis de Sentimiento**: Evalúa el tono y gravedad

### 🏷️ Categorías Disponibles
- **🔴 Acoso Laboral** - Situaciones de hostigamiento o maltrato
- **🟠 Discriminación** - Casos de trato desigual o prejuicios
- **🟡 Fraude/Corrupción** - Irregularidades financieras o éticas
- **🔵 Problemas Técnicos** - Fallas en sistemas o procesos
- **🟢 Seguridad Laboral** - Riesgos o incidentes de seguridad
- **🟣 Violación de Políticas** - Incumplimiento de normativas internas
- **⚪ Otros** - Situaciones no categorizadas

## 📊 Funciones de Exportación

### 📁 Formatos Disponibles
- **📄 Texto Plano (.txt)** - Para lectura simple y accesible
- **📊 CSV (.csv)** - Compatible con Excel y herramientas de análisis
- **🌐 HTML (.html)** - Reportes visuales interactivos
- **🔧 JSON (.json)** - Backup completo y intercambio de datos
- **📈 Reporte Ejecutivo** - Análisis comprehensivo con IA

### 🔍 Opciones de Filtrado
- **Por categoría** - Filtrar por tipo de denuncia
- **Por estado** - Pendiente, en proceso, resuelto
- **Por fecha** - Rango de fechas personalizable
- **Por urgencia** - Nivel de prioridad asignado
- **Filtros combinados** - Múltiples criterios simultáneos

## 🔧 Configuración

### Variables de Entorno (.env)
```env
# Configuración de OpenAI (opcional)
OPENAI_API_KEY=tu_clave_api_aqui

# Configuración de administrador
ADMIN_USERNAME=admin
ADMIN_PASSWORD=tu_password_seguro

# Configuración de archivos
MAX_FILE_SIZE=10485760  # 10MB
EXPORT_PATH=./data/exports/

# Configuración de IA
AI_ENABLED=true
AI_PROVIDER=openai  # openai, local
AI_MODEL=gpt-3.5-turbo
```

### ⚙️ Configuración del Sistema
El archivo `settings.py` contiene:
- Categorías predefinidas y personalizables
- Emojis por tipo de contenido
- Configuración de archivos y límites
- Credenciales de administrador
- Parámetros de IA y análisis

## 🔒 Seguridad y Privacidad

- **🚫 Sin identificación personal**: No se solicita ni almacena información del denunciante
- **🔐 IDs anónimos**: Generados con hash SHA-256 para trazabilidad segura
- **🛡️ Encriptación local**: Procesamiento seguro sin exposición de datos
- **⏰ Sesiones temporales**: Sin persistencia de autenticación
- **🔍 Auditoría de accesos**: Registro de actividades administrativas
- **🗂️ Almacenamiento seguro**: Datos protegidos localmente

## 🚀 Guía de Uso

### Ejecutar el Sistema
```bash
python main.py
```

### 📝 Enviar una Denuncia (Modo Anónimo)
1. Ejecutar el sistema
2. Seleccionar **"Enviar denuncia anónima"**
3. Describir la situación detalladamente
4. El sistema analiza y clasifica automáticamente
5. Revisar la clasificación sugerida
6. Confirmar el envío

### 🔐 Acceso de Administrador
1. En el menú principal, seleccionar **"Modo administrador"**
2. Ingresar credenciales de acceso
3. Acceder a funciones avanzadas:
   - Dashboard de estadísticas
   - Generación de reportes
   - Configuración del sistema
   - Gestión de exportaciones

## 📈 Estadísticas y Reportes

### 📊 Dashboard de Administrador
- **📊 Estadísticas en tiempo real** - Métricas actualizadas
- **📈 Análisis de tendencias** - Patrones y evolución temporal
- **🤖 Reportes de IA** - Insights automatizados
- **⚙️ Estado del sistema** - Monitoreo de salud
- **🎯 KPIs clave** - Indicadores de rendimiento

### 📤 Exportaciones Automáticas
- **🌐 Generación de reportes HTML** - Visualización interactiva
- **📊 Estadísticas detalladas** - Análisis comprehensivo
- **🤖 Análisis ejecutivo con IA** - Resúmenes inteligentes
- **💾 Backups completos** - Respaldo integral del sistema

## 🛠️ Scripts de Utilidad

```bash
# Backup de datos
python scripts/backup_data.py

# Limpieza de archivos temporales
python scripts/cleanup.py

# Migración de datos
python scripts/migrate_data.py

# Análisis de rendimiento
python scripts/performance_check.py
```

## 🐛 Solución de Problemas

### Problemas Comunes

**Error de importación de módulos:**
```bash
pip install -r requirements.txt --upgrade
```

**Problemas con la API de OpenAI:**
- Verificar que la clave API sea válida
- Comprobar conectividad a internet
- Revisar límites de uso de la API

**Errores de permisos de archivo:**
```bash
chmod 755 data/
chmod 644 data/complaints.json
```

## 🔄 Actualizaciones y Mantenimiento

### Respaldo Regular
```bash
# Crear backup automático
python scripts/backup_data.py --auto

# Restaurar desde backup
python scripts/restore_backup.py --file backup_2024_01_15.json
```

### Monitoreo del Sistema
- Revisar logs regularmente
- Monitorear uso de espacio en disco
- Verificar integridad de datos
- Actualizar dependencias periódicamente

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -am 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crear un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o consultas:
- **📧 Email**: soporte@sistema-denuncias.com
- **📖 Documentación**: [Wiki del proyecto](https://github.com/tu-usuario/sistema-denuncias/wiki)
- **🐛 Issues**: [GitHub Issues](https://github.com/tu-usuario/sistema-denuncias/issues)

## 📝 Notas Importantes

> **⚠️ Cambiar credenciales**: Modificar las credenciales por defecto en producción para garantizar seguridad

> **🔒 Privacidad**: El sistema está diseñado para garantizar anonimato total del denunciante

> **🤖 IA Opcional**: Funciona perfectamente sin OpenAI, usando análisis local básico

> **📈 Escalabilidad**: Arquitectura preparada para crecimiento futuro y alta demanda

> **🔧 Personalización**: Completamente configurable según las necesidades organizacionales

---

**Desarrollado con ❤️ para promover la transparencia y la integridad organizacional**
