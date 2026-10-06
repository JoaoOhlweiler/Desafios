from datetime import date, datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

TAXA_DIARIA = Decimal("0.025")  # 2,5% ao dia (juros simples)


def formatar(valor: Decimal) -> str:
    """Formata no padrão brasileiro: R$ 1.234,56"""
    texto = f"{valor.quantize(Decimal('0.01'), ROUND_HALF_UP):,.2f}"
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


def calcular_juros(valor: Decimal, vencimento: date, hoje: date = None):
    """Retorna (dias_de_atraso, juros). Sem atraso, os juros são zero."""
    hoje = hoje or date.today()
    dias = max((hoje - vencimento).days, 0)
    juros = valor * TAXA_DIARIA * dias
    return dias, juros


def ler_valor() -> Decimal:
    while True:
        texto = input("Valor (ex.: 1500,00): R$ ").strip()
        texto = texto.replace("R$", "").replace(" ", "")
        # aqui faz com que aceite "1.500,00" e "1500,00" e "1500.00"
        if "," in texto:
            texto = texto.replace(".", "").replace(",", ".")
        try:
            valor = Decimal(texto)
            if valor > 0:
                return valor
        except InvalidOperation:
            pass
        print("  Valor inválido. Digite um número maior que zero.")
        #0 não é aceito


def ler_data() -> date:
    while True:
        texto = input("Data de vencimento (dd/mm/aaaa): ").strip()
        try:
            return datetime.strptime(texto, "%d/%m/%Y").date()
        except ValueError:
            print("  Data inválida. Use o formato dd/mm/aaaa.")


def main():
    print("=== CÁLCULO DE JUROS POR ATRASO ===\n")
    valor = ler_valor()
    vencimento = ler_data()
    hoje = date.today()

    dias, juros = calcular_juros(valor, vencimento, hoje)

    print(f"\nData de hoje      : {hoje.strftime('%d/%m/%Y')}")
    print(f"Vencimento        : {vencimento.strftime('%d/%m/%Y')}")
    print(f"Valor original    : {formatar(valor)}")
    if dias == 0:
        print("\nConta sem atraso: não há juros a cobrar.")
        return
    print(f"Dias em atraso    : {dias}")
    print(f"Juros ({TAXA_DIARIA * 100:.1f}% ao dia): {formatar(juros)}")
    print(f"Total a pagar     : {formatar(valor + juros)}")


if __name__ == "__main__":
    main()
