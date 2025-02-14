[Ctrl+U]
[Enter]
[Ctrl+L]

```
ssh -i ~/Dev/beta-us-west-2.pem ec2-user@msk.demo.timeplus.com
iceberg_tpe/timeplus/bin/timeplusd client -h 127.0.0.1 -u admin --password changeme
```

```
DROP VIEW IF EXISTS mv_write_iceberg
```

```
DROP STREAM IF EXISTS iceberg.transformed
```

```
DROP DATABASE IF EXISTS iceberg
```

```
DROP STREAM IF EXISTS msk_stream_read
```

```
q
```

```
exit
```
