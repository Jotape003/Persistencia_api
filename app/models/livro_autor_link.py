from sqlmodel import SQLModel, Field

class LivroAutorLink(SQLModel, table=True):
    livro_id: int = Field(foreign_key='livro.id', primary_key=True)
    autor_id: int = Field(foreign_key='autor.id', primary_key=True)