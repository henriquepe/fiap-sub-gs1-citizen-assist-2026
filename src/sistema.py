"""Citizen Assist AI individual. Busca local e determinística; não usa LLM."""
import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys
import unicodedata

BASE = Path(__file__).resolve().parents[1] / 'data' / 'base.json'
AVISO = 'Protótipo acadêmico, não oficial. Não informe dados pessoais. Confirme procedimentos na fonte.'
MODELOS = {
    'curto': 'Apresente a orientação de forma direta, sem adicionar fatos; inclua fonte e data.',
    'passos': 'Apresente os passos verificados em lista numerada, sem inventar etapas; inclua fonte e data.'
}


def normalizar(texto):
    texto = unicodedata.normalize('NFKD', texto.casefold())
    texto = ''.join(c for c in texto if not unicodedata.combining(c))
    return ' '.join(re.findall(r'[a-z0-9]+', texto))


def carregar_base(caminho=BASE):
    try:
        dados = json.loads(Path(caminho).read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        raise ValueError('Base ausente, vazia, ilegível ou JSON inválido.') from exc
    if not isinstance(dados, list) or not dados:
        raise ValueError('A base deve ser uma lista não vazia.')
    campos = ('codigo', 'tema', 'subassunto', 'pergunta', 'orientacao', 'fonte', 'data_verificacao')
    codigos = set()
    for i, reg in enumerate(dados, 1):
        if not isinstance(reg, dict) or any(not isinstance(reg.get(c), str) or not reg[c].strip() for c in campos):
            raise ValueError(f'Registro {i}: campo obrigatório ausente ou inválido.')
        if reg['codigo'] in codigos:
            raise ValueError('Código duplicado na base.')
        codigos.add(reg['codigo'])
        for campo, minimo in [('palavras_chave', 2), ('passos', 1)]:
            valores = reg.get(campo)
            if not isinstance(valores, list) or len(valores) < minimo or any(not isinstance(v, str) or not v.strip() for v in valores):
                raise ValueError(f'Registro {i}: {campo} inválido.')
        if len(set(map(normalizar, reg['palavras_chave']))) < 2:
            raise ValueError('Palavras-chave precisam ser distintas.')
        if not reg['fonte'].startswith('https://'):
            raise ValueError('A fonte deve usar HTTPS.')
        try:
            date.fromisoformat(reg['data_verificacao'])
        except ValueError as exc:
            raise ValueError('Data inválida; use AAAA-MM-DD.') from exc
    return dados


def hierarquia(base):
    arvore = {}
    for reg in base:
        arvore.setdefault(reg['tema'], {}).setdefault(reg['subassunto'], []).append(reg['codigo'])
    return arvore


def validar_consulta(consulta):
    if not consulta.strip() or not normalizar(consulta):
        return 'Digite uma consulta não vazia.'
    if len(consulta) > 300:
        return 'Consulta muito longa: limite de 300 caracteres.'
    if re.search(r'\b\d{3}[. ]?\d{3}[. ]?\d{3}[- ]?\d{2}\b|[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}', consulta):
        return 'Não informe dados pessoais; use somente uma dúvida genérica.'
    return None


def buscar(base, consulta, tema=None):
    erro = validar_consulta(consulta)
    if erro:
        return {'status': 'invalida', 'mensagem': erro, 'resultados': []}
    temas = hierarquia(base)
    if tema is not None and tema not in temas:
        return {'status': 'tema_invalido', 'mensagem': 'Tema inexistente.', 'resultados': []}
    frase = ' ' + normalizar(consulta) + ' '
    resultados = []
    for reg in base:
        if tema is not None and reg['tema'] != tema:
            continue
        palavras = sorted({normalizar(p) for p in reg['palavras_chave']})
        encontradas = [p for p in palavras if ' ' + p + ' ' in frase]
        if encontradas:
            resultados.append({'registro': reg, 'pontos': len(encontradas), 'encontradas': encontradas})
    resultados.sort(key=lambda item: (-item['pontos'], item['registro']['codigo']))
    if not resultados:
        return {'status': 'sem_resposta', 'mensagem': 'A base não contém resposta suficiente para essa consulta. Consulte o canal oficial.', 'resultados': []}
    return {'status': 'sugestoes' if len(resultados) > 1 else 'encontrada', 'mensagem': 'Confira se o assunto sugerido corresponde à sua dúvida.', 'resultados': resultados[:3]}


def apresentar(registro, formato='passos'):
    if formato not in MODELOS:
        raise ValueError('Formato inválido.')
    texto = registro['orientacao'] if formato == 'curto' else '\n'.join(f'{i}. {p}' for i, p in enumerate(registro['passos'], 1))
    return f"[{registro['codigo']}] {registro['pergunta']}\n{texto}\nFonte: {registro['fonte']}\nVerificação: {registro['data_verificacao']}\n{AVISO}"


def ler(mensagem):
    valor = input(mensagem).strip()
    if valor.casefold() in ('/sair', 'sair'):
        raise EOFError
    return valor


def menu(base):
    temas = list(hierarquia(base))
    print('CITIZEN ASSIST AI | Henrique Pires Espindola | RM 568600')
    print(AVISO)
    print('Comandos em qualquer etapa: /menu para voltar; /sair para encerrar.')
    while True:
        print('\nMENU: ' + ' | '.join(f'{i}. {t}' for i, t in enumerate(temas, 1)) + ' | 3. Buscar em todos | 0. Sair')
        opcao = ler('Opção: ')
        if opcao == '0':
            return
        if opcao == '/menu':
            continue
        if opcao not in [str(i) for i in range(1, len(temas) + 2)]:
            print('Opção inválida. Escolha 1, 2, 3 ou 0.')
            continue
        tema = temas[int(opcao)-1] if int(opcao) <= len(temas) else None
        if tema:
            print('Subassuntos: ' + ', '.join(hierarquia(base)[tema]))
        consulta = ler('Dúvida (sem dados pessoais): ')
        if consulta == '/menu':
            continue
        resultado = buscar(base, consulta, tema)
        print(resultado['mensagem'])
        if not resultado['resultados']:
            continue
        for i, item in enumerate(resultado['resultados'], 1):
            print(f"{i}. {item['registro']['pergunta']} ({item['pontos']} palavra(s)-chave)")
        while True:
            escolha = ler('Escolha uma sugestão ou /menu: ')
            if escolha == '/menu':
                break
            if not escolha.isdigit() or not 1 <= int(escolha) <= len(resultado['resultados']):
                print('Sugestão inválida.')
                continue
            reg = resultado['resultados'][int(escolha)-1]['registro']
            while True:
                formato = ler('Formato: 1. Curto | 2. Passo a passo | /menu: ')
                if formato == '/menu':
                    break
                if formato not in ('1', '2'):
                    print('Formato inválido.')
                    continue
                print(apresentar(reg, 'curto' if formato == '1' else 'passos'))
                break
            break


def main():
    parser = argparse.ArgumentParser(description=AVISO)
    parser.add_argument('--base', type=Path, default=BASE)
    parser.add_argument('--consulta')
    parser.add_argument('--tema')
    parser.add_argument('--formato', choices=MODELOS, default='passos')
    args = parser.parse_args()
    try:
        base = carregar_base(args.base)
    except ValueError as exc:
        print('Erro: ' + str(exc), file=sys.stderr)
        return 1
    if args.consulta is not None:
        resultado = buscar(base, args.consulta, args.tema)
        print(resultado['mensagem'])
        for item in resultado['resultados']:
            print(apresentar(item['registro'], args.formato))
            print()
    else:
        try:
            menu(base)
        except (EOFError, KeyboardInterrupt):
            pass
        print('Consulta encerrada.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
