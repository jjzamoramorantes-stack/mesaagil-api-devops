# MesaÁgil — API REST de Gestión de Solicitudes de Soporte

Módulo representativo de la API REST de **MesaÁgil** desarrollado como evidencia práctica inicial de la **Entrega 1 (Semana 3)** en la asignatura *Testing Automatizado y DevOps* de la **Maestría en Ingeniería de Software** (Corporación Universitaria Iberoamericana).

## Descripción del Proyecto

MesaÁgil provee un servicio web REST para registrar solicitudes de soporte técnico, asignar prioridades y gestionar su ciclo de vida (`abierta`, `en_progreso`, `cerrada`). El diseño encapsula las reglas de dominio de la organización, garantizando explícitamente la invariante crítica identificada en el diagnóstico: **una solicitud cerrada únicamente puede reabrirse si se registra un motivo válido**.

### Estructura del Repositorio

```text
mesaagil-api-devops/
├── app/
│   ├── __init__.py
│   ├── main.py          # Endpoints FastAPI (/health, /solicitudes)
│   ├── models.py        # Esquemas Pydantic y enumeraciones de estado/prioridad
│   └── service.py       # Lógica de negocio e invariantes de dominio
├── tests/
│   └── test_solicitudes.py  # 5 pruebas unitarias (patrón Preparar–Actuar–Verificar)
├── .gitignore
├── requirements.txt
└── README.md
```

## Requisitos e Instalación Local

1. Clonar el repositorio y ubicarse en la carpeta raíz:
   ```bash
   git clone https://github.com/jjzamoramorantes/mesaagil-api-devops.git
   cd mesaagil-api-devops
   ```

2. Crear y activar un entorno virtual en Python 3.11+:
   ```bash
   python -m venv .venv
   # En Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   # En Linux / macOS:
   source .venv/bin/activate
   ```

3. Instalar las dependencias fijadas:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución de las Pruebas Unitarias

Las pruebas unitarias están implementadas con `pytest` siguiendo el patrón **Preparar–Actuar–Verificar (Arrange–Act–Assert)**. Para ejecutarlas con salida detallada:

```bash
pytest -v
```

### Cobertura funcional de las pruebas incluidas
1. `test_crear_solicitud_asigna_estado_abierta_y_correlativo`: Verifica la creación inicial en estado `abierta` e incremento de identificador.
2. `test_asignar_prioridad_actualiza_solicitud_activa`: Comprueba el cambio válido de prioridad en solicitudes activas.
3. `test_reabrir_solicitud_cerrada_sin_motivo_lanza_error`: Valida el rechazo ante intentos de reapertura sin motivo o con cadenas vacías.
4. `test_reabrir_solicitud_cerrada_con_motivo_valido_permite_transicion`: Verifica la reapertura exitosa cuando se documenta el motivo.
5. `test_cambiar_prioridad_en_solicitud_cerrada_es_rechazado`: Asegura la inmutabilidad de prioridad sobre solicitudes cerradas.

## Ejecución Local de la API (Opcional)

```bash
uvicorn app.main:app --reload
```
Documentación interactiva disponible en `http://127.0.0.1:8000/docs`.

## Actualiza documentación y detalles en README
