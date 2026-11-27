# ERP DE VAREJO - TDE Parte 2
# Algoritmos e Estruturas de Dados - 2026.2
#
#
#
# Autores: Gabriel Santos Silva, Kauan dos Reis Moreira e Leonardo Maltez
# Declaro que este código foi desenvolvido por mim, com base no meu próprio
# entendimento e esforço. Não houve plágio ou cópia integral de terceiros.
# Ferramentas de IA, quando utilizadas, foram apenas como apoio ao aprendizado
# e não para a geração integral deste código.






class NoAVL:
    def __init__(self, produto):
        self.produto = produto
        self.esquerda = None
        self.direita = None
        self.altura = 1


class ArvoreAVL:
    def __init__(self):
        self.raiz = None
        self.quantidade = 0
        self.comparacoes = 0

    def altura(self, no):
        if no is None:
            return 0
        return no.altura

    def atualizar_altura(self, no):
        esquerda = self.altura(no.esquerda)
        direita = self.altura(no.direita)
        no.altura = 1 + max(esquerda, direita)

    def fator_balanceamento(self, no):
        if no is None:
            return 0
        return self.altura(no.esquerda) - self.altura(no.direita)

    def rotacao_direita(self, y):
        x = y.esquerda
        subarvore = x.direita
        x.direita = y
        y.esquerda = subarvore
        self.atualizar_altura(y)
        self.atualizar_altura(x)
        return x

    def rotacao_esquerda(self, x):
        y = x.direita
        subarvore = y.esquerda
        y.esquerda = x
        x.direita = subarvore
        self.atualizar_altura(x)
        self.atualizar_altura(y)
        return y

    def _balancear(self, no):
        if no is None:
            return None
        self.atualizar_altura(no)
        fator = self.fator_balanceamento(no)
        if fator > 1:
            if self.fator_balanceamento(no.esquerda) < 0:
                no.esquerda = self.rotacao_esquerda(no.esquerda)
            return self.rotacao_direita(no)
        if fator < -1:
            if self.fator_balanceamento(no.direita) > 0:
                no.direita = self.rotacao_direita(no.direita)
            return self.rotacao_esquerda(no)
        return no

    def _inserir(self, no, produto):
        if no is None:
            return NoAVL(produto), True
        self.comparacoes += 1
        if produto['codigo'] < no.produto['codigo']:
            no.esquerda, inserido = self._inserir(no.esquerda, produto)
        elif produto['codigo'] > no.produto['codigo']:
            no.direita, inserido = self._inserir(no.direita, produto)
        else:
            return no, False
        if inserido:
            no = self._balancear(no)
        return no, inserido

    def inserir(self, produto):
        self.raiz, inserido = self._inserir(self.raiz, produto)
        if inserido:
            self.quantidade += 1
        return inserido

    def buscar(self, codigo):
        atual = self.raiz
        while atual is not None:
            self.comparacoes += 1
            if codigo == atual.produto['codigo']:
                return atual.produto
            if codigo < atual.produto['codigo']:
                atual = atual.esquerda
            else:
                atual = atual.direita
        return None

    def _menor_no(self, no):
        atual = no
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    def _remover(self, no, codigo):
        if no is None:
            return None, None
        self.comparacoes += 1
        if codigo < no.produto['codigo']:
            no.esquerda, removido = self._remover(no.esquerda, codigo)
        elif codigo > no.produto['codigo']:
            no.direita, removido = self._remover(no.direita, codigo)
        else:
            removido = no.produto
            if no.esquerda is None:
                return no.direita, removido
            if no.direita is None:
                return no.esquerda, removido
            sucessor = self._menor_no(no.direita)
            no.produto = sucessor.produto
            no.direita, _ = self._remover(no.direita, sucessor.produto['codigo'])
        if removido is None:
            return no, None
        return self._balancear(no), removido

    def remover(self, codigo):
        self.raiz, removido = self._remover(self.raiz, codigo)
        if removido is not None:
            self.quantidade -= 1
        return removido

    def _em_ordem(self, no):
        if no is not None:
            yield from self._em_ordem(no.esquerda)
            yield no.produto
            yield from self._em_ordem(no.direita)

    def _pre_ordem(self, no):
        if no is not None:
            yield no.produto
            yield from self._pre_ordem(no.esquerda)
            yield from self._pre_ordem(no.direita)

    def _pos_ordem(self, no):
        if no is not None:
            yield from self._pos_ordem(no.esquerda)
            yield from self._pos_ordem(no.direita)
            yield no.produto

    def __iter__(self):
        return self._em_ordem(self.raiz)

    def __len__(self):
        return self.quantidade

    def em_ordem(self):
        return list(self._em_ordem(self.raiz))

    def pre_ordem(self):
        return list(self._pre_ordem(self.raiz))

    def pos_ordem(self):
        return list(self._pos_ordem(self.raiz))

    def validar(self):
        def verificar(no, minimo, maximo):
            if no is None:
                return 0, 0, True
            codigo = no.produto['codigo']
            if (minimo is not None and codigo <= minimo) or (maximo is not None and codigo >= maximo):
                return 0, 0, False
            he, qe, ok_e = verificar(no.esquerda, minimo, codigo)
            hd, qd, ok_d = verificar(no.direita, codigo, maximo)
            altura_correta = 1 + max(he, hd)
            balanceada = abs(he - hd) <= 1
            return altura_correta, 1 + qe + qd, ok_e and ok_d and balanceada and no.altura == altura_correta
        _, quantidade, ok = verificar(self.raiz, None, None)
        return ok and quantidade == self.quantidade



class FilaPrioridade:
    def __init__(self):
        self.itens = []
        self.comparacoes = 0

    def __len__(self):
        return len(self.itens)

    def limpar(self):
        self.itens = []

    def _maior_prioridade(self, a, b):
        self.comparacoes += 1
        if a['prioridade'] != b['prioridade']:
            return a['prioridade'] > b['prioridade']
        return a['ordem'] < b['ordem']

    def inserir(self, item):
        self.itens.append(item)
        indice = len(self.itens) - 1
        while indice > 0:
            pai = (indice - 1) // 2
            if self._maior_prioridade(self.itens[indice], self.itens[pai]):
                self.itens[indice], self.itens[pai] = self.itens[pai], self.itens[indice]
                indice = pai
            else:
                break

    def remover(self):
        if len(self.itens) == 0:
            return None
        if len(self.itens) == 1:
            return self.itens.pop()
        maior = self.itens[0]
        self.itens[0] = self.itens.pop()
        indice = 0
        while True:
            esquerda = 2 * indice + 1
            direita = 2 * indice + 2
            maior_indice = indice
            if esquerda < len(self.itens) and self._maior_prioridade(self.itens[esquerda], self.itens[maior_indice]):
                maior_indice = esquerda
            if direita < len(self.itens) and self._maior_prioridade(self.itens[direita], self.itens[maior_indice]):
                maior_indice = direita
            if maior_indice == indice:
                break
            self.itens[indice], self.itens[maior_indice] = self.itens[maior_indice], self.itens[indice]
            indice = maior_indice
        return maior

    def em_ordem_prioridade(self):
        copia = FilaPrioridade()
        copia.itens = self.itens.copy()
        resultado = []
        while len(copia) > 0:
            resultado.append(copia.remover())
        return resultado

    def __iter__(self):
        return iter(self.em_ordem_prioridade())


comparacoes_merge_sort = 0

def merge_sort_produtos(lista, chave=lambda p: p['estoque']):
    global comparacoes_merge_sort
    if len(lista) <= 1:
        return lista[:]
    meio = len(lista) // 2
    esquerda = merge_sort_produtos(lista[:meio], chave)
    direita = merge_sort_produtos(lista[meio:], chave)
    resultado = []
    i = 0
    j = 0
    while i < len(esquerda) and j < len(direita):
        comparacoes_merge_sort += 1
        if chave(esquerda[i]) <= chave(direita[j]):
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1
    while i < len(esquerda):
        resultado.append(esquerda[i])
        i += 1
    while j < len(direita):
        resultado.append(direita[j])
        j += 1
    return resultado


def ordem_cadastro(registros):
    return merge_sort_produtos(list(registros), lambda p: p['_ordem'])


def reproduzir_empates_selecao(original, ordenados, chave):
    """Reproduz as trocas da seleção usando heaps de posições por chave.
    Descartam-se posições antigas quando já não pertencem ao grupo.
    """
    global comparacoes_merge_sort
    n = len(original)
    if n < 2:
        return original[:]
    grupos = [0] * n
    heaps = []
    sequencia = []
    anterior = None
    for posicao, item in ordenados:
        valor = chave(item)
        if not heaps or valor != anterior:
            heaps.append(FilaPrioridade())
            anterior = valor
        grupo = len(heaps) - 1
        grupos[posicao] = grupo
        sequencia.append(grupo)
        heaps[grupo].inserir({'prioridade': -posicao, 'ordem': 0})
    saida = original[:]
    for i, grupo in enumerate(sequencia):
        if grupos[i] == grupo:
            continue
        heap = heaps[grupo]
        while True:
            j = -heap.remover()['prioridade']
            if j >= i and grupos[j] == grupo:
                break
        deslocado = grupos[i]
        saida[i], saida[j] = saida[j], saida[i]
        grupos[i], grupos[j] = grupos[j], grupos[i]
        heaps[deslocado].inserir({'prioridade': -j, 'ordem': 0})
    comparacoes_merge_sort += sum(h.comparacoes for h in heaps)
    return saida


comparacoes_fila_preparo = 0


produtos = ArvoreAVL()
fornecedores = []


historico = []


fila_reposicao = FilaPrioridade()
proxima_ordem_produto = 0


def ler_inteiro(mensagem, minimo=None):
    while True:
        try:
            valor = int(input(mensagem))

            if minimo is not None and valor < minimo:
                print("Digite um valor maior ou igual a", minimo)
                continue

            return valor

        except ValueError:
            print("Digite um número inteiro válido.")


def ler_float(mensagem, minimo=None):
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))

            if minimo is not None and valor < minimo:
                print("Digite um valor maior ou igual a", minimo)
                continue

            return valor

        except ValueError:
            print("Digite um número válido.")


def ler_texto(mensagem):
    while True:
        valor = input(mensagem).strip()

        if valor != "":
            return valor

        print("Este campo é obrigatório.")


def buscar_produto(codigo):
    return produtos.buscar(codigo)


def buscar_fornecedor(codigo):
    for fornecedor in fornecedores:
        if fornecedor["codigo"] == codigo:
            return fornecedor

    return None

def cadastrar_produto():
    global proxima_ordem_produto
    print("\n CADASTRAR PRODUTO ")

    codigo = ler_inteiro("Código: ", 1)

    if buscar_produto(codigo) is not None:
        print("Já existe um produto com esse código.")
        return

    nome = ler_texto("Nome: ")
    preco = ler_float("Preço: R$ ", 0)
    estoque = ler_inteiro("Quantidade em estoque: ", 0)
    estoque_minimo = ler_inteiro("Estoque mínimo: ", 0)

    produto = {
        "codigo": codigo,
        "nome": nome,
        "preco": preco,
        "estoque": estoque,
        "estoque_minimo": estoque_minimo,
        "_ordem": proxima_ordem_produto
    }
    proxima_ordem_produto += 1

    produtos.inserir(produto)

    atualizar_fila_reposicao()

    print("Produto cadastrado com sucesso.")


def consultar_produto():
    print("\n CONSULTAR PRODUTO ")

    codigo = ler_inteiro("Código do produto: ", 1)
    produto = buscar_produto(codigo)

    if produto is None:
        print("Produto não encontrado.")
        return

    mostrar_produto(produto)


def alterar_produto():
    print("\n ALTERAR PRODUTO ")

    codigo = ler_inteiro("Código do produto: ", 1)
    produto = buscar_produto(codigo)

    if produto is None:
        print("Produto não encontrado.")
        return

    print("Deixe o campo vazio para manter o valor atual.")

    nome = input("Nome [" + produto["nome"] + "]: ").strip()
    if nome != "":
        produto["nome"] = nome

    preco_texto = input(
        "Preço [" + format(produto["preco"], ".2f") + "]: "
    ).strip()

    if preco_texto != "":
        try:
            preco = float(preco_texto.replace(",", "."))
            if preco < 0:
                print("Preço inválido. Valor anterior mantido.")
            else:
                produto["preco"] = preco
        except ValueError:
            print("Preço inválido. Valor anterior mantido.")

    estoque_texto = input(
        "Estoque [" + str(produto["estoque"]) + "]: "
    ).strip()

    if estoque_texto != "":
        try:
            estoque = int(estoque_texto)
            if estoque < 0:
                print("Estoque inválido. Valor anterior mantido.")
            else:
                produto["estoque"] = estoque
        except ValueError:
            print("Estoque inválido. Valor anterior mantido.")

    minimo_texto = input(
        "Estoque mínimo [" + str(produto["estoque_minimo"]) + "]: "
    ).strip()

    if minimo_texto != "":
        try:
            estoque_minimo = int(minimo_texto)
            if estoque_minimo < 0:
                print("Estoque mínimo inválido. Valor anterior mantido.")
            else:
                produto["estoque_minimo"] = estoque_minimo
        except ValueError:
            print("Estoque mínimo inválido. Valor anterior mantido.")

    atualizar_fila_reposicao()
    print("Produto alterado com sucesso.")


def remover_produto():
    print("\n  REMOVER PRODUTO ")

    codigo = ler_inteiro("Código do produto: ", 1)

    produto = produtos.remover(codigo)
    if produto is None:
        print("Produto não encontrado.")
        return

    atualizar_fila_reposicao()

    print("Produto removido:", produto["nome"])


def listar_produtos():
    print("\n  LISTA DE PRODUTOS  ")

    if len(produtos) == 0:
        print("Nenhum produto cadastrado.")
        return

    for produto in produtos:
        mostrar_produto(produto)


def mostrar_produto(produto):
    print(
        "Código:", produto["codigo"],
        "| Nome:", produto["nome"],
        "| Preço: R$", format(produto["preco"], ".2f"),
        "| Estoque:", produto["estoque"],
        "| Mínimo:", produto["estoque_minimo"]
    )

def cadastrar_fornecedor():
    print("\n  CADASTRAR FORNECEDOR  ")

    codigo = ler_inteiro("Código: ", 1)

    if buscar_fornecedor(codigo) is not None:
        print("Já existe um fornecedor com esse código.")
        return

    nome = ler_texto("Nome: ")
    cnpj = ler_texto("CNPJ: ")
    telefone = ler_texto("Telefone: ")

    fornecedor = {
        "codigo": codigo,
        "nome": nome,
        "cnpj": cnpj,
        "telefone": telefone
    }

    fornecedores.append(fornecedor)

    print("Fornecedor cadastrado com sucesso.")


def consultar_fornecedor():
    print("\n  CONSULTAR FORNECEDOR  ")

    codigo = ler_inteiro("Código do fornecedor: ", 1)
    fornecedor = buscar_fornecedor(codigo)

    if fornecedor is None:
        print("Fornecedor não encontrado.")
        return

    mostrar_fornecedor(fornecedor)


def alterar_fornecedor():
    print("\n  ALTERAR FORNECEDOR  ")

    codigo = ler_inteiro("Código do fornecedor: ", 1)
    fornecedor = buscar_fornecedor(codigo)

    if fornecedor is None:
        print("Fornecedor não encontrado.")
        return

    print("Deixe o campo vazio para manter o valor atual.")

    nome = input("Nome [" + fornecedor["nome"] + "]: ").strip()
    if nome != "":
        fornecedor["nome"] = nome

    cnpj = input("CNPJ [" + fornecedor["cnpj"] + "]: ").strip()
    if cnpj != "":
        fornecedor["cnpj"] = cnpj

    telefone = input(
        "Telefone [" + fornecedor["telefone"] + "]: "
    ).strip()

    if telefone != "":
        fornecedor["telefone"] = telefone

    print("Fornecedor alterado com sucesso.")


def remover_fornecedor():
    print("\n  REMOVER FORNECEDOR   ")

    codigo = ler_inteiro("Código do fornecedor: ", 1)

    posicao = -1

    for i in range(len(fornecedores)):
        if fornecedores[i]["codigo"] == codigo:
            posicao = i
            break

    if posicao == -1:
        print("Fornecedor não encontrado.")
        return

    fornecedor = fornecedores.pop(posicao)

    print("Fornecedor removido:", fornecedor["nome"])


def listar_fornecedores():
    print("\n  LISTA DE FORNECEDORES  ")

    if len(fornecedores) == 0:
        print("Nenhum fornecedor cadastrado.")
        return

    for fornecedor in fornecedores:
        mostrar_fornecedor(fornecedor)


def mostrar_fornecedor(fornecedor):
    print(
        "Código:", fornecedor["codigo"],
        "| Nome:", fornecedor["nome"],
        "| CNPJ:", fornecedor["cnpj"],
        "| Telefone:", fornecedor["telefone"]
    )

def registrar_movimento(tipo, produto, quantidade):
    movimento = {
        "tipo": tipo,
        "codigo": produto["codigo"],
        "nome": produto["nome"],
        "quantidade": quantidade
    }

    historico.append(movimento)


def mostrar_historico():
    print("\n HISTÓRICO DA PILHA ")

    if len(historico) == 0:
        print("Nenhuma movimentação registrada.")
        return

   
    i = len(historico) - 1

    while i >= 0:
        movimento = historico[i]

        print(
            "Movimento:", movimento["tipo"],
            "| Produto:", movimento["nome"],
            "| Quantidade:", movimento["quantidade"]
        )

        i -= 1


def desfazer_ultima_movimentacao():
    print("\n DESFAZER ÚLTIMA MOVIMENTAÇÃO")

    if len(historico) == 0:
        print("Não existe movimentação para desfazer.")
        return

    movimento = historico.pop()

    produto = buscar_produto(movimento["codigo"])

    if produto is None:
        print("O produto dessa movimentação não existe mais.")
        return

    if movimento["tipo"] == "ENTRADA":
        produto["estoque"] -= movimento["quantidade"]

    elif movimento["tipo"] == "SAIDA":
        produto["estoque"] += movimento["quantidade"]

    atualizar_fila_reposicao()

    print("Última movimentação desfeita.")
    print("Produto:", produto["nome"])
    print("Estoque atual:", produto["estoque"])

def entrada_estoque():
    print("\n    ENTRADA DE ESTOQUE    ")

    codigo = ler_inteiro("Código do produto: ", 1)
    produto = buscar_produto(codigo)

    if produto is None:
        print("Produto não encontrado.")
        return

    quantidade = ler_inteiro("Quantidade de entrada: ", 1)

    produto["estoque"] += quantidade

    registrar_movimento("ENTRADA", produto, quantidade)
    atualizar_fila_reposicao()

    print("Entrada registrada.")
    print("Estoque atual:", produto["estoque"])


def saida_estoque():
    print("\n   SAÍDA DE ESTOQUE    ")

    codigo = ler_inteiro("Código do produto: ", 1)
    produto = buscar_produto(codigo)

    if produto is None:
        print("Produto não encontrado.")
        return

    quantidade = ler_inteiro("Quantidade de saída: ", 1)

    if quantidade > produto["estoque"]:
        print("Estoque insuficiente.")
        return

    produto["estoque"] -= quantidade

    registrar_movimento("SAIDA", produto, quantidade)
    atualizar_fila_reposicao()

    print("Saída registrada.")
    print("Estoque atual:", produto["estoque"])

def calcular_prioridade(produto):
    estoque = produto["estoque"]
    minimo = produto["estoque_minimo"]

    if estoque == 0:
        return 3

    if estoque < minimo:
        return 2

    if estoque == minimo:
        return 1

    return 0


def atualizar_fila_reposicao():
    global comparacoes_merge_sort, comparacoes_fila_preparo
    fila_reposicao.limpar()
    comparacoes_merge_sort = 0
    candidatos = []
    for produto in produtos:
        if calcular_prioridade(produto) > 0:
            candidatos.append(produto)
    originais = ordem_cadastro(candidatos)
    itens = [{"codigo": p["codigo"], "nome": p["nome"],
              "estoque": p["estoque"], "prioridade": calcular_prioridade(p)}
             for p in originais]
    grupos = [[], [], []]
    for i, item in enumerate(itens):
        grupos[3 - item['prioridade']].append((i, item))
    ordenados = grupos[0] + grupos[1] + grupos[2]
    exatos = reproduzir_empates_selecao(itens, ordenados,
                                        lambda item: -item['prioridade'])
    comparacoes_fila_preparo = comparacoes_merge_sort
    for ordem, item in enumerate(exatos):
        item['ordem'] = ordem
        fila_reposicao.inserir(item)


def mostrar_fila_prioridade():
    print("\n   FILA DE PRIORIDADE  ")

    atualizar_fila_reposicao()

    if len(fila_reposicao) == 0:
        print("Nenhum produto precisa de reposição.")
        return

    for item in fila_reposicao:
        print(
            "Prioridade:", item["prioridade"],
            "| Código:", item["codigo"],
            "| Produto:", item["nome"],
            "| Estoque:", item["estoque"]
        )


def processar_reposicao():
    print("\n   PROCESSAR REPOSIÇÃO  ")

    atualizar_fila_reposicao()

    if len(fila_reposicao) == 0:
        print("Nenhum produto na fila.")
        return

    item = fila_reposicao.remover()

    print("Produto selecionado para reposição:")
    print("Código:", item["codigo"])
    print("Produto:", item["nome"])
    print("Prioridade:", item["prioridade"])
    print("Estoque atual:", item["estoque"])


def produtos_ordenados_por_estoque():
    global comparacoes_merge_sort
    comparacoes_merge_sort = 0
    original = ordem_cadastro(produtos)
    ordenados = merge_sort_produtos(list(enumerate(original)),
                                    lambda par: par[1]['estoque'])
    return reproduzir_empates_selecao(original, ordenados,
                                       lambda p: p['estoque'])


def relatorio_ordenado():
    print("\n  PRODUTOS ORDENADOS POR ESTOQUE  ")

    ordenados = produtos_ordenados_por_estoque()

    if len(ordenados) == 0:
        print("Nenhum produto cadastrado.")
        return

    for produto in ordenados:
        mostrar_produto(produto)


def listar_produtos_pre_ordem():
    print("\n  PRODUTOS EM PRE-ORDEM  ")
    if len(produtos) == 0:
        print("Nenhum produto cadastrado.")
        return
    for produto in produtos.pre_ordem():
        mostrar_produto(produto)


def listar_produtos_pos_ordem():
    print("\n  PRODUTOS EM POS-ORDEM  ")
    if len(produtos) == 0:
        print("Nenhum produto cadastrado.")
        return
    for produto in produtos.pos_ordem():
        mostrar_produto(produto)


def filtrar_produtos():
    print("\n  FILTRAR PRODUTOS  ")

    print("1 - Estoque abaixo do mínimo")
    print("2 - Estoque igual ao mínimo")
    print("3 - Estoque acima do mínimo")

    opcao = input("Escolha: ")

    encontrou = False

    for produto in ordem_cadastro(produtos):
        mostrar = False

        if opcao == "1":
            if produto["estoque"] < produto["estoque_minimo"]:
                mostrar = True

        elif opcao == "2":
            if produto["estoque"] == produto["estoque_minimo"]:
                mostrar = True

        elif opcao == "3":
            if produto["estoque"] > produto["estoque_minimo"]:
                mostrar = True

        else:
            print("Opção inválida.")
            return

        if mostrar:
            mostrar_produto(produto)
            encontrou = True

    if not encontrou:
        print("Nenhum produto encontrado nesse filtro.")

def menu_produtos():
    while True:
        
        print("\n          MENU DE PRODUTOS")
        print("1 - Cadastrar produto")
        print("2 - Consultar produto")
        print("3 - Alterar produto")
        print("4 - Remover produto")
        print("5 - Listar produtos")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar_produto()
        elif opcao == "2":
            consultar_produto()
        elif opcao == "3":
            alterar_produto()
        elif opcao == "4":
            remover_produto()
        elif opcao == "5":
            listar_produtos()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


def menu_fornecedores():
    while True:
        print("     MENU DE FORNECEDORES")
        print("1 - Cadastrar fornecedor")
        print("2 - Consultar fornecedor")
        print("3 - Alterar fornecedor")
        print("4 - Remover fornecedor")
        print("5 - Listar fornecedores")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar_fornecedor()
        elif opcao == "2":
            consultar_fornecedor()
        elif opcao == "3":
            alterar_fornecedor()
        elif opcao == "4":
            remover_fornecedor()
        elif opcao == "5":
            listar_fornecedores()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


def menu_estoque():
    while True:
        print("     MOVIMENTAÇÃO DE ESTOQUE")
        print("1 - Entrada de estoque")
        print("2 - Saída de estoque")
        print("3 - Histórico")
        print("4 - Desfazer última movimentação")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            entrada_estoque()
        elif opcao == "2":
            saida_estoque()
        elif opcao == "3":
            mostrar_historico()
        elif opcao == "4":
            desfazer_ultima_movimentacao()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


def menu_prioridade():
    while True:
        print("       FILA DE PRIORIDADE")
        print("1 - Exibir fila")
        print("2 - Processar próxima reposição")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            mostrar_fila_prioridade()
        elif opcao == "2":
            processar_reposicao()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


def menu_relatorios():
    while True:
        print("          RELATÓRIOS")
        print("1 - Listar todos os produtos")
        print("2 - Filtrar produtos")
        print("3 - Exibir fila de prioridade")
        print("4 - Exibir histórico da pilha")
        print("5 - Produtos ordenados por estoque")
        print("6 - Listar fornecedores")
        print("7 - Produtos em pré-ordem")
        print("8 - Produtos em pós-ordem")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            listar_produtos()
        elif opcao == "2":
            filtrar_produtos()
        elif opcao == "3":
            mostrar_fila_prioridade()
        elif opcao == "4":
            mostrar_historico()
        elif opcao == "5":
            relatorio_ordenado()
        elif opcao == "6":
            listar_fornecedores()
        elif opcao == "7":
            listar_produtos_pre_ordem()
        elif opcao == "8":
            listar_produtos_pos_ordem()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


def menu_principal():
    while True:
        print("\n")
        print("          ERP - LOJA VAREJISTA")
        print("1 - Gerenciar produtos")
        print("2 - Gerenciar fornecedores")
        print("3 - Movimentação de estoque")
        print("4 - Fila de prioridade")
        print("5 - Buscar produto")
        print("6 - Relatórios")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_produtos()

        elif opcao == "2":
            menu_fornecedores()

        elif opcao == "3":
            menu_estoque()

        elif opcao == "4":
            menu_prioridade()

        elif opcao == "5":
            consultar_produto()

        elif opcao == "6":
            menu_relatorios()

        elif opcao == "0":
            print("Programa encerrado.")
            break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu_principal()
