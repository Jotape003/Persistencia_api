from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from models.livro import Livro
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
