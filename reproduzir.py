"""Executa os testes, benchmark e relatório a partir da raiz do projeto."""
from pathlib import Path
import subprocess
import sys
import os
ROOT = Path(__file__).resolve().parent
for nome, saida in [('testes.py','saida_testes.txt'),('teste_equivalencia.py','saida_equivalencia.txt'),('benchmark.py','saida_benchmark.txt')]:
    with (ROOT/'experimentos'/saida).open('w',encoding='utf-8') as f:
        subprocess.run([sys.executable, str(ROOT/'experimentos'/nome)], cwd=ROOT, stdout=f, stderr=subprocess.STDOUT, check=True, env={**os.environ,'PYTHONUTF8':'1'})
subprocess.run([sys.executable, str(ROOT/'gerar_relatorio.py')], cwd=ROOT, check=True)
