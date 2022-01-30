CREATE TABLE "public"."arbitros" ( arbitro_id varchar(36) NOT NULL, arbitro varchar(50));

CREATE TABLE "public"."times" ( time_id varchar(36) NOT NULL, time varchar(50));

CREATE TABLE "public"."tecnicos" ( tecnico_id varchar(36) NOT NULL, tecnico varchar(50));

CREATE TABLE "public"."estadios" ( estadio_id varchar(36) NOT NULL, estadio varchar(50));

CREATE TABLE "public"."rodadas" ( 
  rodada_id varchar(36) NOT NULL,
  time_visitante_id varchar(36),
  time_mandante_id varchar(36),
  tecnico_visitante_id varchar(36),
  tecnico_mandante_id varchar(36),
  arbitro_id varchar(36),
  estadio_id varchar(36),
  dia int,
  mes int,
  ano int,
  hora int,
  minuto int,
  rodada int,
  colocacao_mandante int,
  colocacao_visitante int,
  gols_mandante int,
  gols_visitante int,
  escanteios_mandante int,
  escanteios_visitante int,
  faltas_mandante int,
  faltas_visitante int,
  chutes_bola_parada_mandante int,
  chutes_bola_parada_visitante int,
  desefas_mandante int,
  desefas_visitante int,
  impedimentos_mandante int,
  impedimentos_visitante int,
  chutes_mandante int,
  chutes_visitante int,
  chutes_fora_mandante int,
  chutes_fora_visitate int) 
distkey(rodada_id) compound sortkey(rodada_id);

CREATE VIEW DUAL AS SELECT 'X' AS DUMMY;



