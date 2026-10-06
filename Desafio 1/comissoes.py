import json
import sys
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP


def calcular_comissao(valor: Decimal) -> Decimal:
    """Regra de comissão por venda."""
    if valor < Decimal("100"):
        return Decimal("0")
    if valor < Decimal("500"):
        return valor * Decimal("0.01")
    return valor * Decimal("0.05")


def formatar(valor: Decimal) -> str:
    """Formata no padrão brasileiro: R$ 1.234,56"""
    texto = f"{valor.quantize(Decimal('0.01'), ROUND_HALF_UP):,.2f}"
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


def main(caminho: str) -> None:
    with open(caminho, encoding="utf-8") as f:
        # parse_float=Decimal evita erros de arredondamento com dinheiro
        dados = json.load(f, parse_float=Decimal)

    total_vendido = defaultdict(Decimal)
    total_comissao = defaultdict(Decimal)

    for venda in dados["vendas"]:
        nome = venda["vendedor"]
        valor = Decimal(venda["valor"])
        total_vendido[nome] += valor
        total_comissao[nome] += calcular_comissao(valor)

    print(f"{'Vendedor':<18}{'Total vendido':>18}{'Comissão':>16}")
    print("-" * 52)
    for nome in total_vendido:
        print(f"{nome:<18}{formatar(total_vendido[nome]):>18}"
              f"{formatar(total_comissao[nome]):>16}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "vendas.json")
