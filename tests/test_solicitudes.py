import pytest
from app.models import (
    CambioEstadoRequest,
    EstadoSolicitud,
    PrioridadSolicitud,
    SolicitudCrear,
)
from app.service import ReglaNegocioError, ServicioSolicitudes


def test_crear_solicitud_asigna_estado_abierta_y_correlativo():
    # Preparar (Arrange)
    servicio = ServicioSolicitudes()
    datos = SolicitudCrear(
        titulo="Fallo en facturación electrónica",
        descripcion="El módulo de exportación PDF arroja timeout al generar comprobantes.",
        cliente="Comercializadora Andina S.A.S.",
        prioridad=PrioridadSolicitud.ALTA,
    )

    # Actuar (Act)
    creada = servicio.crear_solicitud(datos)

    # Verificar (Assert)
    assert creada.id == 1
    assert creada.estado == EstadoSolicitud.ABIERTA
    assert creada.prioridad == PrioridadSolicitud.ALTA
    assert creada.motivo_reapertura is None


def test_asignar_prioridad_actualiza_solicitud_activa():
    # Preparar (Arrange)
    servicio = ServicioSolicitudes()
    solicitud = servicio.crear_solicitud(
        SolicitudCrear(
            titulo="Consulta sobre reportes mensuales",
            descripcion="Solicitamos orientación para filtrar ventas por sucursal.",
            cliente="Distribuidora El Puente",
        )
    )

    # Actuar (Act)
    actualizada = servicio.asignar_prioridad(solicitud.id, PrioridadSolicitud.CRITICA)

    # Verificar (Assert)
    assert actualizada.prioridad == PrioridadSolicitud.CRITICA


def test_reabrir_solicitud_cerrada_sin_motivo_lanza_error():
    # Preparar (Arrange)
    servicio = ServicioSolicitudes()
    solicitud = servicio.crear_solicitud(
        SolicitudCrear(
            titulo="Error de autenticación en portal web",
            descripcion="Usuarios reportan rechazo de credenciales válidas en horario pico.",
            cliente="Logística Bogotá Ltda.",
        )
    )
    servicio.cambiar_estado(solicitud.id, CambioEstadoRequest(nuevo_estado=EstadoSolicitud.CERRADA))

    # Actuar y Verificar (Act & Assert)
    with pytest.raises(ReglaNegocioError, match="motivo de reapertura"):
        servicio.cambiar_estado(
            solicitud.id,
            CambioEstadoRequest(nuevo_estado=EstadoSolicitud.ABIERTA, motivo_reapertura="   "),
        )


def test_reabrir_solicitud_cerrada_con_motivo_valido_permite_transicion():
    # Preparar (Arrange)
    servicio = ServicioSolicitudes()
    solicitud = servicio.crear_solicitud(
        SolicitudCrear(
            titulo="Intermitencia en sincronización de inventario",
            descripcion="Las existencias no se actualizan tras confirmar pedidos en caja.",
            cliente="Ferretería Central",
        )
    )
    servicio.cambiar_estado(solicitud.id, CambioEstadoRequest(nuevo_estado=EstadoSolicitud.CERRADA))
    motivo = "El cliente reporta que la intermitencia persiste tras el reinicio del nodo."

    # Actuar (Act)
    reabierta = servicio.cambiar_estado(
        solicitud.id,
        CambioEstadoRequest(nuevo_estado=EstadoSolicitud.EN_PROGRESO, motivo_reapertura=motivo),
    )

    # Verificar (Assert)
    assert reabierta.estado == EstadoSolicitud.EN_PROGRESO
    assert reabierta.motivo_reapertura == motivo


def test_cambiar_prioridad_en_solicitud_cerrada_es_rechazado():
    # Preparar (Arrange)
    servicio = ServicioSolicitudes()
    solicitud = servicio.crear_solicitud(
        SolicitudCrear(
            titulo="Actualización de certificados SSL",
            descripcion="Renovación preventiva de certificados antes de vencimiento anual.",
            cliente="Consultores Asociados",
        )
    )
    servicio.cambiar_estado(solicitud.id, CambioEstadoRequest(nuevo_estado=EstadoSolicitud.CERRADA))

    # Actuar y Verificar (Act & Assert)
    with pytest.raises(ReglaNegocioError, match="solicitud cerrada"):
        servicio.asignar_prioridad(solicitud.id, PrioridadSolicitud.ALTA)
