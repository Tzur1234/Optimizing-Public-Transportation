# Public Transit Status with Apache Kafka

In this project, I constructed a streaming event pipeline around Apache Kafka and its ecosystem. Using public data from the [Chicago Transit Authority](https://www.transitchicago.com/data/), I built an event pipeline around Kafka that allowed me to simulate and display the status of train lines in real time.

Upon completing the project, I was able to monitor a website to observe trains moving from station to station.


![Final User Interface](images/ui.png)


## Prerequisites

The following are required to run this project:

* Docker
* Python 3.7
* Access to a computer with a minimum of 16gb+ RAM and a 4-core CPU to execute the simulation

## Description

The Chicago Transit Authority (CTA) has tasked me with developing a dashboard displaying system status for its commuters. I've decided to utilize Kafka and ecosystem tools such as REST Proxy and Kafka Connect to achieve this objective.

The architecture will look like so:

![Project Architecture](images/diagram.png)

In order to successfully complete my project, I had to undertake the following tasks:

### Step 1: Create Kafka Producers
The initial step in my plan involved configuring the train stations to emit specific events. The CTA had installed sensors on each side of every train station, which could be programmed to trigger actions whenever a train arrived at the station.


### Step 2: Configure Kafka REST Proxy Producer
As part of the project, I collected weather data and utilized Kafka's REST Proxy to transmit this data into Kafka. The weather hardware, which is aged and has hardware limitations, made it impossible to use the Python Client Library. Therefore, I employed HTTP REST to establish the connection and send the data to Kafka.


### Step 3: Configure Kafka Connect
Finally, I extracted station information from our PostgreSQL database into Kafka. I've decided to use the [Kafka JDBC Source Connector](https://docs.confluent.io/current/connect/kafka-connect-jdbc/source-connector/index.html).


### Step 4: Configure the Faust Stream Processor
I leveraged Faust Stream Processing to enhance the raw Stations table from Kafka Connect. By ingesting data from the Kafka Connect topic, I transformed and refined the information, addressing unnecessary data and configuring line color details.


### Step 5: Configure the KSQL Table
After that, I used KSQL to group together the turnstile data for each station. This made the data more helpful by summarizing the counts for each station, ensuring that other client programes always have the latest count information.


### Step 6: Create Kafka Consumers
After collecting all the data in Kafka, my final task was to retrieve the data into the web server responsible for providing transit status pages to commuters.



### Documentation I have used
In addition to the course content you have already reviewed, you may find the following examples and documentation helpful in completing this assignment:

* [Confluent Python Client Documentation](https://docs.confluent.io/current/clients/confluent-kafka-python/#)
* [Confluent Python Client Usage and Examples](https://github.com/confluentinc/confluent-kafka-python#usage)
* [REST Proxy API Reference](https://docs.confluent.io/current/kafka-rest/api.html#post--topics-(string-topic_name))
* [Kafka Connect JDBC Source Connector Configuration Options](https://docs.confluent.io/current/connect/kafka-connect-jdbc/source-connector/source_config_options.html)

## Directory Layout

```
├── consumers
│   ├── consumer.py 
│   ├── faust_stream.py 
│   ├── ksql.py 
│   ├── models
│   │   ├── lines.py
│   │   ├── line.py 
│   │   ├── station.py 
│   │   └── weather.py 
│   ├── requirements.txt
│   ├── server.py
│   ├── topic_check.py
│   └── templates
│       └── status.html
└── producers
    ├── connector.py 
    ├── models
    │   ├── line.py
    │   ├── producer.py 
    │   ├── schemas
    │   │   ├── arrival_key.json
    │   │   ├── arrival_value.json 
    │   │   ├── turnstile_key.json
    │   │   ├── turnstile_value.json 
    │   │   ├── weather_key.json
    │   │   └── weather_value.json 
    │   ├── station.py 
    │   ├── train.py
    │   ├── turnstile.py 
    │   ├── turnstile_hardware.py
    │   └── weather.py 
    ├── requirements.txt
    └── simulation.py
```

## Running and Testing

To run the simulation, you must first start up the Kafka ecosystem on their machine utilizing Docker Compose.

```%> docker-compose up```

Docker compose will take a 3-5 minutes to start, depending on your hardware. Please be patient and wait for the docker-compose logs to slow down or stop before beginning the simulation.

Once docker-compose is ready, the following services will be available:

| Service | Host URL | Docker URL | Username | Password |
| --- | --- | --- | --- | --- |
| Public Transit Status | [http://localhost:8888](http://localhost:8888) | n/a | ||
| Landoop Kafka Connect UI | [http://localhost:8084](http://localhost:8084) | http://connect-ui:8084 |
| Landoop Kafka Topics UI | [http://localhost:8085](http://localhost:8085) | http://topics-ui:8085 |
| Landoop Schema Registry UI | [http://localhost:8086](http://localhost:8086) | http://schema-registry-ui:8086 |
| Kafka | PLAINTEXT://localhost:9092,PLAINTEXT://localhost:9093,PLAINTEXT://localhost:9094 | PLAINTEXT://kafka0:9092,PLAINTEXT://kafka1:9093,PLAINTEXT://kafka2:9094 |
| REST Proxy | [http://localhost:8082](http://localhost:8082/) | http://rest-proxy:8082/ |
| Schema Registry | [http://localhost:8081](http://localhost:8081/ ) | http://schema-registry:8081/ |
| Kafka Connect | [http://localhost:8083](http://localhost:8083) | http://kafka-connect:8083 |
| KSQL | [http://localhost:8088](http://localhost:8088) | http://ksql:8088 |
| PostgreSQL | `jdbc:postgresql://localhost:5432/cta` | `jdbc:postgresql://postgres:5432/cta` | `cta_admin` | `chicago` |

Note that to access these services from your own machine, you will always use the `Host URL` column.

When configuring services that run within Docker Compose, like **Kafka Connect you must use the Docker URL**. When you configure the JDBC Source Kafka Connector, for example, you will want to use the value from the `Docker URL` column.

### Running the Simulation

There are two pieces to the simulation, the `producer` and `consumer`. As you develop each piece of the code, it is recommended that you only run one piece of the project at a time.

However, if you are want to verify the end-to-end system prior to submission, it is critical that you open a terminal window for each piece and run them at the same time. **If you do not run both the producer and consumer at the same time you will not be able to successfully complete the project**.

#### To run the `producer`:

1. `cd producers`
2. `virtualenv venv`
3. `. venv/bin/activate`
4. `pip install -r requirements.txt`
5. `python simulation.py`

Once the simulation is running, you may hit `Ctrl+C` at any time to exit.

#### To run the Faust Stream Processing Application:
1. `cd consumers`
2. `virtualenv venv`
3. `. venv/bin/activate`
4. `pip install -r requirements.txt`
5. `faust -A faust_stream worker -l info`


#### To run the KSQL Creation Script:
1. `cd consumers`
2. `virtualenv venv`
3. `. venv/bin/activate`
4. `pip install -r requirements.txt`
5. `python ksql.py`

#### To run the `consumer`:

** NOTE **: Do not run the consumer until you have reached Step 6!
1. `cd consumers`
2. `virtualenv venv`
3. `. venv/bin/activate`
4. `pip install -r requirements.txt`
5. `python server.py`

Once the server is running, you may hit `Ctrl+C` at any time to exit.
