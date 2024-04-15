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
    .appName("AdLogProcessing") \
    .getOrCreate()

spark.sql("use etl;")

#adlogs = spark.read.json("/sjm/data/adlogs/*")
adlogs = spark.read.json("/sjm/data/adlogs/"+time)

df_adlogs = adlogs.select(
    "Ad.ad_id",
    "Ad.ad_name",
    "Ad.ad_explain",
    "Ad.genre",
    "Ad.click_count",
    "Ad.viewing_time",
    "Ad.start_time",
    "Ad.end_time",
    "User.account",
    "User.gender",
    "User.age",
    "User.click",
    "User.view",
    "User.total_time")

analysis_data = df_adlogs.select(
    df_adlogs.ad_id,
    df_adlogs.ad_name,
    df_adlogs.ad_explain,
    df_adlogs.genre,
    df_adlogs.click_count.cast('int'),
    df_adlogs.viewing_time.cast('int'),
    df_adlogs.start_time,
    df_adlogs.end_time,
    df_adlogs.account,
    df_adlogs.gender,
    df_adlogs.age.cast('int'),
    df_adlogs.click,
    df_adlogs.view,
    df_adlogs.total_time.cast('int'))

today_total = analysis_data.groupBy("ad_id", "account") \
    .agg(max("viewing_time").alias("view_total")) \
    .groupBy("ad_id") \
    .agg(sum("view_total").alias("view_sum_total")) \
    .withColumn("view_sum_total_minutes", round(col("view_sum_total")/60, 2))


total_click = analysis_data.groupBy("ad_id", "ad_name", "account") \
    .agg(max("click_count").alias("sum_click_count")) \
    .groupBy("ad_id", "ad_name") \
    .agg(sum("sum_click_count").alias("total_click_count")) \


gender_total_viewtime = analysis_data.groupBy("ad_id", "account", "gender") \
    .agg(max("viewing_time").alias("view_total")) \
    .groupBy("ad_id", "gender") \
    .agg(sum("view_total").alias("gender_view_total")) \
    .orderBy(desc("ad_id"))

today_total.show()
total_click.show()
gender_total_viewtime.show()

analysis_data.write \
    .option("encoding", "UTF-8") \
    .partitionBy("ad_name") \
    .mode("overwrite") \
    .saveAsTable("ad_analysis_logs")

spark.stop()
