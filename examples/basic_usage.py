#!/usr/bin/env python3
"""
Exemplo Básico de Uso do HMP Framework
Autor: ROKO
"""

from hmp import HMPRuntime, AgentRegistry, ShellAgent

def main():
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

if __name__ == "__main__":
    main()
