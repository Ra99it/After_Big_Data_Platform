from datetime import datetime, timedelta
from datetime import timezone
import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator

with DAG(
    "ETL",
    default_args= {
        "owner" : "spark",
        "depends_on_past" : True,
        "retries" : 0,
    },
    start_date = datetime(2024, 4,7),
    schedule_interval='* 9 * * *',
    catchup=False,
    tags=["ETL"],
    ) as dag :

    gamelog_cmd = 'export YARN_CONF_DIR=/sjm/spark3/conf2 && /sjm/spark3/bin/spark-submit --master yarn --deploy-mode cluster hdfs:///sjm/data/airflow/py/GameLogETL.py'

    hotellog_cmd = 'export YARN_CONF_DIR=/sjm/spark3/conf2 && /sjm/spark3/bin/spark-submit --master yarn --deploy-mode cluster hdfs:///sjm/data/airflow/py/HotelLogETL.py'

    lostarklog_cmd = 'export YARN_CONF_DIR=/sjm/spark3/conf2 && /sjm/spark3/bin/spark-submit --master yarn --deploy-mode cluster hdfs:///sjm/data/airflow/py/LostArkLogETL.py'

    adlog_cmd = 'export YARN_CONF_DIR=/sjm/spark3/conf2 && /sjm/spark3/bin/spark-submit --master yarn --deploy-mode cluster hdfs:///sjm/data/airflow/py/adLogETL.py'

    task_start = DummyOperator(
    task_id='start_Extract'
    )

    task_suecces = DummyOperator(
    task_id='suecces_ETL'
    )

    task_end = DummyOperator(
    task_id='end'
    )

    task_sleep =  BashOperator(
        task_id="sleep",
        depends_on_past=False,
        bash_command="sleep 30",
    )

    task_spark_gamelog = BashOperator(
        task_id='spark_submit_gamelog_task',
        bash_command=gamelog_cmd,
    ) 

    task_spark_hotellog = BashOperator(
        task_id='spark_submit_hotel_task',
        bash_command=hotellog_cmd,
    )

    task_spark_lostarklog = BashOperator(
        task_id='spark_submit_lostark_task',
        bash_command=lostarklog_cmd,
    )

    task_spark_adlog = BashOperator(
        task_id='spark_submit_ad_task',
        bash_command=adlog_cmd,
    )

task_spark_gamelog >> task_sleep >> task_spark_hotellog >> task_sleep >> task_spark_lostarklog >> task_sleep >> task_spark_adlog >>task_suecces >> task_end    
