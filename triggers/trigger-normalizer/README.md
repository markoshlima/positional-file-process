# trigger-normalizer

Create a AWS Lambda Layer from library PSYCOPG2, the library is already inside `/python` folder, but it also could be downloaded from: 
[psycopg2](https://github.com/jkehler/awslambda-psycopg2 "psycopg2")

The connections inside lambda_handler open and finish for each transaction to avoid any way of lock (pessimist or optimist), it is to take all advantages of Lambda paralelism, and do not have troubles about with Redshift isolation violation principles