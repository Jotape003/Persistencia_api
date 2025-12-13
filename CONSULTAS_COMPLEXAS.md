# Consultas Complexas Implementadas

## Resumo

Este documento descreve as consultas complexas implementadas na API de biblioteca.

## Endpoints Implementados

### 1. **Empréstimos Atrasados**
**Endpoint**: `GET /emprestimos/atrasados/listar`
**Descrição**: Retorna todos os empréstimos que passaram da data de devolução prevista e ainda não foram devolvidos.

**Exemplo de Resposta**:
```json
[
  {
    "id": 5,
    "data_emprestimo": "2025-12-01",
    "data_devolucao_prevista": "2025-12-10",
    "data_devolucao": null,
    "aluno": {
      "id": 3,
      "nome": "Carlos Silva",
      "matricula": "2024003",
      "curso": "Ciência da Computação",
      "email": "carlos@universidade.br"
    },
    "livro": {
      "id": 2,
      "titulo": "Clean Code",
      "ano": 2008,
      "isbn": "978-0132350884",
      "categoria": "Engenharia de Software"
    }
  }
]
```

---

### 2. **Empréstimos Ativos**
**Endpoint**: `GET /emprestimos/ativos/listar`
**Descrição**: Retorna todos os empréstimos que ainda não foram devolvidos.

**Exemplo de Uso**:
```bash
curl http://localhost:8000/emprestimos/ativos/listar
```

---

### 3. **Busca de Livros**
**Endpoint**: `GET /livros/buscar/query?q={termo}`
**Descrição**: Busca livros por título, categoria ou nome do autor. Remove duplicatas automaticamente.

**Parâmetros**:
- `q` (obrigatório): Termo de busca (case-insensitive)

**Exemplos de Uso**:
```bash
# Buscar por título
curl "http://localhost:8000/livros/buscar/query?q=clean"
# Retorna: "Clean Code" e "Clean Architecture"

# Buscar por categoria
curl "http://localhost:8000/livros/buscar/query?q=arquitetura"

# Buscar por autor
curl "http://localhost:8000/livros/buscar/query?q=martin"
# Retorna: Todos os livros de Robert C. Martin e Martin Fowler
```

**Exemplo de Resposta**:
```json
[
  {
    "id": 1,
    "titulo": "Clean Code",
    "ano": 2008,
    "isbn": "978-0132350884",
    "categoria": "Engenharia de Software"
  },
  {
    "id": 11,
    "titulo": "Clean Architecture",
    "ano": 2017,
    "isbn": "978-0134494166",
    "categoria": "Arquitetura"
  }
]
```

---

### 4. **Livros Mais Emprestados (Ranking)**
**Endpoint**: `GET /livros/mais-emprestados/ranking?limit={N}`
**Descrição**: Retorna os N livros mais emprestados com estatísticas.

**Parâmetros**:
- `limit` (opcional, padrão=10, máx=50): Número de livros a retornar

**Exemplo de Uso**:
```bash
curl "http://localhost:8000/livros/mais-emprestados/ranking?limit=5"
```

**Exemplo de Resposta**:
```json
[
  {
    "id": 1,
    "titulo": "Clean Code",
    "ano": 2008,
    "isbn": "978-0132350884",
    "categoria": "Engenharia de Software",
    "total_emprestimos": 25,
    "emprestimos_ativos": 3
  },
  {
    "id": 3,
    "titulo": "Domain-Driven Design",
    "ano": 2003,
    "isbn": "978-0321125217",
    "categoria": "Arquitetura",
    "total_emprestimos": 18,
    "emprestimos_ativos": 1
  }
]
```

---

### 5. **Filtrar Livros por Categoria**
**Endpoint**: `GET /livros/por-categoria/filtrar?categoria={categoria}`
**Descrição**: Retorna todos os livros de uma categoria específica.

**Parâmetros**:
- `categoria` (obrigatório): Nome ou parte do nome da categoria

**Exemplo de Uso**:
```bash
curl "http://localhost:8000/livros/por-categoria/filtrar?categoria=Arquitetura"
```

---

### 6. **Estatísticas Gerais**
**Endpoint**: `GET /estatisticas/`
**Descrição**: Retorna um painel com estatísticas gerais do sistema.

**Exemplo de Uso**:
```bash
curl http://localhost:8000/estatisticas/
```

**Exemplo de Resposta**:
```json
{
  "total_alunos": 15,
  "total_autores": 12,
  "total_livros": 15,
  "total_emprestimos": 20,
  "emprestimos_ativos": 13,
  "emprestimos_finalizados": 7,
  "emprestimos_atrasados": 0,
  "livro_mais_emprestado": "Clean Code",
  "aluno_mais_ativo": "João Silva"
}
```

---

## Como Testar

### 1. **Via Swagger UI** (Recomendado)
Acesse: `http://localhost:8000/docs`

Todas as rotas estarão disponíveis com interface interativa para testar.

### 2. **Via cURL**
```bash
# Iniciar o servidor
python -m uv run uvicorn main:app --reload

# Testar estatísticas
curl http://localhost:8000/estatisticas/ | python -m json.tool

# Testar livros mais emprestados
curl "http://localhost:8000/livros/mais-emprestados/ranking?limit=5" | python -m json.tool

# Testar busca
curl "http://localhost:8000/livros/buscar/query?q=clean" | python -m json.tool

# Testar empréstimos atrasados
curl http://localhost:8000/emprestimos/atrasados/listar | python -m json.tool

# Testar empréstimos ativos
curl http://localhost:8000/emprestimos/ativos/listar | python -m json.tool
```

### 3. **Via Python**
```python
import requests

# Estatísticas
response = requests.get("http://localhost:8000/estatisticas/")
print(response.json())

# Buscar livros
response = requests.get("http://localhost:8000/livros/buscar/query", params={"q": "clean"})
print(response.json())

# Livros mais emprestados
response = requests.get("http://localhost:8000/livros/mais-emprestados/ranking", params={"limit": 5})
print(response.json())
```

---

## Arquivos Modificados/Criados

### Novos Arquivos:
- `routes/estatisticas.py` - Endpoint de estatísticas gerais

### Arquivos Modificados:
- `routes/emprestimos.py` - Adicionados endpoints de atrasados e ativos
- `routes/livros.py` - Adicionados endpoints de busca, ranking e filtro
- `models/livro.py` - Adicionado schema `LivroComEstatisticas`
- `main.py` - Registrado router de estatísticas

---

## Casos de Uso

### Dashboard Administrativo
Use o endpoint `/estatisticas/` para exibir um painel de controle.

### Sistema de Busca
Use `/livros/buscar/query` para implementar uma barra de pesquisa no front-end.

### Gestão de Atrasos
Use `/emprestimos/atrasados/listar` para enviar lembretes aos alunos.

### Relatórios
Use `/livros/mais-emprestados/ranking` para gerar relatórios de popularidade.

---

## Próximas Melhorias (Opcional)

- [ ] Filtrar empréstimos por período de datas
- [ ] Top alunos mais ativos (já tem no /estatisticas, mas pode ter endpoint separado)
- [ ] Média de dias de empréstimo
- [ ] Taxa de devolução no prazo
- [ ] Livros nunca emprestados

---

**Implementado por**: Bruno
**Data**: Dezembro 2025
**Versão**: 1.0
