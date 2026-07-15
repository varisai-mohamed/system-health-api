# System Health Check API - Architecture

## Overview

The System Health Check API is a Python FastAPI-based application designed to evaluate the health of a system composed of multiple interdependent components represented as a Directed Acyclic Graph (DAG).

The application validates the graph structure, traverses it using Breadth-First Search (BFS), performs asynchronous health checks, propagates dependency failures, generates health summaries, and optionally visualizes the DAG as a PNG image.

---

# High-Level Architecture

```text
                   +------------------+
                   |      Client      |
                   +--------+---------+
                            |
                            v
                   +------------------+
                   |    FastAPI API   |
                   +--------+---------+
                            |
              +-------------+-------------+
              |                           |
              v                           v
     +----------------+         +----------------+
     | Request Models |         | Response Models|
     +--------+-------+         +--------+-------+
              |                           |
              +-------------+-------------+
                            |
                            v
                   +------------------+
                   |  DAG Validator   |
                   +--------+---------+
                            |
                            v
                   +------------------+
                   |   DAG Builder    |
                   +--------+---------+
                            |
                            v
                   +------------------+
                   | BFS Traversal    |
                   +--------+---------+
                            |
                            v
                   +------------------+
                   | Health Checker   |
                   |    (Async)       |
                   +--------+---------+
                            |
                            v
                   +------------------+
                   | Health Aggregator|
                   +--------+---------+
                            |
                            v
                   +------------------+
                   | Graph Visualizer |
                   +--------+---------+
                            |
                            v
                   +------------------+
                   | Final Response   |
                   +------------------+
```

---

# Request Processing Flow

```text
Client Request
      |
      v
JSON Deserialization
      |
      v
Request Validation
      |
      v
DAG Construction
      |
      v
BFS Traversal
      |
      v
Asynchronous Health Checks
      |
      v
Dependency Failure Propagation
      |
      v
Health Summary Generation
      |
      v
Graph PNG Generation
      |
      v
API Response
```

---

# Component Responsibilities

## FastAPI Layer

File:

```text
app/main.py
```

Responsibilities:

- Expose REST API endpoints
- Accept requests
- Orchestrate application flow
- Return responses

Endpoints:

```text
GET  /
GET  /health
POST /api/v1/system/health
POST /api/v1/system/graph
```

---

## Model Layer

Files:

```text
app/models/component.py
app/models/health_response.py
```

Responsibilities:

- Request contracts
- Response contracts
- Input validation through Pydantic

---

## Validation Layer

File:

```text
app/validators/dag_validator.py
```

Responsibilities:

- Validate components exist
- Validate unique component IDs
- Validate dependency references
- Validate self-dependencies
- Validate cycle-free DAG structure

Validation Rules:

```text
✓ Components required
✓ Unique IDs required
✓ Dependencies must exist
✓ No self dependency
✓ No cycles
```

---

## DAG Builder

File:

```text
app/services/dag_builder.py
```

Responsibilities:

- Convert request JSON into graph structure
- Build adjacency list representation

Example:

```text
A
├── B
├── C
└── D
```

Graph Structure:

```python
{
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["D"]
}
```

---

## BFS Traversal

File:

```text
app/services/bfs_traversal.py
```

Responsibilities:

- Traverse graph level by level
- Produce deterministic traversal order

Example:

```text
A
├── B
├── C
└── D
```

Traversal Order:

```text
A → B → C → D
```

---

## Asynchronous Health Checker

File:

```text
app/services/health_checker.py
```

Responsibilities:

- Perform component health checks
- Execute asynchronously using asyncio
- Return component health status

Example:

```python
await asyncio.gather(...)
```

Benefits:

- Improved concurrency
- Reduced execution time
- Scalable architecture

---

## Health Aggregator

File:

```text
app/services/health_aggregator.py
```

Responsibilities:

### Failure Propagation

Example:

```text
A → B → D
A → C → D
```

If:

```text
C = FAILED
```

Then:

```text
D = FAILED
```

because D depends on C.

---

### Overall System Health

Produces:

```text
HEALTHY
UNHEALTHY
```

based on component states.

---

### Health Summary

Generates:

```json
{
  "total_components": 4,
  "healthy_components": 2,
  "failed_components": 2,
  "health_percentage": 50.0
}
```

---

## Graph Visualizer

File:

```text
app/services/graph_visualizer.py
```

Responsibilities:

- Generate Graphviz PNG images
- Represent DAG structure
- Highlight failures visually

Color Scheme:

```text
Green = Healthy
Red   = Failed
```

Generated Files:

```text
generated_graphs/
```

Example:

```text
dag_20260715_101530.png
```

---

## Logging Layer

File:

```text
app/utils/logger.py
```

Responsibilities:

- Application logging
- Error logging
- Execution tracking
- Log rotation

Storage:

```text
logs/
```

Files:

```text
system-health.log
system-health.log.1
system-health.log.2
```

---

## Exception Handling

Files:

```text
app/exceptions/api_exception.py
app/exceptions/exception_handler.py
```

Responsibilities:

- Centralized error handling
- Consistent API responses
- Exception logging

Example Response:

```json
{
  "success": false,
  "error": "Duplicate component IDs detected."
}
```

---

# Infrastructure Architecture

```text
                    +----------------+
                    |   GitHub Repo  |
                    +-------+--------+
                            |
                            v
                    +----------------+
                    | GitHub Actions |
                    +-------+--------+
                            |
                +-----------+-----------+
                |                       |
                v                       v
       +----------------+     +----------------+
       | PyTest Tests   |     | Docker Build   |
       +----------------+     +----------------+
```

---

# Deployment Architecture

```text
+-----------------------+
|  Terraform Apply      |
+-----------+-----------+
            |
            v
+-----------------------+
| Docker Container      |
|-----------------------|
| Python 3.12           |
| FastAPI               |
| Graphviz              |
| Application Services  |
+-----------+-----------+
            |
            v
+-----------------------+
| Port 8000             |
+-----------+-----------+
            |
            v
    http://localhost:8000
```

---

# Data Flow Example

Input:

```text
A
├── B
├── C
└── D

D depends on B and C
```

Health Results:

```text
A = HEALTHY
B = HEALTHY
C = FAILED
```

Failure Propagation:

```text
D = FAILED
```

Final Response:

```text
Overall Status = UNHEALTHY
```

---

# Design Principles

The implementation follows:

- Separation of Concerns
- Single Responsibility Principle
- Dependency Injection-Friendly Design
- Testable Architecture
- Container-Ready Deployment
- Infrastructure as Code
- CI/CD Automation
- Observability

---

# Future Improvements

Potential enhancements include:

- Real component integrations
- Prometheus metrics
- Grafana dashboards
- OpenTelemetry tracing
- Kubernetes deployment
- Authentication and authorization
- Cloud deployment (AWS/Azure)
- Persistent graph storage

---

# Author

Varisai Mohamed Ibrahim

System Health Check API Assignment