import csv
import importlib.util
import os
import platform
import random
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = ROOT / 'versao_base' / 'main.py'
OPT_PATH = ROOT / 'versao_otimizada' / 'main.py'
OUT = ROOT / 'experimentos'
REPETICOES = 5
TAMANHOS = [100, 1000, 10000]
CENARIOS = ['aleatorio', 'ordenado', 'inverso']
SEMENTE = 20261127


def carregar(nome, caminho):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nome] = modulo
    spec.loader.exec_module(modulo)
    return modulo


base = carregar('erp_base', BASE_PATH)
opt = carregar('erp_otimizado', OPT_PATH)


def gerar_dados(n, cenario, semente):
    rng = random.Random(semente)
    codigos = list(range(1, n + 1))
    if cenario == 'aleatorio':
        rng.shuffle(codigos)
    elif cenario == 'inverso':
        codigos.reverse()
    produtos = []
    for ordem, codigo in enumerate(codigos):
        estoque = rng.randrange(0, 101)
        produtos.append({
            'codigo': codigo,
            'nome': f'Produto {codigo}',
            'preco': float((codigo % 500) + 1),
            'estoque': (estoque if ordem % 10 == 0 else estoque + 200),
            'estoque_minimo': 100,
            '_ordem': ordem,
        })
    return produtos


def preparar_base(dados):
    base.produtos = [p.copy() for p in dados]
    base.fila_reposicao = []


def preparar_opt(dados):
    opt.produtos = opt.ArvoreAVL()
    for p in dados:
        opt.produtos.inserir(p.copy())
    opt.fila_reposicao = opt.FilaPrioridade()


def medir(funcao):
    inicio = time.perf_counter()
    resultado = funcao()
    return (time.perf_counter() - inicio) * 1000, resultado


def benchmark_caso(n, cenario):
    dados = gerar_dados(n, cenario, SEMENTE + n)
    resultados = []

    # Inserção incremental de 100 novos produtos em um cadastro já existente.
    quantidade_insercao = min(100, n)
    preexistentes = dados[:n - quantidade_insercao]
    novos = []
    for i in range(quantidade_insercao):
        codigo = n + i + 1
        novos.append({
            'codigo': codigo,
            'nome': f'Produto {codigo}',
            'preco': float((codigo % 500) + 1),
            'estoque': 500,
            'estoque_minimo': 100,
            '_ordem': n + i,
        })
    for versao in ('base', 'otimizada'):
        tempos = []
        for _ in range(REPETICOES):
            if versao == 'base':
                preparar_base(preexistentes)
                def inserir_base():
                    for p in novos:
                        if base.buscar_produto(p['codigo']) is None:
                            base.produtos.append(p.copy())
                tempo, _ = medir(inserir_base)
            else:
                preparar_opt(preexistentes)
                def inserir_opt():
                    for p in novos:
                        if opt.buscar_produto(p['codigo']) is None:
                            opt.produtos.inserir(p.copy())
                tempo, _ = medir(inserir_opt)
            tempos.append(tempo)
        resultados.append(linha(n, cenario, 'insercao_amostra_100', versao, tempos, None))

    # Busca de todos os códigos existentes
    chaves = [p['codigo'] for p in dados]
    passo_busca = max(1, n // 100)
    chaves_amostra = chaves[::passo_busca][:100]
    for versao in ('base', 'otimizada'):
        tempos = []
        comparacoes = []
        for _ in range(REPETICOES):
            if versao == 'base':
                preparar_base(dados)
                def buscar_todos():
                    for chave in chaves_amostra:
                        base.buscar_produto(chave)
                tempo, _ = medir(buscar_todos)
                # Cada código é buscado uma vez; total de posições percorridas = n(n+1)/2.
                posicoes = {p["codigo"]: i + 1 for i, p in enumerate(dados)}
                comp = sum(posicoes[chave] for chave in chaves_amostra)
            else:
                preparar_opt(dados)
                opt.produtos.comparacoes = 0
                def buscar_todos_opt():
                    for chave in chaves_amostra:
                        opt.buscar_produto(chave)
                tempo, _ = medir(buscar_todos_opt)
                comp = opt.produtos.comparacoes
            tempos.append(tempo)
            comparacoes.append(comp)
        resultados.append(linha(n, cenario, 'busca_existente', versao, tempos, statistics.mean(comparacoes)))

    # Busca de chaves inexistentes
    ausentes = list(range(n + 1, n + 1 + min(100, n)))
    for versao in ('base', 'otimizada'):
        tempos = []
        comparacoes = []
        for _ in range(REPETICOES):
            if versao == 'base':
                preparar_base(dados)
                def buscar_ausentes():
                    for chave in ausentes:
                        base.buscar_produto(chave)
                tempo, _ = medir(buscar_ausentes)
                comp = n * len(ausentes)
            else:
                preparar_opt(dados)
                opt.produtos.comparacoes = 0
                def buscar_ausentes_opt():
                    for chave in ausentes:
                        opt.buscar_produto(chave)
                tempo, _ = medir(buscar_ausentes_opt)
                comp = opt.produtos.comparacoes
            tempos.append(tempo)
            comparacoes.append(comp)
        resultados.append(linha(n, cenario, 'busca_inexistente', versao, tempos, statistics.mean(comparacoes)))

    # Remoção de todos os registros na ordem em que foram inseridos.
    passo_remocao = max(1, n // 100)
    codigos_remover = [p['codigo'] for p in dados[::passo_remocao][:100]]
    for versao in ('base', 'otimizada'):
        tempos = []
        for _ in range(REPETICOES):
            if versao == 'base':
                preparar_base(dados)
                def remover_base():
                    for codigo in codigos_remover:
                        posicao = -1
                        for i in range(len(base.produtos)):
                            if base.produtos[i]['codigo'] == codigo:
                                posicao = i
                                break
                        if posicao >= 0:
                            base.produtos.pop(posicao)
                tempo, _ = medir(remover_base)
            else:
                preparar_opt(dados)
                def remover_opt():
                    for codigo in codigos_remover:
                        opt.produtos.remover(codigo)
                tempo, _ = medir(remover_opt)
            tempos.append(tempo)
        resultados.append(linha(n, cenario, 'remocao_amostra_100', versao, tempos, None))

    # O relatório ordenado é medido nos três cenários.
    if cenario in CENARIOS:
        # Relatório ordenado por estoque
        saidas_ordenacao = {}
        for versao in ('base', 'otimizada'):
            tempos = []
            comparacoes = []
            for _ in range(REPETICOES):
                if versao == 'base':
                    preparar_base(dados)
                    tempo, ordenados = medir(base.produtos_ordenados_por_estoque)
                    comp = n * (n - 1) // 2
                else:
                    preparar_opt(dados)
                    tempo, ordenados = medir(opt.produtos_ordenados_por_estoque)
                    comp = opt.comparacoes_merge_sort
                tempos.append(tempo)
                comparacoes.append(comp)
                if len(ordenados) != n or any(ordenados[i]['estoque'] > ordenados[i+1]['estoque'] for i in range(n-1)):
                    raise AssertionError('Ordenação incorreta')
            saidas_ordenacao[versao] = [p['codigo'] for p in ordenados]
            resultados.append(linha(n, cenario, 'listagem_ordenada', versao, tempos, statistics.mean(comparacoes)))
        assert saidas_ordenacao['base'] == saidas_ordenacao['otimizada'], 'Ordem divergente'

    # Rebuild da fila de prioridade (a massa possui cerca de 10% de itens elegíveis)
    filas_saida = {}
    for versao in ('base', 'otimizada'):
        tempos = []
        comparacoes = []
        for _ in range(REPETICOES):
            if versao == 'base':
                preparar_base(dados)
                tempo, _ = medir(base.atualizar_fila_reposicao)
                comp = sum(1 for _ in range(max(0, len(base.fila_reposicao)-1)))
                # Selection Sort compara k(k-1)/2 pares.
                comp = len(base.fila_reposicao) * (len(base.fila_reposicao)-1) // 2
                fila = [(x['codigo'], x['prioridade']) for x in base.fila_reposicao]
            else:
                preparar_opt(dados)
                opt.fila_reposicao.comparacoes = 0
                tempo, _ = medir(opt.atualizar_fila_reposicao)
                comp = opt.fila_reposicao.comparacoes + opt.comparacoes_fila_preparo
                fila = [(x['codigo'], x['prioridade']) for x in opt.fila_reposicao.em_ordem_prioridade()]
            tempos.append(tempo)
            comparacoes.append(comp)
            filas_saida[versao] = fila
        resultados.append(linha(n, cenario, 'fila_prioridade_reconstrucao', versao, tempos, statistics.mean(comparacoes)))
    if filas_saida['base'] != filas_saida['otimizada']:
        raise AssertionError('A fila de prioridade não preservou os mesmos registros e prioridades')
    if any(filas_saida['otimizada'][i][1] < filas_saida['otimizada'][i+1][1] for i in range(len(filas_saida['otimizada'])-1)):
        raise AssertionError('Heap não respeitou a prioridade decrescente')

    return resultados


def linha(n, cenario, operacao, versao, tempos, comparacoes):
    media = statistics.mean(tempos)
    desvio = statistics.stdev(tempos) if len(tempos) > 1 else 0.0
    return {
        'registros': n,
        'cenario': cenario,
        'operacao': operacao,
        'versao': versao,
        'repeticoes': len(tempos),
        'media_ms': round(media, 6),
        'desvio_padrao_ms': round(desvio, 6),
        'comparacoes': '' if comparacoes is None else round(comparacoes, 2),
    }


def ambiente():
    mem_total = ''
    try:
        with open('/proc/meminfo', encoding='utf-8') as f:
            for linha_mem in f:
                if linha_mem.startswith('MemTotal:'):
                    mem_total = linha_mem.split(':')[1].strip()
                    break
    except OSError:
        pass
    processador = platform.processor() or platform.machine()
    try:
        with open('/proc/cpuinfo', encoding='utf-8') as f:
            for linha_cpu in f:
                if linha_cpu.lower().startswith('model name'):
                    processador = linha_cpu.split(':', 1)[1].strip()
                    break
    except OSError:
        pass
    return {
        'sistema': platform.platform(),
        'processador': processador,
        'memoria_total': mem_total,
        'python': sys.version.replace('\n', ' '),
        'semente': SEMENTE,
        'repeticoes': REPETICOES,
    }


if __name__ == '__main__':
    todas = []
    for n in TAMANHOS:
        for cenario in CENARIOS:
            print(f'Medindo n={n}, cenário={cenario}...', flush=True)
            todas.extend(benchmark_caso(n, cenario))
    caminho = OUT / 'resultados.csv'
    with caminho.open('w', newline='', encoding='utf-8') as f:
        escritor = csv.DictWriter(f, fieldnames=list(todas[0].keys()))
        escritor.writeheader()
        escritor.writerows(todas)
    with (OUT / 'ambiente.txt').open('w', encoding='utf-8') as f:
        for chave, valor in ambiente().items():
            f.write(f'{chave}: {valor}\n')
    print(f'Resultados gravados em {caminho}')
