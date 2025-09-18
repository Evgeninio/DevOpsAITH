from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, functions as F
import argparse, os, json

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=10000)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--output", type=str, required=True)
    args = p.parse_args()

    conf = SparkConf().setAppName("SparkStatsApp")
    sc = SparkContext(conf=conf)
    spark = SparkSession.builder.getOrCreate()

    df = spark.range(0, args.n, 1, numPartitions=4) \
              .select(((F.rand(seed=args.seed) * 100).cast("int")).alias("value"))

    row = df.agg(
        F.count("*").alias("count"),
        F.sum("value").alias("sum"),
        F.avg("value").alias("avg"),
        F.min("value").alias("min"),
        F.max("value").alias("max"),
        F.expr("percentile_approx(value, 0.5)").alias("median"),
    ).collect()[0]

    stats = {k: row[k] for k in row.asDict()}
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(stats, f)

    print(f"Saved stats to {args.output}: {stats}")
    spark.stop()

if __name__ == "__main__":
    main()
