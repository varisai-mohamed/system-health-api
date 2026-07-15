# System Health Check API

## Overview

System Health Check API is a Python-based REST API built using FastAPI to evaluate the health of a system composed of multiple interdependent components represented as a Directed Acyclic Graph (DAG).

The application accepts a DAG definition as JSON input, validates the graph, traverses it using Breadth-First Search (BFS), performs asynchronous health checks on each component, propagates dependency failures, generates health summaries, and optionally visualizes the DAG as a PNG image.

---

## Features Implemented

### Core Features

- REST API built using FastAPI
- DAG construction from JSON input
- DAG validation
  - Empty component validation
  - Duplicate component validation
  - Missing dependency validation
  - Self dependency validation
  - Circular dependency validation
- Breadth-First Search (BFS) traversal
- Asynchronous component health checks using asyncio
- Dependency failure propagation
- Overall system health calculation
- Health summary generation
- DAG visualization using Graphviz
- PNG graph generation with failed components highlighted in red

### Observability

- Structured logging
- Log file generation
- Log rotation
- Health endpoint
- Custom exception handling

### Engineering Features

- Unit testing using PyTest
- Docker containerization
- Infrastructure as Code using Terraform
- CI/CD pipeline using GitHub Actions

---

## Architecture

```text
Client
  |
  v
FastAPI Endpoint
  |
  v
Validation Layer
  |
  v
DAG Builder
  |
  v
BFS Traversal
  |
  v
Async Health Checks
  |
  v
Failure Propagation
  |
  v
Health Aggregation
  |
  v
Graph Generation
  |
  v
Response
```

---

## Project Structure

```text
system-health-api/

├── app/
│   ├── exceptions/
│   ├── models/
│   ├── services/
│   ├── utils/
│   ├── validators/
│   └── main.py
│
├── tests/
│
├── generated_graphs/
├── logs/
│
├── terraform/
│
├── .github/workflows/
│
├── Dockerfile
├── .dockerignore
├── .gitignore
├── pytest.ini
├── pyproject.toml
├── poetry.lock
└── README.md
```

---

## API Endpoints

### Root Endpoint

```http
GET /
```

Response

```json
{
  "message": "System Health Check API"
}
```

---

### Health Endpoint

```http
GET /health
```

Response

```json
{
  "status": "UP"
}
```

---

### System Health Check

```http
POST /api/v1/system/health
```

Request

```json
{
  "components": [
    {
      "id": "A",
      "dependencies": []
    },
    {
      "id": "B",
      "dependencies": ["A"]
    },
    {
      "id": "C",
      "dependencies": ["A"]
    },
    {
      "id": "D",
      "dependencies": ["B", "C"]
    }
  ]
}
```

Response

```json
{
  "overall_status": "UNHEALTHY",
  "summary": {
    "total_components": 4,
    "healthy_components": 2,
    "failed_components": 2,
    "health_percentage": 50.0
  },
  "components": [
    {
      "component": "A",
      "status": "HEALTHY"
    },
    {
      "component": "B",
      "status": "HEALTHY"
    },
    {
      "component": "C",
      "status": "FAILED"
    },
    {
      "component": "D",
      "status": "FAILED"
    }
  ]
}
```

---

### DAG Graph Generation

```http
POST /api/v1/system/graph
```

Generates a PNG image representing the DAG.

Healthy nodes are displayed in green.

Failed nodes are displayed in red.

Generated images are stored in:

```text
generated_graphs/
```

---

## Validation Rules

The application validates:

- At least one component must exist
- Component IDs must be unique
- Dependencies must reference existing components
- Components cannot depend on themselves
- Graph must be acyclic (DAG)

Invalid requests return appropriate HTTP 400 responses with meaningful error messages.

---

## Assumptions

- Input graph must represent a Directed Acyclic Graph (DAG).
- Component identifiers are unique.
- Health checks are simulated.
- A failed dependency causes all downstream dependent components to fail.
- Graph visualization is generated on demand.
- Health status values are:
  - HEALTHY
  - FAILED

---

## Design Decisions

### Why FastAPI?

- Native async support
- Automatic Swagger documentation
- Lightweight and high-performance framework

### Why BFS?

The assignment explicitly requires BFS traversal.

### Why Async Health Checks?

Allows concurrent execution of component checks and improves scalability.

### Why Separate Validation Layer?

Improves maintainability and separation of concerns.

### Why Graphviz?

Provides a simple and effective way to visualize DAG structures.

---

## Tradeoffs

### Health Check Simulation

Current implementation simulates component health.

Advantages:

- Easy testing
- Self-contained implementation

Limitation:

- Does not connect to actual external systems

### PNG Storage

Generated images are stored locally.

Advantages:

- Simplicity

Limitation:

- Image retention management is not implemented

---

## Local Setup

### Clone Repository

```bash
git clone https://github.com/varisai-mohamed/system-health-api.git

cd system-health-api
```

### Install Dependencies

```bash
poetry install
```

### Run Application

```bash
poetry run uvicorn app.main:app --reload
```

Open:

```text
http://localhost:8000/docs
```

---

## Running Unit Tests

Execute:

```bash
poetry run pytest
```

Generate coverage:

```bash
poetry run pytest --cov=app
```

---

## Docker

Build image:

```bash
docker build -t system-health-api .
```

Run container:

```bash
docker run -d \
-p 8000:8000 \
-v ${PWD}/generated_graphs:/app/generated_graphs \
-v ${PWD}/logs:/app/logs \
--name system-health-api-container \
system-health-api
```

Open:

```text
http://localhost:8000/docs
```

---

## Terraform

Navigate to Terraform folder:

```bash
cd terraform
```

Initialize:

```bash
terraform init
```

Validate:

```bash
terraform validate
```

Apply:

```bash
terraform apply
```

Destroy:

```bash
terraform destroy
```

---

## CI/CD Pipeline

GitHub Actions pipeline automatically performs:

- Source checkout
- Python setup
- Poetry installation
- Dependency installation
- Unit test execution
- Docker image build

Workflow location:

```text
.github/workflows/ci.yml
```

---

## Logging

Application logs are written to:

```text
logs/
```

Log rotation is enabled using:

```text
RotatingFileHandler
```

Generated files:

```text
system-health.log
system-health.log.1
system-health.log.2
```

---

## Future Enhancements

- Prometheus metrics
- Grafana dashboards
- OpenTelemetry tracing
- External health check integrations
- Kubernetes deployment
- Authentication and authorization
- Graph retention and cleanup policies

---

## AI Usage Disclosure

AI-assisted tools were used during development for:

- Solution brainstorming
- Design discussions
- Code review assistance
- Unit test generation assistance
- Documentation generation

All generated code was reviewed, modified where necessary, executed, tested, and validated manually before inclusion in the final solution.

---

## Author

Varisai Mohamed Ibrahim