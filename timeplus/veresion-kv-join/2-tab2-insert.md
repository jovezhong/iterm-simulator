```bash tab=2
proton client -h 127.0.0.1 -m
```

```sql tab=2
-- Change the price back to 799
INSERT INTO dim_products(product_id,price)
VALUES ('iPhone15',799);
```

Now in this tab2, create the other version kv

```sql tab=2
-- Create the other versioned kv
CREATE STREAM orders
(order_id int8, product_id string, quantity int8)
PRIMARY KEY order_id
SETTINGS mode='versioned_kv';
```

Go tab1, press Ctrl+C to cancel (line 56)

```sql tab=2 sleepBefore=40
-- Make 2 orders, 1 iPhone15 and 2 Plus
INSERT INTO orders(order_id, product_id, quantity)
VALUES (1, 'iPhone15',1),(2, 'iPhone15_Plus',2);
```

change the price back to 800

```sql tab=2 sleep=10
-- Change iPhone price to 800
INSERT INTO dim_products(product_id,price)
VALUES ('iPhone15',800);
```

```sql tab=2
-- Order 1 iPhone15
INSERT INTO orders(order_id, product_id, quantity)
VALUES (3, 'iPhone15',1);
```

Last part demo the left join

Go tab1, press Ctrl+C! to create a left join, L67

Let's run a LEFT JOIN

```sql tab=2 sleepBefore=30
-- Add a new product, revenue will be 0
INSERT INTO dim_products(product_id,price) VALUES ('Vision Pro',3000);
```

```sql tab=2 sleep=30
-- Order the AVP, revenue is updated
INSERT INTO orders(order_id, product_id, quantity)
VALUES (4, 'Vision Pro',1);
```
