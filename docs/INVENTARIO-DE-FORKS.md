# Inventário de forks e candidatos — WMK Craft Studio

**Inventário realizado em:** 15/11/2026  
**Origem:** repositórios autorizados na instalação GitHub da conta WalneyNF.  
**Total:** 180 repositórios identificados, 179 públicos; 1 não público(s) **não listado(s) neste documento público**.

## Transparência do levantamento

O inventário consultou o catálogo de repositórios autorizados. Uma seleção de candidatos foi analisada por README, estrutura de arquivos, manifests, scripts de execução, licenças e configurações de build. **Isto não equivale a uma auditoria integral de todos os 180 códigos-fonte**, nem garante funcionamento no Windows ou integração pronta.

Para os demais, apenas o **nome** foi registrado. A classificação temática de candidatos é uma hipótese para orientar investigação, não prova de capacidades.

## A decisão de produto

O WMK Craft Studio terá **usuário iniciante como público principal**, com experiência parecida *em conceito* com o AI Studio Apps: **descrever → gerar projeto original → visualizar execução real → pedir mudança → testar → exportar**.

Não será um clonador de softwares nem usará engenharia reversa. [Especificação do uso sem código](EXPERIENCIA-SEM-CODIGO.md) · [Visão técnica](VISAO-APP-BUILDER.md) · [Política de originalidade](POLITICA_DE_ORIGINALIDADE.md).

## Matriz de escolhas iniciais (sujeita a POC)

| Necessidade | Prioridade | Repositórios | Motivo e ressalva |
| --- | --- | --- | --- |
| Gerador de apps web e fluxo de chat | Alta | [bolt.diy](https://github.com/WalneyNF/bolt.diy) | Possui agente web e fluxo de projeto; depende de infraestrutura Remix/Cloudflare/WebContainers, testar adaptação |
| Acesso a múltiplos modelos | Alta | [freellmapi](https://github.com/WalneyNF/freellmapi) | API compatível com OpenAI; depende da configuração e cota dos provedores |
| Editor de código para modo avançado | Alta | [monaco-editor](https://github.com/WalneyNF/monaco-editor) | Editor embutível; precisa ser conectado ao projeto e ao filesystem |
| Interface por blocos | Alta, após MVP | [blockly](https://github.com/WalneyNF/blockly) | Biblioteca com geradores de código; construir nossa semântica de eventos |
| Templates de jogos 2D | Alta, após MVP web | [WMK-Game-Studio](https://github.com/WalneyNF/WMK-Game-Studio), [ct-js](https://github.com/WalneyNF/ct-js) | Plataformas completas; tratar como **alternativas**, não fundir motores |
| Visual de sites | Média | [hallmark](https://github.com/WalneyNF/hallmark), [taste-skill](https://github.com/WalneyNF/taste-skill) | Escolher uma estratégia de geração por projeto |
| Auditoria independente de interface | Alta | [impeccable](https://github.com/WalneyNF/impeccable) | Regras de qualidade; não ativar modo Live com permissões ampliadas |
| Editor de páginas | Média | [grapesjs](https://github.com/WalneyNF/grapesjs) | Editor HTML visual; exige POC de edição/round-trip de código gerado |
| Desenho de aplicativos | Média | [WMK-App-Builder](https://github.com/WalneyNF/WMK-App-Builder), [WMK-Studio](https://github.com/WalneyNF/WMK-Studio) | Úteis para protótipos; não implementam sozinhos backend |
| Fases de jogos 2D | Média | [ldtk](https://github.com/WalneyNF/ldtk) | Editor de níveis em formato estruturado; integrar depois |
| Gestão empresarial interna | Alternativa | [appsmith](https://github.com/WalneyNF/appsmith), [baserow](https://github.com/WalneyNF/baserow) | Produtos completos e pesados; preferir integração opcional, respeitar componentes/licenças especiais |
| Automações | Restrita | [n8n](https://github.com/WalneyNF/n8n) | Licença Sustainable Use License restritiva; não incorporar livremente em produto WMK |
| Engenharia reversa | **Excluída** | REA e rotinas equivalentes | Fora do produto por orientação expressa do proprietário |

## Catálogo público autorizado

Os nomes abaixo são listados para futura triagem; **não** significam que o software tenha sido executado ou aprovado.

### Construtores de software, editores e integração — 16 candidatos

- [bolt.diy](https://github.com/WalneyNF/bolt.diy)
- [craft-anything](https://github.com/WalneyNF/craft-anything)
- [WMK-App-Builder](https://github.com/WalneyNF/WMK-App-Builder)
- [WMK-Studio](https://github.com/WalneyNF/WMK-Studio)
- [WMK-Game-Studio](https://github.com/WalneyNF/WMK-Game-Studio)
- [magic](https://github.com/WalneyNF/magic)
- [grapesjs](https://github.com/WalneyNF/grapesjs)
- [monaco-editor](https://github.com/WalneyNF/monaco-editor)
- [blockly](https://github.com/WalneyNF/blockly)
- [scratch-blocks](https://github.com/WalneyNF/scratch-blocks)
- [appsmith](https://github.com/WalneyNF/appsmith)
- [baserow](https://github.com/WalneyNF/baserow)
- [microstudio](https://github.com/WalneyNF/microstudio)
- [ct-js](https://github.com/WalneyNF/ct-js)
- [PhaserEditor2D-v3](https://github.com/WalneyNF/PhaserEditor2D-v3)
- [ldtk](https://github.com/WalneyNF/ldtk)

### IA, agentes e provedores — 15 candidatos

- [freellmapi](https://github.com/WalneyNF/freellmapi)
- [OmniRoute](https://github.com/WalneyNF/OmniRoute)
- [ollama](https://github.com/WalneyNF/ollama)
- [crewAI](https://github.com/WalneyNF/crewAI)
- [langflow](https://github.com/WalneyNF/langflow)
- [n8n](https://github.com/WalneyNF/n8n)
- [Claude-Code-Game-Studios](https://github.com/WalneyNF/Claude-Code-Game-Studios)
- [openclaw](https://github.com/WalneyNF/openclaw)
- [DeepSeek-Coder](https://github.com/WalneyNF/DeepSeek-Coder)
- [DeepSeek-V3](https://github.com/WalneyNF/DeepSeek-V3)
- [Qwen](https://github.com/WalneyNF/Qwen)
- [comfy-mcp](https://github.com/WalneyNF/comfy-mcp)
- [ComfyUI](https://github.com/WalneyNF/ComfyUI)
- [mem0](https://github.com/WalneyNF/mem0)
- [CodeProject.AI-Server](https://github.com/WalneyNF/CodeProject.AI-Server)

### Design, experiência e testes de interface — 8 candidatos

- [hallmark](https://github.com/WalneyNF/hallmark)
- [impeccable](https://github.com/WalneyNF/impeccable)
- [taste-skill](https://github.com/WalneyNF/taste-skill)
- [WMK-Formula](https://github.com/WalneyNF/WMK-Formula)
- [WMK-Document-AI-Studio](https://github.com/WalneyNF/WMK-Document-AI-Studio)
- [WMK-VISION-STUDIO](https://github.com/WalneyNF/WMK-VISION-STUDIO)
- [WMK-RETRO-STUDIO](https://github.com/WalneyNF/WMK-RETRO-STUDIO)
- [WMK-Mesh-Avatar-Studio](https://github.com/WalneyNF/WMK-Mesh-Avatar-Studio)

### Motores, ferramentas e exemplos de jogos — 18 candidatos

- [godot](https://github.com/WalneyNF/godot)
- [GodotJS](https://github.com/WalneyNF/GodotJS)
- [defold](https://github.com/WalneyNF/defold)
- [box2d](https://github.com/WalneyNF/box2d)
- [flame](https://github.com/WalneyNF/flame)
- [love](https://github.com/WalneyNF/love)
- [rpg-phaser](https://github.com/WalneyNF/rpg-phaser)
- [libgdx](https://github.com/WalneyNF/libgdx)
- [jmonkeyengine](https://github.com/WalneyNF/jmonkeyengine)
- [duality](https://github.com/WalneyNF/duality)
- [stride](https://github.com/WalneyNF/stride)
- [openbor](https://github.com/WalneyNF/openbor)
- [rpgboss](https://github.com/WalneyNF/rpgboss)
- [arcadeGameGodotFree](https://github.com/WalneyNF/arcadeGameGodotFree)
- [flappy-bird](https://github.com/WalneyNF/flappy-bird)
- [WMK-Fabrica-Doces](https://github.com/WalneyNF/WMK-Fabrica-Doces)
- [WMK-Fabrica-Brinquedos](https://github.com/WalneyNF/WMK-Fabrica-Brinquedos)
- [WMK-Mystic-Oracle](https://github.com/WalneyNF/WMK-Mystic-Oracle)

### Projetos empresariais e aplicações de dados — 12 candidatos

- [finapp](https://github.com/WalneyNF/finapp)
- [fincontrol](https://github.com/WalneyNF/fincontrol)
- [financiamento](https://github.com/WalneyNF/financiamento)
- [erpintegrado](https://github.com/WalneyNF/erpintegrado)
- [cadastros](https://github.com/WalneyNF/cadastros)
- [controle-km](https://github.com/WalneyNF/controle-km)
- [CodeIgniter4](https://github.com/WalneyNF/CodeIgniter4)
- [gorestaurant](https://github.com/WalneyNF/gorestaurant)
- [confecflow](https://github.com/WalneyNF/confecflow)
- [fluxopro](https://github.com/WalneyNF/fluxopro)
- [banksim](https://github.com/WalneyNF/banksim)
- [WMK-Geo-Bridge](https://github.com/WalneyNF/WMK-Geo-Bridge)

### Outros repositórios — 110 aguardam análise temática

- [98](https://github.com/WalneyNF/98)
- [Alferd-Spritesheet-Unpacker](https://github.com/WalneyNF/Alferd-Spritesheet-Unpacker)
- [animais_drag](https://github.com/WalneyNF/animais_drag)
- [ansiedade](https://github.com/WalneyNF/ansiedade)
- [anysub](https://github.com/WalneyNF/anysub)
- [assets_bundle_cs2](https://github.com/WalneyNF/assets_bundle_cs2)
- [AthenaEnv](https://github.com/WalneyNF/AthenaEnv)
- [bonfire](https://github.com/WalneyNF/bonfire)
- [cadcraft](https://github.com/WalneyNF/cadcraft)
- [cicada](https://github.com/WalneyNF/cicada)
- [claudemy](https://github.com/WalneyNF/claudemy)
- [claw-code](https://github.com/WalneyNF/claw-code)
- [confecflow-web](https://github.com/WalneyNF/confecflow-web)
- [crystaldefense](https://github.com/WalneyNF/crystaldefense)
- [DagorEngine](https://github.com/WalneyNF/DagorEngine)
- [DeepTutor](https://github.com/WalneyNF/DeepTutor)
- [DragonBonesCSharp](https://github.com/WalneyNF/DragonBonesCSharp)
- [DragonBonesJS](https://github.com/WalneyNF/DragonBonesJS)
- [dsh-superagent-prototype](https://github.com/WalneyNF/dsh-superagent-prototype)
- [EasyOCR](https://github.com/WalneyNF/EasyOCR)
- [electron](https://github.com/WalneyNF/electron)
- [eleicoes2026](https://github.com/WalneyNF/eleicoes2026)
- [evolution-api](https://github.com/WalneyNF/evolution-api)
- [FNF-Godot-Engine](https://github.com/WalneyNF/FNF-Godot-Engine)
- [FNF-PsychEngine](https://github.com/WalneyNF/FNF-PsychEngine)
- [Funkin-Bot](https://github.com/WalneyNF/Funkin-Bot)
- [furnace](https://github.com/WalneyNF/furnace)
- [GASP-ALS](https://github.com/WalneyNF/GASP-ALS)
- [godot_bsp_importer](https://github.com/WalneyNF/godot_bsp_importer)
- [godot-friday-night-funkin-fnf](https://github.com/WalneyNF/godot-friday-night-funkin-fnf)
- [godot-simplified-flightsim](https://github.com/WalneyNF/godot-simplified-flightsim)
- [godot-tiled-importer](https://github.com/WalneyNF/godot-tiled-importer)
- [godot-wcode-plugin](https://github.com/WalneyNF/godot-wcode-plugin)
- [GodotTutorials](https://github.com/WalneyNF/GodotTutorials)
- [Grappling-Tutorial-GitHub](https://github.com/WalneyNF/Grappling-Tutorial-GitHub)
- [habblaud](https://github.com/WalneyNF/habblaud)
- [HuntTheAceJSGame](https://github.com/WalneyNF/HuntTheAceJSGame)
- [hyperframes](https://github.com/WalneyNF/hyperframes)
- [Ikemen-GO](https://github.com/WalneyNF/Ikemen-GO)
- [Ikemen-Plus-Ultra](https://github.com/WalneyNF/Ikemen-Plus-Ultra)
- [ingetrazo](https://github.com/WalneyNF/ingetrazo)
- [Inventory_slot](https://github.com/WalneyNF/Inventory_slot)
- [io_export_qmap](https://github.com/WalneyNF/io_export_qmap)
- [jogomemoriagodot](https://github.com/WalneyNF/jogomemoriagodot)
- [jsfxr](https://github.com/WalneyNF/jsfxr)
- [LDtkToUE5](https://github.com/WalneyNF/LDtkToUE5)
- [Lemon-Studio](https://github.com/WalneyNF/Lemon-Studio)
- [LivePortrait](https://github.com/WalneyNF/LivePortrait)
- [LTX-2](https://github.com/WalneyNF/LTX-2)
- [LTX-Video](https://github.com/WalneyNF/LTX-Video)
- [Montreal-Forced-Aligner](https://github.com/WalneyNF/Montreal-Forced-Aligner)
- [mugen](https://github.com/WalneyNF/mugen)
- [MuseTalk](https://github.com/WalneyNF/MuseTalk)
- [n8n_help](https://github.com/WalneyNF/n8n_help)
- [nibbler](https://github.com/WalneyNF/nibbler)
- [obeditor](https://github.com/WalneyNF/obeditor)
- [open-notebook](https://github.com/WalneyNF/open-notebook)
- [openbor-tools](https://github.com/WalneyNF/openbor-tools)
- [operation_lifeline](https://github.com/WalneyNF/operation_lifeline)
- [papagayo-ng](https://github.com/WalneyNF/papagayo-ng)
- [pcsx2](https://github.com/WalneyNF/pcsx2)
- [Plugin-creator-website](https://github.com/WalneyNF/Plugin-creator-website)
- [politica](https://github.com/WalneyNF/politica)
- [portulua](https://github.com/WalneyNF/portulua)
- [PowerShell](https://github.com/WalneyNF/PowerShell)
- [Qodot](https://github.com/WalneyNF/Qodot)
- [Qodot-Entity-Tutorial](https://github.com/WalneyNF/Qodot-Entity-Tutorial)
- [Quake](https://github.com/WalneyNF/Quake)
- [quakedev](https://github.com/WalneyNF/quakedev)
- [rea](https://github.com/WalneyNF/rea)
- [rhubarb-lip-sync](https://github.com/WalneyNF/rhubarb-lip-sync)
- [RMMV](https://github.com/WalneyNF/RMMV)
- [sabedoria](https://github.com/WalneyNF/sabedoria)
- [scrap](https://github.com/WalneyNF/scrap)
- [Seamly2D](https://github.com/WalneyNF/Seamly2D)
- [Simple-Java-Text-Editor](https://github.com/WalneyNF/Simple-Java-Text-Editor)
- [sped-da](https://github.com/WalneyNF/sped-da)
- [sped-esocial](https://github.com/WalneyNF/sped-esocial)
- [sped-nfe](https://github.com/WalneyNF/sped-nfe)
- [stable-diffusion-webui-forge](https://github.com/WalneyNF/stable-diffusion-webui-forge)
- [stickman-video-director](https://github.com/WalneyNF/stickman-video-director)
- [SurfSense](https://github.com/WalneyNF/SurfSense)
- [teardown](https://github.com/WalneyNF/teardown)
- [TP_2DSideScrollerBP](https://github.com/WalneyNF/TP_2DSideScrollerBP)
- [TrenchBroom](https://github.com/WalneyNF/TrenchBroom)
- [tyra](https://github.com/WalneyNF/tyra)
- [tyracraft](https://github.com/WalneyNF/tyracraft)
- [uno-online](https://github.com/WalneyNF/uno-online)
- [urnamaster](https://github.com/WalneyNF/urnamaster)
- [VBA-JSON](https://github.com/WalneyNF/VBA-JSON)
- [verbum](https://github.com/WalneyNF/verbum)
- [Visual-FoxPro-Toolkit-for-.NET](https://github.com/WalneyNF/Visual-FoxPro-Toolkit-for-.NET)
- [VoiceStudio](https://github.com/WalneyNF/VoiceStudio)
- [vscode-drawio](https://github.com/WalneyNF/vscode-drawio)
- [VYRO-Code-Studio](https://github.com/WalneyNF/VYRO-Code-Studio)
- [WebMCP](https://github.com/WalneyNF/WebMCP)
- [whac-a-mole](https://github.com/WalneyNF/whac-a-mole)
- [whisperX](https://github.com/WalneyNF/whisperX)
- [winXP](https://github.com/WalneyNF/winXP)
- [WMK-Avatar-AI](https://github.com/WalneyNF/WMK-Avatar-AI)
- [WMK-Blender-Code-Studio](https://github.com/WalneyNF/WMK-Blender-Code-Studio)
- [WMK-Craft-Studio](https://github.com/WalneyNF/WMK-Craft-Studio)
- [WMK-Geo-Intelligence](https://github.com/WalneyNF/WMK-Geo-Intelligence)
- [WMK-GPS-Tracker](https://github.com/WalneyNF/WMK-GPS-Tracker)
- [WMK-Screen-Studio](https://github.com/WalneyNF/WMK-Screen-Studio)
- [WMK-Subtitle-Studio](https://github.com/WalneyNF/WMK-Subtitle-Studio)
- [WMK-Video-Studio](https://github.com/WalneyNF/WMK-Video-Studio)
- [wmkPortugol](https://github.com/WalneyNF/wmkPortugol)
- [wordcraft](https://github.com/WalneyNF/wordcraft)
- [youtube-comment-downloader](https://github.com/WalneyNF/youtube-comment-downloader)

## Plano de avaliação de cada candidato

1. Confirmar finalidade técnica, documentação, dependências e licença efetiva dos módulos utilizados.
2. Executar teste de instalação, build e operação numa pasta isolada ou no GitHub Actions.
3. Confirmar API/CLI real e medir recursos necessários (CPU, memória, armazenamento).
4. Fazer POC que produza **um artefato editável e funcional**, sem promessas de geração irrestrita.
5. Verificar licenças de imagens, marcas, fontes, modelos, assets e componentes empresariais.
6. Integrar como **adaptador independente**; não copiar todos os arquivos para o projeto principal.
7. Registrar resultado com evidências e status: Aprovado, Bloqueado ou Pendente.

**Créditos:** Walney Moreira Klein — walneyk@hotmail.com
