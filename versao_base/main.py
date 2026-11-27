# ERP DE VAREJO - TDE Parte 1
# Algoritmos e Estruturas de Dados - 2026.2
#
#
#
# Declaração de autoria
# Autores: [Gabriel Santos Silva, Kauan Dos Reis Moreira, Leonardo Maltez]
# Declaro que este código foi desenvolvido por mim, com base no meu próprio
# entendimento e esforço. Não houve plágio ou cópia integral de terceiros.
# Ferramentas de IA, quando utilizadas, foram apenas como apoio ao aprendizado
# e não para a geração integral deste código.




produtos = []
fornecedores = []


historico = []


fila_reposicao = []


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
    for produto in produtos:
        if produto["codigo"] == codigo:
            return produto

    return None


def buscar_fornecedor(codigo):
    for fornecedor in fornecedores:
        if fornecedor["codigo"] == codigo:
            return fornecedor

    return None

def cadastrar_produto():
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
        "estoque_minimo": estoque_minimo
    }

    produtos.append(produto)

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

    posicao = -1

    for i in range(len(produtos)):
        if produtos[i]["codigo"] == codigo:
            posicao = i
            break

    if posicao == -1:
        print("Produto não encontrado.")
        return

    produto = produtos.pop(posicao)
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

    # Mostramos do topo para a base.
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
    fila_reposicao.clear()

    for produto in produtos:
        prioridade = calcular_prioridade(produto)

        if prioridade > 0:
            item = {
                "codigo": produto["codigo"],
                "nome": produto["nome"],
                "estoque": produto["estoque"],
                "prioridade": prioridade
            }

            fila_reposicao.append(item)

    for i in range(len(fila_reposicao)):
        maior = i

        for j in range(i + 1, len(fila_reposicao)):
            if fila_reposicao[j]["prioridade"] > fila_reposicao[maior]["prioridade"]:
                maior = j

        if maior != i:
            temp = fila_reposicao[i]
            fila_reposicao[i] = fila_reposicao[maior]
            fila_reposicao[maior] = temp


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

    item = fila_reposicao.pop(0)

    print("Produto selecionado para reposição:")
    print("Código:", item["codigo"])
    print("Produto:", item["nome"])
    print("Prioridade:", item["prioridade"])
    print("Estoque atual:", item["estoque"])


def produtos_ordenados_por_estoque():
    copia = []

    for produto in produtos:
        copia.append(produto)

    for i in range(len(copia)):
        menor = i

        for j in range(i + 1, len(copia)):
            if copia[j]["estoque"] < copia[menor]["estoque"]:
                menor = j

        if menor != i:
            temp = copia[i]
            copia[i] = copia[menor]
            copia[menor] = temp

    return copia


def relatorio_ordenado():
    print("\n  PRODUTOS ORDENADOS POR ESTOQUE  ")

    ordenados = produtos_ordenados_por_estoque()

    if len(ordenados) == 0:
        print("Nenhum produto cadastrado.")
        return

    for produto in ordenados:
        mostrar_produto(produto)


def filtrar_produtos():
    print("\n  FILTRAR PRODUTOS  ")

    print("1 - Estoque abaixo do mínimo")
    print("2 - Estoque igual ao mínimo")
    print("3 - Estoque acima do mínimo")

    opcao = input("Escolha: ")

    encontrou = False

    for produto in produtos:
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
