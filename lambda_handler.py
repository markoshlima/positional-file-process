import json
import psycopg2
import uuid
import os

def lambda_handler(event, context):
    
    print("iniciando processo de noramalizacao")
    
    #obtem o evento da rodada
    message = event["Records"][0]["body"]
    rodada = json.loads(message)
    
    print("consulta itens de normalizacao")
    #faz a consulta dos itens de normalizacao
    query = ("select "
            	"(select tecnico_id from tecnicos where tecnico = '"+rodada['tecnico_visitante']+"' limit 1) as tecnico_visitante_id, "
            	"(select tecnico_id from tecnicos where tecnico = '"+rodada['tecnico_mandante']+"' limit 1) as tecnico_mandante_id, "
            	"(select time_id from times where time = '"+rodada['time_visitante']+"' limit 1) as time_mandante_id, "
                "(select time_id from times where time = '"+rodada['time_mandante']+"' limit 1) as time_visitante_id, "
            	"(select arbitro_id from arbitros where arbitro = '"+rodada['arbitro']+"' limit 1) as arbitro_id, "
            	"(select estadio_id from estadios where estadio = '"+rodada['estadio']+"' limit 1) as estadio_id "
            "from dual")
    print(query)
    result = fetchOne(query)
    
    #monta o documento do resultado da consulta de normalização
    norm = {
        "tecnico_visitante_id":result[0],
        "tecnico_mandante_id":result[1],
        "time_mandante_id":result[2],
        "time_visitante_id":result[3],
        "arbitro_id":result[4],
        "estadio_id":result[5]
    }
    
    #normaliza o tecnico visitante
    print("normaliza o tecnico visitante")
    if norm['tecnico_visitante_id'] is None:
        norm['tecnico_visitante_id'] = str(uuid.uuid4())
        executeWrite("INSERT INTO tecnicos VALUES ('"+norm['tecnico_visitante_id']+"', '"+rodada['tecnico_visitante']+"')")
    rodada['tecnico_visitante_id'] = norm['tecnico_visitante_id']
    
    #normaliza o tecnico mandante
    print("normaliza o tecnico mandante")
    if norm['tecnico_mandante_id'] is None:
        norm['tecnico_mandante_id'] = str(uuid.uuid4())
        executeWrite("INSERT INTO tecnicos VALUES ('"+norm['tecnico_mandante_id']+"', '"+rodada['tecnico_mandante']+"')")
    rodada['tecnico_mandante_id'] = norm['tecnico_mandante_id']
    
    #normaliza o time visitante
    print("normaliza o time visitante")
    if norm['time_visitante_id'] is None:
        norm['time_visitante_id'] = str(uuid.uuid4())
        executeWrite("INSERT INTO times VALUES ('"+norm['time_visitante_id']+"', '"+rodada['time_visitante']+"')")
    rodada['time_visitante_id'] = norm['time_visitante_id']
    
    #normaliza o time mandante
    print("normaliza o time mandante")
    if norm['time_mandante_id'] is None:
        norm['time_mandante_id'] = str(uuid.uuid4())
        executeWrite("INSERT INTO times VALUES ('"+norm['time_mandante_id']+"', '"+rodada['time_mandante']+"')")
    rodada['time_mandante_id'] = norm['time_mandante_id']
    
    #normaliza o arbitro
    print("normaliza o arbitro")
    if norm['arbitro_id'] is None:
        norm['arbitro_id'] = str(uuid.uuid4())
        executeWrite("INSERT INTO arbitros VALUES ('"+norm['arbitro_id']+"', '"+rodada['arbitro']+"')")
    rodada['arbitro_id'] = norm['arbitro_id']
    
    #verifica o estadio
    print("normaliza o estadio")
    if norm['estadio_id'] is None:
        norm['estadio_id'] = str(uuid.uuid4())
        executeWrite("INSERT INTO estadios VALUES ('"+norm['estadio_id']+"', '"+rodada['estadio']+"')")
    rodada['estadio_id'] = norm['estadio_id']
    

    #remove os nomes da rodada
    rodada.pop("tecnico_visitante")
    rodada.pop("tecnico_mandante")
    rodada.pop("time_visitante")
    rodada.pop("time_mandante")
    rodada.pop("arbitro")
    rodada.pop("estadio")
    
    #adiciona a rodada noramalizada
    print("salva rodada")
    query = ("INSERT INTO rodadas VALUES("
              "'"+rodada['rodada_id']+"',"
              "'"+rodada['time_visitante_id']+"',"
              "'"+rodada['time_mandante_id']+"',"
              "'"+rodada['tecnico_visitante_id']+"',"
              "'"+rodada['tecnico_mandante_id']+"',"
              "'"+rodada['arbitro_id']+"',"
              "'"+rodada['estadio_id']+"',"
              +rodada['dia']+","
              +rodada['mes']+","
              +rodada['ano']+","
              +rodada['hora']+","
              +rodada['minuto']+","
              +rodada['rodada']+","
              +rodada['colocacao_mandante']+","
              +rodada['colocacao_visitante']+","
              +rodada['gols_mandante']+","
              +rodada['gols_visitante']+","
              +rodada['escanteios_mandante']+","
              +rodada['escanteios_visitante']+","
              +rodada['faltas_mandante']+","
              +rodada['faltas_visitante']+","
              +rodada['chutes_bola_parada_mandante']+","
              +rodada['chutes_bola_parada_visitante']+","
              +rodada['desefas_mandante']+","
              +rodada['desefas_visitante']+","
              +rodada['impedimentos_mandante']+","
              +rodada['impedimentos_visitante']+","
              +rodada['chutes_mandante']+","
              +rodada['chutes_visitante']+","
              +rodada['chutes_fora_mandante']+","
              +rodada['chutes_fora_visitate']+")")
    print(query)
    executeWrite(query)

    #fim do processo
    print("fim do processo")

#executa a operacao de escrita    
def executeWrite(query):
    conn = getConn()
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()

#obtem um registro de consulta
def fetchOne(query):
    conn = getConn()
    cur = conn.cursor()
    cur.execute(query)
    response = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return response

#obtem a conexao com Redshift    
def getConn():
    return psycopg2.connect(dbname = os.environ['dbname'],
                            host= os.environ['host'],
                            port= os.environ['port'],
                            user= os.environ['user'],
                            password= os.environ['password'])
    