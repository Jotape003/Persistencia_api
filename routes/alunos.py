from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from models.aluno import Aluno
from models.emprestimo import Emprestimo
from database import get_session

router = APIRouter(
    prefix="/alunos",
    tags=["alunos"]
)

@router.post("/", response_model=Aluno)
def create_aluno(aluno: Aluno, session: Session = Depends(get_session)):
    session.add(aluno)
    session.commit()
    session.refresh(aluno)
    return aluno

@router.get("/", response_model=list[Aluno])
def read_alunos(offset: int = 0, limit: int = Query(default=10, le=100),
                session: Session = Depends(get_session)):
    alunos = session.exec(select(Aluno).offset(offset).limit(limit)).all()
    return alunos

@router.get("/{aluno_id}", response_model=Aluno)
def read_aluno(aluno_id: int, session: Session = Depends(get_session)):
    aluno = session.get(Aluno, aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno

@router.put("/{aluno_id}", response_model=Aluno)
def update_aluno(aluno_id: int, aluno: Aluno, session: Session = Depends(get_session)):
    db_aluno = session.get(Aluno, aluno_id)
    if not db_aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    for key, value in aluno.model_dump(exclude_unset=True).items():
        setattr(db_aluno, key, value)
    session.add(db_aluno)
    session.commit()
    session.refresh(db_aluno)
    return db_aluno

@router.delete("/{aluno_id}")
def delete_aluno(aluno_id: int, session: Session = Depends(get_session)):
    aluno = session.get(Aluno, aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    session.delete(aluno)
    session.commit()
    return {"detail": "Aluno deletado com sucesso"}


# Relacionamento com emprestimos
@router.get("/{aluno_id}/emprestimos", response_model=list[Emprestimo])
def get_emprestimos_of_aluno(aluno_id: int, session: Session = Depends(get_session)):
    aluno = session.get(Aluno, aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    statement = select(Emprestimo).where(Emprestimo.aluno_id == aluno_id)
    emprestimos = session.exec(statement).all()
    return emprestimos