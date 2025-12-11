from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from models.autor import Autor
from database import get_session

router = APIRouter(
    prefix="/autores",
    tags=["autores"]
)

@router.post("/", response_model=Autor)
def create_autor(autor: Autor, session: Session = Depends(get_session)):
    session.add(autor)
    session.commit()
    session.refresh(autor)
    return autor

@router.get("/", response_model=list[Autor])
def read_autores(offset: int = 0, limit: int = Query(default=10, le=100),
                 session: Session = Depends(get_session)):
    autores = session.exec(select(Autor).offset(offset).limit(limit)).all()
    return autores

@router.get("/{autor_id}", response_model=Autor)
def read_autor(autor_id: int, session: Session = Depends(get_session)):
    autor = session.get(Autor, autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    return autor

@router.put("/{autor_id}", response_model=Autor)
def update_autor(autor_id: int, autor: Autor, session: Session = Depends(get_session)):
    db_autor = session.get(Autor, autor_id)
    if not db_autor:
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    for key, value in autor.model_dump(exclude_unset=True).items():
        setattr(db_autor, key, value)
    session.add(db_autor)
    session.commit()
    session.refresh(db_autor)
    return db_autor

@router.delete("/{autor_id}")
def delete_autor(autor_id: int, session: Session = Depends(get_session)):
    autor = session.get(Autor, autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    session.delete(autor)
    session.commit()
    return {"detail": "Autor deletado com sucesso"}
