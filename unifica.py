import csv

precos = {}
with open("produto.csv", newline="", encoding="utf-8") as f:
    for linha in csv.DictReader(f):
        precos[linha["descItem"]] = float(linha["vlPreco"])

borda, massa, bebida = {}, {}, {}
qtd, total = {}, {}
with open("item_pedido.csv", newline="", encoding="utf-8") as f:
    for linha in csv.DictReader(f):
        idPedido = linha["idPedido"]
        tipo = linha["descTipoItem"]
        item = linha["descItem"]
        qtd[idPedido] = qtd.get(idPedido, 0) + 1
        total[idPedido] = round(total.get(idPedido, 0) + precos[item], 2)
        if tipo == "borda":
            borda[idPedido] = item
        elif tipo == "massa":
            massa[idPedido] = item
        elif tipo == "bebida":
            bebida[idPedido] = item

campos = ["idPedido", "dtPedido", "descUF", "flKetchup", "borda", "massa", "bebida", "qtdItens", "precoTotal"]

with open("pedido.csv", newline="", encoding="utf-8") as f:
    linhas_saida = []
    for linha in csv.DictReader(f):
        idPedido = linha["idPedido"]
        linhas_saida.append([idPedido, linha["dtPedido"], linha["descUF"],
        linha["flKetchup"],
        borda.get(idPedido, ""), massa.get(idPedido, ""),
        bebida.get(idPedido, ""),
        qtd.get(idPedido, 0), total.get(idPedido, 0)])

with open("pedidos_unificado.csv", "w", newline="", encoding="utf-8") as out:
    w = csv.writer(out)
    w.writerow(campos)
    w.writerows(linhas_saida)

print(f"OK: {len(linhas_saida)} pedidos escritos em 'pedidos_unificado.csv'")