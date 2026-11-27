from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, KeepTogether, Image, HRFlowable)
from reportlab.graphics.shapes import Drawing, String, Line, Rect
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import black, white
import os, hashlib

from pathlib import Path
import csv
ROOT = Path(__file__).resolve().parent
OUT = str(ROOT / 'relatorio_tecnico.pdf')
CSV = ROOT / 'experimentos' / 'resultados.csv'
# A geração falha se o CSV ou as evidências reais estiverem ausentes.
with CSV.open(encoding='utf-8', newline='') as f:
    rows = list(csv.DictReader(f))
idx = {(int(r['registros']),r['cenario'],r['operacao'],r['versao']):r for r in rows}
# Informe aqui eventuais correções da Parte 1 que o grupo confirmar.
CORRECOES_PARTE1 = []
OBSERVACAO_PARTE1 = ('Na Parte 1, foram utilizados recursos de programação que ainda não haviam sido abordados em sala de aula, o que caracterizou um problema de adequação ao conteúdo da disciplina. A adequação ao conteúdo ministrado foi considerada na evolução para a Parte 2.')
from xml.sax.saxutils import escape
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def med(op, versao, n=10000, cenario='aleatorio'):
    return float(idx[n, cenario, op, versao]['media_ms'])

def comp(op, versao, n=10000, cenario='aleatorio'):
    return float(idx[n, cenario, op, versao]['comparacoes'])

def fmt(x, casas=3):
    return f'{x:,.{casas}f}'.replace(',', '_').replace('.', ',').replace('_', '.')

def ganho(op, n=10000, cenario='aleatorio'):
    return med(op, 'base', n, cenario) / med(op, 'otimizada', n, cenario)

def resumo_tempo(op, n=10000, cenario='aleatorio'):
    return (f'base {fmt(med(op, "base", n, cenario))} ms; otimizada '
            f'{fmt(med(op, "otimizada", n, cenario))} ms; razão base/otimizada '
            f'{fmt(ganho(op, n, cenario), 2)}×')

ambiente = dict(l.split(': ', 1) for l in (ROOT/'experimentos'/'ambiente.txt').read_text(encoding='utf-8').splitlines() if ': ' in l)
base_hash = hashlib.sha256((ROOT/'versao_base'/'main.py').read_bytes()).hexdigest()
assert base_hash == (ROOT/'experimentos'/'hashes.txt').read_text().split()[0], 'Hash da base mudou'
correcoes = ('Nenhuma correção de funcionamento da Parte 1 foi registrada antes das medições; o arquivo base permanece idêntico ao original fornecido.' if not CORRECOES_PARTE1 else 'Correções antes das medições: ' + '; '.join(CORRECOES_PARTE1))
correcoes = OBSERVACAO_PARTE1 + ' ' + correcoes

def evidencias():
    linhas = []
    for comando, arquivo in [('testes.py','saida_testes.txt'), ('teste_equivalencia.py','saida_equivalencia.txt'), ('benchmark.py','saida_benchmark.txt')]:
        texto = (ROOT/'experimentos'/arquivo).read_text(encoding='utf-8').strip()
        if not texto:
            raise ValueError(f'Evidência vazia: {arquivo}')
        if comando == 'benchmark.py':
            texto = '\n'.join(texto.splitlines()[-4:])
        linhas.extend(['$ python experimentos/'+comando, texto])
    return '<br/>'.join(escape(linha) for bloco in linhas for linha in bloco.splitlines())

for op, nome, titulo in [('busca_inexistente','fig_busca.png','Busca por registro inexistente (100 consultas)'), ('fila_prioridade_reconstrucao','fig_heap.png','Reconstrução da fila de prioridade'), ('listagem_ordenada','fig_lista.png','Listagem ordenada por estoque')]:
    fig, ax = plt.subplots(figsize=(11.52, 5.03))
    ns = (100, 1000, 10000)
    for versao, label, estilo in [('base','Versão base','o-'), ('otimizada','Versão otimizada','s--')]:
        ax.plot(ns, [med(op, versao, n) for n in ns], estilo, label=label, linewidth=2)
    ax.set(xscale='log', yscale='log', xlabel='Quantidade de registros', ylabel='Tempo médio (ms)', title=titulo)
    ax.grid(True, which='both', alpha=.35)
    ax.legend()
    fig.tight_layout()
    fig.savefig(ROOT/nome, dpi=150)
    plt.close(fig)

PAGE=A4

# Use a metrically compatible Times-family font where available.
font_regular='/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf'
font_bold='/usr/share/fonts/truetype/liberation2/LiberationSerif-Bold.ttf'
font_italic='/usr/share/fonts/truetype/liberation2/LiberationSerif-Italic.ttf'
if os.path.exists(font_regular):
    pdfmetrics.registerFont(TTFont('SBC-Times',font_regular))
    pdfmetrics.registerFont(TTFont('SBC-Times-Bold',font_bold))
    pdfmetrics.registerFont(TTFont('SBC-Times-Italic',font_italic))
    F='SBC-Times'; FB='SBC-Times-Bold'; FI='SBC-Times-Italic'
else:
    F='Times-Roman'; FB='Times-Bold'; FI='Times-Italic'

# Formatação ajustada conforme o guia SBC fornecido pelo professor.
# O guia recebido é um PDF de instruções; por isso, este gerador aplica seus
# parâmetros com ReportLab, mas não substitui o preenchimento do template editável.
doc=SimpleDocTemplate(OUT,pagesize=PAGE,rightMargin=3*cm,leftMargin=3*cm,
                      topMargin=3.5*cm,bottomMargin=2.5*cm,
                      title='Evolução e otimização de um ERP de varejo com árvore AVL, Merge Sort e heap binário',
                      author='Gabriel Santos Silva, Kauan dos Reis Moreira, Leonardo Maltez')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleSBC',fontName=FB,fontSize=16,leading=19,alignment=TA_CENTER,spaceBefore=12,spaceAfter=12))
styles.add(ParagraphStyle(name='Authors',fontName=FB,fontSize=12,leading=15,alignment=TA_CENTER,spaceAfter=4))
styles.add(ParagraphStyle(name='Affil',fontName=F,fontSize=12,leading=14,alignment=TA_CENTER,spaceAfter=12))
styles.add(ParagraphStyle(name='EmailSBC',fontName='Courier',fontSize=10,leading=12,alignment=TA_CENTER,spaceBefore=6,spaceAfter=6))
styles.add(ParagraphStyle(name='BodySBC',fontName=F,fontSize=12,leading=14,alignment=TA_JUSTIFY,firstLineIndent=1.27*cm,spaceBefore=6,spaceAfter=0))
styles.add(ParagraphStyle(name='BodyFirstSBC',fontName=F,fontSize=12,leading=14,alignment=TA_JUSTIFY,firstLineIndent=0,spaceBefore=6,spaceAfter=0))
styles.add(ParagraphStyle(name='AbstractSBC',fontName=F,fontSize=12,leading=14,alignment=TA_JUSTIFY,leftIndent=0.8*cm,rightIndent=0.8*cm,spaceBefore=3,spaceAfter=5))
styles.add(ParagraphStyle(name='Heading1SBC',fontName=FB,fontSize=13,leading=17,alignment=TA_LEFT,spaceBefore=12,spaceAfter=5,keepWithNext=True))
styles.add(ParagraphStyle(name='Heading2SBC',fontName=FB,fontSize=12,leading=14,alignment=TA_LEFT,spaceBefore=8,spaceAfter=4,keepWithNext=True))
styles.add(ParagraphStyle(name='CaptionSBC',fontName='Helvetica-Bold',fontSize=10,leading=12,alignment=TA_CENTER,spaceBefore=6,spaceAfter=6,leftIndent=0.8*cm,rightIndent=0.8*cm))
styles.add(ParagraphStyle(name='SmallSBC',fontName=F,fontSize=8.5,leading=10,alignment=TA_LEFT,spaceBefore=2,spaceAfter=2))
styles.add(ParagraphStyle(name='RefSBC',fontName=F,fontSize=12,leading=14,alignment=TA_LEFT,leftIndent=0.5*cm,firstLineIndent=-0.5*cm,spaceBefore=6,spaceAfter=0))
styles.add(ParagraphStyle(name='CodeSBC',fontName=F,fontSize=10.5,leading=12.5,alignment=TA_LEFT,leftIndent=12,spaceBefore=3,spaceAfter=3))

story=[]
_first_paragraph=True
def P(txt,style='BodySBC'): story.append(Paragraph(txt,styles[style]))
def H(txt,level=1):
    global _first_paragraph
    _first_paragraph=True
    P(txt,'Heading1SBC' if level==1 else 'Heading2SBC')
def para(txt):
    global _first_paragraph
    P(txt,'BodyFirstSBC' if _first_paragraph else 'BodySBC')
    _first_paragraph=False
def caption(txt):
    P(txt,'CaptionSBC')
    story[-1].keepWithNext = True
def bullet(txt): P('&bull;&nbsp;&nbsp;'+txt)
def table(data,widths=None,font=8.3,repeatRows=1):
    t=Table(data,colWidths=widths,repeatRows=repeatRows,hAlign='LEFT')
    t.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),F),('FONTSIZE',(0,0),(-1,-1),font),
        ('LEADING',(0,0),(-1,-1),font+1.5),('TEXTCOLOR',(0,0),(-1,-1),black),
        ('BACKGROUND',(0,0),(-1,0),white),('FONTNAME',(0,0),(-1,0),FB),
        ('LINEABOVE',(0,0),(-1,0),0.8,black),('LINEBELOW',(0,0),(-1,0),0.6,black),
        ('LINEBELOW',(0,-1),(-1,-1),0.8,black),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),
        ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
    ]))
    story.append(t); story.append(Spacer(1,5))

# First page
P('Evolução e otimização de um ERP de varejo com árvore AVL, Merge Sort e heap binário','TitleSBC')
P('Gabriel Santos Silva, Kauan dos Reis Moreira, Leonardo Maltez','Authors')
P('UNIFAN — Centro Universitário Nobre<br/>Algoritmos e Estruturas de Dados — 2026.2','Affil')
P('kauancaco10@gmail.com; zgabriel049@gmail.com; mwseradep@gmail.com','EmailSBC')
P(f'<b>Abstract.</b> This paper compares a retail ERP baseline with a manually implemented AVL tree, Merge Sort and binary heap. Identical datasets of 100, 1,000 and 10,000 records were tested five times. For 10,000 random records, baseline-to-optimized time ratios were {ganho("busca_inexistente"):.2f} for unsuccessful search, {ganho("listagem_ordenada"):.2f} for stock listing and {ganho("fila_prioridade_reconstrucao"):.2f} for queue reconstruction. The comparison includes exact tie ordering and discusses implementation costs. Ratios above one indicate improvement.','AbstractSBC')
P('<b>Keywords—</b> AVL tree, Merge Sort, binary heap, algorithm analysis.','AbstractSBC')
P(f'<b>Resumo.</b> Este trabalho compara um ERP de varejo original com uma versão que utiliza AVL, Merge Sort e heap binário manuais. Foram testados conjuntos idênticos de 100, 1.000 e 10.000 registros, com cinco repetições. Para 10.000 registros aleatórios, as razões de tempo base/otimizada foram {fmt(ganho("busca_inexistente"),2)} na busca inexistente, {fmt(ganho("listagem_ordenada"),2)} na listagem e {fmt(ganho("fila_prioridade_reconstrucao"),2)} na fila. A comparação preserva a ordem dos empates e discute os custos. Razões acima de um indicam melhoria.','AbstractSBC')
P('<b>Palavras-chave—</b> árvore AVL, Merge Sort, heap binário, análise de algoritmos.','AbstractSBC')

H('1. Introdução')
para('O sistema desenvolvido na Parte 1 representa um ERP simplificado para uma loja varejista. Ele mantém cadastros de produtos e fornecedores, movimentações de estoque, histórico reversível por pilha, fila de prioridade para reposição e relatórios. Na versão original, os produtos eram armazenados em uma lista, a busca era sequencial e o relatório de estoque utilizava Selection Sort. Essas escolhas são simples e adequadas a volumes pequenos, mas seu custo cresce à medida que o cadastro aumenta.')
para('O objetivo desta etapa foi evoluir o ERP sem retirar suas funcionalidades, substituindo a estrutura principal por uma árvore balanceada e melhorando a ordenação e a fila de prioridade. Foram implementadas inserção, busca, remoção, balanceamento e rotações AVL; travessias em ordem, pré-ordem e pós-ordem; Merge Sort aplicado ao relatório real de estoque; e heap binário para a fila de reposição. Também foram medidos tempos e comparações em condições controladas para verificar o impacto das alterações.')
para('A eficiência algorítmica afeta o tempo de resposta, o uso de recursos e a capacidade de crescimento de um sistema. A análise assintótica permite estimar como o custo varia com o tamanho da entrada, embora fatores de implementação e constantes também influenciem os tempos observados [Cormen et al. 2022].')

para('A seção 2 apresenta a teoria; a seção 3 descreve a metodologia; a seção 4 discute os resultados; as seções 5 e 6 apresentam a conclusão e trabalhos futuros.')
H('2. Fundamentação Teórica')
H('2.1 Estruturas preservadas da Parte 1',2)
para('A versão base usa listas para produtos e fornecedores. Inserir ao final de uma lista dinâmica custa O(1) amortizado; buscar por código custa O(n); e remover custa O(n), pois é necessário localizar o registro e deslocar os seguintes [Goodrich et al. 2013]. Na versão otimizada, a lista de fornecedores foi mantida; a AVL substitui apenas o cadastro principal de produtos.')
para('O histórico é uma pilha com comportamento LIFO: registrar uma movimentação acrescenta um elemento ao topo e desfazer remove o último elemento, ambos em O(1) amortizado. A pilha foi preservada. Os dicionários continuam sendo apenas o formato dos registros, não substituindo as estruturas ou algoritmos implementados.')
H('2.2 Algoritmos da versão base',2)
para('<b>Busca sequencial.</b> Percorre os registros comparando o código de cada produto com a chave. O melhor caso é O(1), quando a chave está na primeira posição; o caso médio e o pior caso são O(n), inclusive quando a chave não existe.')
para('<b>Selection Sort.</b> Em cada posição, procura o menor elemento do trecho ainda não ordenado e o troca para a posição corrente. Realiza n(n−1)/2 comparações, portanto é O(n²) nos casos melhor, médio e pior. Não é estável [Goodrich et al. 2013].')
para('<b>Fila de prioridade da base.</b> Os produtos com estoque menor ou igual ao mínimo recebem prioridade 3 (estoque zerado), 2 (abaixo do mínimo) ou 1 (igual ao mínimo). A lista é reordenada por Selection Sort, com custo O(k²), e o atendimento remove o primeiro item, operação que desloca os demais e custa O(k).')
H('2.3 Árvore binária de busca AVL',2)
para('A AVL é uma árvore binária de busca auto-balanceável: chaves menores ficam à esquerda e maiores à direita. O fator de balanceamento é a altura esquerda menos a altura direita e deve permanecer entre −1 e +1. Rotações restauram essa condição após inserções ou remoções [Adelson-Velsky e Landis 1962; Andrade 2026b, 2026c]. Cada nó guarda o produto, os filhos e a altura.')
para('Na busca, compara-se a chave com o nó atual e segue-se para um dos filhos até encontrar a chave ou atingir um nó nulo. Na inserção, cria-se o nó na posição vazia e, no retorno da recursão, atualizam-se alturas e fatores. Na remoção, tratam-se folha, nó com um filho e nó com dois filhos; neste último caso, o sucessor em ordem substitui o nó removido. As quatro rotações possíveis são simples à direita, simples à esquerda, esquerda-direita e direita-esquerda. Cada rotação custa O(1); como a altura da AVL é O(log n), busca, inserção e remoção têm pior caso O(log n).')
H('2.4 Travessias',2)
para('Em ordem visita esquerda, nó e direita e produz chaves crescentes; pré-ordem visita o nó antes dos filhos, mostrando a hierarquia a partir da raiz; pós-ordem visita os filhos antes do nó. Cada travessia visita os n nós e custa O(n).')
H('2.5 Merge Sort',2)
para('O Merge Sort usa divisão e conquista: divide a sequência ao meio, ordena recursivamente as metades e intercala os resultados comparando os primeiros elementos disponíveis. O caso base é uma sequência com zero ou um elemento. Ao escolher o elemento da esquerda nos empates (comparação com ≤), o algoritmo é estável. Seu custo é O(n log n) nos casos melhor, médio e pior, com memória auxiliar O(n) [Cormen et al. 2022; Andrade 2026a]. No ERP, substitui o Selection Sort no relatório de produtos por estoque.')
H('2.6 Heap binário e fila de prioridade',2)
para('A fila de prioridade retira sempre o elemento de maior prioridade. O heap máximo é uma árvore binária completa armazenada em vetor, em que o pai tem prioridade não inferior à dos filhos. Para o índice i, o pai está em (i−1)//2 e os filhos em 2i+1 e 2i+2. Consultar o máximo custa O(1); inserir e remover a raiz custam O(log k), pois o elemento sobe ou desce pela altura do heap. Construir a fila por k inserções custa O(k log k) [Williams 1964; Cormen et al. 2022]. Na implementação, o desempate usa a posição equivalente à saída da versão base.')

H('3. Metodologia')
H('3.1 Preservação da versão base e preparação',2)
para('O código da Parte 1 foi mantido em versao_base/main.py e seu hash SHA-256 foi registrado. A base usa lista de produtos, busca sequencial, Selection Sort no relatório e na fila, além de lista de fornecedores e pilha. ' + escape(correcoes) + ' Repositório: <link href="https://github.com/kauanxxxx1/tde-2-estrutura-de-dados-e-algoritmos" color="black">https://github.com/kauanxxxx1/tde-2-estrutura-de-dados-e-algoritmos</link>.')
H('3.2 Etapas de evolução: decisões, dificuldades, soluções e validação',2)
H('3.2.1 Cadastro e AVL',2)
para('Após congelar e medir a base, o cadastro passou a usar ArvoreAVL. O desafio foi preservar os vínculos e alturas durante as rotações: atualizam-se primeiro os filhos, depois a altura do nó que desce e a do novo topo. Na remoção com dois filhos, utiliza-se o sucessor em ordem. O método validar() verifica chaves, alturas, quantidade e balanceamento; os testes cobrem as quatro rotações, duplicatas e remoções.')
H('3.2.2 Travessias e ordenação',2)
para('As travessias foram implementadas separadamente para evitar trocar a ordem das visitas. O teste confere a sequência crescente em ordem e a quantidade de elementos nas outras duas. O Merge Sort substitui o Selection Sort no relatório por estoque; a intercalação usa dois índices e copia os elementos restantes, evitando perdas. O teste verifica a ordem crescente e a sequência exata com estoques repetidos.')
H('3.2.3 Otimização adicional: heap binário',2)
para(f'Com 10.000 registros aleatórios, a base gastou {fmt(med("fila_prioridade_reconstrucao", "base"))} ms na reconstrução da fila e {fmt(med("listagem_ordenada", "base"))} ms na listagem. O heap foi escolhido para reduzir o custo quadrático da fila. Para preservar a ordem original dos empates, foram usadas posições calculadas com heaps auxiliares. Na fila final, a prioridade é seguida pela posição equivalente à base.')
H('3.2.4 Integração e validação',2)
para('O teste de equivalência verifica busca, remoção e a sequência completa do relatório e da fila, inclusive 120 casos adicionais com empates. A ordem de cadastro é recuperada por Merge Sort sobre o campo _ordem. Para reproduzir as trocas instáveis do Selection Sort sem executá-lo, agrupam-se as chaves ordenadas e consultam-se heaps de posições. Cada posição deslocada é reinserida no heap do seu grupo; posições antigas são descartadas. O custo permanece O(n log n), com memória O(n). A listagem em ordem da AVL é uma nova travessia exigida pelo enunciado.')
H('3.2.5 Pseudocódigo dos algoritmos',2)
P('AVL: buscar(chave): enquanto nó existir, retornar produto se igual; senão seguir filho esquerdo se menor, direito se maior. Inserir: criar nó na posição vazia; rejeitar duplicata; atualizar altura e balancear no retorno. Remover: localizar chave; substituir por filho único ou sucessor se houver dois filhos; balancear no retorno. Balancear: fator acima de 1 ou abaixo de −1 exige rotação simples ou dupla conforme fator do filho.','CodeSBC')
P('Travessias: se nó nulo, retornar; em ordem: esquerda, nó, direita; pré-ordem: nó, esquerda, direita; pós-ordem: esquerda, direita, nó.','CodeSBC')
P('Merge Sort: se tamanho ≤ 1, retornar lista; dividir ao meio; ordenar metades recursivamente; intercalar pelo menor estoque, escolhendo a esquerda em empate; copiar sobras. Empates: agrupar chaves ordenadas; para cada posição, retirar do heap do grupo a menor posição válida; trocar e reinserir a posição deslocada. Heap: inserir no fim e subir enquanto maior que o pai; remover raiz, mover último item para a raiz e descer pelo maior filho até restaurar a ordem.','CodeSBC')
H('3.3 Experimentos e reprodutibilidade',2)
para('O benchmark usa semente ' + escape(ambiente['semente']) + ', três volumes (100, 1.000 e 10.000), cenários aleatório, crescente e decrescente e ' + escape(ambiente['repeticoes']) + ' repetições. Ambas as versões recebem os mesmos dados. São medidos inserção, remoção e busca (amostras de 100 operações), listagem e reconstrução da fila com time.perf_counter [Python Software Foundation 2026]. A fila contém cerca de 10% de produtos elegíveis. As comparações de ordenação e fila incluem o preparo dos empates. O ambiente registrado em ambiente.txt é: ' + escape(ambiente['processador']) + '; memória: ' + escape(ambiente.get('memoria_total') or 'não informada') + '; sistema: ' + escape(ambiente['sistema']) + '; Python: ' + escape(ambiente['python'].split()[0]) + '. Para reproduzir, executar testes.py, teste_equivalencia.py e benchmark.py em experimentos/, conforme README, e depois gerar_relatorio.py.')

OPS = {'Busca existente': 'busca_existente', 'Busca inexistente': 'busca_inexistente', 'Listagem ordenada': 'listagem_ordenada', 'Inserção (100)': 'insercao_amostra_100', 'Remoção (100)': 'remocao_amostra_100', 'Reconstrução fila': 'fila_prioridade_reconstrucao'}
def timing(labels, cases):
    out = [['Operação','n / cenário','Base: média ± DP','Otim.: média ± DP','Ganho','Var. %']]
    fmt = lambda x: f'{x:.3f}'.replace('.', ',')
    for label in labels:
        for n, scenario in cases:
            op = OPS[label]
            b,o = [idx[n,scenario,op,v] for v in ('base','otimizada')]
            bm,om = float(b['media_ms']),float(o['media_ms'])
            out.append([label, str(n) if scenario=='aleatorio' else scenario, fmt(bm)+' ± '+fmt(float(b['desvio_padrao_ms'])),fmt(om)+' ± '+fmt(float(o['desvio_padrao_ms'])),fmt(bm/om),f'{(om/bm-1)*100:.1f}'.replace('.',',')])
    table(out,[3.0*cm,1.45*cm,3.1*cm,3.1*cm,1.35*cm,1.3*cm],7.6)
H('4. Resultados e Discussões')
para('Evidência de execução dos scripts (saídas lidas dos arquivos de terminal):')
P(evidencias(), 'CodeSBC')
para('As tabelas apresentam as medições de resultados.csv. O ganho é calculado como tempo da versão base dividido pelo tempo da versão otimizada; valores acima de 1 indicam vantagem da versão otimizada. DP indica desvio padrão; tempos em ms. A variação percentual é (otimizada − base) / base × 100.')
caption('Tabela 1. Tempos médios das operações principais no cenário aleatório.')
timing(['Busca existente', 'Busca inexistente', 'Listagem ordenada'], [(100, 'aleatorio'), (1000, 'aleatorio'), (10000, 'aleatorio')])
para('A Tabela 1 compara as buscas e a listagem. A AVL descarta um lado da árvore a cada nível; o Merge Sort reduz o crescimento quadrático para O(n log n), incluindo o ajuste dos empates.')
caption('Tabela 2. Tempos médios de inserção, remoção e reconstrução da fila no cenário aleatório.')
timing(['Inserção (100)', 'Remoção (100)', 'Reconstrução fila'], [(100, 'aleatorio'), (1000, 'aleatorio'), (10000, 'aleatorio')])
para('As razões das Tabelas 1 e 2 distinguem ganhos e perdas em cada volume. Estruturas mais complexas têm custos constantes de chamadas, alocação e balanceamento; a comparação inclui o preparo de empates.')
caption('Tabela 3. Comparações para n = 10.000 no cenário aleatório.')
data=[['Operação','Base','Otimizada','Redução']]
for op,label in [('busca_existente','Busca existente (100 consultas)'),('busca_inexistente','Busca inexistente (100 consultas)'),('listagem_ordenada','Listagem ordenada'),('fila_prioridade_reconstrucao','Fila de prioridade')]:
    b,o=comp(op,'base'),comp(op,'otimizada')
    data.append([label,fmt(b,0),fmt(o,0),fmt((1-o/b)*100,2)+'%'])
table(data,[5.0*cm,2.0*cm,2.0*cm,2.0*cm],8.2)
para('A Tabela 3 apresenta as comparações registradas: a busca percorre a lista na base, enquanto a AVL usa sua altura; a ordenação e a fila incluem o custo do tratamento dos empates na versão otimizada.')
caption('Tabela 4. Tempos médios nos cenários ordenado e inverso, n = 10.000.')
timing(['Inserção (100)', 'Busca existente', 'Busca inexistente', 'Remoção (100)', 'Reconstrução fila', 'Listagem ordenada'], [(10000, 'ordenado'), (10000, 'inverso')])
para('Os cenários crescente e decrescente testam a capacidade da AVL de evitar a degeneração em lista. A Tabela 4 permite comparar as operações sob essas condições; tempos absolutos pequenos são sensíveis à variação do ambiente.')

H('4.1 Evidência gráfica do crescimento',2)
para('As Figuras 1 a 3 apresentam os tempos do cenário aleatório em escala logarítmica nos dois eixos, evidenciando as diferenças de crescimento.')
for i, name, desc in [(1,'fig_lista.png','Listagem ordenada por estoque'),(2,'fig_busca.png','Busca inexistente'),(3,'fig_heap.png','Reconstrução da fila')]:
    story.append(KeepTogether([Image(str(ROOT/name),width=13.3*cm,height=13.3*cm*503/1152),Paragraph(f'Figura {i}. {desc} (escala logarítmica).',styles['CaptionSBC'])]))
H('4.2 Discussão individual das otimizações',2)
para('<b>Árvore AVL.</b> Para 10.000 registros, as 100 buscas inexistentes apresentam ' + resumo_tempo('busca_inexistente') + '; as 100 remoções apresentam ' + resumo_tempo('remocao_amostra_100') + '. A AVL reduz a busca linear para O(log n), ao custo de ponteiros, alturas e rotações.')
para('<b>Merge Sort.</b> Para 10.000 produtos, a listagem apresenta ' + resumo_tempo('listagem_ordenada') + '. O Merge Sort e os heaps auxiliares de posições preservam a sequência da base, incluindo empates, com custo O(n log n) e memória auxiliar O(n).')
para('<b>Heap binário.</b> Para 10.000 registros, a reconstrução apresenta ' + resumo_tempo('fila_prioridade_reconstrucao') + '. Para 100 registros: ' + resumo_tempo('fila_prioridade_reconstrucao',100) + '. A reconstrução inclui a travessia, o preparo dos empates e as inserções no heap. Seu custo é O(n + k log k), com k itens elegíveis.')
H('4.3 Teoria, prática, custos e limitações',2)
para('Os resultados acompanham as classes de complexidade esperadas: buscas e remoções na AVL dependem da altura O(log n); o Merge Sort reduz o número de comparações de quadrático para n log n; e o heap evita reordenar integralmente a fila por Selection Sort. Os tempos não coincidem exatamente com as curvas teóricas porque incluem alocação de objetos, chamadas de função, recursão, cópias e custo do interpretador.')
perdas = [(n, op) for n in (100,1000,10000) for op in OPS.values() if ganho(op,n) < 1]
rotulos = {v:k for k,v in OPS.items()}
para(('No cenário aleatório, a otimizada foi mais lenta em: ' + '; '.join(f'{rotulos[op]} (n={n})' for n,op in perdas) + '. ' if perdas else 'No cenário aleatório não foram observadas perdas de tempo médio. ') + 'A árvore e os heaps possuem custos constantes, alocação e manutenção de estruturas adicionais; o tratamento exato dos empates também aumenta o trabalho.')
para('A massa de dados para a fila contém cerca de 10% de produtos elegíveis. A ordenação foi medida nos três cenários. Buscas, inserções e remoções são amostras de 100 operações e não representam toda a interface do ERP, que também reconstrói a fila em atualizações. Os tempos podem variar entre máquinas e execuções.')

H('5. Conclusão')
para('O sistema passou a usar AVL manual, três travessias, Merge Sort e heap binário. Para 10.000 registros aleatórios, as razões base/otimizada de busca inexistente, listagem e fila foram, respectivamente, ' + ', '.join(fmt(ganho(op),2)+'×' for op in ('busca_inexistente','listagem_ordenada','fila_prioridade_reconstrucao')) + '. Razões acima de um indicam ganhos; abaixo de um indicam perdas. Os testes confirmam a equivalência da sequência dos empates nos casos avaliados.')
para('As funcionalidades de produtos, fornecedores, movimentação de estoque, histórico reversível, fila e relatórios foram mantidas na versão otimizada. As verificações cobrem rotações, remoções, busca, travessias, ordenação e prioridade, enquanto o teste de equivalência compara as duas versões sobre a mesma massa de dados. Os resultados se limitam ao ambiente registrado, aos três volumes, às cinco repetições e às amostras de 100 operações. Novos experimentos em outras máquinas e com métricas de memória podem ampliar a validade dos resultados.')

H('6. Trabalhos Futuros')
para('(1) Uma tabela hash manual para consulta de fornecedores por código atacaria a busca linear O(n); o ganho esperado no caso médio seria próximo de O(1), validado com colisões e diferentes fatores de carga. (2) Índices secundários para estoque mínimo e nome de produto reduziriam a necessidade de percorrer todos os produtos em filtros específicos; a validação compararia o custo de atualização dos índices com o tempo das consultas. (3) Uma árvore B ou B+ persistida em disco seria adequada a cadastros muito maiores que a memória disponível; o ganho seria avaliado por leituras e escritas de páginas e tempo de consulta.')

H('Referências')
refs=[
'ADELSON-VELSKY, G. M.; LANDIS, E. M. An algorithm for the organization of information. <i>Doklady Akademii Nauk SSSR</i>, v. 146, p. 263–266, 1962. (Tradução: <i>Soviet Mathematics Doklady</i>, v. 3, p. 1259–1263.)',
'ANDRADE, J. C. AED — Tema 6: Algoritmos de Ordenação — Parte 2. Material de aula. UNIFAN — Centro Universitário Nobre, 2026a.',
'ANDRADE, J. C. AED — Tema 7: Introdução a Árvores. Material de aula. UNIFAN — Centro Universitário Nobre, 2026b.',
'ANDRADE, J. C. AED — Tema 8: Árvores AVL — Revisado. Material de aula. UNIFAN — Centro Universitário Nobre, 2026c.',
'CORMEN, T. H. et al. <i>Introduction to Algorithms</i>. 4. ed. Cambridge: MIT Press, 2022.',
'GOODRICH, M. T.; TAMASSIA, R.; GOLDWASSER, M. H. <i>Data Structures and Algorithms in Python</i>. Hoboken: Wiley, 2013.',
'PYTHON SOFTWARE FOUNDATION. <i>time — Time access and conversions: perf_counter</i>. Python 3 Documentation, 2026. Disponível em: https://docs.python.org/3/library/time.html. Acesso em: 27 nov. 2026.',
'WILLIAMS, J. W. J. Algorithm 232: Heapsort. <i>Communications of the ACM</i>, v. 7, n. 6, p. 347–348, 1964.'
]
for r in refs: P(r,'RefSBC')

# Exportação editável: sem o arquivo do professor, recria-se a formatação SBC.
# Se sbc_template.docx estiver na raiz, ele será usado como documento de origem.
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from html.parser import HTMLParser

def exportar_editavel(elementos):
    modelo = ROOT/'sbc_template.docx'
    d = Document(str(modelo)) if modelo.exists() else Document()
    if modelo.exists():
        body = d._element.body
        for child in list(body):
            if child.tag != qn('w:sectPr'):
                body.remove(child)
    else:
        sec = d.sections[0]
        sec.page_width,sec.page_height = Cm(21),Cm(29.7)
        sec.top_margin,sec.bottom_margin = Cm(3.5),Cm(2.5)
        sec.left_margin,sec.right_margin = Cm(3),Cm(3)
    d.core_properties.title = 'Evolução e otimização de um ERP de varejo'
    d.core_properties.author = 'Gabriel Santos Silva, Kauan dos Reis Moreira, Leonardo Maltez'
    class Marcacao(HTMLParser):
        def __init__(self, par, st):
            super().__init__(convert_charrefs=True)
            self.par,self.st,self.bold,self.italic = par,st,False,False
        def handle_starttag(self, tag, attrs):
            if tag == 'br': self.par.add_run().add_break()
            if tag == 'b': self.bold=True
            if tag == 'i': self.italic=True
        def handle_endtag(self,tag):
            if tag == 'b': self.bold=False
            if tag == 'i': self.italic=False
        def handle_data(self, text):
            r=self.par.add_run(text)
            r.font.name = 'Arial' if self.st.name=='CaptionSBC' else ('Courier New' if self.st.name=='EmailSBC' else 'Times New Roman')
            r.font.size=Pt(self.st.fontSize)
            r.bold=self.bold or self.st.fontName in (FB,'Helvetica-Bold')
            r.italic=self.italic
    def add(el):
        if isinstance(el, Paragraph):
            st=el.style
            par=d.add_paragraph()
            par.alignment={TA_CENTER:WD_ALIGN_PARAGRAPH.CENTER,TA_JUSTIFY:WD_ALIGN_PARAGRAPH.JUSTIFY,TA_LEFT:WD_ALIGN_PARAGRAPH.LEFT}.get(st.alignment, WD_ALIGN_PARAGRAPH.LEFT)
            f=par.paragraph_format
            f.space_before=Pt(st.spaceBefore);f.space_after=Pt(st.spaceAfter)
            f.line_spacing=Pt(st.leading)
            if st.name=='CodeSBC': f.keep_together=True
            f.first_line_indent=Pt(st.firstLineIndent);f.left_indent=Pt(st.leftIndent);f.right_indent=Pt(st.rightIndent)
            f.keep_with_next=bool(getattr(st,'keepWithNext',False)) or (st.name=='CaptionSBC' and el.getPlainText().startswith('Tabela'))
            if st.name in ('TitleSBC','Authors','Affil','EmailSBC'): f.keep_with_next=True
            Marcacao(par,st).feed(el.text)
        elif isinstance(el, Table):
            vals=el._cellvalues
            t=d.add_table(rows=len(vals),cols=len(vals[0]));t.alignment=WD_TABLE_ALIGNMENT.LEFT;t.autofit=False
            for col,w in zip(t.columns,el._argW): col.width=Pt(w)
            for i,row in enumerate(vals):
                tr=t.rows[i]._tr.get_or_add_trPr();tr.append(OxmlElement('w:cantSplit'))
                if i==0: tr.append(OxmlElement('w:tblHeader'))
                for j,val in enumerate(row):
                    c=t.cell(i,j); c.width=Pt(el._argW[j]); par=c.paragraphs[0]
                    par.paragraph_format.space_after=Pt(0);par.paragraph_format.space_before=Pt(0);par.paragraph_format.line_spacing=Pt(9.5)
                    run=par.add_run(str(val));run.font.name='Times New Roman';run.font.size=Pt(8);run.bold=i==0
                    if i in (0,len(vals)-1):
                        borders=OxmlElement('w:tcBorders'); edge=OxmlElement('w:bottom');edge.set(qn('w:val'),'single');edge.set(qn('w:sz'),'4');borders.append(edge);c._tc.get_or_add_tcPr().append(borders)
        elif isinstance(el, KeepTogether):
            for sub in el._content: add(sub)
        elif isinstance(el, Image):
            par=d.add_paragraph();par.alignment=WD_ALIGN_PARAGRAPH.CENTER;par.paragraph_format.keep_with_next=True
            par.paragraph_format.space_after=Pt(0)
            par.add_run().add_picture(el.filename,width=Pt(el.drawWidth))
        elif isinstance(el, PageBreak): d.add_page_break()
    for e in elementos: add(e)
    d.save(ROOT/'relatorio_tecnico.docx')

exportar_editavel(story)

# Build PDF

doc.build(story)
print(OUT)
print('bytes',os.path.getsize(OUT))
