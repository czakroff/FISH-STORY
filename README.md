# FISH-STORY

Summary statement: A system to process and present marine fish eDNA data.

Summary

<hr/>

![Prototype Dashboard](/img/prototype_dash.png)

<hr/>

Summary

[Demo presentation.](https://docs.google.com/presentation/d/1t4P6ZO3N_uhLGB01bQVNy7vKSV2dOdr_eI_YuR1Riek/edit?usp=sharing)

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

## Dataset

[NCBI Bioproject](https://www.ncbi.nlm.nih.gov//bioproject/525068)
[Publication](https://www.frontiersin.org/articles/10.3389/fmars.2019.00732/full?utm_source=fweb&utm_medium=nblog&utm_campaign=ba-sci-fmars-marine-biodiversity-dna#h3)

## Workflow

## Installation and Dependencies

### Create Instances

| Host | Instance type |
|------------------|---------------|
| sparkmaster | m4.large |
| sparkworker{1-3} | m4.large |
| postgresql | m5a.large |
| dashboard | t2.micro |

### Install software packages

#### Java
Hosts: all

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

#### Postgresql
Hosts: postgresql
[Installation Guide & Tutorial](https://blog.insightdatascience.com/simply-install-postgresql-58c1e4ebf252)

#### Python 
##### Pyspark/SparkSQL
Hosts: sparkmaster
[Installation Guide](https://towardsdatascience.com/pyspark-and-sparksql-basics-6cb4bf967e53)

##### pandas, dashboard
Hosts: sparkmaster
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

##### Nginx
Hosts: dashboard
[Installation Guide](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04)

##### Gunicorn
Hosts: dashboard
[Installation Guide](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04)

## Engineering challenges

## Trade-offs

## Future Work