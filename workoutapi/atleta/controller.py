from uuid import uuid4
from datetime import datetime
from fastapi import APIRouter, Body, status
from sqlalchemy.future import select

from contrib.dependencies import DatabaseDependency
from atleta.schemas import AtletaIn, AtletaOut
from atleta.models import AtletaModel
from categorias.models import CategoriaModel  # se quiser usar a consulta

router = APIRouter()

@router.post(
    '/',
    summary='Criar um novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut
)
async def post(
    db_session: DatabaseDependency,
    atleta_in: AtletaIn = Body(...),
):
    breakpoint()
    # Consulta opcional à tabela de categorias
    categoria = (await db_session.execute(select(CategoriaModel))).filter_by([nome=atleta_in.categoria]).scalars().first()

    atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
    atleta_model = AtletaModel(**atleta_out.model_dump())

    db_session.add(atleta_model)
    await db_session.commit()

    return atleta_out





