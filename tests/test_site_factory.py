"""Testes do primeiro Studio Web: resultado real, segurança e exportação."""
import io
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
import zipfile
from http.server import ThreadingHTTPServer
from pathlib import Path

from site_factory import SiteFactory
from studio_web import Handler, BASE
from wmk_core import ProjectManager


class SiteFactoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.manager = ProjectManager(self.tmp.name)
        self.factory = SiteFactory(self.manager)

    def test_real_files_and_reopening(self):
        project = self.factory.create("Flor do Vale", "Arranjos florais para ocasiões especiais.")
        slug = project["id"]
        folder = Path(self.tmp.name) / slug / "arquivos"
        for filename in ("index.html", "style.css", "script.js", "LEIA-ME.txt"):
            self.assertTrue((folder / filename).is_file())
        self.assertIn("Flor do Vale", (folder / "index.html").read_text(encoding="utf-8"))
        self.assertIn("#16856a", (folder / "style.css").read_text(encoding="utf-8"))
        reloaded = self.manager.load(slug)
        self.assertEqual(reloaded["site_spec"]["title"], "Flor do Vale")

    def test_html_is_escaped_no_code_injection(self):
        project = self.factory.create("Loja <script>alert(1)</script>", "Trabalho com <img src=x onerror=alert(1)>")
        page = (Path(self.tmp.name) / project["id"] / "arquivos" / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("<script>alert(1)</script>", page)
        self.assertNotIn("<img src=x", page)
        self.assertIn("&lt;script&gt;", page)
        self.assertIn("&lt;img", page)

    def test_changes_update_files_without_dropping_original(self):
        project = self.factory.create("Exemplo", "Apresentação inicial", "portfolio", "verde")
        self.assertEqual(self.factory.change(project, "Mude a cor para azul"), "Cor principal alterada para azul.")
        self.assertEqual(self.factory.change(project, "Altere o título para Novo Título"), "Título atualizado.")
        self.assertEqual(self.factory.change(project, "Adicione uma seção sobre Serviços"), "Nova seção adicionada.")
        folder = Path(self.tmp.name) / project["id"] / "arquivos"
        self.assertIn("#2864c5", (folder / "style.css").read_text(encoding="utf-8"))
        body = (folder / "index.html").read_text(encoding="utf-8")
        self.assertIn("Novo Título", body)
        self.assertIn("Serviços", body)
        self.assertEqual(self.manager.load(project["id"])["site_spec"]["kind"], "portfolio")

    def test_unsupported_request_does_not_fake_success(self):
        project = self.factory.create("Modelo", "Texto")
        before = dict(project["site_spec"])
        with self.assertRaisesRegex(ValueError, "não compreendo pedidos livres"):
            self.factory.change(project, "Adicione pagamento via cartão")
        self.assertEqual(project["site_spec"], before)

    def test_download_zip_contains_complete_site(self):
        project = self.factory.create("Meu trabalho", "Portfolio pessoal")
        stream = io.BytesIO(self.factory.zip_bytes(project))
        with zipfile.ZipFile(stream) as archive:
            self.assertEqual(
                set(archive.namelist()), {"index.html", "style.css", "script.js", "LEIA-ME.txt"},
            )
            self.assertIn("Meu trabalho", archive.read("index.html").decode())

    def test_validation(self):
        with self.assertRaises(ValueError):
            self.factory.create("teste", "", "institucional")
        with self.assertRaises(ValueError):
            self.factory.create("teste", "abc", "modelo-desconhecido")
        with self.assertRaises(ValueError):
            self.factory.create("teste", "abc", color="not-a-color")
        with self.assertRaises(ValueError):
            self.factory.create("../fora", "abc")
        self.assertEqual(self.manager.list_projects(), [])


class StudioWebApiTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.manager = ProjectManager(self.tmp.name)
        self.factory = SiteFactory(self.manager)
        handler = type("TestHandler", (Handler,), {"manager": self.manager, "factory": self.factory})
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.base = f"http://127.0.0.1:{self.server.server_port}"
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)

    def get(self, path):
        with urllib.request.urlopen(self.base + path, timeout=5) as response:
            return response.status, response.read(), response.headers

    def post(self, path, data, headers=None):
        payload = json.dumps(data).encode()
        hdr = {"Content-Type": "application/json", "X-WMK-Request": "1", "Origin": self.base}
        if headers:
            hdr.update(headers)
        request = urllib.request.Request(self.base + path, data=payload, headers=hdr, method="POST")
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status, json.load(response)

    def test_first_site_end_to_end(self):
        status, data, _ = self.get("/api/health")
        self.assertEqual(status, 200)
        self.assertFalse(json.loads(data)["ai"])
        status, body = self.post("/api/projects", {
            "name": "Clube da Leitura", "prompt": "Livros e encontros semanais",
            "kind": "institucional", "color": "verde"
        })
        self.assertEqual(status, 201)
        slug = body["project"]["id"]
        status, content, headers = self.get(f"/preview/{slug}/index.html")
        self.assertEqual(status, 200)
        self.assertIn("Clube da Leitura", content.decode())
        self.assertIn("Content-Security-Policy", headers)
        status, update = self.post(f"/api/projects/{slug}/change", {"message": "Mude a cor para roxo"})
        self.assertEqual(status, 200)
        self.assertIn("roxo", update["message"])
        _, css, _ = self.get(f"/preview/{slug}/style.css")
        self.assertIn("#7455bf", css.decode())
        status, zipped, _ = self.get(f"/api/projects/{slug}/download")
        self.assertEqual(status, 200)
        with zipfile.ZipFile(io.BytesIO(zipped)) as archive:
            self.assertTrue(archive.testzip() is None)
        _, all_items, _ = self.get("/api/projects")
        self.assertEqual(len(json.loads(all_items)["projects"]), 1)

    def test_reject_cross_origin_and_missing_csrf_header(self):
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            self.post("/api/projects", {"name": "x", "prompt": "y"}, {"Origin": "https://evil.example"})
        self.assertEqual(ctx.exception.code, 403)
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            self.post("/api/projects", {"name": "x", "prompt": "y"}, {"X-WMK-Request": "0"})
        self.assertEqual(ctx.exception.code, 403)

    def test_no_path_traversal_in_preview(self):
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            self.get("/preview/../site_factory.py")
        self.assertEqual(ctx.exception.code, 404)

    def test_static_frontend_is_served(self):
        for path in ("/", "/style.css", "/app.js"):
            status, body, _ = self.get(path)
            self.assertEqual(status, 200)
            self.assertTrue(body)


if __name__ == "__main__":
    unittest.main()
