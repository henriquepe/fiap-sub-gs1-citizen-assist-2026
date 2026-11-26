import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from sistema import BASE, carregar_base, buscar, apresentar, hierarquia

class SistemaTest(unittest.TestCase):
 def setUp(self): self.base=carregar_base()
 def test_base(self):
  self.assertEqual(len(self.base),10); self.assertEqual(len(hierarquia(self.base)),2)
 def test_normalizacao(self): self.assertEqual(buscar(self.base,'NÍVEL OURO')['resultados'][0]['registro']['codigo'],'G03')
 def test_palavra_inteira(self): self.assertEqual(buscar(self.base,'recriar universos')['status'],'sem_resposta')
 def test_ranking(self):
  res=buscar(self.base,'custo papel digital documentos certidao casamento emitir')['resultados']
  self.assertEqual(len(res),3); self.assertEqual([r['pontos'] for r in res],sorted([r['pontos'] for r in res],reverse=True))
 def test_empate_estavel(self):
  self.assertEqual([r['registro']['codigo'] for r in buscar(self.base,'senha gratis')['resultados']],['C02','G02'])
 def test_sem_resposta(self): self.assertEqual(buscar(self.base,'cotação do euro')['status'],'sem_resposta')
 def test_vazia(self): self.assertEqual(buscar(self.base,'  ')['status'],'invalida')
 def test_tema_invalido(self): self.assertEqual(buscar(self.base,'senha','inexistente')['status'],'tema_invalido')
 def test_filtro(self): self.assertEqual(buscar(self.base,'senha','Identidade CIN')['status'],'sem_resposta')
 def test_privacidade(self): self.assertEqual(buscar(self.base,'meu email teste@example.com')['status'],'invalida')
 def test_modelos(self):
  for modo in ('curto','passos'):
   txt=apresentar(self.base[0],modo); self.assertIn(self.base[0]['fonte'],txt); self.assertIn('2026-11-25',txt)
 def test_arquivos_invalidos(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'base.json'
   with self.assertRaises(ValueError): carregar_base(p)
   for txt in ['', '[]', '{}','nao json','[{}]']:
    p.write_text(txt)
    with self.assertRaises(ValueError): carregar_base(p)
 def test_atualizacao_sem_alterar_codigo(self):
  dados=json.loads(BASE.read_text()); dados[0]['orientacao']='Texto corrigido para teste.'
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'b.json';p.write_text(json.dumps(dados))
   self.assertIn('Texto corrigido',apresentar(carregar_base(p)[0],'curto'))
 def test_comandos_interativos(self):
  for entrada in ['1\n/menu\n0\n','3\nsenha\n/menu\n0\n','3\nsenha\n1\n/menu\n0\n','1\n/sair\n']:
   r=subprocess.run([sys.executable,str(BASE.parents[1]/'src/sistema.py')],input=entrada,text=True,capture_output=True,timeout=5)
   self.assertEqual(r.returncode,0);self.assertIn('Consulta encerrada',r.stdout)

if __name__=='__main__': unittest.main()
