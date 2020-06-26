# FISH-STORY

Monitoring fisheries with environmental DNA.

Environmental DNA (eDNA) is a rapidly growing tool that allows scientists, stakeholders, conservationists, and ecosystem managers to understand what species are present in an ecosystem and how that changes with time. As genomic costs decrease and the amount of genomic data we can extract rapidly increases, eDNA is quickly becoming viable as a tool to enhance or replace human visual surveys and other expensive or intensive means of ecosystem monitoring. In theory, for this to be useful, eDNA would have to be performed regularly across time and space within a system, which would quickly result in enormous volumes of read data that would need to be stored, processed, and likely re-processed as processing pipelines and taxonomic reference databases improve over time.

FISH-STORY is intended as a proof of concept: that eDNA data, if regularly sampled, could be stored, processed, and re-processed in a distributed cloud architecture pipeline. In this case, a marine metagenome sample was used to build the foundation of a platform that could eventually provide information on which fish are present in a system, how diverse the fish are within that system, and how those metrics change over sequential sampling in time. Further, the system would retain and re-process unidentified DNA reads (the "dark genome") of the samples and update the summarized results with these new data over time. 

<hr/>

![Prototype Dashboard](/img/prototype_dash.png)

<hr/>

This project was performed during the Summer 2020 Insight Data Engineering Silicon Valley (remote) session and so only a basic framework/foundation was constructed within the intense 3 or so weeks of learning and project time. 

The core intent of the project was to build a database (ideally a distributed NoSQL database) to partition and prioritize the storage of reads as they are ingested, processed, re-processed over time. The idea was to maintain recent and unidentified reads (the dark genome) in a priority data store, while reads that were identified or aged out were summarized, condensed, and/or removed. Therefore, as time went on (say collecting monthly as part of a time-series), the most recent trends would be focused on to be the most robust while holes in the historical data were eventually filled in.

This would result in a dashboard showing present species and ecosystem diversity across time that ecosystem managers, coastal stakeholders, researchers, and conservationists could use to easily examine the state and change of the fish in this system over time. The core idea is also very extensible. For example, if sampling was increased spatially to more locations, geolocation data could be added and the dashboard could have a map (or maps) of species distributions over time.


[Insight Demo Presentation](https://docs.google.com/presentation/d/1t4P6ZO3N_uhLGB01bQVNy7vKSV2dOdr_eI_YuR1Riek/edit?usp=sharing)

## Table of Contents
1. [Overview](README.md#FISH-STORY)
1. [Architecture](README.md#Architecture)
1. [Dataset](README.md#Dataset)
1. [Work Flow](README.md#Workflow)
1. [Installation and Dependencies](README.md#Installation-and-Dependencies)
1. [Engineering challenges](README.md#Engineering-challenges)
1. [Trade-offs](README.md#Trade-offs)
1. [Future Work](README.md#Future-Work)

## Architecture

<hr/>

![Tech Stack](/img/tech_stack.png)

<hr/>

The tech stack centers around Spark's processing framework, which was chosen for its range of tools and utilities. Data is imported from S3/NCBI using SRAtools to produce a local paired set of FastQ files, which are then ingested by Spark and transfered as a table of reads to PostgreSQL.

Spark can then ingest reads from the PostgreSQL database, run them through a distributed processing framework using OBITools, which results in an output fasta of reads that have been taxonomically identified.

Finally, the results fasta is ingested into Spark and stored as a new table in PostgreSQL. A dashboard instance reads these data to produce visualizations of species presence and dark genome (unidentified reads) status.

## Dataset

The dataset used for this project is a set of paired-end marine metagenome sequencing runs sampled from the California Current system. A description of the data can be found at: [NCBI Bioproject](https://www.ncbi.nlm.nih.gov//bioproject/525068).  

This dataset has been processed and [published](https://www.frontiersin.org/articles/10.3389/fmars.2019.00732/full?utm_source=fweb&utm_medium=nblog&utm_campaign=ba-sci-fmars-marine-biodiversity-dna#h3) by Closek et al. (2019) in Frontiers in Marine Science and is available open access.

## Workflow

## Installation and Dependencies

### Create AWS Instances

| Host | Instance type |
|------------------|---------------|
| sparkmaster | m5a.4xlarge |
| sparkworker{1-3} | m5a.4xlarge |
| postgresql | m5a.large |
| dashboard | t2.micro |

### Install software packages

#### Java
Hosts: all  

```shell script
	sudo apt install openjdk-8-jre-headless  
```

#### Scala
Hosts: sparkmaster, sparkworkers 

```
	sudo apt install scala  
```

#### Spark
Hosts: sparkmaster and sparkworkers  
[Installation Guide](https://blog.insightdatascience.com/simply-install-spark-cluster-mode-341843a52b88)

#### SRAtools
Hosts: sparkmaster  
[Installation Guide](https://github.com/ncbi/sra-tools/wiki)  
[Using SRAtools in AWS](https://www.ncbi.nlm.nih.gov/sra/docs/sra-aws-download/)

#### OBITools3
Hosts: sparkmaster  
[Installation Guide & Tutorial](https://git.metabarcoding.org/obitools/obitools3/wikis/home)  

Be sure to install Cmake

#### Postgresql
Hosts: postgresql  
[Installation Guide & Tutorial](https://blog.insightdatascience.com/simply-install-postgresql-58c1e4ebf252)  

Note: sparkmaster will require the latest [JDBC PostgreSQL Driver](https://jdbc.postgresql.org/download.html)

#### Python 
##### Pyspark/SparkSQL
Hosts: sparkmaster  
[Installation Guide](https://towardsdatascience.com/pyspark-and-sparksql-basics-6cb4bf967e53)

##### pandas
Hosts: sparkmaster, dashboard  
[Installation Guide](https://pandas.pydata.org/)

##### psycopg2
Hosts: sparkmaster, dashboard  
[Installation Guide](https://www.psycopg.org/docs/install.html)  

Be sure to install libpq-dev

##### Dash
Hosts: dashboard  
[Installation Guide](https://dash.plotly.com/)

##### Plotly Express
Hosts: dashboard  
[Installation Guide](https://plotly.com/python/plotly-express/)

#### Nginx
Hosts: dashboard  
[Installation Guide](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04)

#### Gunicorn
Hosts: dashboard  
[Installation Guide](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04)

## Engineering challenges

### Distributed eDNA processing
Originally, the plan was to recreate the [eDNA processing pipeline](https://github.com/jimmyodonnell/banzai) used by the researchers that collected, processed, and published this dataset. However, many of the tools required proved inaccessible or deprecated, so it became evident that recreating this system would take much longer than the time for the project allowed. The processing tool was switched too OBITools3 because it was an accessible and self-contained package that Spark could call through os functions, but may not be the most optimal system and would need to be tuned for the best representation of the data. The ingestion and processing steps are deeply inefficient and time-consuming and would need to be optimized for better overall performance.

### Apache HBase
The intent of this project was to optimize the storage architecture of a mock time-series of eDNA reads, so much time was spent trying to build a distributed Apache HBase architecture that could best represent the paired reads, their metadata, and their taxonomic identities as column families in an HBase database. This structure would then be partitioned so as to prioritize recent and unidentified reads and optimize processing/re-processing of the continually growing dataset. However, it proved too difficult to connect Spark with HBase in the desired distributed configuration in the time the project allowed, so PostgreSQL was substituted as a relational database due to quick and functional connectors that exist between Spark, Python, and Postgres. Further, the dataset lends itself to future linking with geospatial data, which Postgres is better equipped to expand into.

### Connecting to PostgreSQL in Gunicorn
Despite the dashboard operating as one whole script (accessing the Postgres database and running the Dash app) in the shell during testing, for some reason the connection to another instance to access Postgres would never complete in Gunicorn and caused the workers to timeout and never construct the webpage. The script was thus split into a script that must be run on the dashboard instance to create a local .csv of the results data and a Dash app script that Gunicorn runs in order to produce the [webpage](http://thedatacookery.club).

## Trade-offs

### Functionality in Time
The primary trade-off in this project was that envisioned functionalities had to be let go of for the sake of having a minimally functional product by the project deadline. The base functionality was enough of a challenge to get running in the timeframe that the desired goals of creating a mock time-series, partitioning storage to prioritize data, and automating the re-processing cycle were not implemented.

### SQL vs. NoSQL
For a number of reasons (the paired raw data form, the presence of blank data points in the taxonomies, the desired to distribute and partition the data), a NoSQL architecture made more sense to work with for this eDNA data. However, time and functionality demanded that a quick and serviceable solution be produced, so a relational database was substituted in. Though this still serves to represent and store the paired read data well, it is not optimal for maintaining a robust and fluid taxonomic identity for each read.

## Future Work

### Split Ingestion of Reads to Postgres (not every read has a mate)

### Optimize Processing

### Store and/or Clear Intermediate Data

### Geolocation Data (in Postgres or by connecting HBase to Spark through GEOMESA)

### Partition and Distribute Storage

### Mock Full Time Series

### Automate Workflow and Re-Processing with Airflow

### Increase Dashboard Visualizations and Information
