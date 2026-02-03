# Learning Assistant Backend

## Overview

This repository contains the backend for a **Learning Assistant** application designed to generate educational content and supporting assets based on a given topic and learner context. It also offers quiz based on the topic and summary of scores

The purpose of this project is to demonstrate:

- Clean API design
- Clear separation of concerns
- Thoughtful use of modern Python tooling
- End to end collaboration with a frontend application

The backend is intentionally scoped to focus on core logic and developer experience rather than production scale completeness.

## Tech Stack

- **Python 3.11**
- **FastAPI** for API routing and request handling
- **Pydantic** for request and response validation
- **Async-first design** for non-blocking operations


### Key directories

**app/**  
Entry point for the FastAPI application. Responsible for wiring routes and dependencies.

**services/**  
Contains the core business logic. This layer is intentionally separated from the API layer to keep route handlers thin and logic testable.


## Architecture Overview

The backend follows a lightweight layered architecture:

- **API layer**
  - Handles HTTP requests and responses
  - Validates inputs and outputs using Pydantic
  - Delegates work to services

- **Service layer**
  - Contains lesson generation logic
  - Handles image generation or retrieval
  - Encapsulates external API interactions

This structure makes it easier to:

- Test core logic in isolation
- Evolve APIs without rewriting business logic
- Swap implementations if requirements change

---

## Core Features

- Generate lesson content based on a given topic and learning level
- Support additional enrichment such as image generation
- Clean and predictable API responses for frontend consumption
- Clear separation between orchestration and business logic


## Design Decisions

### Service-based approach

Business logic is extracted into services rather than embedded in route handlers.

### Async by default

Endpoints and services are designed to be asynchronous to support I/O bound workloads such as external API calls.

### Intentional scope

The following features were deliberately excluded to keep the project focused:

- Authentication and user management
- Persistent storage
- Background task queues

These would be natural next steps in a production environment, but were not required in early stage of this project.


## Testing Strategy

The current focus is on correctness and clarity rather than exhaustive coverage.

With additional time, testing would include:

- More unit tests for lesson and image services
- Contract tests for API request and response schemas
- Mocked external service calls for deterministic behavior

---

## Running the Application Locally

### 1. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```
### 2. Install dependencies 

`pip install -r requirements.txt`


### 3. Start the server

`uvicorn app.main:app --reload`


### Access API documentation
[Open API docs](http://localhost:8000/docs)

