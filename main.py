"""Inicializador do WMK Craft Studio e teste de instalação sem interface gráfica."""
from __future__ import annotations

import sys
from pathlib import Path

from wmk_core import ProjectManager


def self_test(destination: str) -> int:
    """Exercita escrita, leitura e relatório; seguro para runners sem desktop."""
    try:
        manager = ProjectManager(Path(destination))
        project = manager.create("Teste de compilação", "desktop", "Validação do pacote Windows.")
        manager.add_task(project, "Abrir projeto salvo")
        loaded = manager.load(project["id"])
        report = manager.export_report(loaded)
        if loaded["tasks"][0]["title"] != "Abrir projeto salvo" or not report.is_file():
            raise RuntimeError("Verificação de persistência falhou.")
        return 0
    except Exception as exc:
        print(f"Falha no autoteste: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--self-test":
        raise SystemExit(self_test(sys.argv[2]))
    if len(sys.argv) > 1:
        print("Uso: WMK-Craft-Studio.exe [--self-test DIRETORIO]", file=sys.stderr)
        raise SystemExit(2)
    # Carrega Tkinter somente ao abrir a interface.
    from wmk_app import main
    main()
