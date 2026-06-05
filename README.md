# Production-Ready Modular REST API

A highly scalable, production-grade REST API built with Python and Flask. This project demonstrates backend engineering best practices, including layered architecture (N-Tier), JSON Web Token (JWT) authentication, robust error handling, and comprehensive automated testing.

## 🚀 Key Features

* **Layered Architecture:** Strict separation of concerns (Routes ➔ Validators ➔ Services ➔ Repositories) preventing business logic from leaking into the presentation layer.
* **JWT Authentication:** Secure user registration, login, and protected route access using `Flask-JWT-Extended` with Bearer tokens.
* **Global Error Handling:** Custom middleware that intercepts backend exceptions and formats them into a strict, predictable JSON contract. No raw HTML stack traces are ever exposed.
* **Request Validation:** Custom validation layer to enforce data integrity, schema rules, and type checking before requests hit the business logic.
* **Automated Test Suite:** 100% core workflow coverage using `pytest`, verifying authentication flows, CRUD operations, and validation logic.
* **Postman Integration:** Includes a pre-configured Postman collection with automated environment variables for seamless testing.

## 🏗️ System Architecture

This API follows a standard N-Tier design pattern:
1. **Presentation Layer (`app/routes`):** Parses HTTP requests and returns standardized JSON responses.
2. **Validation Layer (`app/validators`):** First line of defense against malformed payloads.
3. **Business Logic Layer (`app/services`):** The core application rules and orchestrator.
4. **Data Access Layer (`app/repositories`):** Database abstractions (currently utilizing an in-memory data store for easy local testing).

*See `docs/architecture.md` for full data flow details.*

## 🛠️ Quick Start

### 1. Prerequisites
Ensure you have Python 3.10+ installed on your system.

### 2. Installation
Clone the repository and install the required dependencies:
```bash
git clone <your-repo-url>
cd rest_api_service
pip install -r requirements.txt
```

### 3. Run the Test Suite
Always ensure the API passes its health checks before booting:
```bash
python -m pytest tests/ -v
```

### 4. Boot the Server
Start the application module:
```bash
python -m app.app
```
The server will be available at `http://localhost:5000`.

## 📚 Documentation

Comprehensive documentation is provided in the `/docs` directory:
* **API Contract (`api_contract.md`):** Complete listing of all endpoints, required headers, and expected JSON payloads.
* **Error Responses (`error_responses.md`):** Reference guide for the standardized error envelope and HTTP status codes.

To test the API instantly, import the `postman/collection.json` file into your Postman workspace.

## 🤝 Authors
* **Thejasri Kanagala** - Backend & Architecture
