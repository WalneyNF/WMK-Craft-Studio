"""Fábrica inicial de sites originais — templates locais, sem IA e sem dependências."""
from __future__ import annotations

import html
import io
import re
import zipfile
from pathlib import Path

from wmk_core import ProjectManager

COLORS = {
    "verde": "#16856a", "azul": "#2864c5", "roxo": "#7455bf",
    "laranja": "#d06a24", "rosa": "#bd417c", "vermelho": "#b23d48",
    "preto": "#27313f", "dourado": "#a6792a",
}
KINDS = {"institucional": "Site institucional", "vitrine": "Vitrine de produtos", "portfolio": "Portfólio"}
MAX_INPUT = 4000


def clean(value: str, limit: int = 160) -> str:
    if not isinstance(value, str):
        raise ValueError("Informe um texto válido.")
    value = re.sub(r"[\x00-\x1f\x7f]", " ", value).strip()
    if not value or len(value) > limit:
        raise ValueError(f"O texto precisa ter de 1 a {limit} caracteres.")
    return value


def escaped(value: str) -> str:
    return html.escape(str(value), quote=True)


class SiteFactory:
    """Gera sites a partir de conteúdos autorais; não lê nem reproduz sites externos."""

    def __init__(self, manager: ProjectManager):
        self.manager = manager

    def _folder(self, project: dict) -> Path:
        return self.manager._safe_directory(project["id"]) / "arquivos"

    def create(self, name: str, prompt: str, kind: str = "institucional", color: str = "verde") -> dict:
        name = clean(name, 100)
        if "/" in name or "\\" in name or ".." in name:
            raise ValueError("O nome não pode conter separadores de pasta ou dois pontos consecutivos.")
        prompt = clean(prompt, MAX_INPUT)
        if kind not in KINDS or color not in COLORS:
            raise ValueError("Selecione um modelo e uma cor válidos.")
        project = self.manager.create(name, "web", prompt)
        project["site_spec"] = {
            "kind": kind,
            "color": color,
            "title": name,
            "subtitle": prompt[:220],
            "sections": [],
            "cta": "Conheça nosso trabalho" if kind != "vitrine" else "Explorar catálogo",
        }
        self.manager.log(project, "Site inicial definido com template autoral; sem uso de IA.")
        self.generate(project)
        return project

    def generate(self, project: dict) -> None:
        spec = project.get("site_spec")
        if not isinstance(spec, dict):
            raise ValueError("Projeto não contém especificação de site.")
        if spec.get("kind") not in KINDS or spec.get("color") not in COLORS:
            raise ValueError("Modelo ou cor inválidos.")
        folder = self._folder(project)
        if folder.is_symlink() or folder.resolve().parent != self.manager._safe_directory(project["id"]):
            raise ValueError("Destino inválido.")
        folder.mkdir(parents=True, exist_ok=True)
        pages = {
            "index.html": self._html(project, spec),
            "style.css": self._css(spec),
            "script.js": self._js(),
            "LEIA-ME.txt": self._readme(project, spec),
        }
        for filename, contents in pages.items():
            path = folder / filename
            if path.is_symlink():
                raise ValueError("Arquivo de destino inválido.")
            path.write_text(contents, encoding="utf-8")
        self.manager.save(project)

    def _html(self, project: dict, spec: dict) -> str:
        name = escaped(spec["title"])
        subtitle = escaped(spec["subtitle"])
        cta = escaped(spec["cta"])
        label = KINDS[spec["kind"]]
        kind = spec["kind"]
        cards = {
            "institucional": [
                ("Atendimento", "Apresente aqui como você atende seus clientes."),
                ("Soluções", "Descreva os serviços que sua empresa realmente oferece."),
                ("Sobre nós", "Conte sua história com informações verdadeiras."),
            ],
            "vitrine": [
                ("Produto A", "Substitua por um produto real, sua imagem e preço."),
                ("Produto B", "Substitua por um produto real, sua imagem e preço."),
                ("Produto C", "Substitua por um produto real, sua imagem e preço."),
            ],
            "portfolio": [
                ("Projeto A", "Apresente um trabalho de sua autoria."),
                ("Projeto B", "Descreva o objetivo e o resultado real."),
                ("Projeto C", "Inclua uma captura de seu próprio projeto."),
            ],
        }[kind]
        card_markup = "\n".join(
            f'<article class="item"><span class="item-number">0{i}</span>'
            f'<h3>{escaped(title)}</h3><p>{escaped(desc)}</p></article>'
            for i, (title, desc) in enumerate(cards, 1)
        )
        extra = "\n".join(
            f'<section class="extra" id="extra-{i}"><div class="container">'
            f'<h2>{escaped(text)}</h2><p>Edite esta seção para acrescentar informações de sua autoria.</p>'
            f'</div></section>'
            for i, text in enumerate(spec.get("sections", [])[:5], 1)
        )
        return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escaped(spec['subtitle'][:150])}">
  <title>{name} — site original</title>
  <link rel="stylesheet" href="./style.css">
</head>
<body>
  <header class="site-header">
    <nav class="container" aria-label="Navegação principal">
      <a class="brand" href="#inicio">{name}</a>
      <div class="links"><a href="#sobre">Sobre</a><a href="#destaques">Destaques</a><a href="#contato">Contato</a></div>
    </nav>
  </header>
  <main id="inicio">
    <section class="hero">
      <div class="container hero-grid">
        <div><p class="eyebrow">{escaped(label)} · Criação independente</p>
        <h1>{name}<span class="accent">.</span></h1>
        <p class="lead">{subtitle}</p>
        <a class="button" href="#destaques">{cta}<span aria-hidden="true"> →</span></a></div>
        <div class="art" aria-hidden="true"><div class="art-circle"></div><div class="art-card one"></div><div class="art-card two"></div><div class="art-mark">W</div></div>
      </div>
    </section>
    <section class="section" id="sobre"><div class="container split">
      <p class="section-number">01 / Apresentação</p>
      <div><h2>Uma boa ideia merece uma apresentação própria.</h2>
      <p>Este texto é um modelo demonstrativo. Substitua-o por informações verdadeiras sobre seu negócio ou projeto.</p></div>
    </div></section>
    <section class="section alt" id="destaques"><div class="container">
      <p class="section-number">02 / {escaped(label)}</p>
      <h2>O que você pode apresentar</h2>
      <div class="cards">{card_markup}</div>
    </div></section>
    {extra}
    <section class="contact" id="contato"><div class="container contact-inner">
      <div><p class="eyebrow">03 / Próximo passo</p><h2>Conte a sua história.</h2>
      <p>Personalize os textos e acrescente um contato verdadeiro antes de publicar.</p></div>
      <a class="button light" href="#inicio">Voltar ao início ↑</a>
    </div></section>
  </main>
  <footer><div class="container footer-inner"><span>{name}</span>
  <span>Site de demonstração original gerado pelo WMK Craft Studio. Conteúdo ilustrativo.</span></div></footer>
  <script src="./script.js" defer></script>
</body>
</html>
"""

    def _css(self, spec: dict) -> str:
        accent = COLORS[spec["color"]]
        return f"""/* WMK Craft Studio — folha autoral. Edite livremente. */
:root {{ --ink:#13212b; --muted:#516372; --paper:#f7f9f8; --line:#dce5e5;
  --accent:{accent}; --deep:#122f39; --white:#fff; --radius:16px; }}
* {{ box-sizing:border-box }}
html {{ scroll-behavior:smooth }}
body {{ margin:0; background:var(--paper); color:var(--ink); font:16px/1.6 system-ui,Segoe UI,sans-serif }}
a {{ color:inherit; text-decoration:none }}
a:focus-visible,button:focus-visible {{ outline:3px solid var(--accent); outline-offset:4px }}
.container {{ width:min(1120px,calc(100% - 40px)); margin:auto }}
.site-header {{ position:sticky; top:0; z-index:5; background:#f7f9f8f0; backdrop-filter:blur(14px); border-bottom:1px solid var(--line) }}
nav {{ min-height:76px; display:flex; justify-content:space-between; align-items:center; gap:24px }}
.brand {{ font-weight:800; letter-spacing:-.04em; font-size:1.2rem }}
.links {{ display:flex; gap:26px; font-size:.9rem; color:var(--muted) }}
.links a:hover {{ color:var(--accent) }}
.hero {{ padding:95px 0 110px; overflow:hidden }}
.hero-grid {{ display:grid; grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr); gap:40px; align-items:center }}
.eyebrow,.section-number {{ font-size:.77rem; letter-spacing:.14em; text-transform:uppercase; font-weight:800; color:var(--accent) }}
h1 {{ font-size:clamp(3.2rem,7vw,6.4rem); line-height:1.04; letter-spacing:-.075em; margin:18px 0 25px; overflow-wrap:break-word }}
.accent {{ color:var(--accent) }}
.lead {{ max-width:52ch; color:var(--muted); font-size:1.16rem; margin-bottom:32px }}
.button {{ display:inline-flex; align-items:center; gap:12px; padding:15px 25px; border-radius:9px; background:var(--accent); color:white; font-weight:750; transition:transform .18s }}
.button:hover {{ transform:translateY(-2px) }}
.art {{ min-height:390px; border-radius:var(--radius); position:relative; background:linear-gradient(145deg,var(--deep),#1c5557); overflow:hidden; isolation:isolate }}
.art-circle {{ width:335px; height:335px; background:var(--accent); opacity:.6; border-radius:50%; position:absolute; top:-76px; right:-95px }}
.art-card {{ position:absolute; width:57%; height:39%; background:#ffffff1c; border:1px solid #ffffff4d; backdrop-filter:blur(10px); border-radius:20px; rotate:-12deg; left:12%; top:28% }}
.art-card.two {{ rotate:11deg; left:39%; top:42%; background:#ffffff30 }}
.art-mark {{ position:absolute; font-weight:900; font-size:12rem; color:#ffffffd8; bottom:-70px; left:12%; line-height:1 }}
.section {{ padding:105px 0; border-top:1px solid var(--line) }}
.section.alt {{ background:#eaf1ef }}
.split {{ display:grid; grid-template-columns:1fr 2fr; gap:50px }}
h2 {{ font-size:clamp(2rem,4vw,3.25rem); letter-spacing:-.055em; line-height:1.13; margin:8px 0 24px }}
.section p:not(.section-number),.contact p:not(.eyebrow),.item p {{ color:var(--muted) }}
.cards {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:18px; margin-top:42px }}
.item {{ min-height:230px; padding:30px; background:white; border:1px solid var(--line); border-radius:12px }}
.item-number {{ font-weight:800; color:var(--accent) }}
.item h3 {{ font-size:1.25rem; margin:35px 0 8px }}
.item p {{ margin:0; font-size:.93rem }}
.extra {{ padding:70px 0; border-top:1px solid var(--line) }}
.contact {{ background:var(--deep); color:white; padding:85px 0 }}
.contact-inner {{ display:flex; justify-content:space-between; align-items:center; gap:30px }}
.contact h2 {{ margin-bottom:12px }}
.contact p:not(.eyebrow) {{ color:#c7d9dc }}
.button.light {{ background:white; color:var(--deep); white-space:nowrap }}
footer {{ padding:26px 0; color:var(--muted); font-size:.78rem }}
.footer-inner {{ display:flex; justify-content:space-between; gap:18px }}
@media(max-width:760px) {{
 .links {{ gap:12px; font-size:.78rem }} nav {{ min-height:68px; }}
 .hero {{ padding:52px 0 70px }}
 .hero-grid,.split {{ grid-template-columns:1fr }}
 .art {{ min-height:250px }}
 .cards {{ grid-template-columns:1fr }}
 .section {{ padding:70px 0 }}
 .contact-inner,.footer-inner {{ flex-direction:column; align-items:flex-start }}
}}
@media(prefers-reduced-motion:reduce) {{
 html {{ scroll-behavior:auto }} .button {{ transition:none }}
}}
"""

    @staticmethod
    def _js() -> str:
        return '/* Site independente: navegação por âncoras funciona sem JavaScript. */\n'

    @staticmethod
    def _readme(project: dict, spec: dict) -> str:
        return (
            f"Projeto: {project['name']}\n"
            f"Tipo: {KINDS[spec['kind']]}\n\n"
            "Abra index.html em qualquer navegador atual.\n"
            "Edite os textos em index.html, cores e estilos em style.css.\n"
            "Este site é um modelo original; os produtos e textos são ilustrativos.\n"
            "Não há pagamentos, carrinho ou backend neste protótipo.\n\n"
            "Criado no WMK Craft Studio — Walney Moreira Klein — walneyk@hotmail.com\n"
        )

    def change(self, project: dict, instruction: str) -> str:
        instruction = clean(instruction, 500)
        if not isinstance(project.get("site_spec"), dict):
            raise ValueError("Projeto não é um site gerado pelo Studio.")
        spec = project["site_spec"]
        lowered = instruction.casefold()
        if any(term in lowered for term in ("cor", "tema", "paleta")):
            for name in COLORS:
                if re.search(r"\b" + name + r"\b", lowered):
                    spec["color"] = name
                    description = f"Cor principal alterada para {name}."
                    break
            else:
                raise ValueError("Cor não identificada. Opções: " + ", ".join(COLORS) + ".")
        elif (m := re.match(
            r"(?:mude|altere|troque|defina)\s+(?:o\s+)?(?:título|titulo|nome)\s+(?:para|por|como)\s+(.+)",
            instruction, flags=re.I,
        )):
            spec["title"] = clean(m.group(1), 100)
            description = "Título atualizado."
        elif (m := re.match(
            r"(?:mude|altere|troque|defina)\s+(?:o\s+)?(?:subtítulo|subtitulo|texto principal|descrição)\s+(?:para|por|como)\s+(.+)",
            instruction, flags=re.I,
        )):
            spec["subtitle"] = clean(m.group(1), 220)
            description = "Texto de apresentação atualizado."
        elif (m := re.match(
            r"(?:adicione|crie|inclua)\s+(?:uma\s+)?seção\s+(?:sobre|de|para)\s+(.+)",
            instruction, flags=re.I,
        )):
            if len(spec.get("sections", [])) >= 5:
                raise ValueError("O modelo inicial permite até cinco seções extras.")
            spec.setdefault("sections", []).append(clean(m.group(1), 80))
            description = "Nova seção adicionada."
        else:
            raise ValueError(
                "Ainda não compreendo pedidos livres. Experimente: "
                "'Mude a cor para azul', 'Altere o título para ...', "
                "'Mude o texto principal para ...' ou 'Adicione uma seção sobre ...'. "
                "Integração com IA ainda não implementada."
            )
        self.generate(project)
        self.manager.log(project, description)
        return description

    def zip_bytes(self, project: dict) -> bytes:
        folder = self._folder(project)
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for filename in ("index.html", "style.css", "script.js", "LEIA-ME.txt"):
                path = folder / filename
                if path.is_symlink() or not path.is_file():
                    raise ValueError("Arquivo inválido para exportação.")
                archive.write(path, arcname=filename)
        return buffer.getvalue()
