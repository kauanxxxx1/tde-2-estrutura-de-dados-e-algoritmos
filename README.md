# TDE 2 — Algoritmos e Estruturas de Dados

ERP de varejo (UNIFAN, 2026.2), evoluído a partir da Parte 1.
Autores: Gabriel Santos Silva, Kauan dos Reis Moreira e Leonardo Maltez.

## Estrutura

- `versao_base/main.py`: código da Parte 1 (lista, pilha, fila de prioridade com Selection Sort, busca sequencial). O hash SHA-256 está em `experimentos/hashes.txt`.
- `versao_otimizada/main.py`: ERP com árvore AVL, travessias (em ordem, pré-ordem e pós-ordem), Merge Sort e heap binário, todos implementados manualmente.
- `experimentos/benchmark.py`: gera dados com semente fixa e compara as duas versões.
- `experimentos/testes.py`: testes da AVL, rotações, remoção, travessias, Merge Sort e heap.
- `experimentos/teste_equivalencia.py`: compara os resultados das duas versões.
- `experimentos/resultados.csv`, `ambiente.txt`, `resultado_validacao.txt`: medições, ambiente e validação.
- `relatorio_tecnico.pdf`, `gerar_relatorio.py`, `fig_*.png`: relatório técnico e sua geração.

## Como executar

Requer Python 3.10 ou superior. O ERP não tem dependências externas.

```bash
python versao_base/main.py
python versao_otimizada/main.py
```

## Testes

```bash
python experimentos/testes.py
python experimentos/teste_equivalencia.py
```

## Medições

```bash
python experimentos/benchmark.py
```

Semente fixa `20261127`; volumes de 100, 1.000 e 10.000 registros; cenários aleatório, ordenado e inverso; cinco repetições por medição. Buscas e remoções usam amostras de 100 operações; a inserção mede 100 novos registros sobre uma base já existente. A ordenação é medida nos três cenários. O teste de equivalência também verifica a ordem exata dos empates.

## Relatório

```bash
pip install reportlab pillow matplotlib python-docx
python reproduzir.py
```

O gerador lê o CSV, o ambiente e as saídas de terminal, recalcula os ganhos e regenera os gráficos e o PDF, além de uma versão DOCX editável. O arquivo `sbc_template.doc` é o modelo original fornecido pelo professor; `sbc_template.docx` é sua conversão editável, usada como base pelo gerador. O PDF é exportado diretamente do Word preenchido. Instale o LibreOffice (com `soffice` disponível no PATH, ou no local padrão do Windows) para a exportação automática. A variável `CORRECOES_PARTE1` deve ser confirmada pelo grupo. A base original permanece intacta. Os tempos variam conforme a máquina.
