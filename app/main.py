from typing import List
from fastapi import FastAPI, HTTPException, status
from app.models import (
    CambioEstadoRequest,
    PrioridadSolicitud,
    Solicitud,
    SolicitudCrear,
)
from app.service import ReglaNegocioError, ServicioSolicitudes

app = FastAPI(
    title="MesaÁgil - API de Gestión de Solicitudes",
    description="Módulo representativo REST para el reto de Testing Automatizado y DevOps.",
    version="0.1.0",
)

servicio = ServicioSolicitudes()


@app.get("/health", tags=["Operación"])
def verificar_salud() -> dict:
    return {"status": "ok", "servicio": "mesaagil-api"}


@app.post("/solicitudes", response_model=Solicitud, status_code=status.HTTP_201_CREATED, tags=["Solicitudes"])
def registrar_solicitud(payload: SolicitudCrear) -> Solicitud:
    return servicio.crear_solicitud(payload)


@app.get("/solicitudes", response_model=List[Solicitud], tags=["Solicitudes"])
def consultar_solicitudes() -> List[Solicitud]:
    return servicio.listar_solicitudes()


@app.patch("/solicitudes/{solicitud_id}/prioridad", response_model=Solicitud, tags=["Solicitudes"])
def actualizar_prioridad(solicitud_id: int, prioridad: PrioridadSolicitud) -> Solicitud:
    try:
        return servicio.asignar_prioridad(solicitud_id, prioridad)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ReglaNegocioError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc


@app.patch("/solicitudes/{solicitud_id}/estado", response_model=Solicitud, tags=["Solicitudes"])
def actualizar_estado(solicitud_id: int, cambio: CambioEstadoRequest) -> Solicitud:
    try:
        return servicio.cambiar_estado(solicitud_id, cambio)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ReglaNegocioError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
