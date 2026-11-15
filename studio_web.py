"""Servidor HTTP local do WMK Studio Web — sem dependências de terceiros.

Apenas 127.0.0.1; sem acesso remoto, autenticação pública ou publicação automática.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from site_factory import SiteFactory
from wmk_core import ProjectManager

BASE = Path(__file__).resolve().parent / "studio"
SAFE_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
PREVIEW = re.compile(r"/preview/([a-z0-9]+(?:-[a-z0-9]+)*)/(index\.html|style\.css|script\.js)\Z")
PROJECT_API = re.compile(r"/api/projects/([a-z0-9]+(?:-[a-z0-9]+)*)(?:/(change|download))?\Z")
STATIC = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/style.css": ("style.css", "text/css; charset=utf-8"),
    "/app.js": ("app.js", "application/javascript; charset=utf-8"),
}
MIME = {
    "index.html": "text/html; charset=utf-8",
    "style.css": "text/css; charset=utf-8",
    "script.js": "application/javascript; charset=utf-8",
}


class Handler(BaseHTTPRequestHandler):
    manager: ProjectManager
    factory: SiteFactory

    def _common_headers(self, mime: str, length: int, preview: bool = False) -> None:
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(length))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        if preview:
            self.send_header(
                "Content-Security-Policy",
                "default-src 'none'; style-src 'self'; script-src 'self'; "
                "img-src 'self' data:; font-src 'self'; base-uri 'none'; form-action 'none'",
            )
        elif mime.startswith("text/html"):
            self.send_header(
                "Content-Security-Policy",
                "default-src 'none'; script-src 'self'; style-src 'self'; "
                "img-src 'self' data:; font-src 'self'; connect-src 'self'; "
                "frame-src 'self'; base-uri 'none'; form-action 'none'",
            )

    def _write(self, content: bytes, mime: str, status: int = 200, preview: bool = False) -> None:
        self.send_response(status)
        self._common_headers(mime, len(content), preview)
        self.end_headers()
        self.wfile.write(content)

    def _json(self, obj: object, status: int = 200) -> None:
        data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self._write(data, "application/json; charset=utf-8", status)

    def _error(self, status: int, reason: str) -> None:
        self._json({"error": reason}, status)

    @staticmethod
    def _summary(project: dict) -> dict:
        spec = project.get("site_spec") or {}
        return {
            "id": project["id"], "name": project["name"],
            "description": project.get("description", ""),
            "kind": project.get("kind", ""),
            "spec": spec,
            "updated_at": project.get("updated_at", ""),
            "history": project.get("history", [])[-30:],
        }

    def do_GET(self) -> None:
        path = urlsplit(self.path).path
        if path in STATIC:
            filename, mime = STATIC[path]
            try:
                self._write((BASE / filename).read_bytes(), mime)
            except FileNotFoundError:
                self._error(404, "Arquivo da interface não encontrado.")
            return
        if path == "/api/health":
            self._json({"status": "ok", "mode": "local-template", "ai": False})
            return
        if path == "/api/projects":
            self._json({"projects": [
                self._summary(p) for p in self.manager.list_projects()
                if isinstance(p.get("site_spec"), dict)
            ]})
            return
        if match := PREVIEW.fullmatch(path):
            slug, filename = match.groups()
            try:
                folder = self.manager._safe_directory(slug) / "arquivos"
                full = folder / filename
                if full.is_symlink() or full.resolve().parent != folder.resolve() or not full.is_file():
                    self._error(404, "Prévia indisponível.")
                    return
                self._write(full.read_bytes(), MIME[filename], preview=True)
            except (ValueError, OSError):
                self._error(404, "Prévia indisponível.")
            return
        if match := PROJECT_API.fullmatch(path):
            slug, action = match.groups()
            try:
                project = self.manager.load(slug)
                if not isinstance(project.get("site_spec"), dict):
                    raise FileNotFoundError()
                if action == "download":
                    payload = self.factory.zip_bytes(project)
                    self.send_response(200)
                    self._common_headers("application/zip", len(payload))
                    self.send_header("Content-Disposition", f'attachment; filename="{slug}.zip"')
                    self.end_headers()
                    self.wfile.write(payload)
                elif action is None:
                    self._json({"project": self._summary(project)})
                else:
                    self._error(404, "Rota não encontrada.")
            except (ValueError, FileNotFoundError, OSError, json.JSONDecodeError):
                self._error(404, "Projeto não encontrado.")
            return
        self._error(404, "Rota não encontrada.")

    def _read_json(self) -> dict:
        if self.headers.get("X-WMK-Request") != "1":
            raise PermissionError("Requisição não autorizada.")
        origin = self.headers.get("Origin", "")
        host = self.headers.get("Host", "")
        expected = f"http://{host}"
        if origin and origin != expected:
            raise PermissionError("Origem não autorizada.")
        if not re.fullmatch(r"(?:127\.0\.0\.1|localhost):\d{1,5}", host):
            raise PermissionError("Host não autorizado.")
        if self.headers.get("Content-Type", "").split(";")[0].strip() != "application/json":
            raise ValueError("Envie um JSON válido.")
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            raise ValueError("Tamanho inválido.") from None
        if not 1 <= length <= 10000:
            raise ValueError("A requisição excede o limite.")
        value = json.loads(self.rfile.read(length))
        if not isinstance(value, dict):
            raise ValueError("O conteúdo precisa ser um objeto JSON.")
        return value

    def do_POST(self) -> None:
        path = urlsplit(self.path).path
        try:
            body = self._read_json()
            if path == "/api/projects":
                project = self.factory.create(
                    body.get("name", ""), body.get("prompt", ""),
                    body.get("kind", "institucional"), body.get("color", "verde"),
                )
                self._json({"project": self._summary(project)}, HTTPStatus.CREATED)
                return
            if (match := PROJECT_API.fullmatch(path)) and match.group(2) == "change":
                project = self.manager.load(match.group(1))
                description = self.factory.change(project, body.get("message", ""))
                self._json({"message": description, "project": self._summary(project)})
                return
            self._error(404, "Rota não encontrada.")
        except PermissionError as exc:
            self._error(403, str(exc))
        except FileExistsError:
            self._error(409, "Já existe um projeto com esse nome. Escolha outro.")
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            self._error(400, str(exc))
        except (OSError, FileNotFoundError):
            self._error(500, "Falha ao gravar o projeto. Consulte os logs.")

    def log_message(self, format: str, *args: object) -> None:
        # Evita registrar prompts, tokens ou dados de projeto em logs HTTP.
        if os.environ.get("WMK_HTTP_DEBUG") == "1":
            super().log_message(format, *args)


def serve(port: int = 8765, root: str | None = None, launch: bool = False) -> None:
    manager = ProjectManager(root)
    factory = SiteFactory(manager)
    handler = type("LocalStudioHandler", (Handler,), {"manager": manager, "factory": factory})
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    address = f"http://127.0.0.1:{server.server_port}"
    print(f"WMK Craft Studio Web: {address}")
    print(f"Projetos: {manager.root}")
    print("Ctrl+C para encerrar. Modo inicial: templates locais, SEM geração por IA.")
    if launch:
        webbrowser.open(address)
    try:
        server.serve_forever(poll_interval=0.2)
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        server.server_close()


def self_test() -> int:
    """Exercita também o executável empacotado sem abrir browser ou porta."""
    try:
        with tempfile.TemporaryDirectory(prefix="wmk-web-smoke-") as directory:
            manager = ProjectManager(directory)
            factory = SiteFactory(manager)
            project = factory.create("Verificação Web", "Site de demonstração original.")
            factory.change(project, "Mude a cor para azul")
            folder = manager._safe_directory(project["id"]) / "arquivos"
            if "#2864c5" not in (folder / "style.css").read_text(encoding="utf-8"):
                return 1
            if not factory.zip_bytes(project):
                return 1
            if not (BASE / "index.html").is_file():
                return 1
        print("WMK Studio Web: autoteste aprovado.")
        return 0
    except Exception as exc:
        print(f"WMK Studio Web: falha no autoteste: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WMK Craft Studio: protótipo web local sem código")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--root", default=os.environ.get("WMK_PROJECTS_DIR"))
    parser.add_argument("--open", action="store_true")
    parser.add_argument("--self-test", action="store_true", help="Testa site e pacote sem abrir interface")
    args = parser.parse_args()
    if args.self_test:
        raise SystemExit(self_test())
    serve(args.port, args.root, args.open or bool(getattr(sys, "frozen", False)))
