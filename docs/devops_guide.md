# Docker commands

```sh
# Force rebuild (--build) images before rurnning up a container
docker compose -f ./devops/compose/docker-compose.dev.yml --env-file .env up --build

# Build & Run container with .env file in detach mode (-d)
docker compose -f ./devops/compose/docker-compose.dev.yml --env-file .env up -d

# Remove container
docker compose -f ./devops/compose/docker-compose.dev.yml down -v

# List for containers
docker ps

# Interact with a docker service when the container is up
# Container name: compose-db-1 (from docker ps)
docker exec --env-file .env -it compose-db-1 psql -U username -d database
# Container name: compose-api-1 (from docker ps)
docker exec --env-file .env -it compose-api-1 alembic revision --autogenerate -m "init"
docker exec --env-file .env -it compose-api-1 alembic upgrade head

# Wipe out all images and containers
docker system prune -af

# Wipe out all volumes
docker volume prune -af

# Wipe out all volumes
docker image prune -af
```