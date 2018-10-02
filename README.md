# APACHE SPARK
**Qual o objetivo do comando cache em Spark?**
Comando cache e igual que o camando persist. Ajuda com melhorar da eficencia da leitura 
de um arquivo e permite que resultados intermediários de operações lazy sejam iguais, 
possam ser armazenados e reutilizados repetidamente  

**O mesmo código implementado em Spark é normalmente mais rápido que a implementação 
equivalente em MapReduce. Por quê?**
Pelo abordagem do processamento: o Spark pode fazer isso na memória, enquanto o Hadoop 
MapReduce precisa ler e gravar em um disco. Como resultado, a velocidade de processamento 
difere significativamente - o Spark pode ser até 100 vezes mais rápido

**Qual é a função do SparkContext ?**
É um cliente do ambiente de execução do Spark também configura serviços internos e 
estabelece uma conexão com um ambiente de execução do Spark. Também usa-se para criar RDDs,
acessar serviços do Spark e executar jobs. 

**Explique com suas palavras o que é Resilient Distributed Datasets (RDD)**
Um dos fundamentos do Apache Spark é o RDD que foi criado para aproveitar mais o 
armazenamento da memória principal. Assim, quando carregamos um conjunto de dados a 
ser processado no Spark, a estrutura que vamos usar internamente para despejar os dados 
é um RDD. Ao colocar-lo em um RDD, em função de como configuramos nosso ambiente de 
trabalho no Spark, a lista das entradas que compõem nosso conjunto de dados serão 
divididas em um número específico de partições (será "paralelizado"), cada um deles 
armazenado em um dos server do nosso cluster para processamento de Big Data.

**GroupByKey é menos eficiente que reduceByKey em grandes dataset. Por quê?**
Aplicando groupByKey () em um conjunto de dados de pares (K, V), os dados são misturados 
de acordo com o valor da chave K em outro RDD. Nesta transformação, muita transferência 
de dados desnecessária pela rede, cria a necessidade de escrever os dados em disco 
e resulta um impacto negativo bastante significante na performance.
Aplicando reduceByKey em um dataset (K, V), antes de embaralhar os dados na mesma 
máquina com a mesma chave são combinados, resultando em um conjunto menor de dados 
sendo transferido.





**Explique o que o código Scala abaixo faz.**

1.- val textFile = sc.textFile("hdfs://...")
2.- val counts = textFile.flatMap(line => line.split( " " ))
3.-            .map(word => (word,1)) ##
4.-            .reduceByKey(_+_) ##
5.- counts.saveAsTextFile("hdfs://...") ##

Aqui o detalhe: na linha (1) estamos lendo um arquivo. Na linha (2) o conteúdo de cada linha do 
arquivo é separado pelo delimitador "" e retornado em uma lista. Na linha (3) cada item na 
lista (word) é transformado em um objeto de mapa (chave-valor) com a chave mesmo word e valor 1.
Na linha (4) os valores são adicionados através da soma. Na linha (5) o RDD resultante é salvo 
com o valor de cada elemento em um arquivo texto.

