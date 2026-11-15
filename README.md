# WMK Craft Studio

**Estude necessidades, avalie funcionalidades observáveis e desenvolva soluções alternativas originais.**

**Autoria:** Walney Moreira Klein — walneyk@hotmail.com  
**Situação:** protótipo desktop v0.1 em desenvolvimento, com compilação Windows x64 configurada no GitHub Actions (execução ainda precisa ser verificada).

> **Política de propriedade intelectual — essencial:** o WMK Craft Studio **NÃO é um clonador de programas**. Ele **não deve** copiar software de terceiros, reproduzir interfaces de maneira substancialmente idêntica, descompilar arquivos, extrair código, contornar proteções, usar marcas alheias para causar confusão, nem incorporar imagens/sons/documentação protegidos sem autorização. O propósito é criar **soluções próprias e independentes** a partir da identificação de necessidades e de funcionalidades observáveis lícitas.

## Para que serve?

O usuário descreve um problema, pode informar uma referência de produto que conhece, registra **apenas características observáveis e legítimas**, define melhorias e elabora um projeto **original**. Os próximos módulos ajudarão a implementar e testar essa proposta.

**Exemplo:**

- Referência conceitual: um sistema de estoque possui cadastro, filtros e relatórios.
- Necessidade: uma pequena empresa precisa organizar produtos sem depender de internet.
- Alternativa original: aplicativo WMK com SQLite, backup local, interface própria, cadastro e relatórios autorais.
- Não permitido: copiar código, ícones, textos, layout distintivo, banco de dados privado ou identidade comercial do software observado.

## O que existe na versão 0.1?

- Interface desktop em português e tema escuro, com divisor de painéis redimensionável.
- Projetos locais persistidos em JSON.
- Cadastro de tarefas e histórico.
- Anotações orientadas para estudo **funcional** e desenvolvimento de alternativas independentes.
- Exportação de relatório e proposta em Markdown.
- Verificação **passiva** de ferramentas instaladas, sem executar programas de terceiros.
- Testes automatizados do núcleo e workflow para empacotamento Windows x64.

**Ainda não existem:** análise automática de programas, leitura de screenshots por IA, geração autônoma de código/jogos, integração operacional com agentes ou testes visuais de software criado. O projeto não inspeciona executáveis e não realiza engenharia reversa.

## Primeiros passos

Com Python 3.12 ou mais recente e Tkinter disponível:

```powershell
python main.py
```

Testes locais, sem interface gráfica:

```powershell
python -m unittest discover -s tests -v
python main.py --self-test .\teste-wmk
```

O autoteste cria um projeto de exemplo na pasta informada. Utilize uma pasta vazia para cada execução.

No GitHub, acesse **Actions → WMK Craft Studio - Testes e Windows x64**. O workflow contém testes em Linux e Windows, compilação com PyInstaller e publicação de um ZIP como artefato. A compilação deve ser considerada validada somente após uma execução bem-sucedida.

## Como preservar a originalidade?

O fluxo obrigatório do produto será **referência permitida → necessidades → abstração de funcionalidades → proposta independente → implementação própria → testes → revisão de propriedade intelectual**.

1. Use descrições, observações de uso legítimo e materiais próprios ou licenciados. Não envie código confidencial, bases de dados privadas ou recursos de terceiros sem direitos.
2. Descreva **o que o usuário precisa realizar**, não como reproduzir uma tela ou componente exclusivo.
3. Faça novas decisões de arquitetura, layout, texto, identidade visual, imagens e implementação.
4. Preserve créditos e licenças quando houver dependências de código aberto.
5. Antes da publicação, revise a proveniência de conteúdos, dependências e eventuais riscos de confundibilidade comercial. Nenhum relatório automatizado garante ausência de infração.

### Legislação brasileira relevante

**Lei nº 9.609/1998 — Lei de Software:** o art. 2º disciplina a proteção de programas de computador. O art. 6º, III, contempla certas semelhanças decorrentes de características funcionais e exigências técnicas; **isso não é autorização geral para copiar código ou produtos**.  
Fonte oficial: https://www2.camara.leg.br/legin/fed/lei/1998/lei-9609-19-fevereiro-1998-364738-normaatualizada-pl.html

**Lei nº 9.610/1998 — Lei de Direitos Autorais:** o art. 8º, I, distingue ideias, métodos e conceitos enquanto tais de expressões protegidas; outras disposições podem proteger obras, textos, imagens, sons e elementos criativos concretos.  
Fonte oficial: https://www2.camara.leg.br/legin/fed/lei/1998/lei-9610-19-fevereiro-1998-365399-normaatualizada-pl.html

**Lei nº 9.279/1996 — Propriedade Industrial:** contém disposições sobre marcas e concorrência desleal, inclusive art. 195. Não reproduza identidade comercial de terceiros de forma que crie confusão sobre a origem do produto.  
Fonte oficial: https://www2.camara.leg.br/legin/fed/lei/1996/lei-9279-14-maio-1996-374644-normaatualizada-pl.html

**Nota:** esta é uma política de produto e uma orientação geral, não uma opinião jurídica ou garantia de legalidade. Em situações específicas, consulte orientação jurídica qualificada. O WMK adota restrições voluntárias mais rigorosas do que algumas exceções legais, inclusive **não oferecer engenharia reversa nem descompilação**.

Leia também [POLITICA_DE_ORIGINALIDADE.md](docs/POLITICA_DE_ORIGINALIDADE.md).

## Arquitetura e próximos passos

O [roadmap](docs/ROADMAP.md) descreve as etapas planejadas. O [manual](docs/MANUAL.md) explica o protótipo e a [arquitetura](docs/ARQUITETURA.md) identifica os módulos já existentes.

[Craft Anything](https://github.com/WalneyNF/craft-anything) poderá ser avaliado no futuro como executor de **novos projetos originais**, somente com operações compatíveis com esta política. **REA não integra o produto nem está no roadmap**: não haverá módulo de engenharia reversa.

Os códigos dos repositórios externos não são copiados para esta aplicação. Seus direitos, licenças, avisos e marcas permanecem com os titulares.

## Licença e autoria

Licença MIT para o código original deste repositório. Materiais de terceiros somente poderão ser incluídos conforme suas próprias licenças e autorizações.

**Walney Moreira Klein — walneyk@hotmail.com**
