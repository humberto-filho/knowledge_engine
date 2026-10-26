import csv
MINUSCULAS = "abcdefghijklmnopqrstuvwxyz"
PERMITIDOS = MINUSCULAS + MINUSCULAS.upper() + "0123456789_"


def eh_simples(texto):
    if not texto or texto[0] not in MINUSCULAS:
        return False
    return all(c in PERMITIDOS for c in texto)


def remove_especiais(texto):
    return (
    texto.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n")
    .replace("\r", "\\r").replace("\t", "\\t")
    )


def valor(entrada):
    texto = str(entrada).strip()
    if eh_simples(texto):
        return texto
    return "'" + remove_especiais(texto) + "'"


def numero(valor):
    n = float(valor)
    return str(int(n)) if n == int(n) else str(n)


def data_hora(iso):
    data, hora = str(iso).split("T")
    ano, mes, dia = (int(p) for p in data.split("-"))
    h, mi, resto = hora.split(":")
    s = int(resto.split(".")[0])
    return f"data_hora({ano}, {mes}, {dia}, {int(h)}, {int(mi)}, {s})"

def preenche(texto):
    texto = str(texto).strip()
    if not texto or texto.lower() == "null":
        return "nao_informado"
    return texto

def main():
    fatos = []
    with open("pedidos_unificado.csv", newline="", encoding="utf-8") as f:
        for l in csv.DictReader(f):
            fatos.append(
                f"pedido({l['idPedido'].strip()}, "
                f"{data_hora(l['dtPedido'])}, "
                f"{valor(l['descUF'])}, "
                f"{preenche(l['flKetchup']).lower()}, "
                f"{valor(preenche(l['borda']))}, "
                f"{valor(preenche(l['massa']))}, "
                f"{valor(preenche(l['bebida']))}, "
                f"{l['qtdItens']}, "
                f"{numero(l['precoTotal'])}).")

    with open("base.pl", "w", encoding="utf-8") as f:
        f.write("\n".join(fatos) + "\n")
    print("Dados escritos em base.pl")

if __name__ == "__main__":
    main()