[Ctrl+L]

Start the client

```bash
proton client -h 127.0.0.1 -m --config-file=/Users/jove/proton-config.xml
```

Highlight it needs 1.5.7 and create the stream

```sql
SELECT version();

-- Create a versioned kv for product list
CREATE STREAM dim_products
(product_id string, price float32)
PRIMARY KEY product_id
SETTINGS mode='versioned_kv';
```

Add some data

```sql
-- Add 2 products
INSERT INTO dim_products(product_id,price)
VALUES ('iPhone15',799),('iPhone15_Plus',899);
```

Show with table

```sql
-- List products
SELECT * FROM table(dim_products);
```

Add more data to override a key

```sql
-- Update the price for iPhone15
INSERT INTO dim_products(product_id,price)
VALUES ('iPhone15',800);

-- New price shown
SELECT * FROM table(dim_products);
```

You can also run this in streaming way.

```sql
-- A streaming SQL
SELECT * FROM dim_products;
```

!! Manully create a new tab (by Cmd+Shift+D)

Wait for Ctrl+C (line 21)

[Ctrl+L]
Start with (INNER) JOIN

```sql
-- Run an INNER JOIN to get total revenues
SELECT orders._tp_time, order_id, product_id,
       quantity, price*quantity AS revenue
FROM dim_products JOIN orders USING(product_id);
```

Wait for Ctrl+C (tab2, line48)

```sql
-- Start the LEFT JOIN
SELECT orders._tp_time, order_id,product_id,
       quantity, price*quantity AS revenue
FROM dim_products LEFT JOIN orders USING(product_id);
```

```sql sleep=10
-- You can also run LEFT JOIN without streaming SQL
SELECT o._tp_time, order_id,product_id,
       quantity, price*quantity AS revenue
FROM table(dim_products) as d
LEFT JOIN table(orders) as o USING(product_id);
```

After the above query is cancelled, clean up

```sql
-- Clean up
drop stream orders;
drop stream dim_products;
```

```sql sleep=10
q;
```
