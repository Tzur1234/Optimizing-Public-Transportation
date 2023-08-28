"""Producer base-class providing common utilites and functionality"""
import logging
import time


from confluent_kafka import avro
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.avro import AvroConsumer, AvroProducer, CachedSchemaRegistryClient

logger = logging.getLogger(__name__)


class Producer:
    """Defines and provides common functionality amongst Producers"""

    # Tracks existing topics across all Producer instances
    existing_topics = set([])

    def __init__(
        self,
        topic_name,
        key_schema,
        value_schema=None,
        num_partitions=1,
        num_replicas=1,
    ):
        """Initializes a Producer object with basic settings"""
        self.topic_name = topic_name
        self.key_schema = key_schema
        self.value_schema = value_schema
        self.num_partitions = num_partitions
        self.num_replicas = num_replicas


        self.broker_properties = {
            "ZOOKEEPER_URL" : "localhost:2181",
            "BROKER_URL" : "PLAINTEXT://localhost:9092",
            "SCHEMA_REGISTRY_URL" : "http://localhost:8081/"
        }

        # If the topic does not already exist, try to create it
        if self.topic_name not in Producer.existing_topics:
            self.create_topic()
            Producer.existing_topics.add(self.topic_name)

        
       
        self.producer = AvroProducer(
            {
            'bootstrap.servers': self.broker_properties.get("BROKER_URL"),
            'schema.registry.url' : self.broker_properties.get("SCHEMA_REGISTRY_URL")
            },
            default_key_schema=key_schema, 
            default_value_schema=value_schema
        )


    def create_topic(self):
        """Creates the producer topic if it does not already exist"""


        adminclient = AdminClient({"bootstrap.servers": self.broker_properties.get('BROKER_URL')})

        # Check topic_name for this producer if it is already exist on the Kafka Broker:
        topics_metadata = adminclient.list_topics(timeout=10)
        if topics_metadata.topics.get(self.topic_name) is not None:
            return

        # Create a new topic
        futures = adminclient.create_topics(
            [
                NewTopic(
                    topic=self.topic_name,
                    num_partitions=self.num_partitions,
                    replication_factor=self.num_replicas,
                )
            ]
        )

        for topic, future in futures.items():
            try:
                future.result()
                print("topic created")
            except Exception as e:
                print(f"failed to create topic {self.topic_name}: {e}")

 
        logger.info("topic creation kafka integration incomplete - skipping")

    def time_millis(self):
        return int(round(time.time() * 1000))

    def close(self):
        """Prepares the producer for exit by cleaning up the producer"""
        self.producer.flush(timeout = 10)
        self.producer.close()
        logger.info("producer close incomplete - skipping")

    def time_millis(self):
        """Use this function to get the key for Kafka Events"""
        return int(round(time.time() * 1000))
