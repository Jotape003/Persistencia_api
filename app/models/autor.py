from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from livro import Livro

class AutorBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    nacionalidade: str
    ano_nascimento: int

class Autor(AutorBase, table=True):
    livros: list['Livro'] = Relationship(
        back_populates='autores',
        link_model='LivroAutorLink'
    )