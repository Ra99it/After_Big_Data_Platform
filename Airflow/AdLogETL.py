from datetime import datetime, timedelta
from datetime import timezone
import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator

with DAG(
    "AdLogETL",
    default_args= {
        "owner" : "spark",
        "depends_on_past" : True,
        "retries" : 0,
    },
    start_date = datetime(2024, 4,7),
    schedule_interval='30 2 * * *',
    catchup=False,
    tags=["ETL"],
    ) as dag :
    
    cmd='export YARN_CONF_DIR=/sjm/spark3/conf2 && /sjm/spark3/bin/spark-submit --master yarn --deploy-mode cluster hdfs:///sjm/data/airflow/py/AdLogETL.py'

    task_start = DummyOperator(
    task_id='start_Extract',
    )

    task_suecces = DummyOperator(
    task_id='suecces_ETL',
    )

    task_end = DummyOperator(
    task_id='end',
    )

    task_spark = BashOperator(
        task_id='spark_submit_task',
        bash_command=cmd,
    )

    visualization_cmd='export YARN_CONF_DIR=/sjm/spark3/conf2 && /sjm/spark3/bin/spark-submit --master yarn --deploy-mode cluster hdfs:///sjm/data/airflow/py/AdLog_Visualization.py'

    #visualization = BashOperator(
        #task_id='task_visualization',                                                                                                        #bash_command=visualization_cmd)

    visualization = DummyOperator(                                                                                                            task_id='visualization',
    )

task_start >> task_spark >> visualization >> task_suecces >> task_end
