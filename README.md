# knowledge_engine

### Participantes

- Humberto Filho Castello Branco Lages Rebello e Castro

### Dataset

https://www.kaggle.com/datasets/teocalvo/pizzaquery

### Construção da base de conhecimento

O dataset disponível no Kaggle é resultado de uma pesquisa realizada pelo YouTuber Téo Calvo, do canal “Téo Me Why”, com o objetivo de identificar os sabores de pizza favoritos de sua audiência. Antes da publicação, os dados foram preparados e organizados em um data lake.

O dataset original é composto por três tabelas relacionadas, que são:
```
produto (85)                pedido (1.106)
descItem ─────────────┐     idPedido ──────────────┐
vlPreco               │     dtPedido               │ 1 : N
                      └───── descItem  item_pedido  idPedido
                             descTipoItem  (10.484)
```
Com os datasets originais do Kaggle são produto.csv, pedido.csv, item_pedido.csv.

A partir disso foi criado o "pedidos_unificado.csv" a partir das três tabelas para respeitar o pedido no enunciado de uma tabela única com uma linha por pedido e nove campos, mesclando variáveis qualitativas e quantitativas.

Suas colunas são dadas por: "idPedido,dtPedido,descUF,flKetchup,borda,massa,bebida,qtdItens,precoTotal"

Com idPedido sendo o identificador, dtPedido a data do pedido, descUF a unidade federativa em que o pedido foi feito. O flKetchup é binário, sendo se tem ketchup ou não (ou não informado, mas isso é tratado depois, na conversão). A borda que é o tipo da borda. A massa que é o tipo da massa da pizza, a bebida que é a bebida pedida. O qtdItens tem a quantidade de itens do pedido. E o precoTotal que é a soma dos preços dos itens (via produto).

### Script para geração da Base de Conhecimento

O script "unifica.py" unifica as três tabelas no "pedidos_unificado.csv", convertendo suas tabelas para uma tabela única de modo a respeitar o enunciado da APS. Esse script lê o cardápio "produto.csv", percorre o "item_pedido.csv" acumulando por pedido a borda, a massa e a bebida escolhidas, a quantidade de itens e a soma de preços e, por fim, os junta com "pedido.csv", gravando em "pedidos_unificado.csv".

O script "gera_base.py" converte cada linha em um fato Prolog. Primeiro, foi realizada uma preparação dos dados para organizá-los de forma que fosse possível realizar consultas em Prolog. Nesse script foi usada a função "eh_simples()" para verificar se é um átomo válido sem aspas. O resultado é usado pela função "valor()" que caso o texto seja simples ele retorna diretamente e, caso contrário, é colocado entre aspas simples após passar por "remove_especiais()",  que escapa os caracteres especiais com barra invertida e transforma as quebras de linha reais em "\n". Ademais é criada a função "numero()" que escolhe o formato numérico a se utilizar, com "3.0" -> "3", enquanto "2.5" -> "2.5". A função "data_hora()" converte de iso para o padrão pedido e, ao final, a função "main()" transforma cada linha do unificado em:
```
pedido(Id, data_hora(Ano, Mes, Dia, Hora, Min, Seg), UF, Ketchup, Borda, Massa, Bebida, QtdItens, PrecoTotal).
```
A função "preenche()" remove os null e coloca "nao_informado" para não haver células vazias.

### Como rodar

Crie um Notebook no site https://swish.swi-prolog.org/ com a base.pl no Program e uma célula com a Query na célula subsequente. Pode ser necessário adicionar ao Program uma regra, mas isso será explicitado na seção subsequente. Para criar a base.pl você roda unifica.py e depois o gera_base.py.

### Perguntas a se fazer com queries em Prolog

Perguntas:

1. Qual o preço médio dos pedidos de um estado? 
2. Qual o estado que mais pede ketchup na pizza? 
3. Qual foi o pedido mais caro de um estado?

Pergunta 1:

Program:
```
preco_medio_uf(UF, Media) :-
    findall(T, pedido(_, _, UF, _, _, _, _, _, T), Totais),
    sum_list(Totais, Soma),
    length(Totais, N),
    Media is Soma / N.
```
Query:
``` 
?- preco_medio_uf('São Paulo', M).
```
Esperado:
M = 44.77 (aproximadamente)

Pergunta 2:
Program:
```
ketchup_por_uf(UF, Quantidade) :-
    setof(U, I^pedido(I, _, U, true, _, _, _, _, _), UFs),
    member(UF, UFs),
    findall(Id, pedido(Id, _, UF, true, _, _, _, _, _), Ids),
    length(Ids, Quantidade).

uf_mais_ketchup(UF, Quantidade) :-
    findall(Q-U, ketchup_por_uf(U, Q), Pares),
    sort(Pares, Ordenados),
    reverse(Ordenados, [Quantidade-UF | _]).
``` 
Query:
```
?- uf_mais_ketchup(UF, Q).
```
Esperado:
Q = 124
UF = 'São Paulo'

Pergunta 3:
Program:
```
pedido_mais_caro_uf(UF, Id, Total) :-
    findall(T-I, pedido(I, _, UF, _, _, _, _, _, T), Pares),
    sort(Pares, Ordenados),
    reverse(Ordenados, [Total-Id | _]).
```

Query:
```
?- pedido_mais_caro_uf('São Paulo', Id, Total).
```
Esperado:
Id = 478
Total = 67

É feita o Program que é colocado na célula Program para indicar uma regra e a query numa célula Query no SWISH. Lembre-se de colocar o Program antes da Query.

