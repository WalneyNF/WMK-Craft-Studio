"""Verificações do armazenamento e dos relatórios do WMK Craft Studio."""
import json
import tempfile
import unittest
from pathlib import Path

from wmk_core import PROJECT_FILE, ProjectManager, slugify


class ProjectManagerTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.manager = ProjectManager(self.directory.name)

    def test_create_persist_and_reopen(self):
        project = self.manager.create("Minha Aplicação", "desktop", "Cadastro")
        self.assertEqual(project["id"], "minha-aplicacao")
        self.assertTrue((Path(self.directory.name) / project["id"] / PROJECT_FILE).exists())
        self.assertEqual(self.manager.load(project["id"])["description"], "Cadastro")
        self.assertEqual(len(self.manager.list_projects()), 1)

    def test_reject_duplicate_names(self):
        self.manager.create("Minha ferramenta")
        with self.assertRaises(FileExistsError):
            self.manager.create("Minha ferramenta!")

    def test_reject_invalid_path(self):
        for slug in ("../../etc", "..", "/tmp/other", "a/b", "a\\b"):
            with self.subTest(slug=slug), self.assertRaises(ValueError):
                self.manager.load(slug)

    def test_reject_empty_name_and_unknown_type(self):
        with self.assertRaises(ValueError):
            self.manager.create("    ")
        with self.assertRaises(ValueError):
            self.manager.create("Sistema", "arquivo-inexistente")

    def test_tasks_and_report(self):
        project = self.manager.create("Controle de estoque", "desktop")
        self.manager.add_task(project, "Cadastrar produto")
        project["tasks"][0]["done"] = True
        self.manager.log(project, "Teste de cadastro concluído")
        loaded = self.manager.load(project["id"])
        self.assertTrue(loaded["tasks"][0]["done"])
        report = self.manager.report_markdown(loaded)
        self.assertIn("- [x] Cadastrar produto", report)
        self.assertIn("Teste de cadastro concluído", report)
        path = self.manager.export_report(loaded)
        self.assertTrue(path.is_file())
        self.assertEqual(path.read_text(encoding="utf-8"), report)

    def test_list_ignores_broken_manifest(self):
        broken = Path(self.directory.name) / "quebrado"
        broken.mkdir()
        (broken / PROJECT_FILE).write_text("{", encoding="utf-8")
        self.assertEqual(self.manager.list_projects(), [])

    def test_slug_accents(self):
        self.assertEqual(slugify("Gestão de Clientes 2026"), "gestao-de-clientes-2026")


if __name__ == "__main__":
    unittest.main()
