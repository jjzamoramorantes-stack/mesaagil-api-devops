from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class PrioridadSolicitud(str, Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"


class EstadoSolicitud(str, Enum):
    ABIERTA = "abierta"
    EN_PROGRESO = "en_progreso"
    CERRADA = "cerrada"


class SolicitudCrear(BaseModel):
    titulo: str = Field(..., min_length=5, max_length=120, description="Resumen breve del incidente")
    descripcion: str = Field(..., min_length=10, description="Detalle técnico de la solicitud")
    cliente: str = Field(..., min_length=2, description="Nombre de la empresa cliente")
    prioridad: PrioridadSolicitud = PrioridadSolicitud.MEDIA


class CambioEstadoRequest(BaseModel):
    nuevo_estado: EstadoSolicitud
    motivo_reapertura: Optional[str] = Field(
        default=None,
        description="Obligatorio cuando se reabre una solicitud que estaba en estado cerrada"
    )


class Solicitud(BaseModel):
    id: int
    titulo: str
    descripcion: str
    cliente: str
    prioridad: PrioridadSolicitud
    estado: EstadoSolicitud
    motivo_reapertura: Optional[str] = None
