from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from models.emprestimo import Emprestimo
from database import get_session

router = APIRouter(
    prefix="/emprestimos",
    tags=["emprestimos"]
)

@router.post("/", response_model=Emprestimo)
def create_emprestimo(emprestimo: Emprestimo, session: Session = Depends(get_session)):
    session.add(emprestimo)
    session.commit()
    session.refresh(emprestimo)
    return emprestimo

@router.get("/", response_model=list[Emprestimo])
def read_emprestimos(offset: int = 0, limit: int = Query(default=10, le=100),
                     session: Session = Depends(get_session)):
    emprestimos = session.exec(select(Emprestimo).offset(offset).limit(limit)).all()
    return emprestimos

@router.get("/{emprestimo_id}", response_model=Emprestimo)
def read_emprestimo(emprestimo_id: int, session: Session = Depends(get_session)):
    emprestimo = session.get(Emprestimo, emprestimo_id)
    if not emprestimo:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
    return emprestimo

@router.put("/{emprestimo_id}", response_model=Emprestimo)
def update_emprestimo(emprestimo_id: int, emprestimo: Emprestimo,
                      session: Session = Depends(get_session)):
    db_emprestimo = session.get(Emprestimo, emprestimo_id)
    if not db_emprestimo:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
    for key, value in emprestimo.model_dump(exclude_unset=True).items():
        setattr(db_emprestimo, key, value)
    session.add(db_emprestimo)
    session.commit()
    session.refresh(db_emprestimo)
    return db_emprestimo

@router.delete("/{emprestimo_id}")
def delete_emprestimo(emprestimo_id: int, session: Session = Depends(get_session)):
    emprestimo = session.get(Emprestimo, emprestimo_id)
    if not emprestimo:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
    session.delete(emprestimo)
    session.commit()
    return {"detail": "Empréstimo deletado com sucesso"}
