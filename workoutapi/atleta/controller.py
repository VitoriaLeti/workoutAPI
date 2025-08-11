from typing import List
from uuid import uuid4
from datetime import datetime
from centro_treinamento.models import CentroDetreinamentoModel
from fastapi import APIRouter, Body, HTTPException, status
from sqlalchemy import UUID
from sqlalchemy.future import select
from uuid import UUID

from fastapi import Path


from contrib.dependencies import DatabaseDependency
from atleta.schemas import AtletaIn, AtletaOut,AtletaUpdate
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
    atleta_in: AtletaIn = Body(...)
):
    # Verifica se a categoria existe
    categoria = (await db_session.execute(
        select(CategoriaModel).filter_by(nome=atleta_in.categoria)
    )).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A categoria '{atleta_in.categoria}' não foi encontrada."
        )

    # Verifica se o centro de treinamento existe
    centro_treinamento = (await db_session.execute(
        select(CentroDetreinamentoModel).filter_by(nome=atleta_in.centro_treinamento)
    )).scalars().first()

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O centro de treinamento '{atleta_in.centro_treinamento}' não foi encontrado."
        )

    # Cria o objeto de saída e o modelo para o banco
    atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())

    atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))
    atleta_model.categoria_id = categoria.pk_id
    atleta_model.centro_treinamento_id = centro_treinamento.pk_id

    db_session.add(atleta_model)
    await db_session.commit()

    return atleta_out


@router.get(
    '/',
    summary='Consultar todos os Atletas',
    status_code=status.HTTP_200_OK,
    response_model=List[AtletaOut],
)
async def query(db_session: DatabaseDependency) -> list[AtletaOut]:
    try:
        atletas: list[AtletaOut] = (
            await db_session.execute(select(AtletaModel))
        ).scalars().all()

        return [AtletaOut.model_validate(atleta) for atleta in atletas]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get(
    "/{id}",
    summary="Consulta um Atleta pelo id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def query(id: UUID, db_session: DatabaseDependency) -> AtletaOut:
    result = await db_session.execute(
        select(AtletaModel).filter_by(pk_id=id)  # ou 'id=id' se o campo for 'id'
    )
    atleta = result.scalars().first()
    return atleta





@router.patch(
    "/{id}",
    summary="Atualiza um atleta pelo id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def update_atleta(
    id: UUID,
    db_session: DatabaseDependency,
    atleta_up: AtletaUpdate = Body(...),
) -> AtletaOut:
    atleta = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta não encontrado no id: {id}",
        )

    atleta_update = atleta_up.model_dump(exclude_unset=True)

    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return atleta





@router.delete(
    "/{id}",
    summary="Deletar um Atleta pelo id",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_atleta(id: UUID, db_session: DatabaseDependency) -> None:
    atleta = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta não encontrado no id: {id}"
        )

    await db_session.delete(atleta)
    await db_session.commit()


