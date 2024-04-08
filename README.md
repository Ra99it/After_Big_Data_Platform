# After_Big_Data_Platform (정리중입니다.)

# 1. 개요 

## 1.1 Big-Data-Platform 이란?
(출처 : https://spacefordata.tistory.com/11)

![image](https://github.com/Ra99it/Before-Big-Data-Platform/assets/122541545/222e3bc4-db4f-4978-ac3d-4fae7c72f0b7)

[내용입력]


## 1.2 서버 정보

<b>1. Hadoop and Spark with Cluster </b>
|인스턴스 이름|성능|기술|
|------|---|---|
|spark-master-01|m5a.xlarge|Hadoop hdfs, yarn, Spark, mysql, airflow|
|spark-worker-01|m5a.xlarge|Hadoop hdfs, yarn, Spark, mysql, airflow|
|spark-worker-02|m5a.xlarge|Hadoop hdfs, yarn, Spark, mysql, cassandra, airflow|
|spark-worker-03|m5a.xlarge|Hadoop hdfs, yarn, Spark, mysql, airflow|

<b>2. Kafka Cluster</b>
|인스턴스 이름|성능|기술|
|------|---|---|
|de-kafka-cluster-1|t2.xlarge |Kafka, fluentd|
|de-kafka-cluster-2|t2.xlarge |Kafka, fluentd|
|de-kafka-cluster-3|t2.xlarge |Kafka, fluentd|

<b>3. OpenSearch Cluster</b>
|인스턴스 이름|성능|기술|
|------|---|---|
|de-os-manager|t2.medium|OpenSearch|
|de-os-coordinator|t2.medium|OpenSearch|
|de-os-data1|t2.medium|OpenSearch|
|de-os-data2|t2.medium|OpenSearch|

<b> 4. Other </b>
|인스턴스 이름|성능|기술|
|------|---|---|
|airflow-redis-01|t3a.micro |Redis|
|airflow-mysql-01|t3a.large |MYSQL|

##  API
https://github.com/Ra99it/Streaming_DataPipeline

# 2. 데이터 파이프라인

![123 drawio](https://github.com/Ra99it/Before-Big-Data-Platform/assets/122541545/19906630-774d-4fad-bc34-764a1d18a8d9)

## 2.1 적용 기술 및 설명

|Programming Language|Data Warehouse|Data Lake|Event Streaming|Data Engineering|
|----|-----------|----|----|-----|
|<img src="https://img.shields.io/badge/java-007396?style=for-the-badge&logo=OpenJDK&logoColor=white"> <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"> <img src="https://img.shields.io/badge/scala-DC322F?style=for-the-badge&logo=scala&logoColor=white">| <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=MySQL&logoColor=white">|<img src="https://img.shields.io/badge/apachehadoop-66CCFF?style=for-the-badge&logo=apachehadoop&logoColor=white">|<img src="https://img.shields.io/badge/Apache Kafka-%3333333.svg?style=for-the-badge&logo=Apache Kafka&logoColor=white"> |<img src="https://img.shields.io/badge/Apache Spark-E25A1C.svg?style=for-the-badge&logo=Apache Spark&logoColor=white"> | 

|Log Collector|NOSQL DB|Log Storage|Data Orchestration|
|----|----|-----|-----|
<img src="https://img.shields.io/badge/fluentd-0E83C8.svg?style=for-the-badge&logo=fluentd&logoColor=white"> | <img src="https://img.shields.io/badge/apachecassandra-1287B1.svg?style=for-the-badge&logo=apachecassandra&logoColor=white"> | <img src="https://img.shields.io/badge/opensearch-005EB8.svg?style=for-the-badge&logo=opensearch&logoColor=white"> | <img src="https://img.shields.io/badge/apacheairflow-017CEE.svg?style=for-the-badge&logo=apacheairflow&logoColor=white"> |


