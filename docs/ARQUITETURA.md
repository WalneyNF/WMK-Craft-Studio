# Arquitetura técnica

## Estrutura

- `main.py`: entrada do aplicativo e autoteste executável/headless.
- `wmk_app.py`: interface Tkinter, navegação, formulários, estudo funcional, tarefas e histórico.
- `wmk_core.py`: domínio, armazenamento JSON e descoberta passiva de comandos.
- `tests/test_core.py`: persistência, validação de nomes, caminhos, estudo funcional e relatórios.
- `.github/workflows/build-windows.yml`: testes Linux/Windows, PyInstaller, autoteste do EXE e artefato ZIP.

## Fronteiras

```text
Interface desktop (Tkinter)
           |
     ProjectManager
           |
 JSON local / briefs originais MD
           |
      [adaptadores futuros]
        /            \
Craft Anything       FreeLLMAPI
(execução autoral)    (gateway IA)
  (futuro)            (futuro)
```

**Importante:** a fronteira de adaptadores é apenas arquitetural no momento. Não existe envio de prompts ou execução de motores externos.

## Contrato JSON (v1)

Cada pasta de projeto contém `wmk_project.json`, com os campos `schema_version`, `id`, `name`, `kind`, `description`, `reference_study`, `status`, `created_at`, `updated_at`, `tasks` e `history`. O objeto `reference_study` separa funcionalidades observadas, necessidades e soluções autorais; nenhum campo contém código extraído de programas de terceiros.

O identificador é calculado a partir do nome (sem acentos e caracteres especiais), com limite de 80 caracteres. Projetos duplicados não são sobrescritos. A pasta de destino é validada contra navegação fora do diretório raiz. Atualizações usam arquivo temporário e `os.replace`.

## Segurança e limitações

- Sem execução de shell ou agentes nesta versão.
- Sem engenharia reversa, inspeção de executáveis ou clonagem de software; é proibido adicionar recursos assim à aplicação.
- Sem armazenamento de chaves, segredos ou tokens.
- A interface apenas abre links públicos e pastas locais selecionadas pelo projeto.
- O JSON recebido deve ser considerado dados não confiáveis; validação de esquema mais profunda está prevista.
- O relatório Markdown é derivado do estado local do projeto e **não representa evidência de teste de software gerado**.
- A validação `--self-test` exercita o armazenamento, não o carregamento da janela Tkinter nem o uso de um mouse real.

## Estratégia de integração

Para utilização de modelos remotos por meio do FreeLLMAPI, deve haver consentimento do usuário para transmitir dados, sem segredos em logs; a conexão deve usar autenticação, loopback e timeouts. Veja [PROVEDORES_IA.md](PROVEDORES_IA.md).

Adaptadores futuros devem obedecer a um contrato versionado com ID do projeto, ação permitida, pasta autorizada, limites de execução, eventos estruturados e evidências verificáveis. Nenhum retorno de agente deve ser promovido automaticamente a 'teste aprovado'.
