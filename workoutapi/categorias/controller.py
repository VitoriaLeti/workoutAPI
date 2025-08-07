from typing import List
from uuid import uuid4
from categorias.models import CategoriaModel
from fastapi import APIRouter, Body, status
from uuid import UUID

from fastapi import HTTPException

from categorias.schemas import CategoriaOut
from contrib.dependencies import DatabaseDependency
from sqlalchemy import select

from workoutapi.atleta.schemas import AtletaIn
from workoutapi.categorias.schemas import CategoriaIn

router = APIRouter()

@router.post(
    '/',
    summary='Criar uma nova Categoria',
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut,
)
async def post(
    db_session: DatabaseDependency,
    categoria_in: CategoriaIn = Body(...)
) -> CategoriaOut:
    categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())

    db_session.add(categoria_model)
    await db_session.commit()
    await db_session.refresh(categoria_model)

    return categoria_out



@router.get(
    '/',
    summary='Consultar todas as Categorias',
    status_code=status.HTTP_200_OK,
    response_model=List[CategoriaOut],
)
async def query(db_session: DatabaseDependency) -> List[CategoriaOut]:
    try:
        categorias = (
            await db_session.execute(select(CategoriaModel))
        ).scalars().all()
        return categorias
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.get(
    '/{id}',
    summary='Consulta uma Categoria pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def query(id: UUID, db_session: DatabaseDependency) -> CategoriaOut:
    categoria: CategoriaOut = (
        await db_session.execute(
            select(CategoriaModel).filter_by(id=id)
        )
    ).scalars().first()

    return categoria

