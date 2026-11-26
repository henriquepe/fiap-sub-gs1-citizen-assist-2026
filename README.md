# Citizen Assist AI — Substitutiva GS 2026

**Henrique Pires Espindola — RM 568600**

## Problema e escopo

Citizen Assist AI — Atividade Substitutiva de Global Solution 2026. Henrique Pires Espindola, RM 568600. Produção em 25/11/2026.

O público são pessoas que precisam localizar orientações básicas sobre Conta gov.br e Carteira de Identidade Nacional (CIN). O problema é a dispersão das informações; o protótipo reúne perguntas frequentes com fontes oficiais e data de verificação.

O programa roda localmente em Python, sem dependências externas, credenciais, serviços pagos ou modelo generativo. A sigla AI identifica o case acadêmico: as respostas são recuperadas de uma base verificada, e não geradas livremente.

Escopo: dez registros, cinco por tema. Cada consulta exige uma palavra ou expressão prevista na base; a interface pede ao usuário que confirme o assunto sugerido. Não se trata de atendimento oficial, emissão de documento ou recuperação real de conta.

Execução: python3 src/sistema.py. Avaliação: python3 src/avaliar.py. Testes de regressão: python3 -m unittest discover -s tests -v. Python 3.10 ou superior; validado nesta execução em Python 3.14.5.

## Base e hierarquia

Arquivo data/base.json: lista de dicionários. Campos obrigatórios: codigo, tema, subassunto, pergunta, palavras_chave (lista com pelo menos dois termos distintos), orientacao, fonte e data_verificacao. O campo passos contém a versão estruturada da orientação.

Hierarquia: raiz Citizen Assist → tema → subassunto → código. Ela é construída pela função hierarquia(), sem uma biblioteca de grafos. Os dois temas aparecem no menu; os subassuntos aparecem ao selecionar um deles.

G01 | Conta gov.br → Criação | Como criar uma conta gov.br?

G02 | Conta gov.br → Recuperação | Como recuperar a senha da conta?

G03 | Conta gov.br → Níveis | Onde consultar os níveis da conta?

G04 | Conta gov.br → Segurança | Como ativar a verificação em duas etapas?

G05 | Conta gov.br → Atendimento | Onde obter ajuda com a conta?

C01 | Identidade CIN → Número único | Qual é o número da CIN?

C02 | Identidade CIN → Custo | A primeira CIN em papel é gratuita?

C03 | Identidade CIN → Emissão | Onde emitir a CIN?

C04 | Identidade CIN → Documentos | Que certidão levar para emitir a CIN?

C05 | Identidade CIN → Formatos | A CIN tem versão digital?

Para atualizar: editar ou acrescentar um objeto no JSON, mantendo o esquema, fonte oficial e data. Reiniciar o programa carrega a mudança. Um teste automatizado corrige a orientação em uma cópia temporária e verifica a apresentação, sem alterar o algoritmo.

## Algoritmo, validação e privacidade

Fluxo: carregar arquivo → validar esquema → mostrar menu → validar consulta → filtrar tema → normalizar texto → contar palavras-chave → ordenar → selecionar orientação → escolher formato → mostrar fonte e data → voltar ao menu.

normalizar() remove acentos e pontuação e converte para minúsculas. A busca verifica palavras inteiras ou expressões contíguas: “cadastro” não corresponde a “recadastro”. Cada palavra-chave distinta soma um ponto; a ordenação é por pontos decrescentes e, no empate, código crescente. Mostram-se até três sugestões.

Uma correspondência lexical é uma candidata, não uma garantia semântica. Mesmo com apenas um resultado, o menu pede confirmação. Sem correspondência, a aplicação informa que a base não contém resposta suficiente e não cria uma orientação.

A busca percorre N registros e K palavras-chave por registro; cada comparação procura um trecho na consulta de tamanho L: aproximadamente O(N×K×L), mais O(M log M) para ordenar M candidatos. Para dez registros, a varredura linear facilita explicação e manutenção.

carregar_base() trata arquivo ausente, vazio, JSON malformado, lista vazia, campo faltando, código duplicado, palavras-chave insuficientes, fonte sem HTTPS e data inválida. buscar() trata consulta vazia, tema inexistente e ausência de resultado. O menu trata opção, sugestão e formato inválidos.

Comandos /menu e /sair permitem navegar e encerrar. EOF e interrupção de teclado também encerram sem traceback. A consulta tem limite de 300 caracteres. Há bloqueio simples de padrões de CPF e e-mail; isso não detecta todos os dados pessoais. Não há gravação de consultas de usuários, telemetria ou chamadas de rede na aplicação.

## Dois formatos e comparação

Instrução curta: “Apresente a orientação de forma direta, sem adicionar fatos; inclua fonte e data.” Instrução em passos: “Apresente os passos verificados em lista numerada, sem inventar etapas; inclua fonte e data.” São modelos determinísticos, não prompts enviados a um LLM.

Pergunta: Esqueci minha senha
Curto: No acesso oficial, escolha a recuperação de senha e siga um dos métodos disponíveis para sua conta.
Passos: 1. Acesse o login oficial e escolha Esqueci minha senha. 2. Siga o método de recuperação oferecido; se não conseguir, consulte o formulário de atendimento indicado na fonte.

Pergunta: A CIN é gratis?
Curto: A primeira emissão em papel é gratuita. Outras modalidades e vias devem ser conferidas no órgão emissor.
Passos: 1. Confirme que a solicitação é da primeira emissão em papel. 2. Verifique no órgão emissor as condições de outras vias ou formatos.

Pergunta: Ativar duas etapas
Curto: No aplicativo gov.br, acesse Segurança da conta. A verificação em duas etapas está disponível para contas prata e ouro.
Passos: 1. Com uma conta prata ou ouro, abra Segurança da conta no aplicativo gov.br e ative a verificação em duas etapas. 2. O código é gerado pelo aplicativo gov.br, não por SMS.

Análise dos formatos: para recuperar senha e ativar duas etapas, o formato em passos torna a sequência de ações mais explícita. Para saber se a primeira via em papel é gratuita, a versão curta responde com menor esforço de leitura. Esta preferência é uma avaliação estrutural, não uma medida de compreensão humana.

Os dois formatos preservam fonte, data e aviso. O conteúdo integral das seis saídas reais está em docs/comparacao_formatos.json. O usuário pode escolher qualquer formato; o padrão da consulta por argumentos é passos.

Acessibilidade: interação textual, mensagens em português, opções numeradas e ausência de dependência de cor. Limites: exige leitura e familiaridade mínima com terminal; não houve avaliação com leitor de tela ou participantes externos.

## Testes, indicadores e tarefas

Foram executadas 18 perguntas planejadas: 16 resultados de acordo com código e status esperados; taxa de acerto = 16/18 × 100 = 88,89%. Tempo médio medido: 0.0571 ms. A amostra inclui dez consultas diretas, variações, ambiguidade, filtro, tema inexistente, vazio e pergunta fora da base.

Tempo medido com perf_counter_ns, uma execução por pergunta e base já em memória; exclui digitação, leitura inicial do arquivo e rede. É uma medição local exploratória, não um benchmark com repetições ou percentis. Ambiente: macOS-27.2-arm64-arm-64bit-Mach-O.

Falhas mantidas: “Quero uma identidade no celular” esperava C05, mas não teve resposta; “Perdi minha credencial de acesso” esperava G02, mas não teve resposta. A busca não conhece esses sinônimos. A abstenção evita inventar fatos, mas reduz cobertura.

14 testes unitários passaram, incluindo arquivos inválidos, campos faltantes, empate, ranking, filtro, normalização, privacidade básica e atualização da base. Os resultados completos e tempos por pergunta estão nos arquivos resultados_testes.json/csv; stdout está em testes_unitarios.txt.

Tarefa 1: selecionar gov.br, consultar senha, escolher orientação e resposta curta, sair. Concluída pelo roteiro automatizado. Menu e fonte aparecem; o passo adicional de confirmação evita assumir intenção, ao custo de uma interação.

Tarefa 2: consultar CIN papel custo, ver duas sugestões, escolher a primeira e formato em passos. Concluída. Dificuldade: duas palavras genéricas apontam assuntos distintos; a seleção explícita permite escolher. O teste inicialmente procurava um código que o menu não exibe; foi corrigido para verificar o texto efetivamente visível.

Tarefa 3: opção 9, consulta vazia, previsão do tempo, sair. Concluída. As mensagens específicas permitem recuperar o fluxo sem traceback. Evidências: docs/roteiros_uso.json. Não houve observação de usuário humano, portanto não se afirma satisfação ou facilidade comprovada.

## Conclusões, melhorias e fontes

O protótipo demonstrou leitura de JSON, listas/dicionários, seleção por condições booleanas, ranking, dois modelos de resposta e tratamento de erros. A separação em funções permite atualizar o conteúdo sem reescrever a busca. A avaliação evidencia cobertura lexical limitada; 88,89% nesta amostra não representa precisão em uso público.

Melhoria 1: ampliar sinônimos revisados para “celular” e “credencial”, com perguntas novas reservadas para avaliação. A motivação são as duas falhas observadas; não basta ajustar a base somente às perguntas já usadas.

Melhoria 2: testar tarefas com pessoas, inclusive baixa familiaridade digital, medir conclusão, tempo e dificuldades e revisar mensagens. A motivação é a ausência de evidência humana. Melhoria 3: revisão periódica das fontes e alerta de conteúdo antigo; data registrada não garante atualização futura.

Limitações adicionais: não entende negação ou intenção, não consulta disponibilidade regional em tempo real e o bloqueio de dados pessoais é parcial. Não substitui órgãos emissores. Nenhum dado pessoal real foi usado nas perguntas.

Fontes consultadas em 25/11/2026: páginas oficiais gov.br para Conta gov.br, recuperação de senha, segurança da conta e CIN. Cada registro contém a URL específica; links completos constam na base e abaixo no README. A estrutura segue os itens solicitados na Tabela 2 do enunciado FIAP; o modelo de referência é github.com/equipe1ccon/FIAP-PORTFOLIO-1CCON.

## Arquivos e execução

```text
python3 src/sistema.py
python3 src/sistema.py --consulta "Esqueci minha senha" --formato curto
python3 src/sistema.py --consulta "CIN papel custo" --tema "Identidade CIN"
python3 src/avaliar.py
python3 -m unittest discover -s tests -v
```

- `src/sistema.py`: interface e lógica.
- `src/avaliar.py`: avaliação reproduzível.
- `data/base.json`: conteúdo.
- `docs/relatorio.pdf`: relatório de seis páginas.
- `docs/link_video.txt`: vídeo não listado.
- `tests/`: testes de regressão.

## Fontes

- https://www.gov.br/governodigital/pt-br/identidade/conta-gov-br
- https://www.gov.br/governodigital/pt-br/acessibilidade-e-usuario/atendimento-gov.br/duvidas-na-conta-gov.br/recuperar-senha-da-conta-gov.br/recuperar-senha-da-conta-gov.br/
- https://www.gov.br/governodigital/pt-br/identidade/conta-gov-br/seguranca-da-conta
- https://www.gov.br/governodigital/pt-br/identidade/cin
- https://www.gov.br/governodigital/pt-br/identidade/identificacao-do-cidadao-e-carteira-de-identidade-nacional/perguntas-frequentes-sobre-a-cin/o-cidadao-tera-que-pagar
- https://www.gov.br/governodigital/pt-br/identidade/cin/perguntas-frequentes-sobre-a-cin/

## Vídeo

[Assistir à demonstração no YouTube](https://youtu.be/baZ_6AuPLIk).
