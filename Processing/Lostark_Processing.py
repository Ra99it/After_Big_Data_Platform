#! /usr/bin/python3

import os
import datetime
from pytz import timezone
from os.path import abspath
from pyspark.sql import SparkSession
from pyspark.context import SparkContext
from pyspark.sql.functions import *

os.environ["YARN_CONF_DIR"] = "/sjm/spark3/conf2"

time = (datetime.datetime.now(timezone('Asia/Seoul')) - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

spark = SparkSession \
    .builder \
    .config("spark.jars", "/sjm/spark3/mysql-connector-java-5.1.49.jar") \
    .config("spark.home", "/sjm/spark3") \
    .config("spark.sql.warehouse.dir", "hdfs:///sjm/sjm_warehouse_mysql_5.7") \
    .config("spark.useHiveContext", True) \
    .config("spark.sql.catalogImplementation", "hive") \
    .config("spark.executor.memory","6g") \
    .config("spark.executor.cores", "2") \
    .config("spark.driver.cores", "1") \
    .config("spark.driver.memory", "6g") \
    .config("spark.executor.instances", "3") \
    .config("spark.driver.extraJavaOptions=-Dfile.encoding", "utf-8") \
    .enableHiveSupport() \
    .master("yarn") \
    .appName("LostArkProcessing") \
    .getOrCreate()

spark.sql("use etl;")

lostark_log = spark.read.json("/sjm/data/lostarklogs/*")
#lostark_log = spark.read.json("/sjm/data/lostarklogs/"+time)

analysis_data = lostark_log.select(
    lostark_log.sessionID,
    lostark_log.startTime,
    lostark_log.gametime,
    lostark_log.success,
    lostark_log.Boss['name'].alias("Boss_name"),
    lostark_log.User['account'].alias('User_account'),
    lostark_log.User['class'].alias('User_class'),
    lostark_log.method,
    lostark_log.inpukey,
    lostark_log.x,
    lostark_log.y,
    lostark_log.status
).withColumn("xy", col('x')+col('y')) \
.withColumnRenamed("inpukey", "inputkey")

training_data = analysis_data.select(
    analysis_data.startTime,
    analysis_data.gametime,
    analysis_data.User_account,
    analysis_data.method,
    analysis_data.x,
    analysis_data.y,
    analysis_data.inputkey,
).withColumn("xy", col('x')+col('y'))

analysis_data.write \
    .partitionBy("sessionID", "User_account", "User_class") \
    .mode("overwrite") \
    .saveAsTable("lostark_analysis_log")

training_data.write \
    .partitionBy("User_account") \
    .mode("overwrite") \
    .saveAsTable("lostark_training_log")

spark.stop()
