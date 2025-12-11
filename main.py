from fastapi import FastAPI
from routes import home, alunos, autores, livros, emprestimos

app = FastAPI()

app.include_router(home.router)
app.include_router(alunos.router)
app.include_router(autores.router)
app.include_router(livros.router)
app.include_router(emprestimos.router)