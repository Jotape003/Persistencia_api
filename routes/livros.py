from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from models.livro import Livro
from models.livro_autor_link import LivroAutorLink
from models.autor import Autor
from models.emprestimo import Emprestimo, EmprestimoWithAluno
from database import get_session

router = APIRouter(
    prefix="/livros",
    tags=["livros"]
)

@router.post("/", response_model=Livro)
def create_livro(livro: Livro, session: Session = Depends(get_session)):
    session.add(livro)
    session.commit()
    session.refresh(livro)
    return livro

@router.get("/", response_model=list[Livro])
def read_livros(offset: int = 0, limit: int = Query(default=10, le=100),
                session: Session = Depends(get_session)):
    livros = session.exec(select(Livro).offset(offset).limit(limit)).all()
    return livros

@router.get("/{livro_id}", response_model=Livro)
def read_livro(livro_id: int, session: Session = Depends(get_session)):
    livro = session.get(Livro, livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro

@router.put("/{livro_id}", response_model=Livro)
def update_livro(livro_id: int, livro: Livro, session: Session = Depends(get_session)):
    db_livro = session.get(Livro, livro_id)
    if not db_livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    for key, value in livro.model_dump(exclude_unset=True).items():
        setattr(db_livro, key, value)
    session.add(db_livro)
    session.commit()
    session.refresh(db_livro)
    return db_livro

@router.delete("/{livro_id}")
def delete_livro(livro_id: int, session: Session = Depends(get_session)):
    livro = session.get(Livro, livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    session.delete(livro)
    session.commit()
    return {"detail": "Livro deletado com sucesso"}


# Relacionamento com autores

@router.post("/{livro_id}/autores/{autor_id}")
def add_autor_to_livro(livro_id: int, autor_id: int, session: Session = Depends(get_session)):
    livro = session.get(Livro, livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    autor = session.get(Autor, autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor não encontrado")

    existente = session.get(LivroAutorLink, (livro_id, autor_id))
    if existente:
        raise HTTPException(status_code=400, detail="Autor já está vinculado a este livro")

    link = LivroAutorLink(livro_id=livro_id, autor_id=autor_id)
    session.add(link)
    session.commit()
    return {"detail": "Autor adicionado ao livro com sucesso"}

@router.get("/{livro_id}/autores", response_model=list[Autor])
def get_autores_of_livro(livro_id: int, session: Session = Depends(get_session)):
    livro = session.get(Livro, livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    statement = select(Autor).join(LivroAutorLink).where(LivroAutorLink.livro_id == livro_id)
    autores = session.exec(statement).all()
    return autores

@router.delete("/{livro_id}/autores/{autor_id}")
def remove_autor_from_livro(livro_id: int, autor_id: int, session: Session = Depends(get_session)):
    link = session.get(LivroAutorLink, (livro_id, autor_id))
    if not link:
        raise HTTPException(status_code=404, detail="Vínculo entre livro e autor não encontrado")
    session.delete(link)
    session.commit()
    return {"detail": "Autor removido do livro com sucesso"}


# Relacionamento com emprestimos

@router.get("/{livro_id}/emprestimos", response_model=list[EmprestimoWithAluno])
def get_emprestimos_of_livro(livro_id: int, session: Session = Depends(get_session)):
    livro = session.get(Livro, livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    statement = (
        select(Emprestimo)
        .where(Emprestimo.livro_id == livro_id)
        .options(selectinload(Emprestimo.aluno))
    )
    emprestimos = session.exec(statement).all()
    return emprestimos