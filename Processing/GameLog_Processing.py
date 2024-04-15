#!/usr/bin/python3

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
    .appName("GameLogETL") \
    .getOrCreate()

spark.sql("use etl;")

#gameLogDF = spark.read.json("hdfs://spark-master-01:9000/sjm/data/gamelogs/*")
gameLogDF = spark.read.json("hdfs://spark-master-01:9000/sjm/data/gamelogs/"+time)

gamelog_EDA1 = gameLogDF.select(
    gameLogDF.roomID,
    gameLogDF.createRoomDate.cast("date"),
    gameLogDF.id,
    gameLogDF.ip,
    gameLogDF.account,
    gameLogDF.champion,
    gameLogDF.ingametime,
    gameLogDF.datetime,
    gameLogDF.status.cast("int"),
    gameLogDF.deathCount.cast("int"),
    gameLogDF.inputkey,
    gameLogDF.method,
    gameLogDF.x,
    gameLogDF.y)

analysis_data = gamelog_EDA1 \
    .withColumn("xy", col('x')+col('y')) \
    .withColumn("buy_item", when(col("method") == "buyItem", 1).otherwise(0)) \
    .orderBy("datetime")

training_data = analysis_data.select(
    analysis_data.createRoomDate,
    analysis_data.datetime,
    analysis_data.ingametime,
    analysis_data.champion,
    analysis_data.x,
    analysis_data.y,
    analysis_data.xy
    ).withColumn("lable", when(col("champion") == "viktor", 1).otherwise(0))

analysis_data.write \
    .option("encoding", "UTF-8") \
    .partitionBy("createRoomDate", "champion") \
    .mode("append") \
    .saveAsTable("LoL_analysis_log")

training_data.write \
    .option("encoding", "UTF-8") \
    .partitionBy("createRoomDate", "champion") \
    .mode("append") \
    .saveAsTable("LoL_training_log")

spark.stop()
