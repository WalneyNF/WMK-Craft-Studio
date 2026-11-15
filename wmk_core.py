"""Modelo de projetos do WMK Craft Studio — sem dependências externas."""
from __future__ import annotations

import json
import os
import re
import tempfile
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = 1
PROJECT_FILE = "wmk_project.json"
PROJECT_TYPES = ("livre", "web", "desktop", "jogo")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def slugify(name: str) -> str:
    if not isinstance(name, str) or not name.strip() or len(name.strip()) > 120:
        raise ValueError("Informe um nome entre 1 e 120 caracteres.")
    normalized = unicodedata.normalize("NFKD", name.strip())
    ascii_name = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")
    if not slug or slug in {".", ".."}:
        raise ValueError("O nome precisa conter letras ou números.")
    return slug[:80].rstrip("-")


def default_projects_dir() -> Path:
    home = Path.home()
    documents = home / "Documents"
    return (documents if documents.exists() else home) / "WMK-Craft-Studio" / "Projetos"


def atomic_write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".wmk-", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


class ProjectManager:
    def __init__(self, root: str | Path | None = None):
        self.root = Path(root) if root else default_projects_dir()
        self.root.mkdir(parents=True, exist_ok=True)
        self.root = self.root.resolve()

    def _safe_directory(self, slug: str) -> Path:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
            raise ValueError("Identificador de projeto inválido.")
        directory = (self.root / slug).resolve()
        if directory.parent != self.root:
            raise ValueError("Caminho de projeto fora da pasta autorizada.")
        return directory

    def create(self, name: str, kind: str = "livre", description: str = "") -> dict:
        slug = slugify(name)
        if kind not in PROJECT_TYPES:
            raise ValueError("Tipo de projeto inválido.")
        if len(description) > 10000:
            raise ValueError("Descrição excede 10.000 caracteres.")
        directory = self._safe_directory(slug)
        directory.mkdir(parents=False, exist_ok=False)
        for subdir in ("arquivos", "logs", "relatorios"):
            (directory / subdir).mkdir()
        created = now_iso()
        project = {
            "schema_version": SCHEMA_VERSION,
            "id": slug,
            "name": name.strip(),
            "kind": kind,
            "description": description,
            "status": "rascunho",
            "created_at": created,
            "updated_at": created,
            "tasks": [],
            "history": [{"at": created, "message": "Projeto criado."}],
        }
        atomic_write_json(directory / PROJECT_FILE, project)
        return project

    def load(self, slug: str) -> dict:
        path = self._safe_directory(slug) / PROJECT_FILE
        with path.open("r", encoding="utf-8") as handle:
            project = json.load(handle)
        if not isinstance(project, dict) or project.get("id") != slug:
            raise ValueError("Arquivo de projeto inválido ou incompatível.")
        if project.get("schema_version") != SCHEMA_VERSION:
            raise ValueError("Versão do projeto não suportada.")
        if not isinstance(project.get("tasks"), list) or not isinstance(project.get("history"), list):
            raise ValueError("Estrutura de projeto inválida.")
        return project

    def list_projects(self) -> list[dict]:
        projects = []
        for directory in self.root.iterdir():
            if not directory.is_dir() or directory.is_symlink():
                continue
            try:
                project = self.load(directory.name)
                projects.append(project)
            except (OSError, ValueError, json.JSONDecodeError):
                continue
        return sorted(projects, key=lambda p: p.get("updated_at", ""), reverse=True)

    def save(self, project: dict) -> None:
        slug = project.get("id")
        if not isinstance(slug, str):
            raise ValueError("Identificador ausente.")
        directory = self._safe_directory(slug)
        if not (directory / PROJECT_FILE).is_file():
            raise FileNotFoundError("Projeto não existe.")
        if project.get("schema_version") != SCHEMA_VERSION:
            raise ValueError("Versão incompatível.")
        project["updated_at"] = now_iso()
        atomic_write_json(directory / PROJECT_FILE, project)

    def add_task(self, project: dict, title: str) -> None:
        title = title.strip()
        if not 1 <= len(title) <= 200:
            raise ValueError("A tarefa precisa ter de 1 a 200 caracteres.")
        project["tasks"].append({"title": title, "done": False})
        self.log(project, f"Tarefa adicionada: {title}")

    def log(self, project: dict, message: str) -> None:
        if not isinstance(message, str) or not 1 <= len(message.strip()) <= 1000:
            raise ValueError("Registro inválido.")
        project["history"].append({"at": now_iso(), "message": message.strip()})
        self.save(project)

    def report_markdown(self, project: dict) -> str:
        lines = [
            f"# Relatório — {project['name']}",
            "",
            f"- Identificador: \`{project['id']}\`",
            f"- Tipo: {project['kind']}",
            f"- Situação: {project['status']}",
            f"- Atualizado em (UTC): {project['updated_at']}",
            "",
            "## Descrição",
            "",
            project.get("description", "") or "Sem descrição.",
            "",
            "## Tarefas",
            "",
        ]
        tasks = project.get("tasks", [])
        if not tasks:
            lines.append("Nenhuma tarefa cadastrada.")
        for task in tasks:
            checked = "x" if task.get("done") else " "
            lines.append(f"- [{checked}] {task.get('title', '')}")
        lines.extend(["", "## Histórico", ""])
        for event in project.get("history", []):
            lines.append(f"- {event.get('at', '')}: {event.get('message', '')}")
        lines.extend(["", "---", "Walney Moreira Klein — walneyk@hotmail.com", ""])
        return "\n".join(lines)

    def export_report(self, project: dict) -> Path:
        directory = self._safe_directory(project["id"]) / "relatorios"
        directory.mkdir(exist_ok=True)
        output = directory / "estado.md"
        output.write_text(self.report_markdown(project), encoding="utf-8")
        return output


def tool_status() -> dict[str, str | None]:
    """Descobre comandos instalados; não executa código externo."""
    from shutil import which
    return {
        "Craft Anything CLI": which("craft-anything-cli"),
        "REA": which("rea"),
        "Node.js": which("node"),
        "npx": which("npx"),
        "Git": which("git"),
    }
