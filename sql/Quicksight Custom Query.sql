select 
(select time from times where time_id = r.time_visitante_id) as time_visitante,
(select time from times where time_id = r.time_mandante_id) as time_mandante,
(select tecnico from tecnicos where tecnico_id = r.tecnico_visitante_id) as tecnico_visitante,
(select tecnico from tecnicos where tecnico_id = r.tecnico_mandante_id) as tecnico_mandante,
(select arbitro from arbitros where arbitro_id = r.arbitro_id) as arbitro,
(select estadio from estadios where estadio_id = r.estadio_id) as estadio,
r.*
from rodadas r;