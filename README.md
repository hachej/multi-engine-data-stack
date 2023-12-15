Setup of a very simple multi engine data stack.

More details in [this](https://juhache.substack.com/p/multi-engine-data-stack-v0) article: 

# Getting Started

1- Install requirements.txt
```
pip install -r requirements.txt
```


1- Set .env
Rename .env.local to .env and complete the following variables:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- BUCKET_NAME

2- Set your dbt/profiles.yml
```
duck:
  target: duck
  outputs:
    duck:
      type: duckdb
      path: dbt.duckdb
      extensions:
        - httpfs
        - parquet
      settings:
        s3_region:
        s3_access_key_id: 
        s3_secret_access_key: 

supabase:
  target: supabase
  outputs: 
    supabase:
      type: postgres
      host: 
      user: postgres
      password: 
      port: 5432
      dbname: postgres
      schema: metric
      threads: 1
      connect_timeout: 30

snow: 
  target: snow
  outputs: 
    snow:
      type: snowflake
      account: 
      user: 
      password: 
      database:
      schema: 
```

4 - Run Risingwage
```
docker run -it --pull=always -p 4566:4566 -p 5691:5691 risingwavelabs/risingwave:latest playground
```

```
psql -h localhost -p 4566 -d dev -U root
```

4- Run Kafka
Ref: https://www.conduktor.io/kafka/kafka-topics-cli-tutorial/

```
cd kafka
git clone https://github.com/conduktor/kafka-stack-docker-compose.git
cd kafka-stack-docker-compose
docker-compose -f zk-single-kafka-single.yml ps
```

Create topic
```
docker exec -it kafka1 /bin/bash
kafka-topics --bootstrap-server localhost:9092 --list
kafka-topics --topic query-topic --create --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092
```

If you need to delete a topic
```
kafka-topics --bootstrap-server localhost:9092 --delete --topic first_topic
```

Interact with kcat
```
# list topics
kcat -b localhost:9092 -L

# produce messages
kcat -b localhost:9092 -t test-topic -P

# consumer messages
kcat -b localhost:9092 -t test-topic -C  # consumer
```

4- Run Shadowtraffic
Create license file (cf shadowtraffic website)
```
cd shadowtraffic
docker run --env-file license.env -v $(pwd)/hello-world.json:/home/config.json shadowtraffic/shadowtraffic:latest --config /home/config.json --watch --sample 10
```

3- Run Dagster
```
dagster dev
```