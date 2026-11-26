"""Avaliação reproduzível; perguntas planejadas, sem dados pessoais reais."""
import csv
import io
import json
from pathlib import Path
import platform
import subprocess
import sys
from time import perf_counter_ns
from sistema import carregar_base, buscar, apresentar

ROOT = Path(__file__).resolve().parents[1]
CASOS = [
 ('Como criar conta?',None,'G01','encontrada'),
 ('Esqueci minha senha',None,'G02','encontrada'),
 ('Quero conta ouro',None,'G03','encontrada'),
 ('Ativar duas etapas',None,'G04','encontrada'),
 ('Preciso de suporte',None,'G05','encontrada'),
 ('Qual o numero da CIN?',None,'C01','encontrada'),
 ('A CIN é gratis?',None,'C02','encontrada'),
 ('Onde tirar identidade?',None,'C03','encontrada'),
 ('Levar certidao de casamento',None,'C04','encontrada'),
 ('Existe CIN digital?',None,'C05','encontrada'),
 ('Quero cadastrar uma conta','Conta gov.br','G01','encontrada'),
 ('A CIN tem custo em papel?','Identidade CIN','C02','sugestoes'),
 ('Qual a previsão do tempo?',None,None,'sem_resposta'),
 ('',None,None,'invalida'),
 ('Ajuda','Tema inexistente',None,'tema_invalido'),
 ('Emitir identidade','Conta gov.br',None,'sem_resposta'),
 ('Quero uma identidade no celular',None,'C05','encontrada'),
 ('Perdi minha credencial de acesso',None,'G02','encontrada'),
]

def main():
 base=carregar_base(); resultados=[]
 for pergunta,tema,esperado,status in CASOS:
  inicio=perf_counter_ns(); res=buscar(base,pergunta,tema); tempo=(perf_counter_ns()-inicio)/1_000_000
  ids=[r['registro']['codigo'] for r in res['resultados']]
  obtido=ids[0] if ids else None
  correto=obtido==esperado and res['status']==status
  resultados.append(dict(pergunta=pergunta,tema=tema,esperado=esperado,resposta_esperada=apresentar(next(r for r in base if r["codigo"]==esperado)) if esperado else status,status_esperado=status,obtido=obtido,status_obtido=res['status'],sugestoes=ids,acerto=correto,tempo_ms=tempo,resposta_exibida=apresentar(res['resultados'][0]['registro']) if ids else res['mensagem']))
 docs=ROOT/'docs'; docs.mkdir(exist_ok=True)
 (ROOT/'data/perguntas_teste.json').write_text(json.dumps([dict(pergunta=p,tema=t,esperado=e,status=s) for p,t,e,s in CASOS],ensure_ascii=False,indent=2))
 (docs/'resultados_testes.json').write_text(json.dumps(resultados,ensure_ascii=False,indent=2))
 with (docs/'resultados_testes.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=resultados[0].keys()); w.writeheader(); w.writerows(resultados)
 metricas=dict(total=len(resultados),acertos=sum(r['acerto'] for r in resultados),taxa_acerto=sum(r['acerto'] for r in resultados)/len(resultados),tempo_medio_ms=sum(r['tempo_ms'] for r in resultados)/len(resultados),python=platform.python_version(),ambiente=platform.platform(),metodo='Uma execução por pergunta, perf_counter_ns, busca com base já carregada; não inclui I/O, digitação ou rede.')
 (docs/'indicadores.json').write_text(json.dumps(metricas,ensure_ascii=False,indent=2))
 comp=[]
 for pergunta in ['Esqueci minha senha','A CIN é gratis?','Ativar duas etapas']:
  reg=buscar(base,pergunta)['resultados'][0]['registro']
  comp.append(dict(pergunta=pergunta,curto=apresentar(reg,'curto'),passos=apresentar(reg,'passos')))
 (docs/'comparacao_formatos.json').write_text(json.dumps(comp,ensure_ascii=False,indent=2))
 roteiros=[('Consulta curta','1\nsenha\n1\n1\n0\n',['G02','Consulta encerrada.']),('Ambiguidade e passos','2\nCIN papel custo\n1\n2\n0\n',['C02','A CIN tem versão digital?','1. Confirme']),('Erros e recuperação','9\n3\n\n3\nqual a previsão do tempo\n0\n',['Opção inválida','não vazia','não contém resposta suficiente','Consulta encerrada.'])]
 uso=[]
 for nome,entrada,marcas in roteiros:
  r=subprocess.run([sys.executable,str(ROOT/'src/sistema.py')],input=entrada,text=True,capture_output=True,timeout=10)
  uso.append(dict(tarefa=nome,entrada=entrada,saida=r.stdout,exit_code=r.returncode,sucesso=r.returncode==0 and all(m in r.stdout for m in marcas),tipo='Roteiro automatizado; não representa teste humano.'))
 (docs/'roteiros_uso.json').write_text(json.dumps(uso,ensure_ascii=False,indent=2))
 print(json.dumps(metricas,ensure_ascii=False,indent=2)); print('Roteiros:',[r['sucesso'] for r in uso])
 if not all(r['sucesso'] for r in uso): raise SystemExit(1)

if __name__=='__main__': main()
