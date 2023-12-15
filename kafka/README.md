https://www.conduktor.io/kafka/kafka-topics-cli-tutorial/




# kafak command: https://www.conduktor.io/kafka/kafka-topics-cli-tutorial/
git clone https://github.com/conduktor/kafka-stack-docker-compose.git
cd kafka-stack-docker-compose


docker exec -it kafka1 /bin/bash
kafka-topics --bootstrap-server localhost:9092 --list
kafka-topics --topic query-topic --create --partitions 3 --replication-factor 1 --bootstrap-server localhost:9092
kafka-topics --bootstrap-server localhost:9092 --delete --topic first_topic