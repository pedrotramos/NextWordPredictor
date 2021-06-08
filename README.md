# Preditor de próxima palavra

## Introdução

Esse projeto tem como objetivo o desenvolvimento de um preditor de próxima palavra, que analisa uma frase e retorna três opções para o usuário. O foco é desenvolver uma ferramenta única para cada pessoa, para que as previsões sejam as mais adequadas para o usuário da ferramenta.

## Desenvolvimento


### Definição da base de dados:

Primeiramente, para estruturar o projeto é necessária a escolha de uma base de dados. Essa, que será utilizada como base da estrutura de frases para a análise. Como o objetivo é criar um preditor específico para cada pessoa, a base de dados escolhida foi a da conversa do WhatsApp de cada usuário. O WhatsApp é o aplicativo de conversas mais utilizado no Brasil e ele permite que baixe sua conversa em arquivos ".txt".

<p  align="center">
  <br><img src="Images/conversa1.png" width= "200"><br><img src="Images/conversa2.png" width= "200"><br><img src="Images/conversa3.png" width= "200"><br>
  <c style="font-size:11px">Imagens 1, 2 e 3: Tutorial de como exportar uma conversa do WhatsApp</c><br><br>
</p>

###  Limpeza dos dados:

Com o arquivo em mãos, inicia-se o processo de desenvolvimento do projeto, de fato. Primeiramente, para que a análise seja feita de maneira correta, é necessária uma limpeza nos dados. Analisando o formato do arquivo gerado pelo WhatsApp, o código ```modules/extractFromWpp.py``` foi desenvolvido para realizar a limpeza de todas as coisas que poderiam interferir na predição.

<p  align="center">
  <br><img src="Images/WhatsAppTxt.png" width= "400"><br>
  <c style="font-size:11px">Imagem 4: Estrutura do arquivo gerado pelo WhatsApp</c><br><br>
</p>

Como o usuário deve baixar as conversas sem as mídias, existem frases nos locais delas que não interessam para o modelo, além das pontuações desnecessárias. As mensagens são precedidas pelo nome de usuário de quem está enviando a mensagem, portanto, ao rodar o arquivo de extração do texto é exigido o nome do WhatsApp da pessoa.

### Estrutura dos dados:

Para a estrutura dos dados ficar mais simples, no arquivo ```modules/lexicon.py``` um dicionário é criado. Ele é dividido em unigramas, bigramas, trigramas e quadrigramas, e dentro de cada chave dessas existem suas palavras, ou conjuntos de palavras, e suas respectivas frequências e probabilidades de serem selecionadas.

Para entender essa estrutura, primeiramente deve-se entender o conceito por trás dos N-gramas.

<p  align="center">
  <br><img src="Images/N-gramas.png" width= "400"><br>
  <c style="font-size:11px">Imagem 5: N-gramas</c><br><br>
</p>

Todas as frases são separadas e divididas em uni, bi, tri e quadrigramas se possível. Caso a frase tenha menos palavras que o N-grama, simplesmente é ignorado. 

Com as frases estruturadas em N-gramas, as probabilidades delas são calculadas a partir de sua frequência no documento dividido pela quantidade total de palavras. É simples pensar para um unigrama, dado que é uma palavra para o total de palavras, porém calcular a probabilidade de um N-grama não é tão intuitivo. Apesar disso, basta verificar a lógica do cálculo, se para calcular a probabilidade de um unigrama deve-se dividir a frequência de um unigrama pelo total de palavras, para calcular a probabilidade de bigramas basta dividir a frequência desse bigrama pela frequência da primeira palavra do bigrama, e assim por diante aumentando o N.

### Cálculo da probabilidade:

### Preditor:

### Execução do programa:

### Conclusão: