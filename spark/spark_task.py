from pyspark import SparkConf, SparkContext, SparkFiles
from pyspark.sql import SparkSession
import sys
import os
import shutil
from random import randint

if __name__ == "__main__":
    conf = SparkConf().setAppName("WordCountApp").setMaster("spark://spark-master:7077")
    sc = SparkContext(conf=conf)
    spark = SparkSession.builder.config(conf=conf).getOrCreate()

    array = [ randint(1, 100) for i in range(10)]
    rdd = sc.parallelize(array)
    sum_spark = rdd.sum() 
    
    sum_count = rdd.aggregate(
        (0, 0),  
        lambda acc, val: (acc[0] + val, acc[1] + 1),  
        lambda acc1, acc2: (acc1[0] + acc2[0], acc1[1] + acc2[1])  
    )
    avg_spark = sum_count[0] / sum_count[1]

    print("Array:", array)
    print("Sum:", sum_spark)
    print("Average:", avg_spark)
    
    spark.stop()