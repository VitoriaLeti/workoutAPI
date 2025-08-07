
from typing import Annotated
from contrib.schemas import BaseSchema
from pydantic import UUID4
from pydantic import Field




class CategoriaIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome da Categoria', example='schale', max_length=10)]

class CategoriaOut(CategoriaIn):
    id: Annotated[UUID4, Field(description='Identificador da categoria')]
