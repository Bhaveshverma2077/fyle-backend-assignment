# Instructions

## Requirements

- Docker needs to be installed and Docker Desktop needs to be running.

## To Run the Project

Command to run from the root of the project

```bash
docker-compose -f ./docker/docker-compose.yml up
```

Now you can access the server using `http://localhost:80` or simply `http://localhost`

## Tests

Tests should only be run after DB migration.

To migrate, delete the `store.sqlite3` file in `core/` (if any), and execute the following commands in the Bash shell of the container we’re about to open:

To get access to the bash shell inside the container, run from the root of the project:

```bash
docker-compose -f ./docker/docker-compose.yml exec backend bash
```

Run the following command to migrate:

1. Set the `FLASK_APP` environment variable:

   ```bash
   export FLASK_APP="/APP/core/server"
   ```

2. Run the database migration:

   ```bash
   flask db upgrade -d ./core/migrations
   ```

After migrating, run the following command to execute the tests:

```bash
pytest
```
