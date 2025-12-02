# 🎭 Sistema de Punto de Venta - Auditorio

Sistema de gestión de ventas de boletos para auditorios desarrollado con Python y Flet. Permite la venta de asientos para eventos, con una interfaz visual interactiva que muestra la disponibilidad en tiempo real.

## 📋 Características

- **Gestión de Eventos**: Visualización de eventos disponibles con información detallada (tipo, descripción, fechas)
- **Selección Visual de Asientos**: Diagrama interactivo con 3 secciones (A1, A2, A3) de 10×10 asientos cada una
- **Estados de Asientos en Tiempo Real**:
  - 🟢 Verde: Disponible
  - 🔴 Rojo: Ocupado
  - 🔵 Azul: Seleccionado
- **Gestión de Clientes**: Registro de datos del cliente (nombres, apellidos, teléfono, correo)
- **Cálculo Automático**: Total de venta actualizado dinámicamente
- **Panel Administrativo**: Sección protegida por contraseña para administración del sistema
- **Base de Datos SQLite**: Persistencia de datos con foreign keys y relaciones

## 🛠️ Tecnologías

- **Python 3.10+**
- **Flet**: Framework para interfaces de usuario modernas
- **SQLite3**: Base de datos embebida
- **Arquitectura MVC**: Separación de responsabilidades

## 📁 Estructura del Proyecto

```
PROYECTO_AUDITORIO/
├── src/
│   ├── main.py              # Punto de entrada de la aplicación
│   ├── venta_view.py        # Vista principal de ventas
│   ├── app_controller.py    # Controlador de lógica de negocio
│   └── db_manager.py        # Gestor de base de datos
├── storage/
│   └── data/
│       └── database.db      # Base de datos SQLite
├── requirements.txt
└── README.md
└── pyproject.toml
```

## 🗄️ Modelo de Base de Datos

### Tablas

- **eventos**: Almacena información de eventos (tipo, descripción, fechas, costo)
- **asientos**: Define los asientos del auditorio (fila, número, sección)
- **clientes**: Registro de clientes (nombres, apellidos, teléfono, correo)
- **boletos**: Relaciona eventos, asientos y clientes (ventas realizadas)

### Relaciones

- Un evento puede tener múltiples boletos
- Un asiento puede venderse para diferentes eventos
- Un cliente puede comprar múltiples boletos
- Foreign keys con `ON DELETE CASCADE` y `ON DELETE SET NULL`

## 🚀 Instalación

1. **Clonar el repositorio**
```bash
cd PROYECTO_AUDITORIO
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación**
```bash
flet run main.py
```

## 💻 Uso

### Módulo de Ventas

1. **Seleccionar Evento**: Click en la tarjeta del evento deseado
2. **Elegir Asientos**: Click en los asientos verdes disponibles (se tornan azules)
3. **Datos del Cliente**: Completar nombres (*) y teléfono (*) obligatorios
4. **Confirmar Venta**: Click en "Confirmar Venta" para procesar

### Panel de Administración

- **Contraseña por defecto**: `contraseña`
- Acceso a funciones administrativas (en desarrollo)

## 🎨 Interfaz de Usuario

- **Tema oscuro** con paleta BLUE_GREY
- **Diseño responsivo** con scroll automático
- **Feedback visual** con SnackBars (verde/éxito, rojo/error, naranja/advertencia)
- **Iconografía clara** con Material Icons
- **Secciones bien delimitadas** con dividers

## ⚙️ Configuración

### Capacidad del Auditorio

- **Total de asientos**: 300 (3 secciones × 100 asientos)
- **Distribución**: 10 filas × 10 columnas por sección
- **Nomenclatura**: Sección-Fila-Número (ej: A1-A5, A2-J10)

### Precio de Boletos

Configurado en `venta_view.py`:
```python
self.PRECIO_BOLETO = 100.0  # Modificar según necesidad
```

## 🔒 Seguridad

- Validación de disponibilidad de asientos antes de confirmar venta
- Prevención de condiciones de carrera en ventas concurrentes
- Encapsulamiento de acceso a base de datos
- Manejo de errores con try-except

## 🐛 Características de Desarrollo

- Inicialización automática de asientos (primera ejecución)
- Evento de demostración pre-cargado
- Mensajes de debug en consola
- Método `cleanup()` para liberación de memoria

## 📝 Notas Técnicas

- **Mapeo de IDs**: Los asientos se mapean desde la BD al construir la interfaz
- **Preservación de estado**: Las selecciones se mantienen durante actualizaciones
- **Optimización de consultas**: Parámetro `check_status` para evitar consultas innecesarias
- **Scroll inteligente**: Altura fija de 600px para sección de asientos

## 🤝 Contribuciones

Proyecto desarrollado como sistema de gestión para auditorios y eventos culturales.

## 📄 Licencia

Proyecto educativo / académico.

---

**Versión**: 1.0.0  
**Última actualización**: Diciembre 2025
