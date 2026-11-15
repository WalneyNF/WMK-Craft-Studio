# Provedores de IA — avaliação do FreeLLMAPI

**Status:** proposta de integração, ainda não implementada no WMK Craft Studio.

## Por que usar

[FreeLLMAPI](https://github.com/WalneyNF/freellmapi) é um serviço local de roteamento de requisições a modelos de terceiros. Sua API principal segue o formato OpenAI e tem suporte documentado a modelos, chat, ferramentas, visão, áudio e outros recursos. O roteamento e a capacidade real dependem dos modelos e provedores habilitados.

O FreeLLMAPI **não é um modelo de IA** e **não fornece, por si, um limite de tokens gratuitos garantido**. Cada usuário deve configurar chaves dos provedores desejados e respeitar as cotas e condições de uso.

O servidor é destinado a **uso local por uma pessoa** e não deve ser exposto diretamente à internet ou à rede local sem medidas próprias de autenticação e proteção.

## Requisitos e operação independente

- Node.js `>=20.18.0 <25` e npm `>=10`; o Dockerfile do fork usa Node 24.22.1.
- API local: `http://127.0.0.1:3001/v1` (porta padrão, configurável).
- Cabeçalho `Authorization: Bearer <chave-unificada>`, obtida no painel do FreeLLMAPI.
- Dashboard no endereço local da instância, para cadastrar chaves, perfis e inspecionar consumo.
- Repositório independente: licenciado em MIT, com copyright de Tashfeen Ahmed — manter o aviso ao redistribuir código.

### Endpoints úteis ao WMK

| Função | Endpoint |
| --- | --- |
| Status básico do servidor | `GET /api/ping` |
| Modelos disponíveis/aptos | `GET /v1/models?execution_status=ready` |
| Criar resposta | `POST /v1/chat/completions` |
| API de resposta para certos agentes | `POST /v1/responses` |
| Metadados de API | `GET /v1/openapi.json` |
| Documentação interativa | `GET /v1/docs` |

Não confundir `GET /v1/models` (catálogo, que pode incluir modelos indisponíveis) com o filtro `execution_status=ready` (provedores configurados sem bloqueio conhecido no momento).

## Exemplo de integração futura em Python (somente demonstração)

Use **apenas** prompts legítimos, autorais, sem dados confidenciais de terceiros e sem material protegido que não possa compartilhar. A variável `WMK_FREELLMAPI_KEY` deve ser definida fora do código e nunca entrar no controle de versão.

```python
import json
import os
import urllib.request

key = os.environ["WMK_FREELLMAPI_KEY"]
payload = {
    "model": "auto",
    "messages": [
        {"role": "system", "content": "Ajude a formular requisitos de uma solução original. Não copie programas de terceiros."},
        {"role": "user", "content": "Descreva requisitos para um controle de estoque offline com SQLite."},
    ],
}
request = urllib.request.Request(
    "http://127.0.0.1:3001/v1/chat/completions",
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    },
    method="POST",
)
with urllib.request.urlopen(request, timeout=45) as response:
    result = json.load(response)
print(result["choices"][0]["message"]["content"])
```

Esse exemplo exige uma instância instalada e configurada e não executa comandos de sistema. Nem todas as chamadas responderão em 45 segundos; o futuro aplicativo deverá controlar timeouts, tentativas e cancelamento na interface.

## Segurança e responsabilidade

1. **Consentimento antes de enviar:** explique que o gateway é local, mas a inferência normalmente roda nos provedores externos escolhidos; prompts e anexos podem sair do computador.
2. **Chaves:** mantenha o token unificado somente na máquina do usuário, fora de arquivos de projeto e logs; não copie chaves de provedores para o WMK. Não inclua chaves em URL.
3. **Loopback:** use 127.0.0.1 por padrão, não `0.0.0.0`. Expor o painel/API em LAN ou internet muda a superfície de risco.
4. **Qualidade:** não confunda uma resposta de LLM com um programa testado. Um gateway não substitui ferramentas de execução, compilação e testes.
5. **Originalidade:** impedir fluxos voltados a clonagem, descompilação, extração ou reprodução fiel de software alheio. Apenas briefs funcionais e criação independente.
6. **Provedores e disponibilidade:** exibir erros reais (401, 429, 5xx), quotas e limitações. Nunca prometer uso gratuito ilimitado.
7. **Licença:** FreeLLMAPI é MIT, mas determinados serviços/catálogos anunciados podem ter benefícios comerciais; avaliar condições de cada recurso antes de oferecer integração.

## Separação recomendada

```text
WMK Craft Studio
  ├── Núcleo local: projetos, briefs, testes e relatórios
  ├── Editor/modelos independentes (futuro)
  ├── Adaptador opcional: Craft Anything, somente construção de código autoral (futuro)
  └── Adaptador opcional: FreeLLMAPI (HTTP loopback, futuro)
        └── Provedores escolhidos pelo usuário (remotos ou endpoints próprios)
```

**Não incluir** REA nem serviços de engenharia reversa no WMK.

## GitHub Actions do fork FreeLLMAPI

No fork existem `.github/workflows/ci.yml` e `.github/workflows/desktop-release.yml`. O CI testa e compila o monorepo em Node 20/22/24, e o workflow desktop possui alvo Windows 2022 porque o módulo nativo `better-sqlite3` exige uma configuração de compilação compatível.

A existência do workflow **não comprova** que ele já executou com êxito no fork. Para redistribuir, revisar segredos de assinatura, marcas, atualizador e destinos de publicação do projeto original.

## Referências

- [README FreeLLMAPI](https://github.com/WalneyNF/freellmapi/blob/main/README.md)
- [API REST FreeLLMAPI](https://github.com/WalneyNF/freellmapi/blob/main/docs/en/api/01-rest-api.md)
- [Política de segurança](https://github.com/WalneyNF/freellmapi/blob/main/SECURITY.md)
- [CI](https://github.com/WalneyNF/freellmapi/blob/main/.github/workflows/ci.yml)
- [Release desktop](https://github.com/WalneyNF/freellmapi/blob/main/.github/workflows/desktop-release.yml)
- [Política de originalidade WMK](POLITICA_DE_ORIGINALIDADE.md)

**Créditos WMK:** Walney Moreira Klein — walneyk@hotmail.com
