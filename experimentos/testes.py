import importlib.util
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('erp_otimizado_teste', ROOT / 'versao_otimizada' / 'main.py')
erp = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = erp
spec.loader.exec_module(erp)


def produto(codigo, estoque=None, ordem=None):
    return {
        'codigo': codigo,
        'nome': f'Produto {codigo}',
        'preco': 10.0,
        'estoque': codigo % 17 if estoque is None else estoque,
        'estoque_minimo': 10,
        '_ordem': codigo if ordem is None else ordem,
    }


def testar_rotacoes_e_busca():
    casos = [
        [30, 20, 10],  # direita
        [10, 20, 30],  # esquerda
        [30, 10, 20],  # esquerda-direita
        [10, 30, 20],  # direita-esquerda
    ]
    for chaves in casos:
        arvore = erp.ArvoreAVL()
        for chave in chaves:
            assert arvore.inserir(produto(chave))
        assert arvore.validar()
        assert arvore.buscar(20)['codigo'] == 20
        assert arvore.buscar(999) is None
        assert not arvore.inserir(produto(20))


def testar_remocao():
    arvore = erp.ArvoreAVL()
    chaves = [50, 30, 70, 20, 40, 60, 80, 35, 45, 65]
    for chave in chaves:
        arvore.inserir(produto(chave))
    for chave in [20, 40, 70, 50, 999, 30, 35, 45, 60, 65, 80]:
        removido = arvore.remover(chave)
        if chave == 999:
            assert removido is None
        else:
            assert removido is not None and removido['codigo'] == chave
        assert arvore.validar()


def testar_travessias_e_merge_sort():
    arvore = erp.ArvoreAVL()
    chaves = list(range(1, 101))
    random.Random(2026).shuffle(chaves)
    for ordem, chave in enumerate(chaves):
        arvore.inserir(produto(chave, estoque=(chave * 7) % 13, ordem=ordem))
    em_ordem = [p['codigo'] for p in arvore.em_ordem()]
    assert em_ordem == list(range(1, 101))
    assert len(arvore.pre_ordem()) == 100
    assert len(arvore.pos_ordem()) == 100
    ordenados = erp.merge_sort_produtos(arvore.em_ordem())
    assert all(ordenados[i]['estoque'] <= ordenados[i+1]['estoque'] for i in range(99))


def testar_heap():
    fila = erp.FilaPrioridade()
    itens = [
        {'codigo': 1, 'prioridade': 2, 'ordem': 0},
        {'codigo': 2, 'prioridade': 3, 'ordem': 1},
        {'codigo': 3, 'prioridade': 1, 'ordem': 2},
        {'codigo': 4, 'prioridade': 3, 'ordem': 3},
    ]
    for item in itens:
        fila.inserir(item)
    saida = [fila.remover() for _ in range(len(fila))]
    assert [x['prioridade'] for x in saida] == [3, 3, 2, 1]
    assert fila.remover() is None


if __name__ == '__main__':
    testar_rotacoes_e_busca()
    testar_remocao()
    testar_travessias_e_merge_sort()
    testar_heap()
    print('Todos os testes automatizados passaram.')
