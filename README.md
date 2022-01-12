# **Introduction**

This project is based for legacy applications that works with positional files to process data.
The objetive is read these positional files when they arrives in AWS S3, and then send to a dataware-house like AWS Redshift, and finally read the results with a Business Intelligence tool as AWS QuickSight.
It's a simple flow, but very rich and usefull for these kind of application.

To simulate this scenario, it is using Soccer Brazilian Championship. The files in folder **'/data'** contains three positional files that can be read and loaded into Redshift throught AWS Glue.

# **Positions**

Below is showed the contract positions about the file.

|name|begin|end|size|
| ------------ | ------------ | ------------ | ------------ |
|dia|1|2|2|
|mês|3|4|2|
|ano|5|8|4|
|hora|9|10|2|
|minuto|11|12|2|
|rodada|13|13|1|
|estadio|14|53|40|
|arbitro|54|83|30|
|time mandante|84|96|13|
|time visitante|97|109|13|
|técnico mandante|110|124|15|
|técnico visitante|125|139|15|
|colocação mandante|140|141|2|
|colocação visitante|142|143|2|
|gols mandante|144|144|1|
|gols visitante|145|145|1|
|escanteios mandante|146|147|2|
|escanteios visitante|148|149|2|
|faltas mandante|150|151|2|
|faltas visitante|152|153|2|
|chutes bola parada mandante|154|155|2|
|chutes bola parada visitante|156|157|2|
|defesas mandante|158|159|2|
|defesas visitante|160|161|2|
|impedimentos mandante|162|163|2|
|impedimentos visitante|164|165|2|
|chutes mandante|166|167|2|
|chutes visitante|168|169|2|
|chutes fora mandante|170|171|2|
|chutes fora visitante|172|173|2|


# **Application Architecture**

![alt text](https://github.com/markoshlima/positional-file-process/blob/main/docs/Architecture%20Application.png?raw=true)

- The files can be uploaded into S3
- S3 triggers a Lambda Function that will copy this file to another repository and starts a Glue Job
- The Glue Job will read this file and process with PySpark to do the ETL Job.
- After transformation, the DataFrame will be saved into Redshift.
- At the end of process, the user can read the results from QuickSight

# **Pricing**

// calculating ...