import json
import os
from datetime import datetime

ARQ_ESTOQUE = "estoque.json"
ARQ_MOVIMENTOS = "movimentacoes.json"


# ---------- Leitura e gravação ----------
def carregar(caminho, chave):
    if not os.path.exists(caminho):
        return []
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)[chave]


def salvar(caminho, chave, dados):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump({chave: dados}, f, ensure_ascii=False, indent=2)


# ---------- Entrada de dados ----------
def ler_inteiro(mensagem, minimo=None):
    while True:
        texto = input(mensagem).strip()
        try:
            valor = int(texto)
        except ValueError:
            print("  Digite um número inteiro válido.")
            continue
        if minimo is not None and valor < minimo:
            print(f"  O valor deve ser no mínimo {minimo}.")
            continue
        return valor


def buscar_produto(produtos, codigo):
    for p in produtos:
        if p["codigoProduto"] == codigo:
            return p
    return None


# ---------- Funcionalidades ----------
def listar_estoque(produtos):
    print(f"\n{'Código':<8}{'Produto':<30}{'Estoque':>8}")
    print("-" * 46)
    for p in produtos:
        print(f"{p['codigoProduto']:<8}{p['descricaoProduto']:<30}{p['estoque']:>8}")


def lancar_movimentacao(produtos, movimentos):
    listar_estoque(produtos)
    print()
    codigo = ler_inteiro("Código do produto: ")
    produto = buscar_produto(produtos, codigo)
    if produto is None:
        print("  Produto não encontrado.")
        return

    print(f"\nProduto: {produto['descricaoProduto']} (estoque atual: {produto['estoque']})")
    print("Tipo de movimentação:\n  1 - Entrada\n  2 - Saída")
    opcao = ler_inteiro("Escolha: ")
    if opcao not in (1, 2):
        print("  Opção inválida.")
        return
    tipo = "ENTRADA" if opcao == 1 else "SAIDA"

    quantidade = ler_inteiro("Quantidade: ", minimo=1)
    if tipo == "SAIDA" and quantidade > produto["estoque"]:
        print(f"  Estoque insuficiente! Disponível: {produto['estoque']}.")
        return

    descricao = input("Descrição da movimentação (ex.: compra, venda, devolução, perda): ").strip()
    if not descricao:
        descricao = "Entrada de mercadoria" if tipo == "ENTRADA" else "Saída de mercadoria"

    produto["estoque"] += quantidade if tipo == "ENTRADA" else -quantidade

    # ID único e sequencial, continuando a partir do último registrado
    novo_id = max((m["id"] for m in movimentos), default=0) + 1
    movimentos.append({
        "id": novo_id,
        "dataHora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "codigoProduto": produto["codigoProduto"],
        "descricaoProduto": produto["descricaoProduto"],
        "tipo": tipo,
        "descricao": descricao,
        "quantidade": quantidade,
        "estoqueFinal": produto["estoque"],
    })

    salvar(ARQ_ESTOQUE, "estoque", produtos)
    salvar(ARQ_MOVIMENTOS, "movimentacoes", movimentos)

    print("\n✔ Movimentação registrada!")
    print(f"  Nº da movimentação : {novo_id}")
    print(f"  Tipo               : {tipo} - {descricao}")
    print(f"  Produto            : {produto['descricaoProduto']}")
    print(f"  Quantidade final em estoque: {produto['estoque']}")


def listar_movimentos(movimentos):
    if not movimentos:
        print("\nNenhuma movimentação registrada ainda.")
        return
    print(f"\n{'Nº':<5}{'Data/Hora':<21}{'Prod.':<7}{'Tipo':<9}{'Qtde':>6}{'Final':>7}  Descrição")
    print("-" * 78)
    for m in movimentos:
        print(f"{m['id']:<5}{m['dataHora']:<21}{m['codigoProduto']:<7}{m['tipo']:<9}"
              f"{m['quantidade']:>6}{m['estoqueFinal']:>7}  {m['descricao']}")


def main():
    produtos = carregar(ARQ_ESTOQUE, "estoque")
    if not produtos:
        print(f"Arquivo {ARQ_ESTOQUE} não encontrado ou vazio.")
        return
    movimentos = carregar(ARQ_MOVIMENTOS, "movimentacoes")

    while True:
        print("\n=== CONTROLE DE ESTOQUE ===")
        print("1 - Lançar movimentação (entrada/saída)")
        print("2 - Consultar estoque")
        print("3 - Histórico de movimentações")
        print("0 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            lancar_movimentacao(produtos, movimentos)
        elif opcao == "2":
            listar_estoque(produtos)
        elif opcao == "3":
            listar_movimentos(movimentos)
        elif opcao == "0":
            print("Até logo!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
