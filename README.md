# RabbitMQ Playground

## Getting started

```bash
docker compose up --build
```

## Design

```mermaid
flowchart LR
    subgraph Docker compose
        subgraph Producer network
            P((Producer)):::P
        end

        subgraph Exchange network
            X{{Exchange}}:::E
            Q[[Queue]]:::Q
        end
        
        subgraph Consumer network
            C1((Consumer)):::C
            C2((Consumer)):::C
        end
    end

    P -- amqps:5671 --> X
    X --> Q
    C1 & C2 -- amqps:5671 --> Q

    classDef P fill:#DAE8FC,stroke:#6C8EBF,stroke-width:2px
    classDef E fill:#F8CECC,stroke:#B85450,stroke-width:2px
    classDef Q fill:#FFF2CC,stroke:#D6B656,stroke-width:2px
    classDef C fill:#D5E8D4,stroke:#82B366,stroke-width:2px
```
