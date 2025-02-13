[Ctrl+U]
[Enter]
[Ctrl+L]

```
cd /tmp
```
[Ctrl+L]

```bash
spark-sql --packages org.apache.iceberg:iceberg-spark-runtime-3.4_2.12:1.7.1,org.apache.iceberg:iceberg-aws-bundle:1.7.1,software.amazon.awssdk:bundle:2.30.2,software.amazon.awssdk:url-connection-client:2.30.2 \
    --conf spark.sql.defaultCatalog=spark_catalog \
    --conf spark.sql.catalog.spark_catalog=org.apache.iceberg.spark.SparkCatalog \
    --conf spark.sql.catalog.spark_catalog.type=rest \
    --conf spark.sql.catalog.spark_catalog.uri=https://glue.us-west-2.amazonaws.com/iceberg \
    --conf spark.sql.catalog.spark_catalog.warehouse=$AWS_12_ID \
    --conf spark.sql.catalog.spark_catalog.rest.sigv4-enabled=true \
    --conf spark.sql.catalog.spark_catalog.rest.signing-name=glue \
    --conf spark.sql.catalog.spark_catalog.rest.signing-region=us-west-2 \
    --conf spark.sql.catalog.spark_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO \
    --conf spark.hadoop.fs.s3a.aws.credentials.provider=org.apache.hadoop.fs.s3a.SimpleAWSCredentialProvider \
    --conf spark.sql.catalog.spark_catalog.rest-metrics-reporting-enabled=false
```

```
show databases;
```

```
use gimitest;
show tables;
select * from coo;
quit;
```
