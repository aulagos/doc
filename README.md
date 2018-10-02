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
