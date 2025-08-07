from typing import List
from uuid import uuid4
from categorias.models import CategoriaModel
from centro_treinamento.models import CentroDetreinamentoModel
from centro_treinamento.schemas import CentroDeTreinamento, CentroDeTreinamentoOut
from fastapi import APIRouter, Body, status
from uuid import UUID

from fastapi import HTTPException

from categorias.schemas import CategoriaOut
from contrib.dependencies import DatabaseDependency
from sqlalchemy import select






router = APIRouter()

@router.post(
    '/',
    summary='Criar um Centro de Treinamento',
    status_code=status.HTTP_201_CREATED,
    response_model=CentroDeTreinamentoOut,
)
async def post(
    db_session: DatabaseDependency,
    centro_in: CentroDeTreinamento = Body(...)
) -> CentroDeTreinamentoOut:
    centro_out = CentroDeTreinamentoOut(id=uuid4(), **centro_in.model_dump())
    centro_model = CentroDetreinamentoModel(**centro_out.model_dump())

    db_session.add(centro_model)
    await db_session.commit()
    await db_session.refresh(centro_model)

    return centro_out




@router.get(
    '/',
    summary='Consultar todos os Centros de Treinamento',
    status_code=status.HTTP_200_OK,
    response_model=List[CentroDeTreinamentoOut],
)
async def query(db_session: DatabaseDependency) -> List[CentroDeTreinamentoOut]:
    try:
        centros = (
            await db_session.execute(select(CentroDetreinamentoModel))
        ).scalars().all()
        return centros
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get(
    '/{id}',
    summary='Consulta um Centro de Treinamento pelo ID',
    status_code=status.HTTP_200_OK,
    response_model=CentroDeTreinamentoOut,
)
async def query(id: UUID, db_session: DatabaseDependency) -> CentroDeTreinamentoOut:
    centro = (
        await db_session.execute(
            select(CentroDetreinamentoModel).filter_by(id=id)
        )
    ).scalars().first()

    if not centro:
        raise HTTPException(status_code=404, detail='Centro de Treinamento não encontrado')

    return centro

