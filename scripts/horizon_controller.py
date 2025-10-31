"""Horizon Controller using AGNO framework.
"""
import datetime as _dt
import os
import sqlite3
import subprocess
import smtplib
from pathlib import Path
import requests

from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools import tool


@tool
def web_search(query: str, top_k: int = 5) -> str:
    """Simple HTML search via DuckDuckGo."""
    r = requests.get("https://duckduckgo.com/html/", params={"q": query}, timeout=15)
    r.raise_for_status()
    return r.text[:1200] + "..."


@tool
def criar_script(nome: str, codigo: str) -> str:
    Path(nome).write_text(codigo, encoding="utf-8")
    return f"✅ Script '{nome}' criado."


@tool
def ler_arquivo(nome: str) -> str:
    return Path(nome).read_text("utf-8") if Path(nome).exists() else f"❌ {nome} não encontrado."


@tool
def executar_script(nome: str) -> str:
    res = subprocess.run(["python3", nome], text=True, capture_output=True)
    return res.stdout or res.stderr


@tool
def send_email(to: str, subject: str, body: str) -> str:
    mail = os.getenv("GMAIL_ADDRESS")
    pwd = os.getenv("GMAIL_APP_PASSWORD")
    if not (mail and pwd):
        return "❌ ENV GMAIL_ADDRESS / GMAIL_APP_PASSWORD ausentes."
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    msg = MIMEMultipart()
    msg["From"] = mail
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.starttls()
        s.login(mail, pwd)
        s.send_message(msg)
    return "✅ E-mail enviado!"


@tool
def listar_repositorios(usuario: str) -> str:
    token = os.getenv("GITHUB_API_TOKEN_ROKO")
    if not token:
        return "❌ token GitHub ausente."
    r = requests.get(
        f"https://api.github.com/users/{usuario}/repos",
        headers={"Authorization": f"Bearer {token}"},
        timeout=20,
    )
    return "\n".join(repo["name"] for repo in r.json())


@tool
def clonar_repo(url: str) -> str:
    try:
        return subprocess.check_output(["git", "clone", url], text=True)
    except subprocess.CalledProcessError as e:
        return e.output


@tool
def commit_push(msg: str) -> str:
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", msg], check=True)
        subprocess.run(["git", "push"], check=True)
        return "✅ push OK!"
    except subprocess.CalledProcessError as e:
        return e.stderr


@tool
def exec_shell(cmd: str) -> str:
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return proc.stdout or proc.stderr


@tool
def debug_trace(trace: str) -> str:
    return "🔍 Debugger ainda em construção."


class Logger:
    """Simple SQLite logger for chat history."""

    def __init__(self, path: str = "horizon_logs.db") -> None:
        self.db = sqlite3.connect(path)
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS logs(ts TEXT, role TEXT, content TEXT)"
        )

    def add(self, role: str, content: str) -> None:
        self.db.execute(
            "INSERT INTO logs VALUES (?,?,?)",
            (_dt.datetime.utcnow().isoformat(timespec="seconds"), role, content),
        )
        self.db.commit()


def worker(model_id: str, tools) -> Agent:
    """Create a sub-agent bound to a specific model and tools."""

    return Agent(model=Groq(id=model_id), tools=tools, show_tool_calls=False)


web_agent = worker("llama-3.1-8b-instant", [web_search])
gmail_agent = worker("llama-3.1-8b-instant", [send_email])
git_agent = worker(
    "llama-3.1-8b-instant",
    [listar_repositorios, clonar_repo, commit_push],
)
shell_agent = worker("llama-3.1-8b-instant", [exec_shell])
code_agent = worker(
    "llama-3.1-8b-instant", [criar_script, ler_arquivo, executar_script]
)
debugger_agent = worker("llama-3.1-8b-instant", [debug_trace])


@tool
def web_tool(question: str) -> str:
    return str(web_agent.run(question))


@tool
def gmail_tool(to: str, subject: str, body: str) -> str:
    return str(
        gmail_agent.run(
            f"Enviar e-mail para {to} com assunto '{subject}' e corpo:\n{body}"
        )
    )


@tool
def git_tool(command: str) -> str:
    return str(git_agent.run(command))


@tool
def shell_tool(cmd: str) -> str:
    return str(shell_agent.run(cmd))


@tool
def code_tool(request: str) -> str:
    return str(code_agent.run(request))


@tool
def debug_tool(trace: str) -> str:
    return str(debugger_agent.run(trace))


class HorizonController:
    """Interactive controller orchestrating several AGNO workers."""

    def __init__(self) -> None:
        self.log = Logger()
        self.agent = Agent(
            model=Groq(id="qwen-qwq-32b"),
            tools=[
                web_tool,
                gmail_tool,
                git_tool,
                shell_tool,
                code_tool,
                debug_tool,
            ],
            show_tool_calls=True,
        )

    def chat(self, prompt: str) -> str:
        self.log.add("user", prompt)
        try:
            reply = str(self.agent.run(prompt))
        except Exception as e:  # noqa: BLE001
            reply = f"⚠️ Erro: {e}"
        self.log.add("assistant", reply)
        return reply


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    bot = HorizonController()
    print("🤖 Horizon IA pronta — Ctrl-C p/ sair")
    try:
        while True:
            txt = input("Você: ").strip()
            if txt.lower() in {"sair", "exit", "quit"}:
                break
            print("ROKO:", bot.chat(txt), "\n")
    except (KeyboardInterrupt, EOFError):
        print("\n👋 Sessão encerrada.")

