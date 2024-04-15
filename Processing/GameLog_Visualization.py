#!/usr/bin/python3

import os
import datetime
from pytz import timezone
from os.path import abspath
from pyspark.sql import SparkSession
from pyspark.context import SparkContext
from pyspark.sql.functions import *

os.environ["YARN_CONF_DIR"] = "/sjm/spark3/conf2"

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

spark.sql("use etl;").show()

time = (datetime.datetime.now(timezone('Asia/Seoul')) - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

visualization = spark.read.table("lol_analysis_log").filter("createRoomDate = '"+time +"'")

champions = visualization.select("champion").distinct()

for champion in champions.rdd.collect() :
    print(champion.champion)
    EDA1 = visualization.filter(col("champion") == champion.champion)
    EDA1 = EDA1.toPandas()
    EDA1.plot.scatter(x='datetime', y='xy')


print("-------------------------------------------")

EDA2 = visualization.groupBy("inputkey") \
    .agg(count("inputkey").alias("input_count")) \
    .selectExpr(
        "inputkey",
        "cast(input_count as int) input_count")

EDA2=EDA2.toPandas()
EDA2=EDA2.set_index("inputkey")
EDA2.plot.pie(x="inputeky", y="input_count")

print("-------------------------------------------")


deathCount_EDA = visualization.groupBy("champion") \
    .agg(max("deathCount").alias("deathCount_1"))

deathCount_EDA = deathCount_EDA.toPandas()

deathCount_EDA.plot.bar(x="champion", y="deathCount_1")

spark.stop()

