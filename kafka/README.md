# Getting started with Kafka 
Apache Kafka is an open-source distributed event streaming platform designed for high-throughput, fault-tolerant, and scalable data streaming.
Kafka is built around publish-subscribe model, allowing producers to send messages to topics, and consumers to subscribe to topics to receive those messages. 
### Topic
Topics are logical channels in which messages are sent by producers, and from which messages are consumed by the consumers. Topics can receive messages of any format without any constraint, however, you cannot query from a topic directly, instead, we need to use consumers to read from any topic channel. Kafka topics are **immutable**, which means we cannot detele nor update 
### Partition 
Kafka topics can be split into partitions, which are the basic unit of parallelism and distribution. Partitions allow Kafka to scale and distribute data across multiple brokers.
### Broker
A Kafka broker is a server that stores and manages the messages published to Kafka topics. Brokers collectively form a Kafka cluster. Producers publish messages to brokers, which then store those messages on disk. Consumers read messages from brokers. As mentioned above, each topic can be made up of multiple partitions, and each partition can be hosted within a broker, in which the messages are stored. 
### Offset 
Offset is a unique identifier within a message in a topic. Consummers keep track of their progress by storing the offset of the last message sent. Offsets have meanings only within a specific partition, meaning that offset 3 in partition 1, does not correspond to offset 3 in partition 2. So, the order of messages are reserved within a partition, but not across partitions. 
### Producers
Producers write data to partitions within a topic. This means that the client application (producer) knows in advance on which partition it's sending the data to, and which message broker is accommodating that partition. Producers can choose to send messages along with a message key. If they provide this optional parameter, messages with similar keys will end up in the same partition, thanks to a hashing strategy. 
### Consumers 
Consumers make requests to the topic brokers, the servers, and get a response back. This is called the pull model. A consumer can choose which partition to read the data from. In case there's a server failure on that partition, consumers know how to recover from it. Within each partitions, the offsets will be read in order. The data is read is bytes format, and the key-values will be deserialized by the consumer into their native format (int, string, etc.). The consumers know the expected format of the key values and choose the right serializer accordingly; this mean that the moment the topic is created, we must not change the data type in order to not break the consumer. So, in case you'd like to change the data type, we must create a new topic with the desired data type.
### Key & value
In Kafka, each message consists of a key and a value. Both the key and value can be serialized separately. The key is typically used for partitioning messages, while the value carries the actual data.
### Kafka Message serielization and deserielization
Serialization is a crucial aspect of Kafka's design because it ensures that messages can be efficiently transmitted and processed by Kafka brokers, producers, and consumers while maintaining compatibility and efficiency. When a producer sends a message to a Kafka topic, it serializes the key and value from their native format into a binary format. Conversely, when a consumer receives a message, it deserializes the binary key and value back into their native format for processing. Kafka provides pluggable serializers and deserializers for various data formats. Common serialization formats include Avro, JSON, and Protobuf. You can also implement custom serializers to handle specific data formats. Proper message serialization can have a significant impact on Kafka's efficiency and performance. Choosing the right serialization format for your use case and ensuring proper serialization and deserialization practices are essential for a smooth Kafka deployment. Efficient serialization reduces the size of messages, leading to lower storage and network transfer costs and faster message processing.
### How clients connect to a Kafka cluster
Each Kafka broker in your cluster is called a bootstrap server. In this cluster of brokers, we only need to connect to this one broker and then the clients will know how to be connected to the entire cluster. So, the Kafka client is going to initiate a connection into this broker, as well as a metadata request; once successful, the bootstrap server is going to return the list of all the brokers in the cluster. When the client has access to that metadate, it will know to which broker it'll need to connect, and which partitions are hosted into which broker. This metadate is available to each broker within the cluster, meaning that the brokers are fully aware of one another within the cluster. 
### Topic Replication Factor
Topics need to have a replication factor greater than one, usually between two and three and most commonly at three. So that way, if a broker is down, that means a Kafka server is stopped for maintenance or for a technical issue. Then another Kafka broker still has a copy of the data to serve and receive. So, it's possible for brokers to replicate data from other brokers. **As a general rule, for a replication factor of N, we can permanently lose up to N-1 brokers and still recover your data.**

An important thing to note is that at any given time, only 1 broker can be a leader of a partition (the main server that hosts that partition); and the producers can only send data to the leader of a partition. Similarly, consumers will only read data from the leader of a partition by default.
Since Kafka 2.4, however, it is possible to configure consumers to read from the closest broker, potentially a replica, to improve latency and improve network costs, especially in the cloud.

# Kafka Docker Compose Quickstart
This guide will walk you through setting up a simple Kafka cluster using Docker Compose, creating a Kafka topic, producing a message, and consuming that message.

### Prerequisites
Before you begin, make sure you have the following installed on your system:

- Docker
- Docker Compose

### Understanding the docker-compose.yml File
We used Docker Compose to pull the Zookeeper and Kafka images and run them as Docker Containers. Here we'll go through the services specified in the docker-compose-yml file:

#### Zookeeper
ZooKeeper is a distributed coordination service required by Kafka for managing distributed brokers. It helps maintain metadata, leader election, and synchronization in a Kafka cluster. We used and pulled the ```confluentinc/cp-zookeeper:7.0.0``` image from Dockerhub. Read their [official page](https://hub.docker.com/_/zookeeper) on Dockerhub for more details. 
#### Kafka Service
Kafka is the core message broker responsible for managing topics, partitions, and message distribution within the Kafka cluster. It relies on ZooKeeper for coordination and management.

### Creating a Topic
Follow the below steps to create a topic: 
- In order to get the two services up & running, run the ```docker-compose up -d``` command. 
- Once that's done, go inside the container using the below command:
```
docker exec -it <image_id> sh
```
- Once inside the container create a topic and provide the name, number of partitions, and a replication factor for that topic hosted inside the broker using the below command: 
```
kafka-topics --create --topic my-topic --partitions 1 --replication-factor 1 --if-not-exists --bootstrap-server kafka:9092
```
### Producing and consuming a message
In order to understand a simple flow of stream from a producer, into a topic, and then to a consumer, we'll send a simple "Hello, world" to a topic:
- Create a producer using the below command and start writing out your message in the console:
```
kafka-console-producer --bootstrap-server kafka:9092 --topic my-topic
```
- Once the message are sent out, create a consumer using the bellow command:
```
kafka-console-consumer --bootstrap-server kafka:9092 --topic my-topic --from-beginning
```
By running the last command, you must be able to see the messages. 