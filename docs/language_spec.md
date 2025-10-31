#######################################################################
#  HMP Language Specification v1.0
#  (c) 2025 Horizon IA • Licença MIT
#######################################################################

=======================================================================
1. INTRODUÇÃO
=======================================================================
HMP é uma Domain-Specific Language que combina linguagem natural com
keywords universais de programação (IF, ELSE, FOR, True, False, etc.).
Serve para descrever, em alto nível, os fluxos de agentes ROKO e suas
calls de ferramentas (“tools”) de maneira legível e 100 % interoperável
com o Horizon Message Protocol (também chamado HMP-envelope).

-----------------------------------------------------------------------
OBJETIVOS-CHAVE
-----------------------------------------------------------------------
• Clareza humana ✦ qualquer dev lê sem precisar do parser.
• Formalidade leve ✦ parser simples converte em AST JSON.
• Ação direta ✦ cada instrução aciona uma tool ou altera contexto.
• Extensibilidade ✦ futuras keywords podem ser adicionadas
  sem quebrar compatibilidade.

=======================================================================
2. GRAMÁTICA BÁSICA (EBNF)
=======================================================================
<program>  ::= { <statement> | <comment> }
<comment>  ::= "#" <texto livre ...>
<statement>::= <assignment> | <control> | <tool-call> | <section>
<assignment>::= "SET" <identifier> "TO" <expr>
<section>   ::= "DEFINE" <identifier> "AS LIST:" | "BEGIN" <id> | "END" <id>
<control>   ::= <if> | <for> | <while>
<if>        ::= "IF" <expr> "THEN" { <statement> } [ "ELSE" { <statement>} ] "ENDIF"
<for>       ::= "FOR" <id> "IN" <expr> "DO" { <statement> } "ENDFOR"
<while>     ::= "WHILE" <expr> "DO" { <statement> } "ENDWHILE"
<tool-call> ::= "CALL" <tool-name> [ "WITH" <kv-pairs> ]
<expr>      ::= literal | <identifier> | <expr> <op> <expr> | "(" <expr> ")"

Literals booleanos: True | False
Operadores lógicos: AND | OR | NOT
Comparação: = , != , > , < , >= , <=
Strings: "texto entre aspas"

=======================================================================
3. PALAVRAS-CHAVE RESERVADAS
=======================================================================
SET, DEFINE, AS, LIST, BEGIN, END,
IF, THEN, ELSE, ENDIF,
FOR, IN, DO, ENDFOR,
WHILE, ENDWHILE,
CALL, WITH, RETURN, True, False

=======================================================================
4. DECLARAÇÃO DE TOOLS
=======================================================================
DEFINE tools AS LIST:
    web.search_query, web.image_query, web.product_query,
    web.open, web.click, web.find,
    web.weather, web.finance, web.sports,
    python, python_user_visible,
    canmore.create_textdoc, canmore.update_textdoc, canmore.comment_textdoc,
    automations.create, automations.update,
    image_gen.text2im,
    user_info.get_user_info

# Cada item é um nome totalmente qualificado disponível
# no runtime da ROKO. O parser armazena a lista e restringe
# CALL a essas entradas (salvo extensão “UNSAFE”).

=======================================================================
5. CONTROLE DE FLUXO & EXPRESSÕES
=======================================================================
• IF-THEN-ELSE segue blocos indentados ou cercados por ENDIF.
• FOR-IN-DO aceita qualquer iterável (lista literal ou variável).
• WHILE repete até condição ser False.
• Operadores AND / OR têm precedência igual; NOT tem precedência maior.

Exemplo:
    IF "imagem" IN user_request AND user_has_uploaded_photo IS False THEN
        CALL image_gen.text2im WITH prompt = "Faça upload de sua foto."
    ENDIF

=======================================================================
6. CHAMADAS DE TOOL
=======================================================================
# Forma canônica
CALL <tool> WITH
    param1 = valor1,
    param2 = valor2,
    …

• Vírgulas opcionais no fim da lista.
• Ausência de WITH ⇒ parâmetros default.
• O runtime converte a chamada HMP em
  JSON próprio para web.run ou outro wrapper.

=======================================================================
7. VARIÁVEIS E CONTEXTO
=======================================================================
• Regra de escopo: variável visível do ponto onde foi SET até o
  fim do bloco atual. Blocos aninhados têm herança de leitura.
• Tipagem dinâmica: valores literais assumem tipo boolean, number
  ou string. Conversão implícita em operações simples
  (concatenar string + number resulta em string).

=======================================================================
8. INTEGRAÇÃO COM O HMP-ENVELOPE
=======================================================================
O Horizon Message Protocol (HMP-envelope) usa mensagens separadas por
pipes ‘|’. Para embutir código HMP:

BEGIN HMP
|TYPE:hmp|
|CODE:
    SET contexto TO "ROKO"
    CALL web.search_query WITH q = "tempo em Lisboa"
    RETURN
|
END HMP

• Blocos CODE terminam quando encontrarem ‘|’ sozinho em nova linha.
• Qualquer saída do parser vira payload HMP codificado em Base64
  (opcional) para evitar conflitos com pipes.

=======================================================================
9. EXEMPLOS COMPLETOS
=======================================================================
# Busca de notícias recentes e geração de PDF

SET assunto TO "criptomoedas"
CALL web.search_query WITH q = assunto AND recency = 3
CALL python_user_visible WITH code = """
import pandas as pd, matplotlib.pyplot as plt
# ... gera gráficos …
"""
CALL automations.create WITH
    title = "Relatório Cripto",
    prompt = "Enviar PDF pronto",
    schedule = "BEGIN:VEVENT
        RRULE:FREQ=DAILY;BYHOUR=9;BYMINUTE=0;BYSECOND=0
    END:VEVENT"
RETURN "Relatório agendado!"

=======================================================================
10. BOAS PRÁTICAS
=======================================================================
• Use comentários (#) para explicar lógica.
• Coloque DEFINE tools no topo.
• Divida scripts longos em SECTIONS: BEGIN Auth, BEGIN Workflow …
• Valide seu HMP com “CALL python --validate” antes de rodar.
• Para paralelismo, combine vários CALL … IN PARALLEL (versão 1.1+).

=======================================================================
11. EXTENSÕES FUTURAS (ROADMAP)
=======================================================================
• TRY / CATCH para tratamento de erro granular.
• PARALLEL / ENDPARALLEL para execução concorrente.
• WAIT UNTIL <expr> para polling reativo.
• MACRO <name> ... ENDMACRO para reutilização.

#######################################################################
#  FIM DO ARQUIVO • readmi.txt
#######################################################################
