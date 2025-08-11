from typing import Annotated
from centro_treinamento.schemas import CentroDeTreinamentoAtleta
from contrib.schemas import BaseSchema
from pydantic import BaseModel,Field,PositiveFloat
from workoutapi.contrib.schemas import BaseSchema, OutMixin
from typing import Optional, Annotated


from workoutapi.categorias.schemas import CategoriaIn



  
class Atleta(BaseSchema):
 nome:Annotated[str,Field(description='Nome do atleta',exemple='joao',max_length=50)]
 cpf:Annotated[str,Field(description='CPF do atleta',exemple='12345678900',max_length=11)]
 idade:Annotated[int,Field(description='Idade do atleta',exemple='25')]
 peso:Annotated[PositiveFloat, Field(description='Peso do atleta',exemple='75.5')]
 altura:Annotated[PositiveFloat, Field(description='altura do atleta',exemple='1.70')]
 sexo:Annotated[str,Field(description='Sexo do atleta',exemple='M',max_length=1)]
 categoria:Annotated[CategoriaIn,Field(description='Categoria do atleta')]
 centro_treinamento:Annotated[CentroDeTreinamentoAtleta,Field(description='Centro de treinamento do atleta')]
 
class AtletaIn(Atleta):
    pass

class AtletaOut(AtletaIn, OutMixin):
    pass


class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description='Nome do atleta', example='Joao', max_length=50)]
    idade: Annotated[Optional[int], Field(None, description='Idade do atleta', example=25)]

