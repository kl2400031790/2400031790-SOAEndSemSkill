# Docker Compose – Multi-Container Microservice

## Aim
To create and deploy a multi-container infrastructure using Docker Compose. The application service and PostgreSQL database run in separate containers and communicate over the Docker Compose network.

## Project structure

```text
docker-compose-microservice-project/
├── docker-compose.yml
├── .env
├── .env.example
├── README.md
└── app/
    ├── Dockerfile
    ├── requirements.txt
    └── app.py
```

## Requirements
- Docker Desktop installed and running on Windows 11
- Docker Compose (included with current Docker Desktop)
- Internet connection for the first build, to download base images and Python packages

## Step 1 – Open the project folder
Extract the ZIP file. Open PowerShell or Windows Terminal in the extracted folder (the folder containing `docker-compose.yml`).

## Step 2 – Build and start both containers
Run:

```powershell
docker compose up -d --build
```

This builds the Flask application image and starts:
- `soa-app-service` – Flask microservice on port 8000
- `soa-app-db` – PostgreSQL database

The application waits for the database health check before starting.

## Step 3 – Check container status

```powershell
docker compose ps
```

Both services should show as running; the database should become healthy.

## Step 4 – Test the deployment
Open this URL in your browser:

```text
http://localhost:8000/api/data
```

Expected response (the record ID may vary):

```json
{
  "status": "success",
  "database": "connected",
  "records": [
    {
      "id": 1,
      "message": "Hello from the PostgreSQL database!"
    }
  ]
}
```

You can also test from PowerShell:

```powershell
Invoke-RestMethod http://localhost:8000/api/data
```

A successful response with `"database": "connected"` confirms that the application container can communicate with the database container.

## Useful commands

```powershell
# View application logs
docker compose logs app-service

# View database logs
docker compose logs app-db

# Stop and remove containers (keeps database volume)
docker compose down

# Stop containers and delete database data too
docker compose down -v
```

## Environment variables
The `.env` file provides `DB_NAME`, `DB_USER`, and `DB_PASSWORD`. Docker Compose passes these values to the database container. The application receives the same credentials and connects to the database using hostname `app-db` (the Compose service name), not `localhost`.

For a real deployment, change the sample database password in `.env` before starting the project. Do not publish real passwords to GitHub.

## Result
The Flask application and PostgreSQL database are deployed in separate Docker containers using Docker Compose. The `/api/data` HTTP endpoint retrieves a record from PostgreSQL and returns `database: connected`, demonstrating successful inter-container communication.
