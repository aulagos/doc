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
