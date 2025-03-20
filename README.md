# FastAPI Key/Value Store API

A simple in-memory key/value store API built with FastAPI and SQLAlchemy.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python run.py
```

The API will be available at http://localhost:10000

## Running on Render

This application is configured to run on Render:
- Binds to host 0.0.0.0
- Uses the PORT environment variable (defaults to 10000)
- Handles HTTP requests properly

## API Documentation

Once the server is running, you can access:
- Interactive API docs (Swagger UI): http://localhost:10000/docs
- Alternative API docs (ReDoc): http://localhost:10000/redoc

## Available Endpoints

- `POST /kv/{key}` - Create or update a key/value pair
- `GET /kv/{key}` - Get the value for a specific key
- `GET /kv/` - List all key/value pairs
- `DELETE /kv/{key}` - Delete a key/value pair

## Example Requests

Create or update a key/value pair:
```bash
curl -X POST "http://localhost:10000/kv/mykey" \
     -H "Content-Type: application/json" \
     -d '{"value": "myvalue"}'
```

Get a value:
```bash
curl "http://localhost:10000/kv/mykey"
```

List all keys:
```bash
curl "http://localhost:10000/kv/"
```

Delete a key:
```bash
curl -X DELETE "http://localhost:10000/kv/mykey"
```

## Note
This API uses an in-memory SQLite database, so all data will be lost when the application is restarted.
