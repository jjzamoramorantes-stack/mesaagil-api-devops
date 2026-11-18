from typing import Dict, List, Optional
from app.models import (
    CambioEstadoRequest,
    EstadoSolicitud,
    PrioridadSolicitud,
    Solicitud,
    SolicitudCrear,
)


class ReglaNegocioError(ValueError):
    """Excepción lanzada cuando se viola una invariante de negocio de MesaÁgil."""


class ServicioSolicitudes:
    """Servicio de dominio encargado de gestionar el ciclo de vida de solicitudes de soporte."""

    def __init__(self) -> None:
        self._solicitudes: Dict[int, Solicitud] = {}
        self._secuencia_id: int = 1

    def crear_solicitud(self, datos: SolicitudCrear) -> Solicitud:
        solicitud = Solicitud(
            id=self._secuencia_id,
            titulo=datos.titulo.strip(),
            descripcion=datos.descripcion.strip(),
            cliente=datos.cliente.strip(),
            prioridad=datos.prioridad,
            estado=EstadoSolicitud.ABIERTA,
        )
        self._solicitudes[self._secuencia_id] = solicitud
        self._secuencia_id += 1
        return solicitud

    def obtener_solicitud(self, solicitud_id: int) -> Solicitud:
        if solicitud_id not in self._solicitudes:
            raise KeyError(f"La solicitud con ID {solicitud_id} no existe.")
        return self._solicitudes[solicitud_id]

    def listar_solicitudes(self) -> List[Solicitud]:
        return list(self._solicitudes.values())

    def asignar_prioridad(self, solicitud_id: int, nueva_prioridad: PrioridadSolicitud) -> Solicitud:
        solicitud = self.obtener_solicitud(solicitud_id)
        if solicitud.estado == EstadoSolicitud.CERRADA:
            raise ReglaNegocioError(
                "No se puede modificar la prioridad de una solicitud cerrada sin reabrirla primero."
            )
        solicitud.prioridad = nueva_prioridad
        return solicitud

    def cambiar_estado(self, solicitud_id: int, cambio: CambioEstadoRequest) -> Solicitud:
        solicitud = self.obtener_solicitud(solicitud_id)

        # Invariante crítica del caso MesaÁgil:
        # Una solicitud cerrada solo puede reabrirse si se registra un motivo válido.
        if solicitud.estado == EstadoSolicitud.CERRADA and cambio.nuevo_estado != EstadoSolicitud.CERRADA:
            motivo_limpio: Optional[str] = (
                cambio.motivo_reapertura.strip() if cambio.motivo_reapertura else None
            )
            if not motivo_limpio:
                raise ReglaNegocioError(
                    "Una solicitud cerrada solo puede reabrirse si se registra el motivo de reapertura."
                )
            solicitud.motivo_reapertura = motivo_limpio

        solicitud.estado = cambio.nuevo_estado
        return solicitud
