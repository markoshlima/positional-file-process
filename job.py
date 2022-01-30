import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import SQLContext
from pyspark.sql.functions import col, substring
import boto3
import json
import uuid

#variaveis globais
args = getResolvedOptions(sys.argv, ["JOB_NAME", "file"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)
sqlContext = SQLContext(spark.sparkContext, spark)
colDefaultName = '_1'
queue_url = '' #URL SQS queue
arquivo = args['file']
bucketFormated = 'soccerfiles-formated'

#leitura do arquivo
print("Lendo arquivo: ", arquivo)
txtfile = sc.textFile(arquivo)

#quebra do arquivo em linhas
print("Quebrando arquivo em linhas")
linesFile = txtfile.map(lambda k: k.split("\\t"))
print("Total de linhas: ", linesFile.count())

#transforma para DataFrame
print("Transformando para DataFrame")
dfPos = linesFile.toDF()

#faz a quebra das linhas baseado na posição
print("Mapeamento das colunas")
rodadas = dfPos.withColumn('dia', col(colDefaultName).substr(1,2))\
          .withColumn('mes', col(colDefaultName).substr(3,2))\
          .withColumn('ano', col(colDefaultName).substr(5,4))\
          .withColumn('hora', col(colDefaultName).substr(9,2))\
          .withColumn('minuto', col(colDefaultName).substr(11,2))\
          .withColumn('rodada', col(colDefaultName).substr(13,1))\
          .withColumn('estadio_nome', col(colDefaultName).substr(14,40))\
          .withColumn('arbitro_nome', col(colDefaultName).substr(54,30))\
          .withColumn('time_mandante_nome', col(colDefaultName).substr(84,13))\
          .withColumn('time_visitante_nome', col(colDefaultName).substr(97,13))\
          .withColumn('tecnico_mandante_nome', col(colDefaultName).substr(110,15))\
          .withColumn('tecnico_visitante_nome', col(colDefaultName).substr(125,15))\
          .withColumn('colocacao_mandante', col(colDefaultName).substr(140,2))\
          .withColumn('colocacao_visitante', col(colDefaultName).substr(142,2))\
          .withColumn('gols_mandante', col(colDefaultName).substr(144,1))\
          .withColumn('gols_visitante', col(colDefaultName).substr(145,1))\
          .withColumn('escanteios_mandante', col(colDefaultName).substr(146,2))\
          .withColumn('escanteios_visitante', col(colDefaultName).substr(148,2))\
          .withColumn('faltas_mandante', col(colDefaultName).substr(150,2))\
          .withColumn('faltas_visitante', col(colDefaultName).substr(152,2))\
          .withColumn('chutes_bola_parada_mandante', col(colDefaultName).substr(154,2))\
          .withColumn('chutes_bola_parada_visitante', col(colDefaultName).substr(156,2))\
          .withColumn('desefas_mandante', col(colDefaultName).substr(158,2))\
          .withColumn('desefas_visitante', col(colDefaultName).substr(160,2))\
          .withColumn('impedimentos_mandante', col(colDefaultName).substr(162,2))\
          .withColumn('impedimentos_visitante', col(colDefaultName).substr(164,2))\
          .withColumn('chutes_mandante', col(colDefaultName).substr(166,2))\
          .withColumn('chutes_visitante', col(colDefaultName).substr(168,2))\
          .withColumn('chutes_fora_mandante', col(colDefaultName).substr(170,2))\
          .withColumn('chutes_fora_visitate', col(colDefaultName).substr(172,2))

#cria a tabela("rodadas")
print("Criando tabela do dataframe")
rodadas.createOrReplaceTempView('rodadas')

#adiciona uuid
rodadas = sqlContext.sql('SELECT r.*, TRIM(estadio_nome) as estadio, TRIM(arbitro_nome) as arbitro, TRIM(time_mandante_nome) as time_mandante, TRIM(time_visitante_nome) as time_visitante, TRIM(tecnico_mandante_nome) as tecnico_mandante, TRIM(tecnico_visitate_nome) as tecnico_visitate, uuid() as rodada_id FROM rodadas r')

#remove colunas desnecessarias
print("Removendo colunas desnecessarias")
rodadas = rodadas.drop('estadio')
rodadas = rodadas.drop('arbitro')
rodadas = rodadas.drop('time_mandante')
rodadas = rodadas.drop('time_visitante')
rodadas = rodadas.drop('tecnico_mandante')
rodadas = rodadas.drop('tecnico_visitate')
rodadas = rodadas.drop(colDefaultName)

#converte para json
print("Convertendo para JSON")
rodadasJson = rodadas.toJSON()

#envia para SQS de forma transacional para tratamenos unitários
print("Enviando para SQS")
sqs = boto3.client('sqs')
total = 1
for row in rodadasJson.collect():
    print("Enviando o documento ", total)
    print(row)
    print("\n")
    response = sqs.send_message(QueueUrl=queue_url, DelaySeconds=10, MessageBody=row)
    print(response['MessageId'])
    print("\n")
    total+=1

total-=1
print("Total de itens enviados: ", total)

#salva DF no S3 formato parquet
print("Enviando dataframe desnormalizado para S3 no formato PARQUET ", total)
idFileName = uuid.uuid4() 
rodadas.write.parquet("s3://"+bucketFormated+"/"+str(idFileName)+".parquet",mode="overwrite")

job.commit()
