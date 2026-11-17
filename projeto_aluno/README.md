# BiblioTauá — Projeto Prático do Aluno (Sprint 04 - Aula 25)
## TASK-204 (Etapa 2): Persistência Relacional com SQLite e Padrão Repository

Bem-vindo(a) ao Encontro 2 da Sprint 04 do sistema **BiblioTauá Livraria Web**!

Na Aula 24, você implementou a hierarquia de exceções (`exceptions.py`) e a entidade de domínio `Cupom` (`models/cupom.py`).
Hoje, conectaremos esse modelo de domínio ao banco de dados relacional **SQLite**, garantindo integridade referencial, consultas protegidas contra SQL Injection e operações concorrentes seguras.

---

## 🌿 Fluxo Git & GitHub do Estudante

Você segue desenvolvendo no seu **próprio repositório no GitHub** (fork):

*   **Opção A (Continuar da Aula 24):**
    ```bash
    git checkout feature/task-204-motor-cupons
    ```
*   **Opção B (Ponto Homologado da Aula 25):**
    ```bash
    git fetch upstream
    git checkout -b feature/task-204-aula25 upstream/aula-25
    ```

---

## 🎯 Suas Tarefas Hoje

1. **`bibliotaua/database.py` (Script DDL SQLite):**
   - Garantir a instrução `CREATE TABLE IF NOT EXISTS cupons (...)` com todas as constraints (`CHECK`, `UNIQUE`, `DEFAULT`).
   - Adicionar a chave estrangeira `cupom_id INTEGER` e `FOREIGN KEY (cupom_id) REFERENCES cupons(id)` na tabela `pedidos`.
   - Criar o índice `idx_cupons_codigo` para buscas instantâneas por código alfanumérico.

2. **`bibliotaua/repositories/cupom_repository.py` (Padrão Repository):**
   - Implementar o construtor `__init__(self, conexao)` armazenando a conexão SQLite.
   - Implementar o conversor `_instanciar_cupom(self, row)` transformando `sqlite3.Row` na entidade de domínio `Cupom`.
   - Implementar `salvar(self, cupom)` usando query parametrizada com `?` (INSERT para novo ou UPDATE se já possui `id`).
   - Implementar `buscar_por_codigo(self, codigo)` com blindagem absoluta contra SQL Injection, lançando `CupomInexistenteError` quando não localizado.
   - Implementar `buscar_por_id(self, cupom_id)` e `listar_todos(self)`.
   - Implementar `registrar_uso(self, codigo)` chamando `cupom.registrar_uso()` (Aula 24) e persistindo o incremento no SQLite.

3. **`main.py` (Script de Verificação Integrada):**
   - Executar os 7 testes práticos no terminal e verificar a compatibilidade 100% com a Aula 24.

---

## 🚀 Como Executar

No terminal, dentro da pasta do projeto, execute:

```bash
python3 main.py
```

**Critério de Aceite:**
Todos os 7 blocos de teste devem exibir status positivo, confirmando a recuperação dos dados, o cálculo de desconto compatível com a Aula 24 e o bloqueio de injeção de SQL.

---

## 💾 Versionamento e Entrega no GitHub

Ao concluir os testes com sucesso, envie o código para seu repositório pessoal:

```bash
git add bibliotaua/database.py bibliotaua/repositories/cupom_repository.py main.py
git commit -m "feat(persistence): implementa DDL cupons e CupomRepository (Aula 25)"
git push origin HEAD
```
