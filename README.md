# HMP Framework ⚙️

![License](https://img.shields.io/badge/license-MIT-blue.svg)

**Desenvolvido por: RokoOfficial**

---

## HMP Framework — Hybrid Messaging Protocol

O **HMP (Hybrid Messaging Protocol)** é um framework modular, leve e extensível para construir agentes computacionais orientados por mensagens estruturadas. Ele padroniza a comunicação, garante a segurança dos tipos e permite a execução auditável e isolada de tarefas.

### Principais Características

- **Mensagens Padronizadas**: Comunicação clara e consistente entre agentes.
- **Sistema de Tipos Explícito**: Garante a segurança e a integridade dos dados.
- **Arquitetura de Agentes**: Componentes registráveis que processam tipos específicos de mensagens.
- **Execução Isolada e Auditável**: Cada mensagem é executada de forma segura e rastreável.
- **Middlewares**: Interceptadores que modificam a execução para adicionar logging, segurança, etc.
- **Extensibilidade**: Suporte a plugins para carregar agentes e funcionalidades de forma dinâmica.

---

## 📂 Estrutura do Projeto

O projeto foi reestruturado para seguir as melhores práticas de desenvolvimento em Python, com uma organização clara de pacotes e módulos:

```
hmp/
├── core/         # Núcleo do framework (runtime, message, typesystem)
├── agents/       # Agentes (shell, rest, etc.)
├── middleware/   # Middlewares
└── plugins/      # Gerenciador de plugins

examples/         # Exemplos de uso prático
docs/             # Documentação detalhada
tests/            # Testes unitários
scripts/          # Scripts auxiliares
```

---

## ⚙️ Instalação

Para instalar o framework, clone o repositório e instale as dependências:

```bash
git clone https://github.com/RokoOfficial/HMP-Protocol-LLMs-Language-.git
cd HMP-Protocol-LLMs-Language-
pip install -e .
```

Para desenvolvimento, instale as dependências de desenvolvimento:

```bash
pip install -e ".[dev]"
```

---

## 🚀 Uso Básico

O exemplo a seguir demonstra como registrar um agente e executar uma mensagem simples:

```python
# examples/basic_usage.py

from hmp import HMPRuntime, AgentRegistry, ShellAgent

# 1. Crie um registro de agentes
registry = AgentRegistry()

# 2. Registre os agentes desejados
registry.register_agent("shell", ShellAgent())

# 3. Crie o runtime do HMP
runtime = HMPRuntime(registry)

# 4. Defina a mensagem a ser executada
# Formato: "agente|payload|contexto"
msg_str = "shell|str:echo Olá, Mundo!"

# 5. Execute a mensagem
response = runtime.execute(msg_str)

print(f"Resposta do Agente: {response.payload[0]}")
# Saída: Resposta do Agente: Olá, Mundo!
```

---

## 📚 Documentação

A documentação completa, incluindo a **especificação da linguagem HMP** e a arquitetura do framework, está disponível no diretório `docs/`.

- **`docs/language_spec.md`**: Detalhes sobre a sintaxe e as palavras-chave da HMP Language.
- **`docs/architecture.md`**: Visão geral da arquitetura do sistema (a ser criado).

---

## 🧪 Testes

Para executar os testes unitários, utilize o `pytest`:

```bash
pytest
```

---

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir *issues* e *pull requests* para melhorias, correções de bugs ou novas funcionalidades.

---

## 🧾 Licença

Este projeto está licenciado sob a **Licença MIT**. Consulte o arquivo `LICENSE` para mais detalhes.

Copyright (c) 2025 RokoOfficial
