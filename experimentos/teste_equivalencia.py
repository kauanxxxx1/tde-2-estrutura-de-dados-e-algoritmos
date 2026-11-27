import importlib.util
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def carregar(nome, caminho):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nome] = modulo
    spec.loader.exec_module(modulo)
    return modulo

base = carregar('erp_base_equiv', ROOT / 'versao_base' / 'main.py')
opt = carregar('erp_opt_equiv', ROOT / 'versao_otimizada' / 'main.py')

rng = random.Random(20261127)
codigos = list(range(1, 501))
rng.shuffle(codigos)
dados = []
for ordem, codigo in enumerate(codigos):
    estoque = rng.randrange(0, 151)
    dados.append({
        'codigo': codigo,
        'nome': f'Produto {codigo}',
        'preco': float(codigo) / 2,
        'estoque': estoque,
        'estoque_minimo': 100,
        '_ordem': ordem,
    })

base.produtos = [p.copy() for p in dados]
opt.produtos = opt.ArvoreAVL()
for p in dados:
    assert opt.produtos.inserir(p.copy())

# Busca: mesma presença/ausência e mesmo produto associado à chave.
for codigo in range(1, 551):
    pb = base.buscar_produto(codigo)
    po = opt.buscar_produto(codigo)
    assert (pb is None) == (po is None)
    if pb is not None:
        assert (pb['codigo'], pb['nome'], pb['estoque']) == (po['codigo'], po['nome'], po['estoque'])

# Listagem ordenada: mesmos registros e mesmo critério de estoque.
ob = base.produtos_ordenados_por_estoque()
oo = opt.produtos_ordenados_por_estoque()
assert ob == oo, 'A sequência completa do relatório deve coincidir'
assert [p['estoque'] for p in ob] == sorted(p['estoque'] for p in ob)
assert [p['estoque'] for p in oo] == sorted(p['estoque'] for p in oo)

# Fila: mesmos produtos elegíveis e mesmas prioridades.
base.atualizar_fila_reposicao()
opt.atualizar_fila_reposicao()
fb = [(x['codigo'], x['prioridade']) for x in base.fila_reposicao]
fo = [(x['codigo'], x['prioridade']) for x in opt.fila_reposicao.em_ordem_prioridade()]
assert fb == fo

# Remoção: mesma chave removida e mesmos registros remanescentes.
remover = codigos[::7]
for codigo in remover:
    pos = next((i for i, p in enumerate(base.produtos) if p['codigo'] == codigo), -1)
    pb = base.produtos.pop(pos) if pos >= 0 else None
    po = opt.produtos.remover(codigo)
    assert pb is not None and po is not None and pb['codigo'] == po['codigo']
assert sorted(p['codigo'] for p in base.produtos) == [p['codigo'] for p in opt.produtos]
assert opt.produtos.validar()

# Casos adicionais com empates e diferentes ordens de cadastro.
for tamanho in (0, 1, 3, 10, 50, 150):
    for _ in range(20):
        codigos = list(range(1, tamanho + 1))
        rng.shuffle(codigos)
        base.produtos = []
        opt.produtos = opt.ArvoreAVL()
        for i, codigo in enumerate(codigos):
            p = dict(codigo=codigo, nome=str(codigo), preco=1.0,
                     estoque=rng.choice([0, 1, 2, 3, 4, 5, 6]),
                     estoque_minimo=5, _ordem=i)
            base.produtos.append(p.copy())
            opt.produtos.inserir(p.copy())
        assert base.produtos_ordenados_por_estoque() == opt.produtos_ordenados_por_estoque()
        base.atualizar_fila_reposicao()
        opt.atualizar_fila_reposicao()
        assert base.fila_reposicao == [{k: v for k, v in item.items() if k != 'ordem'}
                                       for item in opt.fila_reposicao.em_ordem_prioridade()]
print('Equivalência aprovada: busca, remoção, listagem e fila, inclusive empates (120 casos adicionais).')
