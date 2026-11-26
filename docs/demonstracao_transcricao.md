# Citizen Assist AI

Henrique Pires Espindola | RM 568600
Substitutiva de Global Solution 2026

Guia local sobre Conta gov.br e Identidade CIN.
Dez orientações verificadas, dois temas, fontes oficiais.

Objetivo: localizar orientações sem inventar informações.
Python + JSON; sem API paga e sem modelo generativo.

Demonstração do programa • Execução real

# Base separada do algoritmo

data/base.json → lista de dicionários

G01 | Conta gov.br → Criação
G02 | Conta gov.br → Recuperação
G03 | Conta gov.br → Níveis
G04 | Conta gov.br → Segurança
G05 | Conta gov.br → Atendimento
C01 | Identidade CIN → Número único
C02 | Identidade CIN → Custo
C03 | Identidade CIN → Emissão
C04 | Identidade CIN → Documentos
C05 | Identidade CIN → Formatos

Cada registro: pergunta, palavras-chave, orientação, passos,
fonte e data. Editar o JSON não exige reescrever a busca.

Hierarquia construída pela função hierarquia()

# Busca e ordenação

1. Validar consulta e tema.
2. Remover acentos, pontuação e diferença de caixa.
3. Filtrar pelo tema escolhido, se houver.
4. Contar palavras-chave inteiras ou expressões reconhecidas.
5. Ordenar por contagem decrescente; empate por código.
6. Mostrar até três candidatas e pedir confirmação.

Sem correspondência: avisar a limitação.
Uma sugestão lexical não garante que a intenção foi entendida.

Funções separadas: carregar_base, validar_consulta, buscar, apresentar

# Execução: orientação curta

$ python3 src/sistema.py --consulta "A CIN é gratis?" --formato curto

Confira se o assunto sugerido corresponde à sua dúvida.
[C02] A primeira CIN em papel é gratuita?
A primeira emissão em papel é gratuita. Outras modalidades e vias devem ser conferidas no órgão emissor.
Fonte: https://www.gov.br/governodigital/pt-br/identidade/identificacao-do-cidadao-e-carteira-de-identidade-nacional/perguntas-frequentes-sobre-a-cin/o-cidadao-tera-que-pagar
Verificação: 2026-11-25
Protótipo acadêmico, não oficial. Não informe dados pessoais. Confirme procedimentos na fonte.



Saída capturada do processo Python, sem resposta fabricada

# Execução: passo a passo

$ python3 src/sistema.py --consulta "Ativar duas etapas"

Confira se o assunto sugerido corresponde à sua dúvida.
[G04] Como ativar a verificação em duas etapas?
1. Com uma conta prata ou ouro, abra Segurança da conta no aplicativo gov.br e ative a verificação em duas etapas.
2. O código é gerado pelo aplicativo gov.br, não por SMS.
Fonte: https://www.gov.br/governodigital/pt-br/identidade/conta-gov-br/seguranca-da-conta
Verificação: 2026-11-26
Protótipo acadêmico, não oficial. Não informe dados pessoais. Confirme procedimentos na fonte.



A fonte e a data acompanham os dois formatos

# Menu real: Consulta curta (1)

Entrada automatizada: '1\nsenha\n1\n1\n0\n'

CITIZEN ASSIST AI | Henrique Pires Espindola | RM 568600
Protótipo acadêmico, não oficial. Não informe dados pessoais. Confirme procedimentos na fonte.
Comandos em qualquer etapa: /menu para voltar; /sair para encerrar.

MENU: 1. Conta gov.br | 2. Identidade CIN | 3. Buscar em todos | 0. Sair
Opção: Subassuntos: Criação, Recuperação, Níveis, Segurança, Atendimento
Dúvida (sem dados pessoais): Confira se o assunto sugerido corresponde à sua dúvida.
1. Como recuperar a senha da conta? (1 palavra(s)-chave)
Escolha uma sugestão ou /menu: Formato: 1. Curto | 2. Passo a passo | /menu: [G02] Como recuperar a
senha da conta?
No acesso oficial, escolha a recuperação de senha e siga um dos métodos disponíveis para sua conta.
Fonte: https://www.gov.br/governodigital/pt-br/acessibilidade-e-usuario/atendimento-gov.br/duvidas-
na-conta-gov.br/recuperar-senha-da-conta-gov.br/recuperar-senha-da-conta-gov.br/
Verificação: 2026-11-25
Protótipo acadêmico, não oficial. Não informe dados pessoais. Confirme procedimentos na fonte.

MENU: 1. Conta gov.br | 2. Identidade CIN | 3. Buscar em todos | 0. Sair

Transcrição fiel da execução automatizada; partes em sequência

# Menu real: Consulta curta (2)

Opção: Consulta encerrada.

Transcrição fiel da execução automatizada; partes em sequência

# Menu real: Ambiguidade e passos (1)

Entrada automatizada: '2\nCIN papel custo\n1\n2\n0\n'

CITIZEN ASSIST AI | Henrique Pires Espindola | RM 568600
Protótipo acadêmico, não oficial. Não informe dados pessoais. Confirme procedimentos na fonte.
Comandos em qualquer etapa: /menu para voltar; /sair para encerrar.

MENU: 1. Conta gov.br | 2. Identidade CIN | 3. Buscar em todos | 0. Sair
Opção: Subassuntos: Número único, Custo, Emissão, Documentos, Formatos
Dúvida (sem dados pessoais): Confira se o assunto sugerido corresponde à sua dúvida.
1. A primeira CIN em papel é gratuita? (1 palavra(s)-chave)
2. A CIN tem versão digital? (1 palavra(s)-chave)
Escolha uma sugestão ou /menu: Formato: 1. Curto | 2. Passo a passo | /menu: [C02] A primeira CIN em
papel é gratuita?
1. Confirme que a solicitação é da primeira emissão em papel.
2. Verifique no órgão emissor as condições de outras vias ou formatos.
Fonte: https://www.gov.br/governodigital/pt-br/identidade/identificacao-do-cidadao-e-carteira-de-
identidade-nacional/perguntas-frequentes-sobre-a-cin/o-cidadao-tera-que-pagar
Verificação: 2026-11-25
Protótipo acadêmico, não oficial. Não informe dados pessoais. Confirme procedimentos na fonte.

Transcrição fiel da execução automatizada; partes em sequência

# Menu real: Ambiguidade e passos (2)


MENU: 1. Conta gov.br | 2. Identidade CIN | 3. Buscar em todos | 0. Sair
Opção: Consulta encerrada.

Transcrição fiel da execução automatizada; partes em sequência

# Falhas tratadas: consulta vazia e fora da base

$ python3 src/sistema.py --consulta ""
Digite uma consulta não vazia.

$ python3 src/sistema.py --consulta "Qual a previsão do tempo?"
A base não contém resposta suficiente para essa consulta. Consulte o canal oficial.

$ python3 src/sistema.py --base arquivo-inexistente.json
Erro: Base ausente, vazia, ilegível ou JSON inválido.


Arquivo inválido gera erro legível; não há resposta inventada

# Opção inválida: retorno ao fluxo

CITIZEN ASSIST AI | Henrique Pires Espindola | RM 568600
Protótipo acadêmico, não oficial. Não informe dados pessoais. Confirme procedimentos na fonte.
Comandos em qualquer etapa: /menu para voltar; /sair para encerrar.

MENU: 1. Conta gov.br | 2. Identidade CIN | 3. Buscar em todos | 0. Sair
Opção: Opção inválida. Escolha 1, 2, 3 ou 0.

MENU: 1. Conta gov.br | 2. Identidade CIN | 3. Buscar em todos | 0. Sair
Opção: Dúvida (sem dados pessoais): Digite uma consulta não vazia.

MENU: 1. Conta gov.br | 2. Identidade CIN | 3. Buscar em todos | 0. Sair
Opção: Dúvida (sem dados pessoais): A base não contém resposta suficiente para essa consulta. Consulte o canal oficial.

MENU: 1. Conta gov.br | 2. Identidade CIN | 3. Buscar em todos | 0. Sair
Opção: Consulta encerrada.


Roteiro real: opção 9 → vazio → fora da base → sair

# Resultados e limites

14 testes unitários: passaram.
18 perguntas: 16 resultados esperados (88,89%).
Tempo médio local: 0.0571 ms.

Duas falhas de cobertura foram preservadas:
• "identidade no celular" não encontra "digital";
• "credencial de acesso" não encontra "senha".

A medição exclui digitação, leitura inicial e rede.
Não é um benchmark geral; não houve testes com pessoas.

Evidências completas: docs/resultados_testes.json e docs/roteiros_uso.json

# Formatos, segurança e próximos passos

Curto: melhor para uma dúvida factual, como gratuidade.
Passos: explicita ações para senha e segurança da conta.
Essa é uma análise editorial, não uma validação humana.

Não informar dados pessoais. O protótipo não é canal oficial.
Melhorias: sinônimos revisados e avaliação com pessoas.
Fontes precisam de revisão periódica.

Código, relatório e testes estão no repositório.

Citizen Assist AI • Demonstração do protótipo