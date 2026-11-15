"""Interface desktop inicial do WMK Craft Studio (Tkinter, pt-BR)."""
from __future__ import annotations

import json
import os
import sys
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText

from wmk_core import PROJECT_TYPES, ProjectManager, atomic_write_json, tool_status

BG = "#101820"
PANEL = "#182531"
SURFACE = "#223242"
TEXT = "#eff8fa"
MUTED = "#a3b5c2"
ACCENT = "#37d5aa"
REPO_URL = "https://github.com/WalneyNF/WMK-Craft-Studio"
CREDITS = "Walney Moreira Klein — walneyk@hotmail.com"


def settings_path() -> Path:
    folder = Path(os.environ.get("APPDATA", "")) if os.environ.get("APPDATA") else Path.home() / ".config"
    return folder / "WMK-Craft-Studio" / "settings.json"


class Studio(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WMK Craft Studio — Projetos")
        self.minsize(860, 570)
        self.configure(bg=BG)
        self.manager = ProjectManager()
        self.current = None
        self.visible_projects = []
        self.settings_file = settings_path()
        self.settings = self._load_settings()

        self._init_theme()
        self._build_layout()
        try:
            self.geometry(self.settings.get("geometry", "1180x740"))
        except tk.TclError:
            self.geometry("1180x740")
        self.after(150, self._restore_sash)
        self.refresh_projects(select=self.settings.get("last_project"))
        self.protocol("WM_DELETE_WINDOW", self._close)
        self.bind_all("<Control-s>", self._shortcut_save)
        self.bind_all("<Control-n>", self._shortcut_new)

    def _load_settings(self) -> dict:
        try:
            data = json.loads(self.settings_file.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except (OSError, ValueError):
            return {}

    def _init_theme(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(".", background=BG, foreground=TEXT, font=("Segoe UI", 10))
        style.configure("TFrame", background=BG)
        style.configure("TLabel", background=BG, foreground=TEXT)
        style.configure("Muted.TLabel", foreground=MUTED)
        style.configure("Title.TLabel", foreground=ACCENT, font=("Segoe UI Semibold", 19))
        style.configure("TButton", background=SURFACE, foreground=TEXT, padding=(12, 8))
        style.map("TButton", background=[("active", "#30506b")], foreground=[("disabled", MUTED)])
        style.configure("Accent.TButton", background=ACCENT, foreground=BG, padding=(13, 9))
        style.map("Accent.TButton", background=[("active", "#5ae8c1")])
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=PANEL, foreground=MUTED, padding=(14, 9))
        style.map("TNotebook.Tab", background=[("selected", SURFACE)], foreground=[("selected", TEXT)])
        style.configure("TCombobox", fieldbackground=SURFACE, foreground=TEXT)
        style.configure("TPanedwindow", background=BG)

    def _build_layout(self):
        header = ttk.Frame(self, padding=(18, 14))
        header.pack(fill="x")
        ttk.Label(header, text="WMK CRAFT STUDIO", style="Title.TLabel").pack(side="left")
        ttk.Button(header, text="Novo projeto", style="Accent.TButton", command=self.new_project).pack(side="right")
        ttk.Button(header, text="GitHub Actions", command=self.open_actions).pack(side="right", padx=(0, 10))

        self.panes = ttk.Panedwindow(self, orient="horizontal")
        self.panes.pack(expand=True, fill="both", padx=14, pady=(0, 9))
        left = ttk.Frame(self.panes, padding=12)
        right = ttk.Frame(self.panes, padding=8)
        self.panes.add(left, weight=1)
        self.panes.add(right, weight=4)

        ttk.Label(left, text="PROJETOS", font=("Segoe UI Semibold", 12)).pack(anchor="w", pady=(0, 7))
        self.search_var = tk.StringVar()
        search = tk.Entry(left, textvariable=self.search_var, bg=SURFACE, fg=TEXT,
                          insertbackground=TEXT, relief="flat", font=("Segoe UI", 10))
        search.pack(fill="x", ipady=8, pady=(0, 10))
        self.search_var.trace_add("write", lambda *_: self.refresh_projects())
        self.project_list = tk.Listbox(left, bg=PANEL, fg=TEXT, selectbackground="#22614f",
                                       selectforeground=TEXT, relief="flat", borderwidth=0,
                                       highlightthickness=0, activestyle="none",
                                       font=("Segoe UI", 10), exportselection=False)
        self.project_list.pack(fill="both", expand=True)
        self.project_list.bind("<<ListboxSelect>>", self._selection_changed)
        ttk.Button(left, text="Atualizar galeria", command=self.refresh_projects).pack(fill="x", pady=(10, 0))

        self.notebook = ttk.Notebook(right)
        self.notebook.pack(fill="both", expand=True)
        overview = ttk.Frame(self.notebook, padding=18)
        tasks = ttk.Frame(self.notebook, padding=18)
        study = ttk.Frame(self.notebook, padding=18)
        history = ttk.Frame(self.notebook, padding=18)
        tools = ttk.Frame(self.notebook, padding=18)
        self.notebook.add(overview, text="Visão geral")
        self.notebook.add(study, text="Estudo funcional")
        self.notebook.add(tasks, text="Tarefas")
        self.notebook.add(history, text="Histórico")
        self.notebook.add(tools, text="Ferramentas")
        self._overview_tab(overview)
        self._reference_tab(study)
        self._tasks_tab(tasks)
        self._history_tab(history)
        self._tools_tab(tools)

        footer = ttk.Frame(self, padding=(18, 0, 18, 12))
        footer.pack(fill="x")
        self.status_var = tk.StringVar(value="Pronto. Crie ou selecione um projeto.")
        ttk.Label(footer, textvariable=self.status_var, style="Muted.TLabel").pack(side="left")
        ttk.Label(footer, text=CREDITS, style="Muted.TLabel").pack(side="right")

    def _overview_tab(self, frame):
        self.project_heading = ttk.Label(frame, text="Selecione um projeto", style="Title.TLabel")
        self.project_heading.pack(anchor="w", pady=(0, 6))
        self.project_info = ttk.Label(frame, text="Projetos armazenados em JSON no seu computador.",
                                      style="Muted.TLabel")
        self.project_info.pack(anchor="w", pady=(0, 15))
        ttk.Label(frame, text="Descrição / objetivo do projeto").pack(anchor="w")
        self.description = tk.Text(frame, height=13, wrap="word", bg=PANEL, fg=TEXT,
                                   insertbackground=ACCENT, relief="flat", padx=12, pady=12,
                                   font=("Segoe UI", 11))
        self.description.pack(fill="both", expand=True, pady=(7, 14))
        buttons = ttk.Frame(frame)
        buttons.pack(fill="x")
        ttk.Button(buttons, text="Salvar projeto", style="Accent.TButton",
                   command=self.save_current).pack(side="left")
        ttk.Button(buttons, text="Exportar relatório MD",
                   command=self.export_report).pack(side="left", padx=9)
        ttk.Button(buttons, text="Abrir pasta", command=self.open_folder).pack(side="left")

    def _reference_tab(self, frame):
        ttk.Label(frame, text="CRIAR UMA ALTERNATIVA ORIGINAL",
                  font=("Segoe UI Semibold", 14)).pack(anchor="w")
        ttk.Label(
            frame,
            text=("Registre apenas funcionalidades observadas de modo legítimo. "
                  "Não copie código, telas, marcas, recursos protegidos ou arquivos de terceiros. "
                  "Este módulo registra suas observações; não examina executáveis."),
            style="Muted.TLabel", wraplength=710, justify="left"
        ).pack(anchor="w", pady=(7, 9))
        self.reference_inputs = {}
        fields = [
            ("reference_name", "Referência funcional (opcional)"),
            ("observed_features", "Quais funcionalidades você observou?"),
            ("user_needs", "Quais necessidades das pessoas deseja resolver?"),
            ("original_solution", "Como será a SUA solução, com design e código próprios?"),
            ("differentiators", "Quais melhorias e diferenciais pretende oferecer?"),
        ]
        for key, label in fields:
            ttk.Label(frame, text=label).pack(anchor="w", pady=(5, 2))
            if key == "reference_name":
                widget = tk.Entry(frame, bg=PANEL, fg=TEXT, insertbackground=TEXT,
                                  relief="flat", font=("Segoe UI", 10))
                widget.pack(fill="x", ipady=5)
            else:
                widget = tk.Text(frame, height=2, wrap="word", bg=PANEL, fg=TEXT,
                                  insertbackground=TEXT, relief="flat",
                                  padx=8, pady=5, font=("Segoe UI", 10))
                widget.pack(fill="x")
            self.reference_inputs[key] = widget
        buttons = ttk.Frame(frame)
        buttons.pack(fill="x", pady=(12, 0))
        ttk.Button(buttons, text="Salvar estudo", style="Accent.TButton",
                   command=self.save_current).pack(side="left")
        ttk.Button(buttons, text="Copiar proposta MD",
                   command=self.copy_reference_brief).pack(side="left", padx=(8, 0))
        ttk.Button(buttons, text="Salvar proposta MD",
                   command=self.export_reference_brief).pack(side="left", padx=(8, 0))

    def _tasks_tab(self, frame):
        ttk.Label(frame, text="TAREFAS DO PROJETO", font=("Segoe UI Semibold", 14)).pack(anchor="w")
        ttk.Label(frame, text="Marque etapas concluídas; todas as mudanças ficam no histórico.",
                  style="Muted.TLabel").pack(anchor="w", pady=(5, 12))
        self.task_list = tk.Listbox(frame, bg=PANEL, fg=TEXT, selectbackground="#22614f",
                                    relief="flat", highlightthickness=0, font=("Segoe UI", 11))
        self.task_list.pack(expand=True, fill="both")
        input_row = ttk.Frame(frame)
        input_row.pack(fill="x", pady=(12, 8))
        self.task_entry = tk.Entry(input_row, bg=SURFACE, fg=TEXT, insertbackground=TEXT,
                                    relief="flat", font=("Segoe UI", 11))
        self.task_entry.pack(side="left", fill="x", expand=True, ipady=8)
        self.task_entry.bind("<Return>", lambda *_: self.add_task())
        ttk.Button(input_row, text="Adicionar", command=self.add_task).pack(side="right", padx=(8, 0))
        actions = ttk.Frame(frame)
        actions.pack(fill="x")
        ttk.Button(actions, text="Concluir / reabrir", command=self.toggle_task).pack(side="left")
        ttk.Button(actions, text="Excluir tarefa", command=self.delete_task).pack(side="left", padx=8)

    def _history_tab(self, frame):
        ttk.Label(frame, text="HISTÓRICO E EVIDÊNCIAS", font=("Segoe UI Semibold", 14)).pack(anchor="w")
        ttk.Label(frame, text="Registros da aplicação. Não representam testes autônomos de IA.",
                  style="Muted.TLabel").pack(anchor="w", pady=(5, 12))
        self.history_text = ScrolledText(frame, wrap="word", bg=PANEL, fg=TEXT,
                                         insertbackground=ACCENT, font=("Consolas", 10),
                                         relief="flat", state="disabled")
        self.history_text.pack(expand=True, fill="both")
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=(12, 0))
        ttk.Button(row, text="Copiar relatório MD", command=self.copy_report).pack(side="left")
        ttk.Button(row, text="Salvar relatório MD", command=self.export_report).pack(side="left", padx=8)

    def _tools_tab(self, frame):
        ttk.Label(frame, text="INTEGRAÇÕES EXTERNAS", font=("Segoe UI Semibold", 14)).pack(anchor="w")
        info = ("Esta versão identifica comandos no PATH, sem executá-los. "
                "O WMK não clona programas e não realiza engenharia reversa. "
                "A integração futura só poderá criar projetos originais, "
                "respeitando as licenças e a política de propriedade intelectual.")
        ttk.Label(frame, text=info, wraplength=710, justify="left",
                  style="Muted.TLabel").pack(anchor="w", pady=(8, 18))
        self.tool_text = ScrolledText(frame, height=11, wrap="word", bg=PANEL, fg=TEXT,
                                      font=("Consolas", 10), relief="flat", state="disabled")
        self.tool_text.pack(fill="both", expand=True)
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=(12, 0))
        ttk.Button(row, text="Verificar novamente", command=self.refresh_tools).pack(side="left")
        ttk.Button(row, text="Ver código no GitHub",
                   command=lambda: webbrowser.open(REPO_URL)).pack(side="left", padx=8)
        self.refresh_tools()

    def _set_readonly(self, widget, text: str):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget.configure(state="disabled")

    def _restore_sash(self):
        try:
            value = int(self.settings.get("sash", 270))
            self.panes.sashpos(0, min(max(value, 170), self.winfo_width() - 480))
        except (tk.TclError, ValueError, TypeError):
            pass

    def refresh_projects(self, select=None):
        term = self.search_var.get().casefold()
        self.visible_projects = [p for p in self.manager.list_projects()
                                 if term in p["name"].casefold()]
        self.project_list.delete(0, "end")
        for project in self.visible_projects:
            self.project_list.insert("end", project["name"])
        target = select or (self.current or {}).get("id")
        if target:
            for index, project in enumerate(self.visible_projects):
                if project["id"] == target:
                    self.project_list.selection_set(index)
                    self.project_list.activate(index)
                    self.project_list.see(index)
                    if self.current is None:
                        self._show_project(project)
                    break

    def _selection_changed(self, _event):
        selected = self.project_list.curselection()
        if not selected:
            return
        project = self.visible_projects[selected[0]]
        if self.current and project["id"] == self.current["id"]:
            return
        if self.current:
            self.save_current(silent=True)
        self._show_project(self.manager.load(project["id"]))

    def _show_project(self, project):
        self.current = project
        self.project_heading.configure(text=project["name"])
        self.project_info.configure(
            text=f"Tipo: {project['kind']}   •   Pasta: {self.manager.root / project['id']}")
        self.description.delete("1.0", "end")
        self.description.insert("1.0", project.get("description", ""))
        study = project.get("reference_study") or {}
        for key, widget in self.reference_inputs.items():
            widget.delete("1.0", "end") if isinstance(widget, tk.Text) else widget.delete(0, "end")
            if isinstance(widget, tk.Text):
                widget.insert("1.0", study.get(key, ""))
            else:
                widget.insert(0, study.get(key, ""))
        self._refresh_tasks()
        self._refresh_history()
        self.status_var.set(f"Projeto selecionado: {project['name']}")

    def new_project(self):
        dialog = tk.Toplevel(self)
        dialog.title("Novo projeto")
        dialog.configure(bg=BG)
        dialog.geometry("460x350")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        content = ttk.Frame(dialog, padding=22)
        content.pack(fill="both", expand=True)
        ttk.Label(content, text="Nome do projeto").pack(anchor="w")
        name = ttk.Entry(content)
        name.pack(fill="x", pady=(6, 15))
        ttk.Label(content, text="Tipo").pack(anchor="w")
        kind = ttk.Combobox(content, values=PROJECT_TYPES, state="readonly")
        kind.set("livre")
        kind.pack(fill="x", pady=(6, 15))
        ttk.Label(content, text="Descrição inicial").pack(anchor="w")
        desc = tk.Text(content, height=4, bg=PANEL, fg=TEXT, insertbackground=TEXT,
                       relief="flat", wrap="word")
        desc.pack(fill="x", pady=(6, 14))

        def create():
            try:
                project = self.manager.create(name.get(), kind.get(),
                                              desc.get("1.0", "end-1c"))
                dialog.destroy()
                self.search_var.set("")
                self.refresh_projects(select=project["id"])
                self._show_project(project)
            except (OSError, ValueError) as exc:
                messagebox.showerror("Não foi possível criar", str(exc), parent=dialog)
        ttk.Button(content, text="Criar projeto", style="Accent.TButton",
                   command=create).pack(anchor="e")
        name.focus_set()

    def save_current(self, silent=False):
        if not self.current:
            if not silent:
                messagebox.showinfo("Projeto", "Selecione um projeto primeiro.")
            return
        try:
            self.current["description"] = self.description.get("1.0", "end-1c")
            self.current["reference_study"] = {
                key: (widget.get("1.0", "end-1c") if isinstance(widget, tk.Text)
                      else widget.get())
                for key, widget in self.reference_inputs.items()
            }
            self.manager.save(self.current)
            self.status_var.set("Projeto salvo com sucesso.")
        except (OSError, ValueError) as exc:
            messagebox.showerror("Falha ao salvar", str(exc))

    def _refresh_tasks(self):
        self.task_list.delete(0, "end")
        if not self.current:
            return
        for task in self.current.get("tasks", []):
            marker = "☑" if task.get("done") else "☐"
            self.task_list.insert("end", f"{marker}  {task['title']}")

    def _refresh_history(self):
        events = (self.current or {}).get("history", [])
        text = "\n".join(f"[{event['at']}] {event['message']}" for event in events)
        self._set_readonly(self.history_text, text or "Nenhum registro.")

    def add_task(self):
        if not self.current:
            return
        try:
            self.manager.add_task(self.current, self.task_entry.get())
            self.task_entry.delete(0, "end")
            self._refresh_tasks()
            self._refresh_history()
        except ValueError as exc:
            messagebox.showwarning("Tarefa", str(exc))

    def _selected_task_index(self):
        chosen = self.task_list.curselection()
        return chosen[0] if chosen and self.current else None

    def toggle_task(self):
        index = self._selected_task_index()
        if index is None:
            return
        task = self.current["tasks"][index]
        task["done"] = not task["done"]
        self.manager.log(self.current, f"Tarefa {'concluída' if task['done'] else 'reaberta'}: {task['title']}")
        self._refresh_tasks()
        self.task_list.selection_set(index)
        self._refresh_history()

    def delete_task(self):
        index = self._selected_task_index()
        if index is None:
            return
        task = self.current["tasks"].pop(index)
        self.manager.log(self.current, f"Tarefa excluída: {task['title']}")
        self._refresh_tasks()
        self._refresh_history()

    def copy_report(self):
        if not self.current:
            return
        self.save_current(silent=True)
        self.clipboard_clear()
        self.clipboard_append(self.manager.report_markdown(self.current))
        self.status_var.set("Relatório Markdown copiado.")

    def export_report(self):
        if not self.current:
            messagebox.showinfo("Relatório", "Selecione um projeto primeiro.")
            return
        try:
            self.save_current(silent=True)
            file = self.manager.export_report(self.current)
            self.status_var.set(f"Relatório salvo em: {file}")
            messagebox.showinfo("Exportação concluída", f"Arquivo salvo:\n{file}")
        except (OSError, ValueError) as exc:
            messagebox.showerror("Erro na exportação", str(exc))

    def copy_reference_brief(self):
        if not self.current:
            messagebox.showinfo("Proposta", "Selecione um projeto primeiro.")
            return
        self.save_current(silent=True)
        self.clipboard_clear()
        self.clipboard_append(self.manager.reference_markdown(self.current))
        self.status_var.set("Brief de alternativa original copiado em Markdown.")

    def export_reference_brief(self):
        if not self.current:
            messagebox.showinfo("Proposta", "Selecione um projeto primeiro.")
            return
        try:
            self.save_current(silent=True)
            file = self.manager.export_reference_brief(self.current)
            self.status_var.set(f"Proposta original salva em: {file}")
            messagebox.showinfo("Exportação concluída", f"Arquivo salvo:\n{file}")
        except (OSError, ValueError) as exc:
            messagebox.showerror("Erro na exportação", str(exc))

    def open_folder(self):
        if not self.current:
            return
        location = self.manager.root / self.current["id"]
        webbrowser.open(location.as_uri())

    def open_actions(self):
        webbrowser.open(REPO_URL + "/actions")

    def refresh_tools(self):
        status = tool_status()
        details = "\n".join(
            f"{name}: {location or 'NÃO ENCONTRADO NO PATH'}"
            for name, location in status.items()
        )
        self._set_readonly(self.tool_text, details)

    def _shortcut_save(self, _event):
        self.save_current()
        return "break"

    def _shortcut_new(self, _event):
        self.new_project()
        return "break"

    def _close(self):
        if self.current:
            self.save_current(silent=True)
        state = {
            "geometry": self.geometry(),
            "last_project": (self.current or {}).get("id"),
        }
        try:
            state["sash"] = self.panes.sashpos(0)
            atomic_write_json(self.settings_file, state)
        except (OSError, tk.TclError, ValueError):
            pass
        self.destroy()


def main():
    try:
        Studio().mainloop()
    except Exception as exc:
        # Uma falha de inicialização em um executável --windowed não pode ser silenciosa.
        import traceback
        log = settings_path().parent / "erro-inicializacao.log"
        try:
            log.parent.mkdir(parents=True, exist_ok=True)
            log.write_text(traceback.format_exc(), encoding="utf-8")
        except OSError:
            pass
        try:
            messagebox.showerror("WMK Craft Studio — erro", f"{exc}\n\nLog: {log}")
        except Exception:
            print(traceback.format_exc(), file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
