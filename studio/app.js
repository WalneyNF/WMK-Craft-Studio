/* WMK Craft Studio Web — protótipo funcional local, sem IA.
 * Não executa código recebido de agentes. Previews usam iframe sandboxed. */
"use strict";

const $ = (id) => document.getElementById(id);
const app = {
  project: null,
  projects: [],
  tab: "preview",
  device: "desktop",
};

async function api(path, data = undefined) {
  const options = data === undefined
    ? { method: "GET", cache: "no-store" }
    : { method: "POST", headers: { "Content-Type": "application/json", "X-WMK-Request": "1" }, body: JSON.stringify(data) };
  const response = await fetch(path, options);
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || "Não foi possível concluir a operação.");
  return payload;
}

function notify(text, success = false) {
  const el = $("notice");
  el.textContent = text;
  el.classList.toggle("success", success);
}

function appendMessage(who, heading, description) {
  const row = document.createElement("div");
  row.className = "chat-message " + (who === "user" ? "user" : "assistant");
  if (who !== "user") {
    const avatar = document.createElement("span");
    avatar.className = "chat-avatar";
    avatar.textContent = "W";
    row.appendChild(avatar);
  }
  const bubble = document.createElement("div");
  bubble.className = "message";
  if (heading) {
    const strong = document.createElement("strong");
    strong.textContent = heading;
    bubble.appendChild(strong);
  }
  const p = document.createElement("p");
  p.textContent = description;
  bubble.appendChild(p);
  row.appendChild(bubble);
  $("conversationLog").appendChild(row);
  $("chatScroll").scrollTop = $("chatScroll").scrollHeight;
}

function renderProjects() {
  const filter = $("filterProjects").value.toLocaleLowerCase("pt-BR");
  const root = $("projectList");
  root.replaceChildren();
  const projects = app.projects.filter((p) => p.name.toLocaleLowerCase("pt-BR").includes(filter));
  if (!projects.length) {
    const empty = document.createElement("p");
    empty.className = "hint";
    empty.textContent = "Nenhum site encontrado. Crie o primeiro!";
    root.appendChild(empty);
  }
  for (const project of projects) {
    const row = document.createElement("button");
    row.className = "project-row" + (app.project?.id === project.id ? " active" : "");
    row.type = "button";
    const name = document.createElement("span");
    name.textContent = project.name;
    const kind = document.createElement("small");
    kind.textContent = ({
      institucional: "Site institucional",
      vitrine: "Vitrine de produtos",
      portfolio: "Portfólio",
    })[project.spec.kind] || "Site";
    row.append(name, kind);
    row.addEventListener("click", () => selectProject(project.id));
    root.appendChild(row);
  }
}

async function refreshProjects() {
  const payload = await api("/api/projects");
  app.projects = payload.projects;
  renderProjects();
}

async function selectProject(id) {
  try {
    const payload = await api("/api/projects/" + encodeURIComponent(id));
    app.project = payload.project;
    $("promptForm").classList.add("hidden");
    $("changeForm").classList.remove("hidden");
    $("downloadProject").disabled = false;
    $("projectStatus").textContent = app.project.name;
    $("conversationLog").replaceChildren();
    appendMessage("assistant", "Projeto aberto",
      "Seu site está pronto para visualizar. Experimente mudar a cor, o título ou adicionar uma seção. Os arquivos ficam guardados no seu computador.");
    renderProjects();
    showTab(app.tab);
    notify("Projeto aberto. A prévia mostra o site realmente gerado.", true);
  } catch (error) {
    notify(error.message);
  }
}

function resetNew() {
  app.project = null;
  $("promptForm").classList.remove("hidden");
  $("changeForm").classList.add("hidden");
  $("downloadProject").disabled = true;
  $("projectStatus").textContent = "Aguardando criação";
  $("emptyPreview").classList.remove("hidden");
  $("frameWrap").classList.add("hidden");
  $("codePane").classList.add("hidden");
  $("infoPane").classList.add("hidden");
  $("siteFrame").removeAttribute("src");
  $("conversationLog").replaceChildren();
  $("siteName").value = "";
  $("sitePrompt").value = "";
  notify("");
  renderProjects();
  $("siteName").focus();
}

function refreshFrame() {
  if (!app.project) return;
  $("siteFrame").src = "/preview/" + encodeURIComponent(app.project.id) + "/index.html?v=" + Date.now();
}

async function showCode() {
  if (!app.project) return;
  try {
    const filename = $("codeSelect").value;
    const url = "/preview/" + encodeURIComponent(app.project.id) + "/" + filename + "?v=" + Date.now();
    const response = await fetch(url, { cache: "no-store" });
    if (!response.ok) throw new Error("Arquivo não encontrado.");
    $("codeText").textContent = await response.text();
  } catch (error) {
    $("codeText").textContent = error.message;
  }
}

function addDetail(grid, label, value) {
  const dt = document.createElement("dt");
  dt.textContent = label;
  const dd = document.createElement("dd");
  dd.textContent = value;
  grid.append(dt, dd);
}

function showInfo() {
  const root = $("infoPane");
  root.replaceChildren();
  if (!app.project) return;
  const title = document.createElement("h2");
  title.textContent = "Informações do projeto";
  root.append(title);
  const dl = document.createElement("dl");
  addDetail(dl, "Nome", app.project.name);
  addDetail(dl, "Descrição", app.project.description);
  addDetail(dl, "Modelo", app.project.spec.kind);
  addDetail(dl, "Cor", app.project.spec.color);
  addDetail(dl, "Atualizado", app.project.updated_at);
  root.appendChild(dl);
  const heading = document.createElement("h2");
  heading.textContent = "Histórico";
  root.append(heading);
  const list = document.createElement("ul");
  for (const event of app.project.history.slice().reverse()) {
    const line = document.createElement("li");
    line.textContent = event.message + " — " + event.at;
    list.appendChild(line);
  }
  root.appendChild(list);
}

function showTab(name) {
  app.tab = name;
  for (const [id, tab] of [["tabPreview", "preview"], ["tabCode", "code"], ["tabInfo", "info"]]) {
    $(id).classList.toggle("active", tab === name);
    $(id).setAttribute("aria-selected", String(tab === name));
  }
  $("emptyPreview").classList.toggle("hidden", Boolean(app.project) || name !== "preview");
  $("frameWrap").classList.toggle("hidden", !app.project || name !== "preview");
  $("codePane").classList.toggle("hidden", !app.project || name !== "code");
  $("infoPane").classList.toggle("hidden", !app.project || name !== "info");
  if (name === "preview" && app.project) refreshFrame();
  if (name === "code" && app.project) showCode();
  if (name === "info" && app.project) showInfo();
}

async function handleCreate(event) {
  event.preventDefault();
  const button = $("createButton");
  if (button.disabled) return;
  button.disabled = true;
  notify("Criando site com template local...");
  const name = $("siteName").value;
  const prompt = $("sitePrompt").value;
  const kind = $("siteKind").value;
  const color = $("siteColor").value;
  try {
    const result = await api("/api/projects", { name, prompt, kind, color });
    await refreshProjects();
    await selectProject(result.project.id);
    appendMessage("user", "", prompt);
    appendMessage("assistant", "Primeira versão criada",
      "Criei os arquivos HTML, CSS e JavaScript do site com estilo responsivo. A prévia está executando localmente. Não usei IA nem conteúdo de sites de terceiros.");
    $("siteName").value = "";
    $("sitePrompt").value = "";
    showTab("preview");
    notify("Site gerado! Você já pode visualizar, alterar e baixar.", true);
  } catch (error) {
    notify(error.message);
  } finally {
    button.disabled = false;
  }
}

async function handleChange(event) {
  event.preventDefault();
  if (!app.project) return;
  const button = $("changeButton");
  if (button.disabled) return;
  const message = $("changePrompt").value.trim();
  button.disabled = true;
  try {
    const result = await api("/api/projects/" + encodeURIComponent(app.project.id) + "/change", { message });
    app.project = result.project;
    appendMessage("user", "", message);
    appendMessage("assistant", "Alteração aplicada", result.message);
    $("changePrompt").value = "";
    await refreshProjects();
    showTab(app.tab);
    notify(result.message, true);
  } catch (error) {
    appendMessage("assistant", "Não alterei o projeto", error.message);
    notify(error.message);
  } finally {
    button.disabled = false;
  }
}

async function copyBrief() {
  if (!app.project) return;
  const p = app.project;
  const spec = p.spec;
  const lines = [
    "# Projeto — " + p.name, "", "## Pedido original", "", p.description, "",
    "## Configuração", "", "- Tipo: " + spec.kind, "- Cor: " + spec.color,
    "- Título: " + spec.title, "- Texto: " + spec.subtitle, "",
    "## Histórico",
    ...p.history.map((h) => "- " + h.at + ": " + h.message),
    "", "Criação autoral — WMK Craft Studio",
  ];
  try {
    await navigator.clipboard.writeText(lines.join("\n"));
    notify("Resumo Markdown copiado.", true);
  } catch {
    notify("O navegador não permitiu copiar. Use os detalhes do projeto.");
  }
}

function setupResize(handleId, variable, minimum, maximum) {
  const handle = $(handleId);
  let startX = 0;
  let startWidth = 0;
  handle.addEventListener("pointerdown", (event) => {
    if (window.matchMedia("(max-width:840px)").matches) return;
    startX = event.clientX;
    startWidth = parseInt(getComputedStyle(document.documentElement).getPropertyValue(variable), 10);
    handle.setPointerCapture(event.pointerId);
    handle.classList.add("dragging");
  });
  handle.addEventListener("pointermove", (event) => {
    if (!handle.hasPointerCapture(event.pointerId)) return;
    const value = Math.min(maximum, Math.max(minimum, startWidth + event.clientX - startX));
    document.documentElement.style.setProperty(variable, value + "px");
  });
  handle.addEventListener("pointerup", (event) => {
    if (!handle.hasPointerCapture(event.pointerId)) return;
    handle.releasePointerCapture(event.pointerId);
    handle.classList.remove("dragging");
    try {
      localStorage.setItem("wmk_web_layout", JSON.stringify({
        left: getComputedStyle(document.documentElement).getPropertyValue("--left").trim(),
        middle: getComputedStyle(document.documentElement).getPropertyValue("--middle").trim(),
      }));
    } catch { /* Armazenamento desativado no navegador. */ }
  });
  handle.addEventListener("keydown", (event) => {
    if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
    event.preventDefault();
    const current = parseInt(getComputedStyle(document.documentElement).getPropertyValue(variable), 10);
    const next = Math.min(maximum, Math.max(minimum, current + (event.key === "ArrowRight" ? 20 : -20)));
    document.documentElement.style.setProperty(variable, next + "px");
  });
}

function restoreLayout() {
  try {
    const saved = JSON.parse(localStorage.getItem("wmk_web_layout") || "{}");
    for (const [variable, value, lo, hi] of [["--left", saved.left, 160, 320], ["--middle", saved.middle, 290, 600]]) {
      if (typeof value === "string" && /^\d+px$/.test(value)) {
        document.documentElement.style.setProperty(variable, Math.min(hi, Math.max(lo, parseInt(value, 10))) + "px");
      }
    }
  } catch { /* Nenhum layout salvo. */ }
}

function initialize() {
  $("promptForm").addEventListener("submit", handleCreate);
  $("changeForm").addEventListener("submit", handleChange);
  $("newProject").addEventListener("click", resetNew);
  $("filterProjects").addEventListener("input", renderProjects);
  $("tabPreview").addEventListener("click", () => showTab("preview"));
  $("tabCode").addEventListener("click", () => showTab("code"));
  $("tabInfo").addEventListener("click", () => showTab("info"));
  $("codeSelect").addEventListener("change", showCode);
  $("reloadPreview").addEventListener("click", refreshFrame);
  $("downloadProject").addEventListener("click", () => {
    if (app.project) window.location.href = "/api/projects/" + encodeURIComponent(app.project.id) + "/download";
  });
  $("viewMobile").addEventListener("click", () => {
    app.device = "mobile";
    $("frameWrap").classList.add("mobile");
    showTab("preview");
  });
  $("viewDesktop").addEventListener("click", () => {
    app.device = "desktop";
    $("frameWrap").classList.remove("mobile");
    showTab("preview");
  });
  $("copyBrief").addEventListener("click", copyBrief);
  restoreLayout();
  setupResize("resizeLeft", "--left", 160, 320);
  setupResize("resizeMid", "--middle", 290, 600);
  refreshProjects().then(() => {
    if (app.projects.length) selectProject(app.projects[0].id);
  }).catch((error) => notify("Não foi possível carregar os projetos: " + error.message));
}

document.addEventListener("DOMContentLoaded", initialize);
