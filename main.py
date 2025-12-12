from fastapi import FastAPI
from routes import home, alunos, autores, livros, emprestimos

from models.aluno import Aluno
from models.emprestimo import Emprestimo, EmprestimoWithLivro, EmprestimoWithAluno
from models.livro import Livro
from models.autor import Autor

Aluno.model_rebuild()
Emprestimo.model_rebuild()
EmprestimoWithLivro.model_rebuild()
EmprestimoWithAluno.model_rebuild()
Livro.model_rebuild()
Autor.model_rebuild()

app = FastAPI()

app.include_router(home.router)
app.include_router(alunos.router)
app.include_router(autores.router)
app.include_router(livros.router)
app.include_router(emprestimos.router)