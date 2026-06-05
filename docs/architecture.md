# System Architecture

This document outlines the high-level architecture and data flow of the REST API Service.

## Layered Design Pattern
The service strictly adheres to a Layered Architecture (also known as N-Tier Architecture). This ensures separation of concerns, testability, and future-proof scalability. 

By preventing business logic from leaking into the routing layer, we ensure the application remains modular and easy to maintain.

### Architecture Data Flow
```text
[ HTTP Client / Postman ]
          │
          ▼  (JSON Payload)
┌─────────────────────────────────┐
│     Global Middleware Layer     │
│ (Error Handlers, Rate Limiting) │
└─────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│       Presentation Layer        │
│       (app/routes/*.py)         │
│ - Parses HTTP requests          │
│ - Enforces JWT Authentication   │
│ - Returns JSON responses        │
└─────────────────────────────────┘
          │
          ▼  (Python Dictionaries)
┌─────────────────────────────────┐
│        Validation Layer         │
│     (app/validators/*.py)       │
│ - Enforces schema contracts     │
│ - Validates data types/lengths  │
└─────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│      Business Logic Layer       │
│      (app/services/*.py)        │
│ - Core application rules        │
│ - Handles password hashing      │
│ - Orchestrates data flow        │
└─────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│       Data Access Layer         │
│    (app/repositories/*.py)      │
│ - Database abstractions         │
│ - CRUD operations               │
│ - Isolates DB dependencies      │
└─────────────────────────────────┘
          │
          ▼
[ Underlying Database / Storage ]
```

## Module Responsibilities

1. **Routes (`app/routes`):** Act strictly as traffic cops. They read the incoming HTTP request, pass the data to the Service layer, and format the Service's output back into an HTTP response. No business logic belongs here.
2. **Validators (`app/validators`):** Act as the first line of defense. They ensure malformed requests (e.g., missing required fields, strings that are too long) are rejected before hitting the core application logic.
3. **Services (`app/services`):** The brain of the API. This layer checks if usernames are unique, verifies passwords, and applies business rules.
4. **Repositories (`app/repositories`):** The abstraction over the database. If we migrate from PostgreSQL to MongoDB, we only need to rewrite this layer; the Services and Routes remain completely unchanged.
5. **Middleware (`app/middleware`):** Catches unexpected exceptions (like 500 Internal Server Errors or 404s) and standardizes them into a consistent JSON format so clients never receive raw HTML stack traces.