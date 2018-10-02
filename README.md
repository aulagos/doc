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

## 1 --> estamos lendo um arquivo
## 2 --> o conteúdo de cada linha do arquivo é separado pelo delimitador "" e retornado em uma lista
## 3 --> cada item na lista (word) é transformado em um objeto de mapa (chave-valor) com a chave mesmo word e valor 1
## 4 --> os valores são adicionados através da soma
## 5 --> o RDD resultante é salvo com o valor de cada elemento em um arquivo texto






**HTTP requests to the NASA Kennedy Space Center WWW server**
Dados :
● Jul 01 to Jul 31, ASCII format, 20.7 MB gzip compressed , 205.2 MB. (NASA_access_log_Jul95.gz)
● Aug 04 to Aug 31, ASCII format, 21.8 MB gzip compressed , 167.8 MB. (NASA_access_log_Aug95.gz)

**Questões**
**Responda as seguintes questões devem ser desenvolvidas em Spark utilizando a sua linguagem de preferência.**

pd. o arquivo não tem um delimitador específico, então o erro 404 foi considerado o último campo igual a "-" (atende quase 95%)

import os
import sys

os.environ['SPARK_HOME'] = "C:/apache-spark/spark-2.3.1-bin-hadoop2.7"

sys.path.append("C:/apache-spark/spark-2.3.1-bin-hadoop2.7/python/")
sys.path.append("C:/apache-spark/spark-2.3.1-bin-hadoop2.7/python/lib/py4j-0.10.7-src.zip")

from pyspark import SparkContext
from operator import add

logFile_J = "C:/Users/CLAR_SURFACE/Desktop/semantix/access_log_Jul95"
logFile_A = "C:/Users/CLAR_SURFACE/Desktop/semantix/access_log_Aug95"

sc = SparkContext("local", "semantix app")

julho = sc.textFile(logFile_J).cache()
agosto = sc.textFile(logFile_A).cache()


# --------------------------
# 1.- Número de hosts únicos.
julho_c = julho.flatMap(lambda line: line.split(' ')[0]).distinct().count()
agosto_c = agosto.flatMap(lambda line: line.split(' ')[0]).distinct().count()

print('Número de hosts únicos em Julho: %s' % julho_c)
print('Número de hosts únicos em Agosto %s' % agosto_c)

# ------------------------
# 2.- O total de erros 404.
julho_404 = julho.filter(lambda line: line.split(' ')[-1] == '-').cache().count()
agosto_404 = agosto.filter(lambda line: line.split(' ')[-1] == '-').cache().count()

print('O total de erros 404 in Julho: %s' % julho_404)
print('O total de erros 404 in Agosto %s' % agosto_404)


# -----------------------------------------
# 3.- Os 5 URLs que mais causaram erro 404.

def top5_urls(rdd):
    urls = rdd.filter(lambda line: line.split(' ')[-1] == '-').cache()
    counts = urls.map(lambda line1: (line1, 1)).reduceByKey(add)
    top5 = counts.sortBy(lambda line2: -line2[1]).take(5)

    print('\nOs 5 URLs que mais causaram erro 404:')
    for url, quantidade in top5:
        print(url, quantidade)

    return top5


top5_urls(julho)
top5_urls(agosto)


# ------------------------------------
# 4.- Quantidade de erros 404 por dia.

def error_por_dia(rdd):
    daily = rdd.filter(lambda line: line.split(' ')[-1] == '-').cache()
    days = daily.map(lambda line1: line1.split('[')[1].split(':')[0])
    counts = days.map(lambda line2: (line2, 1)).reduceByKey(add).collect()

    print('\nQuantidade de erros 404 por dia:')
    for data, quantidade in counts:
        print(data, quantidade)

    return counts


error_por_dia(julho)
error_por_dia(agosto)


# -------------------------------
# 5.- O total de bytes retornados.

def total_bytes(rdd):
    def byte_count(line):
        try:
            count = int(line.split(" ")[-1])
            if count < 0:
                raise ValueError()
            return count

        except:
            return 0

    count = rdd.map(byte_count).reduce(add)

    return count


print('Total de bytes retornados em Julho: %s' % total_bytes(julho))
print('total de bytes retornados em Agosto: %s' % total_bytes(agosto))
