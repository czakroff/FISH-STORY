from pyspark.sql import SparkSession
import os

spark = SparkSession.builder.appName("SimpleApp").getOrCreate()

os.system("obi import --quality-solexa wolf_tutorial/wolf_F.fastq wolf/reads1")
os.system("obi import --quality-solexa wolf_tutorial/wolf_R.fastq wolf/reads2")
os.system("obi import --ngsfilter wolf_tutorial/wolf_diet_ngsfilter.txt wolf/ngsfile")
os.system("obi ls wolf")

spark.stop()
