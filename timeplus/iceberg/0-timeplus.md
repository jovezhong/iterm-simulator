[Ctrl+U]
[Enter]
[Ctrl+L]

```
ssh -i ~/Dev/beta-us-west-2.pem ec2-user@msk.demo.timeplus.com
iceberg_tpe/timeplus/bin/timeplusd client -h 127.0.0.1 -u admin --password changeme -m
```

```sql
CREATE EXTERNAL STREAM msk_stream_read(
  org_id string,
  float_value nullable(float32),
  array_of_records array(tuple(a_str string, a_num int32))
)
SETTINGS
    type='kafka',
    brokers='b-1.democluster1.70hytn.c6.kafka.us-west-2.amazonaws.com:9098',
    topic='topic2',
    security_protocol='SASL_SSL',
    sasl_mechanism='AWS_MSK_IAM',
    data_format='Avro',
    format_schema='avro_schema';

SELECT * FROM msk_stream_read LIMIT 3;

CREATE DATABASE iceberg
ENGINE =  Iceberg('https://glue.us-west-2.amazonaws.com/iceberg')
SETTINGS  catalog_type='rest',
          warehouse='753502519061', storage_endpoint='https://tp-iceberg-demo.s3.us-west-2.amazonaws.com',
          rest_catalog_sigv4_enabled=true, rest_catalog_signing_region='us-west-2', rest_catalog_signing_name='glue';

CREATE STREAM iceberg.transformed(
  timestamp datetime64,
  org_id string,
  float_value float,
  array_length int,
  max_num int,
  min_num int
);
CREATE MATERIALIZED VIEW default.mv_write_iceberg INTO iceberg.transformed AS
SELECT now() AS timestamp, org_id,float_value, length(`array_of_records.a_num`) AS array_length,
array_max(`array_of_records.a_num`) AS max_num,array_min(`array_of_records.a_num`) AS min_num
FROM default.msk_stream_read
SETTINGS s3_min_upload_file_size=1024;
```
