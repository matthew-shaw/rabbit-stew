# RabbitMQ Experiments

This experiment demonstrates:

- Using the Pika library for Python to create a RabbitMQ client, used by producers and consumers
- Secure connections using mutual SSL authentication over TLS between three segregated networks
- A direct exchange with routing keys used to bind queues for consumers
- Multiple consumers receiving messages from shared queues using round-robin dispatching and prefetching, to parrallelise work
- Consumer Acknowledgements and Publisher Confirms for increased data safety
- Durable queues and persistent messages for increased fault tolerance
- Python type annotations and checking using mypy
- Container scaling using Docker Compose for local development

## Getting started

```bash
docker compose up --build
```

## Design

```mermaid
flowchart TB
    client(Client)
    subgraph Docker compose
        subgraph Producer network
            P((Producer)):::P
        end

        subgraph Broker network
            X{{Chores}}:::X
            Q1[[parents_tasks]]:::Q
            Q2[[kids_tasks]]:::Q
        end
        
        subgraph Consumer network
            C1((Parent A)):::C
            C2((Parent B)):::C
            C3((Kid A)):::C
            C4((Kid B)):::C
        end
    end

    client -- http --> P
    P -- amqps --> X
    X -- parents --> Q1
    X -- kids --> Q2
    Q1 -- amqps --> C1 & C2
    Q2 -- amqps --> C3 & C4

    classDef P fill:#DAE8FC,stroke:#6C8EBF,stroke-width:2px
    classDef X fill:#F8CECC,stroke:#B85450,stroke-width:2px
    classDef Q fill:#FFF2CC,stroke:#D6B656,stroke-width:2px
    classDef C fill:#D5E8D4,stroke:#82B366,stroke-width:2px
```
