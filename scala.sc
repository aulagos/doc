#Explique o que o código Scala abaixo faz.

val textFile = sc.textFile("hdfs://...") 
val counts = textFile.flatMap(line => line.split( " " ))
            .map(word => (word,1))
            .reduceByKey(_+_)
counts.saveAsTextFile("hdfs://...")

#Aqui o detalhe: 
#Na linha (1) estamos lendo um arquivo. 
#Na linha (2) o conteúdo de cada linha do arquivo é separado pelo delimitador "" e retornado em uma lista. 
#Na linha (3) cada item na lista (word) é transformado em um objeto de mapa (chave-valor) com a chave mesmo word e valor 1.
#Na linha (4) os valores são adicionados através da soma. 
#Na linha (5) o RDD resultante é salvo com o valor de cada elemento em um arquivo texto.
