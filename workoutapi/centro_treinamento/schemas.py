
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from contrib.models import BaseModel
from pydantic import Field
from typing import Annotated
from contrib.schemas import BaseSchema
from pydantic import UUID4


class CentroDeTreinamento(BaseSchema):
 nome: Annotated[str, Field(description='Nome de Centro detreinamento', example='CT king', max_length=20)]
 endereco: Annotated[str, Field(description='Endereço do Centro de treinamento', example='Rua x,Q02', max_length=60)]
 proprietario: Annotated[str, Field(description='Proprietario do Centro de treinamento', example='Marcos', max_length=30)]

class CentroDeTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(
        description='Nome do centro de treinamento',
        example='CT King',
        max_length=20
    )]

class CentroDeTreinamentoOut(CentroDeTreinamento):
    id: Annotated[UUID4, Field(
        description='Identificador de Centro de treinamento',
    )]

