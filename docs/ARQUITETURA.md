# Arquitetura técnica

## Estrutura

- `main.py`: entrada do aplicativo e autoteste executável/headless.
- `wmk_app.py`: interface Tkinter, navegação, formulários, tarefas e histórico.
- `wmk_core.py`: domínio, armazenamento JSON e descoberta passiva de comandos.
- `tests/test_core.py`: persistência, validação de nomes, caminhos, tarefas e relatórios.
- `.github/workflows/build-windows.yml`: testes Linux/Windows, PyInstaller, autoteste do EXE e artefato ZIP.

## Fronteiras

```text
Interface desktop (Tkinter)
           |
     ProjectManager
           |
 JSON local / relatórios MD
           |
      [adaptadores]
        /      \
 Craft Anything  REA/MCP
  (futuro)      (futuro)
```

**Importante:** a fronteira de adaptadores é apenas arquitetural no momento. Não existe envio de prompts ou execução de motores externos.

## Contrato JSON (v1)

Cada pasta de projeto contém `wmk_project.json`, com os campos `schema_version`, `id`, `name`, `kind`, `description`, `status`, `created_at`, `updated_at`, `tasks` e `history`.

O identificador é calculado a partir do nome (sem acentos e caracteres especiais), com limite de 80 caracteres. Projetos duplicados não são sobrescritos. A pasta de destino é validada contra navegação fora do diretório raiz. Atualizações usam arquivo temporário e `os.replace`.

## Segurança e limitações

- Sem execução de shell ou agentes nesta versão.
- Sem armazenamento de chaves, segredos ou tokens.
- A interface apenas abre links públicos e pastas locais selecionadas pelo projeto.
- O JSON recebido deve ser considerado dados não confiáveis; validação de esquema mais profunda está prevista.
- O relatório Markdown é derivado do estado local do projeto e **não representa evidência de teste de software gerado**.
- A validação `--self-test` exercita o armazenamento, não o carregamento da janela Tkinter nem o uso de um mouse real.

## Estratégia de integração

Adaptadores futuros devem obedecer a um contrato versionado com ID do projeto, ação permitida, pasta autorizada, limites de execução, eventos estruturados e evidências verificáveis. Nenhum retorno de agente deve ser promovido automaticamente a 'teste aprovado'.
