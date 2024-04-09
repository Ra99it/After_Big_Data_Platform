# After_Big_Data_Platform (정리중입니다.)

# 1. 개요 

## 1.1 Big-Data-Platform 이란?
(출처 : https://spacefordata.tistory.com/11)

![image](https://github.com/Ra99it/Before-Big-Data-Platform/assets/122541545/222e3bc4-db4f-4978-ac3d-4fae7c72f0b7)

**빅데이터 플랫폼**은 대량의 데이터를 수집, 저장, 관리, 분석할 수 있는 통합 시스템을 말합니다. 이러한 플랫폼은 기업이나 조직이 방대한 양의 구조화되지 않은 데이터를 효율적으로 처리하고, 이를 통해 인사이트를 얻거나 의사결정을 지원하기 위해 설계되었습니다. 빅데이터 플랫폼은 다음과 같은 주요 기능들을 포함합니다.

**데이터 수집 및 통합**: 다양한 소스로부터 데이터를 수집하고, 이를 플랫폼 내에서 통합하여 관리합니다. 이 데이터는 웹사이트, 소셜 미디어, IoT(사물인터넷) 기기, 기업 내부 시스템 등 다양한 출처에서 올 수 있습니다.

**데이터 저장**: 수집된 데이터는 구조화된 데이터베이스, 비구조화된 데이터 레이크, 혹은 둘의 조합에 저장될 수 있습니다. 이 데이터를 효과적으로 저장하고 관리하기 위해 분산 스토리지 시스템을 사용할 수도 있습니다.

**데이터 처리 및 분석**: 대량의 데이터를 처리하고 분석하기 위한 도구와 알고리즘을 제공합니다. 이는 실시간 분석, 배치 처리, 스트리밍 데이터 처리 등 다양한 방식을 포함할 수 있습니다.

**데이터 시각화 및 보고**: 분석 결과를 시각적으로 표현하여 사용자가 이해하기 쉽게 만듭니다. 대시보드, 그래프, 보고서 등 다양한 형태로 정보를 제공하여 의사결정 과정을 지원합니다.

보안 및 거버넌스: 데이터의 보안, 품질, 준수, 접근 권한 관리 등을 포함하여, 데이터의 전 생애주기를 걸쳐 거버넌스를 제공합니다.

**개인 역량을 위한 프로젝트로, 데이터의 규모나 서버의 크기는 실무와는 다소 거리가 있습니다.**  <br>
**하지만 데이터의 규모 및 서버의 크기를 제외한 고 가용성을 위해 클러스터로 운영하고 있으며,** <br>
**Big-Data-Platform이 수행할 수 있는 대부분의 작업을 수행 할 수 있습니다.**

# 2. 데이터 파이프라인

## 2.1 서버 정보

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

## 2.2 아키텍처

![123 drawio](https://github.com/Ra99it/Before-Big-Data-Platform/assets/122541545/19906630-774d-4fad-bc34-764a1d18a8d9)

## 2.3 사용기술

|Programming Language|Data Warehouse|Data Lake|Event Streaming|Data Engineering|
|----|-----------|----|----|-----|
|<img src="https://img.shields.io/badge/java-007396?style=for-the-badge&logo=OpenJDK&logoColor=white"> <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"> <img src="https://img.shields.io/badge/scala-DC322F?style=for-the-badge&logo=scala&logoColor=white">| <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=MySQL&logoColor=white">|<img src="https://img.shields.io/badge/apachehadoop-66CCFF?style=for-the-badge&logo=apachehadoop&logoColor=white">|<img src="https://img.shields.io/badge/Apache Kafka-%3333333.svg?style=for-the-badge&logo=Apache Kafka&logoColor=white"> |<img src="https://img.shields.io/badge/Apache Spark-E25A1C.svg?style=for-the-badge&logo=Apache Spark&logoColor=white"> | 

|Log Collector|NOSQL DB|Log Storage|Data Orchestration|
|----|----|-----|-----|
<img src="https://img.shields.io/badge/fluentd-0E83C8.svg?style=for-the-badge&logo=fluentd&logoColor=white"> | <img src="https://img.shields.io/badge/apachecassandra-1287B1.svg?style=for-the-badge&logo=apachecassandra&logoColor=white"> | <img src="https://img.shields.io/badge/opensearch-005EB8.svg?style=for-the-badge&logo=opensearch&logoColor=white"> | <img src="https://img.shields.io/badge/apacheairflow-017CEE.svg?style=for-the-badge&logo=apacheairflow&logoColor=white"> |

# 3. 진행

## 3.1 과정
![제목 없는 다이어그램 drawio](https://github.com/Ra99it/Before-Big-Data-Platform/assets/122541545/0598d9cd-2a95-40f3-bc5e-059b94b38ad3)

**Data Collection**
1. 외부 API로 실시간으로 데이터를 수집합니다. 데이터 수집은 지속적으로 기능을 수행합니다.
2. 실시간적인 데이터 배치 및 시각화도 가능합니다.
3. 수집 된 데이터는 최종적으로 Data Lake인 Hadoop HDFS로 저장합니다.
4. 수집 된 데이터는 날짜를 기준으로 저장됩니다. ex) 2024-04-10,

**Extract**
1. 수집 된 데이터가 저장되어 있는 HDFS로 작업이 필요한 데이터를 가져옵니다.

**Transform**
1. 데이터의 목적에 맞게 데이터 전처리 과정을 진행합니다.
2. 분석을 위한 전처리를 진행합니다.
3. 학습을 위한 전처리를 진행합니다.

**Load**
1. 목적에 맞게 전처리 과정을 거친 데이터가 정형 데이터일 경우 Data Warehouse로 저장합니다.
2. 전처리 과정을 거친 데이터가 반정형 데이터일 경우 Cassandra로 저장합니다.
3. 전처리 과정을 거친 데이터가 비정형 데이터일 경우 Data Lake로 저장합니다.
4. Data Warehouse로 저장할 경우, 데이터가 많아지면 데이터 접근 속도가 느려질 수 있기 때문에 데이터 파티셔닝을 진행합니다.

**Analyze**
1. 분석을 위해 전처리 과정을 거친 데이터를 시각화합니다.

**Learning**
1. 학습을 위해 전처리 과정을 거친 데이터를 활용 해 머신러닝 및 딥러닝을 진행합니다.

**Airflow**
1. 위 과정에 있는 단계를 특정 시간에 자동으로 실행합니다.
2. 예시로 2024-04-10를 기준으로, 어제인 2024-04-09개의 수집 된 데이터를 작업하게 됩니다.
3. 실패 할 경우, 다시 실행합니다. 최대 3번

최종적으로 모든 과정을 자동화로 지속적으로 데이터를 수집하고, 데이터 목적에 맞게 ETL작업을 수행하며, 효율적으로 운영하게 됩니다. <br>
Learning 단계는 아직 수행하지 않고있습니다.

## 3.2 시작
API에 대한 자세한 설명은 https://github.com/Ra99it/Streaming_DataPipeline 참고 해 주세요.

### 3.2.1 게임 이상탐지 학습을 위한 데이터 파이프라인

### 3.2.2 숙박 사이트의 사용자의 행동 분석을 위한 데이터 파이프라인

### 3.2.3 S사 L 게임의 플레이어 행동 분석 및 이상 탐지 학습을 위한 데이터 파이프라인

### 3.3.4 광고에 대한 분석 및 시청자의 분석을 위한 데이터 파이프라인

## 3.3 종료
