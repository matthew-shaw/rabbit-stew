# RabbitMQ Playground

## Getting started

```bash
docker compose up --build
```

## Design

```mermaid
flowchart LR
    P((Producer)):::P
    X{{Exchange}}:::E
    Q[[Queue]]:::Q
    C((Consumer)):::C

    P --> X
    X --> Q
    Q --> C

    classDef P fill:#DAE8FC,stroke:#6C8EBF,stroke-width:2px
    classDef E fill:#F8CECC,stroke:#B85450,stroke-width:2px
    classDef Q fill:#FFF2CC,stroke:#D6B656,stroke-width:2px
    classDef C fill:#D5E8D4,stroke:#82B366,stroke-width:2px
```
