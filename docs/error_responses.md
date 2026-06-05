# Standard Error Responses

To ensure predictable and programmatic error handling for all API consumers, this service enforces a strict, standardized JSON error envelope for all non-2xx responses.

Raw HTML stack traces are **never** exposed to the client, preventing infrastructure leakage and security vulnerabilities.

## Standard Error Envelope

Every error returned by the API will follow this exact structure:

```json
{
  "success": false,
  "error": {
    "code": "STRING_ERROR_CODE",
    "message": "Human-readable description of what went wrong."
  }
}
```

## Error Codes Reference

### 400 Bad Request
Triggered when the client sends malformed JSON, fails schema validation, or omits required fields.
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Field 'name' is required and must be a string of at least 3 characters."
  }
}
```

### 401 Unauthorized
Triggered when an endpoint requires a JWT token, but the token is missing, expired, or invalid. Also triggered during login failure.
```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication is required and has failed or has not yet been provided."
  }
}
```

### 404 Not Found
Triggered when requesting a resource ID that does not exist in the database, or requesting a route that is not registered.
```json
{
  "success": false,
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Item with ID '12345' not found."
  }
}
```

### 405 Method Not Allowed
Triggered when hitting a valid URL with an invalid HTTP method (e.g., sending a `POST` request to a `GET`-only route).
```json
{
  "success": false,
  "error": {
    "code": "METHOD_NOT_ALLOWED",
    "message": "The method specified in the request is not allowed."
  }
}
```

### 409 Conflict
Triggered when a request violates a unique constraint in the system (e.g., registering an already existing username).
```json
{
  "success": false,
  "error": {
    "code": "CONFLICT",
    "message": "Username already exists"
  }
}
```

### 500 Internal Server Error
Triggered by an unhandled backend exception. The actual stack trace is logged internally for Site Reliability Engineers, while the client receives a safe, generic message.
```json
{
  "success": false,
  "error": {
    "code": "INTERNAL_SERVER_ERROR",
    "message": "An unexpected error occurred while processing your request."
  }
}
```