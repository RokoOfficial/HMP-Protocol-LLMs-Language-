# HMP Framework ⚙️

![License](https://img.shields.io/badge/license-MIT-blue.svg)

# Desenvolvido por: ROKO

### HMP Framework — Hybrid Messaging Protocol

**Versão:** 1.0  
**Autor:** ROKO  
**Descrição:** Framework modular para agentes computacionais orientados por mensagens estruturadas.

---

## 📘 Índice

- Visão Geral
- Instalação
- Conceitos-Chave
- Mensagem HMP
- Sistema de Tipos
- Agentes
- Registrando Agentes e Plugins
- Middlewares
- Execução de Mensagens
- Execução em Lote
- Exemplos
- Expansões Avançadas

---

## 📌 Visão Geral

O HMP é um **framework leve e extensível** para executar mensagens entre agentes computacionais, com:
- **Mensagens padronizadas**
- **Tipos explícitos e seguros**
- **Agentes registráveis**
- **Execução isolada e auditável**
- **Integração nativa com Shell, REST, ML, e muito mais**

---

## ⚙️ Instalação

```bash
git clone <seu-repo>
cd HMP
pip install -r requirements.txt
```

---

## 🧩 Conceitos-Chave

| Conceito       | Descrição |
|----------------|-----------|
| **HMPMessage** | Unidade básica de comunicação entre agentes |
| **Agente**     | Componente que processa um tipo de mensagem |
| **Middleware** | Intercepta e modifica execução (log, segurança, etc) |
| **TypeSystem** | Padroniza os tipos em payload/contexto |
| **PluginManager** | Carrega agentes/modificadores de forma dinâmica |

---

## 📨 Mensagem HMP

**Formato:**

```text
agente|payload1,payload2|chave1=valor1;chave2=valor2
```

**Exemplo:**
```text
shell|str:ls -lah|timeout=float:3.5;cwd=str:/home/user
```

---

## 🔢 Sistema de Tipos

O `HMPTypeSystem` suporta:

| Prefixo | Tipo        | Exemplo             |
|---------|-------------|---------------------|
| int     | Inteiro     | `int:42`            |
| float   | Decimal     | `float:3.14`        |
| str     | Texto       | `str:hello`         |
| bool    | Booleano    | `bool:true`         |
| json    | Objeto JSON | `json:{"k":"v"}`    |
| bin     | Binário     | `bin:<base64>`      |
| dt      | Data/hora   | `dt:2024-01-01T12`  |

---

## 🤖 Agentes

### ShellAgent
Executa comandos locais de forma segura.

```text
shell|str:ls -lah|timeout=float:2.0
```

### RESTAgent
Faz requisições HTTP.

```text
rest|str:GET,str:https://api.site.com|headers=json:{"Authorization":"Bearer xyz"}
```

### MLModelAgent
Simula inferência de um modelo.

```text
mlmodel|json:[1,2,3]|model_path=str:/model/fake.pkl
```

### DataPipeAgent
Simula fluxo de dados entre etapas.

```text
datapipe|str:entrada,str:transformador,str:saida
```

---

## 🧠 Registrando Agentes e Plugins

```python
from HMP.agent_base import AgentRegistry
from HMP.agents import ShellAgent

registry = AgentRegistry()
registry.register_agent("shell", ShellAgent())
```

### Com Plugin

```python
from HMP.plugin import PluginManager
pm = PluginManager(registry)
pm.load_plugin("plugins/meu_plugin.py")
```

---

## 🧱 Middlewares

Exemplo de middleware de log:

```python
from HMP.agent_base import Middleware

class Logger(Middleware):
    def pre_execute(self, msg): ...
    def post_execute(self, orig, res): ...
```

Registrar:
```python
registry.add_middleware(Logger())
```

---

## 🧪 Execução de Mensagens

```python
from HMP.runtime import HMPRuntime

runtime = HMPRuntime(registry)
msg = "shell|str:whoami"
resposta = runtime.execute(msg)
print(resposta)
```

---

## 📂 Execução em Lote

```python
mensagens = [
  "shell|str:ls",
  "rest|str:GET,str:https://httpbin.org/get"
]
resultados = runtime.batch_execute(mensagens)
```

---

## 🧪 Exemplos

### Rodar comando e postar resposta em API

```text
shell|str:cat arquivo.txt
rest|str:POST,str:https://meusite.com|data=json:<output_do_shell>
```

---

## 🚀 Expansões Avançadas

Você pode criar e integrar:

- `SQLAgent` → Executar queries em bancos reais
- `LLMAgent` → Conectar a OpenAI ou LLM local
- `GraphAgent` → Manipular grafos ou dados relacionais
- `HistoryMiddleware` → Armazenar logs e replay
- `REPL` → CLI interativa em terminal
- `WebDashboard` → Interface gráfica com logs e execução

---

## 🌐 Horizon Controller

Script de exemplo utilizando o framework **AGNO** para orquestrar múltiplos agentes.
Para iniciar uma sessão interativa:

```bash
python horizon_controller.py
```

---

## 🧾 Licença

MIT — Desenvolvido por [Você]

Para detalhes sobre a linguagem de alto nível utilizada pelos agentes,
consulte o arquivo `readmi.txt` que contém a **especificação do HMP
Language v1.0**.
