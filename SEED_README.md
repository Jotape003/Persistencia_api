# Script de Seed - Documentação

## 📋 Descrição

Script para popular o banco de dados com dados realistas de teste para o sistema de biblioteca.

## 📊 Dados Criados

O script cria:

- ✅ **15 Alunos** de diversos cursos (Ciência da Computação, Engenharia de Software, Sistemas de Informação, Engenharia de Dados)
- ✅ **12 Autores** clássicos e modernos da computação (Robert C. Martin, Martin Fowler, etc.)
- ✅ **15 Livros** técnicos de programação e engenharia de software
- ✅ **20 Empréstimos** (13 ativos, 7 finalizados, incluindo casos de atraso)
- ✅ **Relacionamentos N:N** entre Livros e Autores

## 🚀 Como Executar

### Método 1: Com UV (Recomendado)
```bash
python -m uv run python seed.py
```

### Método 2: Com ambiente virtual ativado
```bash
# Windows
.venv\Scripts\activate
python seed.py

# Linux/Mac
source .venv/bin/activate
python seed.py
```

## ⚙️ Funcionalidades

### Proteção contra duplicação
- O script verifica se já existem dados no banco
- Se houver dados, pergunta se você quer limpar antes de popular
- Evita erros de constraint violation

### Função de limpeza (opcional)
Para limpar o banco manualmente antes de executar:

```python
# Descomente esta linha no arquivo seed.py (dentro da função main):
limpar_banco()
```

## 📚 Exemplos de Dados Criados

### Alunos
- Ana Silva (2024001) - Ciência da Computação
- Bruno Santos (2024002) - Engenharia de Software
- Carla Oliveira (2024003) - Sistemas de Informação
- ... e mais 12 alunos

### Livros
- Clean Code (2008) - Robert C. Martin
- Refactoring (1999) - Martin Fowler
- Domain-Driven Design (2003) - Eric Evans
- Design Patterns (1994) - Gang of Four
- The Pragmatic Programmer (1999) - Andrew Hunt & David Thomas
- ... e mais 10 livros

### Empréstimos
- **Ativos**: Empréstimos sem data de devolução (13 casos)
- **Finalizados**: Empréstimos com devolução dentro do prazo (5 casos)
- **Atrasados**: Empréstimos devolvidos após o prazo (2 casos)

## 🔍 Verificar Dados Inseridos

Para visualizar os dados inseridos:

```bash
python -m uv run python verificar_dados.py
```

Este script mostra:
- Lista de alunos cadastrados
- Lista de autores
- Livros com seus autores e informações
- Empréstimos ativos com detalhes

## 🎯 Casos de Uso para Testes

Os dados criados são úteis para testar:

1. **CRUD básico**: Todos os modelos têm pelo menos 10 instâncias
2. **Relacionamentos 1:N**: Alunos → Empréstimos, Livros → Empréstimos
3. **Relacionamentos N:N**: Livros ↔ Autores (com tabela de ligação)
4. **Consultas complexas**:
   - Livros por autor
   - Empréstimos ativos (sem devolução)
   - Empréstimos atrasados (prevista < hoje e não devolvido)
   - Histórico de empréstimos por aluno
   - Disponibilidade de livros (quantidade > empréstimos ativos)

## 🛠️ Estrutura do Código

```python
seed.py
├── limpar_banco()              # Remove todos os dados
├── seed_alunos()               # Cria 15 alunos
├── seed_autores()              # Cria 12 autores
├── seed_livros()               # Cria 15 livros
├── vincular_livros_autores()   # Cria relações N:N
├── seed_emprestimos()          # Cria 20 empréstimos
├── exibir_estatisticas()       # Mostra resumo dos dados
└── main()                      # Orquestra tudo
```

## 📝 Notas Importantes

- ✅ Funciona com **SQLite** (desenvolvimento) e **PostgreSQL** (produção)
- ✅ Respeita **foreign keys** (ordem de inserção correta)
- ✅ Usa dados **realistas** (livros reais, nomes brasileiros)
- ✅ Compatível com **Windows** (encoding UTF-8 configurado)
- ✅ Datas **relativas** (baseadas na data atual)

## 🐛 Solução de Problemas

### Erro: "UNIQUE constraint failed"
- O banco já tem dados. Execute com a opção de limpar ou remova o `biblioteca.db`

### Erro de encoding no Windows
- O script já tem tratamento para isso, mas se persistir, use:
  ```bash
  chcp 65001
  python seed.py
  ```

### Banco não atualiza
- Verifique se está usando o arquivo `.env` correto
- Confirme que a `DATABASE_URL` aponta para o banco certo

## 📦 Dependências

Todas as dependências já estão no `pyproject.toml`:
- sqlmodel
- python-dotenv
- alembic

---

**Criado por**: Bruno (Etapa 8 do projeto)
**Data**: Dezembro 2025
**Versão**: 1.0
