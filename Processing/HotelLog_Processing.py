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
    .appName("HotelLogProcessing") \
    .getOrCreate()

spark.sql("use etl;")

#hotellogs = spark.read.json("/sjm/data/hotellogs/*")
hotellogs = spark.read.json("/sjm/data/hotellogs/"+time)

hotellog_1 = hotellogs.select(
    hotellogs.id,
    hotellogs.ip,
    hotellogs.datetime,
    hotellogs.account,
    hotellogs.age,
    hotellogs.method,
    hotellogs.status.cast('int')
    )

analysis_data = hotellog_1 \
    .withColumn("buyNum", split(col("method"), "/buy/places/", 2)[1].alias("buyNum")).fillna(value="0",subset=["buyNum"]) \
    .withColumn("click_place", split(col("method"), "/places/", 2)[1]).fillna(value="0", subset=["click_place"]) \
    .withColumn("cilck_subhome", split(col("method"), "/sub-home/", 2)[1]) \

analysis_data.write \
    .partitionBy("account") \
    .mode("append") \
    .saveAsTable("hotel_analysis_log")

spark.stop()
